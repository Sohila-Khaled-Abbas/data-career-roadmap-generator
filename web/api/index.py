from fastapi import FastAPI, HTTPException, Path, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
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

PARQUET_PATH = os.path.join(ROOT_DIR, "data", "egypt_data_skills.parquet")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

class SkillFrequency(BaseModel):
    skill: str
    frequency: int

class RoadmapGenerateRequest(BaseModel):
    profile: str
    skills: List[str]

class RoadmapResponse(BaseModel):
    profile: str
    markdown: str

def load_parquet_data() -> pd.DataFrame:
    # On Vercel, files in the root are included in the deployment
    if not os.path.exists(PARQUET_PATH):
        raise HTTPException(status_code=503, detail="Market data not found. Please ensure 'data/' folder is committed.")
    return pd.read_parquet(PARQUET_PATH)

@app.get("/api/v1/profiles")
def get_profiles():
    df = load_parquet_data()
    return sorted(df['searched_profile'].dropna().unique().tolist())

@app.get("/api/v1/skills/{profile}/top")
def get_top_skills(profile: str, limit: int = 15):
    df = load_parquet_data()
    profile_df = df[df['searched_profile'].str.lower() == profile.lower()]
    
    all_skills = []
    for skills_string in profile_df['skills_detected']:
        if pd.notna(skills_string):
            all_skills.extend([s.strip() for s in skills_string.split(',')])
            
    skill_counts = Counter(all_skills)
    return [SkillFrequency(skill=s, frequency=f) for s, f in skill_counts.most_common(limit)]

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
