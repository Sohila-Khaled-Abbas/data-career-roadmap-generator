import pandas as pd
import sqlite3
import re
from datetime import datetime
import time
import os
import json
import google.generativeai as genai
from scrapling import Fetcher

# API Key loaded from Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# Target profiles
TARGET_PROFILES = [
    "Data Analyst", "Data Engineer", "Analytics Engineer",
    "Data Scientist", "Machine Learning Engineer"
]

class RealJobScraper:
    def __init__(self):
        # Configure Scrapling fetcher for stealth
        self.fetcher = Fetcher()
        
    def fetch_linkedin_jobs(self, job_title, location="Egypt"):
        print(f"[Scrapling] Fetching real LinkedIn jobs for: {job_title} in {location}")
        query = job_title.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"
        
        try:
            page = self.fetcher.get(url)
            job_cards = page.css('div.base-card')
            
            extracted = []
            for card in job_cards[:5]: # Limit to top 5 per profile to save time/API calls
                title_elem = card.css_first('.base-search-card__title')
                company_elem = card.css_first('.base-search-card__subtitle')
                link_elem = card.css_first('.base-card__full-link')
                
                title = title_elem.text.strip() if title_elem else ""
                company = company_elem.text.strip() if company_elem else ""
                job_url = link_elem.attrib.get('href', '') if link_elem else ""
                
                description = ""
                # Fetch actual job description if link exists
                if job_url:
                    try:
                        # Add a small delay to avoid rate limits
                        time.sleep(1)
                        desc_page = self.fetcher.get(job_url)
                        desc_elem = desc_page.css_first('.show-more-less-html__markup')
                        description = desc_elem.text.strip() if desc_elem else f"Job Title: {title}. Company: {company}."
                    except Exception as e:
                        print(f"Failed to fetch description for {title}: {e}")
                        description = f"Job Title: {title}. Company: {company}."

                if title and company:
                    extracted.append({
                        "title": title,
                        "company": company,
                        "description": description
                    })
            return extracted
        except Exception as e:
            print(f"[ERROR] Scrapling fetch failed: {e}")
            return []

def extract_skills_dynamically(description_text):
    """
    Uses Gemini 2.0 Flash to extract technical skills from REAL job descriptions.
    """
    if not API_KEY or not description_text.strip():
        return []

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"Extract ONLY technical tools, programming languages, and frameworks from this real job description as a JSON list of strings (no other text). Description: {description_text[:2000]}"
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        return json.loads(text.strip())
    except Exception as e:
        print(f"[ERROR] Skill Extraction failed: {e}")
        return []

def process_job_data(jobs, profile):
    processed_data = []
    crawl_date = datetime.now().strftime("%Y-%m-%d")
    
    for job in jobs:
        print(f"    [Gemini Flash] Analyzing real job: {job['title']} at {job['company']}...")
        skills = extract_skills_dynamically(job['description'])
        processed_data.append({
            "crawl_date": crawl_date,
            "searched_profile": profile,
            "job_title": job.get("title", ""),
            "company": job.get("company", ""),
            "raw_description": job.get("description", "")[:500] + "...", # truncate for storage
            "skills_detected": ", ".join(skills),
            "skill_count": len(skills)
        })
        time.sleep(1) # Respect Gemini API limits
    return processed_data

def save_to_parquet(df, filename="data/egypt_data_skills.parquet"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_parquet(filename, index=False)

def main():
    scraper = RealJobScraper()
    all_processed_jobs = []
    
    for profile in TARGET_PROFILES:
        raw_jobs = scraper.fetch_linkedin_jobs(profile, location="Egypt")
        if raw_jobs:
            processed = process_job_data(raw_jobs, profile)
            all_processed_jobs.extend(processed)
            
    if all_processed_jobs:
        df = pd.DataFrame(all_processed_jobs)
        
        # Save to the web/api/data folder so Vercel can use it immediately
        save_to_parquet(df, "web/api/data/egypt_data_skills.parquet")
        # Also save to root for local dev
        save_to_parquet(df, "data/egypt_data_skills.parquet")
        
        print(f"[SUCCESS] Real Data ETL Pipeline Completed. Scraped {len(all_processed_jobs)} real jobs.")
    else:
        print("[ERROR] No real data extracted. Check your internet connection or LinkedIn blocking.")

if __name__ == "__main__":
    main()
