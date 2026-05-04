import pandas as pd
import os
import time
from collections import Counter
from google import genai
try:
    from dotenv import load_dotenv
    load_dotenv()
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

def main():
    parquet_source = "data/egypt_data_skills.parquet"
    
    if not os.path.exists(parquet_source):
        print(f"❌ Pipeline output {parquet_source} not found. Run the ETL script first.")
        return

    try:
        df = pd.read_parquet(parquet_source)
        profiles = df['searched_profile'].unique()
        
        print(f"🔍 Found {len(profiles)} unique job profiles in data.")
        
        for profile in profiles:
            print(f"\n🚀 Processing roadmap for: {profile}...")
            
            top_skills = load_and_aggregate_skills(df, profile)
            if not top_skills:
                print(f"⚠️ No skills identified for {profile}, skipping.")
                continue
                
            roadmap_md = generate_roadmap_with_llm(profile, top_skills)
            
            if roadmap_md:
                save_markdown(roadmap_md, profile)
            else:
                print(f"❌ Failed to generate roadmap for {profile}")
                
            time.sleep(1) # Rate limit respect
            
    except Exception as e:
        print(f"Error executing roadmap generation: {e}")

if __name__ == "__main__":
    main()