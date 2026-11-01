from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import sqlite3
import os
import sys
import re
import logging
from collections import Counter

# Add src to path to import roadmap generator
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(ROOT_DIR, 'src'))
from roadmap_generator import generate_roadmap_with_llm

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Data & AI Career Roadmap API",
    description="API to serve job market insights and AI-generated learning roadmaps.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # wildcard origins are not compatible with credentialed CORS
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
PARQUET_PATH = os.path.join(ROOT_DIR, "data", "egypt_data_skills.parquet")
SQLITE_PATH = os.path.join(ROOT_DIR, "data", "market_trends.db")
OUTPUT_DIR = os.getenv("ROADMAP_OUTPUT_DIR", os.path.join(ROOT_DIR, "output"))
logger = logging.getLogger(__name__)


def roadmap_file_path(profile: str) -> str:
    """Use a single safe filename component, even for untrusted role names."""
    slug = re.sub(r"[^\\w-]+", "_", profile.casefold(), flags=re.UNICODE).strip("_")[:80]
    if not slug or slug in (".", ".."):
        raise HTTPException(status_code=422, detail="Invalid roadmap profile name.")
    return os.path.join(OUTPUT_DIR, f"roadmap_{slug}.md")

# Pydantic Models
class SkillFrequency(BaseModel):
    skill: str
    frequency: int

class InsightResponse(BaseModel):
    total_postings: int
    avg_skills_per_posting: float
    latest_crawl_date: Optional[str] = None

class RoadmapGenerateRequest(BaseModel):
    profile: str
    skills: List[str]

class RoadmapResponse(BaseModel):
    profile: str
    markdown: str

# Helper Functions
def load_parquet_data() -> pd.DataFrame:
    if not os.path.exists(PARQUET_PATH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Parquet data file not found. Please run the ETL pipeline first."
        )
    try:
        return pd.read_parquet(PARQUET_PATH)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read parquet data: {str(e)}"
        )

# API Endpoints
@app.get("/api/v1/profiles", response_model=List[str], tags=["Data"])
def get_profiles():
    """Retrieve a list of all available job profiles."""
    df = load_parquet_data()
    if 'searched_profile' not in df.columns:
        return []
    profiles = df['searched_profile'].dropna().unique().tolist()
    return sorted(profiles)

@app.get("/api/v1/insights/{profile}", response_model=InsightResponse, tags=["Insights"])
def get_insights(profile: str = Path(..., title="The job profile to query")):
    """Retrieve high-level metrics for a specific profile."""
    df = load_parquet_data()
    profile_df = df[df['searched_profile'].str.lower() == profile.lower()]
    
    if profile_df.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for profile: {profile}")
    
    total_postings = len(profile_df)
    avg_skills = round(profile_df['skill_count'].mean(), 1) if 'skill_count' in profile_df.columns else 0.0
    latest_date = str(profile_df['crawl_date'].max()) if 'crawl_date' in profile_df.columns else None

    return InsightResponse(
        total_postings=total_postings,
        avg_skills_per_posting=avg_skills,
        latest_crawl_date=latest_date
    )

@app.get("/api/v1/skills/{profile}/top", response_model=List[SkillFrequency], tags=["Insights"])
def get_top_skills(
    profile: str = Path(..., title="The job profile to query"),
    limit: int = Query(15, ge=1, le=100, description="Number of top skills to return")
):
    """Aggregate and return the top requested skills for a specific profile."""
    df = load_parquet_data()
    profile_df = df[df['searched_profile'].str.lower() == profile.lower()]
    
    if profile_df.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for profile: {profile}")
        
    all_skills = []
    if 'skills_detected' in profile_df.columns:
        for skills_string in profile_df['skills_detected']:
            if pd.notna(skills_string) and skills_string.strip():
                skills = [s.strip() for s in skills_string.split(',')]
                all_skills.extend(skills)
                
    if not all_skills:
        return []

    skill_counts = Counter(all_skills)
    top_skills_data = skill_counts.most_common(limit)
    
    return [SkillFrequency(skill=s, frequency=f) for s, f in top_skills_data]

@app.post("/api/v1/roadmaps/generate", response_model=RoadmapResponse, tags=["Roadmaps"])
def generate_roadmap(request: RoadmapGenerateRequest):
    """Generate a roadmap with Gemini while leaving the read-only API available offline."""
    if not request.skills:
        raise HTTPException(status_code=400, detail="Must provide at least one skill.")
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=503, detail="AI roadmap generation is not configured.")

    filename = roadmap_file_path(request.profile)
    try:
        roadmap_md = generate_roadmap_with_llm(request.profile, request.skills)
    except Exception:
        logger.exception("Roadmap generation failed.")
        raise HTTPException(status_code=502, detail="AI roadmap generation failed.") from None
    if not roadmap_md:
        raise HTTPException(status_code=502, detail="AI roadmap generation is temporarily unavailable.")

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(roadmap_md)
    except OSError:
        # Read-only or ephemeral serverless filesystems must not break generation.
        logger.warning("Roadmap generated but could not be saved on this instance.")
    return RoadmapResponse(profile=request.profile, markdown=roadmap_md)


@app.get("/api/v1/roadmaps/{profile}", response_model=RoadmapResponse, tags=["Roadmaps"])
def get_saved_roadmap(profile: str = Path(..., title="The job profile to look for")):
    """Retrieve a roadmap stored locally on this instance, if still available."""
    filename = roadmap_file_path(profile)
    if not os.path.isfile(filename):
        raise HTTPException(status_code=404, detail="No saved roadmap found for this profile.")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except OSError:
        logger.exception("Could not read saved roadmap.")
        raise HTTPException(status_code=500, detail="Failed to read saved roadmap.") from None
    return RoadmapResponse(profile=profile, markdown=content)
