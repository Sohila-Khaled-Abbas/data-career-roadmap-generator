from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import sqlite3
import os
import sys
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
PARQUET_PATH = os.path.join(ROOT_DIR, "data", "egypt_data_skills.parquet")
SQLITE_PATH = os.path.join(ROOT_DIR, "data", "market_trends.db")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

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
    """Trigger the Claude AI roadmap generation logic."""
    if not request.skills:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Must provide at least one skill.")
        
    try:
        # Call the existing LLM generator logic
        roadmap_md = generate_roadmap_with_llm(request.profile, request.skills)
        if not roadmap_md:
             raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate roadmap via AgentRouter API."
            )
            
        # Optionally save the generated roadmap to the output folder
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.join(OUTPUT_DIR, f"roadmap_{request.profile.replace(' ', '_').lower()}.md")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(roadmap_md)
            
        return RoadmapResponse(profile=request.profile, markdown=roadmap_md)
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating roadmap: {str(e)}"
        )

@app.get("/api/v1/roadmaps/{profile}", response_model=RoadmapResponse, tags=["Roadmaps"])
def get_saved_roadmap(profile: str = Path(..., title="The job profile to look for")):
    """Retrieve a previously generated roadmap from the output directory."""
    filename = os.path.join(OUTPUT_DIR, f"roadmap_{profile.replace(' ', '_').lower()}.md")
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No saved roadmap found for profile: {profile}")
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return RoadmapResponse(profile=profile, markdown=content)
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read saved roadmap: {str(e)}"
        )
