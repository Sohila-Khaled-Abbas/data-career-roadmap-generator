import pandas as pd
import requests
import json
import os
from collections import Counter

# OpenRouter API Key
API_KEY = "sk-LbPg7LXBCBEZgBuCnDoKhkl1k6CYhOeRXODRxSwX4PkSkz6D"

def load_and_aggregate_skills(parquet_file, target_profile):
    """
    Reads the ETL output and calculates the most frequent skills for a specific role.
    """
    if not os.path.exists(parquet_file):
        raise FileNotFoundError(f"Pipeline output {parquet_file} not found. Run the ETL script first.")

    df = pd.read_parquet(parquet_file)
    
    # Filter for the requested profile
    profile_df = df[df['searched_profile'].str.lower() == target_profile.lower()]
    
    if profile_df.empty:
        raise ValueError(f"No data found for profile: {target_profile}")

    # Aggregate and count all skills
    all_skills = []
    for skills_string in profile_df['skills_detected']:
        if pd.notna(skills_string) and skills_string.strip():
            # Split by comma and clean whitespace
            skills = [s.strip() for s in skills_string.split(',')]
            all_skills.extend(skills)

    # Get frequency distribution
    skill_counts = Counter(all_skills)
    
    # Return the top 15 skills to keep the roadmap focused
    top_skills = [skill for skill, count in skill_counts.most_common(15)]
    return top_skills

def generate_roadmap_with_llm(profile, skills):
    """
    Uses the Gemini REST API to reason about skill dependencies and generate a Markdown roadmap.
    """
    print(f"Analyzing pedagogical dependencies for {profile} based on top skills: {skills}...")
    
    url = "https://agentrouter.org/v1/chat/completions"
    
    system_instruction = """
    You are a strict, senior technical lead and mentor. 
    Your job is to take a list of highly requested skills from the job market and arrange them into a logical, 
    step-by-step learning roadmap. You must group them logically (e.g., Prerequisites, Core, Advanced).
    Do not just list the tools; explain *why* they must be learned in this specific order.
    Output the result strictly in clean Markdown format.
    """
    
    user_prompt = f"Profile: {profile}\nTarget Skills based on market data: {', '.join(skills)}\n\nGenerate a sequential learning roadmap in Markdown."

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'Originator': 'codex_cli_rs',
        'Version': '0.101.0',
        'User-Agent': 'codex_cli_rs/0.101.0 (Mac OS 26.0.1; arm64) Apple_Terminal/464'
    }
    
    # Implementing exponential backoff as required
    delays = [1, 2, 4, 8, 16]
    for attempt, delay in enumerate(delays):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            # Extract text from the nested JSON response
            text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            if text:
                return text
            else:
                raise ValueError("Empty response from API")
                
        except requests.exceptions.RequestException:
            if attempt == len(delays) - 1:
                print(f"API request failed after {len(delays)} retries.")
                return None
            time.sleep(delay)

def save_markdown(content, profile):
    """Saves the LLM output to a formatted Markdown file."""
    filename = f"output/roadmap_{profile.replace(' ', '_').lower()}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Roadmap successfully generated and saved to: {filename}")

def main():
    target_profile = "Data Engineer" # Change this to test other profiles
    parquet_source = "data/egypt_data_skills.parquet"
    
    try:
        top_skills = load_and_aggregate_skills(parquet_source, target_profile)
        print(f"Top market skills identified: {top_skills}")
        
        roadmap_md = generate_roadmap_with_llm(target_profile, top_skills)
        
        if roadmap_md:
            save_markdown(roadmap_md, target_profile)
            
    except Exception as e:
        print(f"Error executing roadmap generation: {e}")

if __name__ == "__main__":
    import time # needed for the backoff retry logic
    main()