import pandas as pd
import os
import sqlite3
import time
from collections import Counter
from google import genai
try:
    from dotenv import load_dotenv, find_dotenv
    # Search upward from this script file, not from CWD
    _env_path = find_dotenv(usecwd=False)
    if _env_path:
        load_dotenv(_env_path)
except ImportError:
    pass

# API Key loaded from Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_API_KEY environment variable is not set! Roadmap generation cannot proceed.")

client = genai.Client(api_key=API_KEY)

def load_and_aggregate_skills(df, target_profile):
    """
    Calculates the most frequent skills for a specific role from the provided dataframe.
    """
    profile_df = df[df['searched_profile'].str.lower() == target_profile.lower()]
    
    if profile_df.empty:
        return []

    all_skills = []
    for skills_string in profile_df['skills_detected']:
        if pd.notna(skills_string) and skills_string.strip():
            skills = [s.strip() for s in skills_string.split(',')]
            all_skills.extend(skills)

    skill_counts = Counter(all_skills)
    top_skills = [skill for skill, count in skill_counts.most_common(15)]
    return top_skills

def generate_roadmap_with_llm(profile, skills):
    """
    Uses Gemini 2.0 Flash to reason about skill dependencies and generate a Markdown roadmap.
    """
    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY is not set.")
        return None

    print(f"🚀 Generating roadmap for {profile} using Gemini...")
    
    try:
        prompt = f"""
        You are a senior technical lead and career mentor.
        Based on market data for the profile '{profile}', the most in-demand skills are: {', '.join(skills)}.
        
        Generate a sequential, step-by-step learning roadmap in Markdown.
        1. Group skills into logical phases (e.g., Fundamentals, Core Tools, Advanced).
        2. Explain briefly why each step is important.
        3. Keep the tone professional and encouraging.
        
        Output ONLY the Markdown content.
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        print(f"❌ Gemini Roadmap Generation failed: {e}")
        return None

def save_markdown(content, profile):
    """Saves the LLM output to a formatted Markdown file."""
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = f"output/roadmap_{profile.replace(' ', '_').lower()}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Roadmap successfully generated and saved to: {filename}")

def load_data(db_path="data/egypt_data_skills.db", parquet_path="data/egypt_data_skills.parquet"):
    """Load job skills data from SQLite DB with Parquet as fallback."""
    if os.path.exists(db_path):
        try:
            con = sqlite3.connect(db_path)
            df  = pd.read_sql("SELECT * FROM job_skills", con)
            con.close()
            print(f"Loaded {len(df)} records from SQLite: {db_path}")
            return df
        except Exception as e:
            print(f"SQLite load failed ({e}), falling back to Parquet")
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        print(f"Loaded {len(df)} records from Parquet: {parquet_path}")
        return df
    return None

def main():
    db_path      = "data/egypt_data_skills.db"
    parquet_path = "data/egypt_data_skills.parquet"
    
    df = load_data(db_path, parquet_path)
    if df is None:
        print(f"No data found. Run scraper_pipeline.py first.")
        return

    profiles = df["searched_profile"].unique()
    print(f"Found {len(profiles)} unique job profiles in data.")
    
    for profile in profiles:
        print(f"\nProcessing roadmap for: {profile}...")
        
        top_skills = load_and_aggregate_skills(df, profile)
        if not top_skills:
            print(f"No skills identified for {profile}, skipping.")
            continue
            
        roadmap_md = generate_roadmap_with_llm(profile, top_skills)
        
        if roadmap_md:
            save_markdown(roadmap_md, profile)
        else:
            print(f"Failed to generate roadmap for {profile}")
            
        time.sleep(1)

if __name__ == "__main__":
    main()