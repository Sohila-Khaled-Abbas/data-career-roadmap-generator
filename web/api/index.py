from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import sqlite3
import os
import sys
from collections import Counter

# For Vercel Serverless, we point to our local src copy
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from roadmap_generator import generate_roadmap_with_llm

app = FastAPI()

# Enable CORS (though less critical on Vercel due to rewrites)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PARQUET_PATH = os.path.join(os.path.dirname(__file__), "data", "egypt_data_skills.parquet")
DB_PATH      = os.path.join(os.path.dirname(__file__), "data", "egypt_data_skills.db")
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "output")

class SkillFrequency(BaseModel):
    skill: str
    frequency: int

class RoadmapGenerateRequest(BaseModel):
    profile: str
    skills: List[str]

class RoadmapResponse(BaseModel):
    profile: str
    markdown: str

def load_data() -> pd.DataFrame:
    """Load job skills data from SQLite DB, falling back to Parquet."""
    if os.path.exists(DB_PATH):
        try:
            con = sqlite3.connect(DB_PATH)
            df  = pd.read_sql("SELECT * FROM job_skills", con)
            con.close()
            return df
        except Exception:
            pass
    if os.path.exists(PARQUET_PATH):
        return pd.read_parquet(PARQUET_PATH)
    raise HTTPException(
        status_code=503,
        detail="Market data not found. Ensure egypt_data_skills.db or .parquet is committed."
    )

@app.get("/api/v1/profiles")
def get_profiles():
    df = load_data()
    return sorted(df['searched_profile'].dropna().unique().tolist())

@app.get("/api/v1/skills/{profile}/top")
def get_top_skills(profile: str, limit: int = 15):
    df = load_data()
    profile_df = df[df['searched_profile'].str.lower() == profile.lower()]
    
    all_skills = []
    for skills_string in profile_df['skills_detected']:
        if pd.notna(skills_string) and skills_string.strip():
            all_skills.extend([s.strip() for s in skills_string.split(',') if s.strip()])
            
    skill_counts = Counter(all_skills)
    return [SkillFrequency(skill=s, frequency=f) for s, f in skill_counts.most_common(limit)]

@app.get("/api/v1/jobs")
def get_jobs(profile: Optional[str] = None, source: Optional[str] = None, limit: int = 50):
    """Return raw job records, optionally filtered by profile and/or source board."""
    df = load_data()
    if profile:
        df = df[df['searched_profile'].str.lower() == profile.lower()]
    if source:
        if 'source' in df.columns:
            df = df[df['source'].str.lower() == source.lower()]
    cols = ['crawl_date', 'searched_profile', 'source', 'job_title', 'company', 'job_url', 'skills_detected', 'skill_count']
    cols = [c for c in cols if c in df.columns]
    return df[cols].head(limit).to_dict(orient='records')

@app.post("/api/v1/roadmaps/generate")
def generate_roadmap(request: RoadmapGenerateRequest):
    roadmap_md = generate_roadmap_with_llm(request.profile, request.skills)
    if not roadmap_md:
        raise HTTPException(status_code=502, detail="AI Generation failed.")
    return RoadmapResponse(profile=request.profile, markdown=roadmap_md)

@app.get("/api/v1/roadmaps/{profile}")
def get_saved_roadmap(profile: str):
    filename = os.path.join(OUTPUT_DIR, f"roadmap_{profile.replace(' ', '_').lower()}.md")
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="No pre-generated roadmap.")
    with open(filename, 'r', encoding='utf-8') as f:
        return RoadmapResponse(profile=profile, markdown=f.read())
