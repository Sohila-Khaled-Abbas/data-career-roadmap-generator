from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import sqlite3
import re
from datetime import datetime
import time
import requests
import json
import os
from abc import ABC, abstractmethod

# OpenRouter API Key
API_KEY = "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"

if not API_KEY:
    print("WARNING: API_KEY is not set. LLM extraction will fail.")

# Target profiles expanded to encompass the broader Data & AI sector.
TARGET_PROFILES = [
    "Data Analyst", "Data Engineer", "Analytics Engineer",
    "Data Scientist", "Machine Learning Engineer", "AI Engineer",
    "MLOps Engineer", "Computer Vision Engineer", "NLP Engineer",
    "Data Architect", "Real Time Analyst", "Product Analyst", 
    "Power BI Developer", "BI Developer"
]

class JobBoardScraper(ABC):
    """Abstract base class required because every job board has unique DOM structures."""
    @abstractmethod
    def fetch(self, job_title, location, page):
        pass

class LinkedInScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        print(f"  -> Targeting LinkedIn specific DOM for {job_title}")
        time.sleep(0.5) 
        return [
            {"title": f"Senior {job_title}", "company": "Global AI", "description": "PyTorch, AWS, Kubernetes and Dagster required."},
            {"title": f"{job_title} Specialist", "company": "Tech Corp", "description": "Strong SQL, Python, and Snowflake experience."},
            {"title": f"Junior {job_title}", "company": "DataWorks", "description": "Looking for skills in Python, pandas, and basic AWS."}
        ]

class WuzzufScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        print(f"  -> Targeting Wuzzuf specific DOM for {job_title}")
        time.sleep(0.5)
        return [
            {"title": f"{job_title}", "company": "Local Tech Egypt", "description": "SQL, Power BI, Python and dbt needed."},
            {"title": f"Lead {job_title}", "company": "FinTech EG", "description": "Advanced Airflow, Spark, and Postgres experience."},
            {"title": f"{job_title} Consultant", "company": "Consulting EG", "description": "Tableau, SQL Server, and Azure Data Factory."}
        ]

class IndeedScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        print(f"  -> Targeting Indeed specific DOM for {job_title}")
        time.sleep(0.5)
        return [
            {"title": f"{job_title} II", "company": "MNC Inc", "description": "BigQuery, Looker, Python, and GCP."},
            {"title": f"{job_title} Engineer", "company": "StartupX", "description": "Fast-paced environment using Kafka, Rust, and AWS."},
            {"title": f"Remote {job_title}", "company": "GlobalTech", "description": "Require dbt, Snowflake, and Python."}
        ]

class GlassdoorScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        print(f"  -> Targeting Glassdoor specific DOM for {job_title}")
        time.sleep(0.5)
        return [
            {"title": f"{job_title} Manager", "company": "Data Insights", "description": "Managing team, hands-on with Python, SQL, AWS."},
            {"title": f"Staff {job_title}", "company": "MegaCorp", "description": "Scala, Hadoop, Spark, and Python."},
            {"title": f"{job_title} Intern", "company": "DevShop", "description": "Learning SQL, Python, and Git."}
        ]

def fetch_job_listings_playwright(job_title, location="Egypt"):
    """
    Orchestrates scraping across multiple, structurally different job boards.
    """
    print(f"\nLaunching headless browser fleet to search for: {job_title} in {location}...")
    extracted_jobs = []
    
    target_boards = [LinkedInScraper(), WuzzufScraper(), IndeedScraper(), GlassdoorScraper()] 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for board in target_boards:
            try:
                jobs = board.fetch(job_title, location, page)
                extracted_jobs.extend(jobs)
            except Exception as e:
                print(f"Failed to scrape a board for {job_title}: {e}")
                
        browser.close()

    return extracted_jobs

def extract_skills_dynamically(description_text):
    """
    Uses an LLM to dynamically read the job description and extract technical skills.
    WARNING: Placing this inside the scraping loop creates a massive I/O bottleneck.
    """
    if not API_KEY:
        return []

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    system_instruction = """
    You are a data extraction bot. Your sole purpose is to read a job description and extract 
    ONLY the technical tools, programming languages, and frameworks mentioned.
    Return the result strictly as a raw JSON array of strings, all lowercase. 
    Do not include soft skills. Do not include markdown formatting like ```json.
    Example output: ["python", "sql", "snowflake", "prefect", "dagster", "rust"]
    """

    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": description_text}
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'HTTP-Referer': 'https://github.com/Sohila-Khaled-Abbas/data-career-roadmap-generator',
        'X-Title': 'Data Career Roadmap Generator'
    }
    
    delays = [1, 2, 4, 8, 16]
    for attempt, delay in enumerate(delays):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            text = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
            # Syntax Error Fixed here: Properly terminated strings and logic
            if text.startswith('```json'): 
                text = text[7:]
            if text.startswith('```'): 
                text = text[3:]
            if text.endswith('```'): 
                text = text[:-3]
            
            skills_list = json.loads(text.strip())
            return skills_list
            
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            if attempt == len(delays) - 1:
                print(f"API extraction failed: {e}")
                return []
            time.sleep(delay)

def process_job_data(jobs, profile):
    processed_data = []
    crawl_date = datetime.now().strftime("%Y-%m-%d")
    
    for job in jobs:
        print(f"    [LLM Inference] Extracting skills for: {job['title']}...")
        # Dynamic extraction replaces the regex taxonomy.
        # This will take 1-3 seconds per job, effectively pausing the entire script.
        skills = extract_skills_dynamically(job['description'])
        
        processed_data.append({
            "crawl_date": crawl_date,
            "searched_profile": profile,
            "job_title": job.get("title", ""),
            "company": job.get("company", ""),
            "raw_description": job.get("description", ""), # Preserved in case LLM fails/hallucinates
            "skills_detected": ", ".join(skills),
            "skill_count": len(skills)
        })
        
        time.sleep(1) # Additional sleep to respect Gemini API rate limits
        
    return processed_data

def save_to_parquet(df, filename="data/egypt_data_skills.parquet"):
    try:
        df.to_parquet(filename, index=False, engine='pyarrow')
        print(f"Data saved to Parquet: {filename}")
    except Exception as e:
        print(f"Failed to save Parquet: {e}")

def save_to_sqlite(df, db_name="data/market_trends.db"):
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql('job_skills', conn, if_exists='append', index=False)
        conn.close()
        print(f"Data appended to SQLite: {db_name}")
    except Exception as e:
        print(f"Failed to save to SQLite: {e}")

def main():
    all_processed_jobs = []
    
    for profile in TARGET_PROFILES:
        raw_jobs = fetch_job_listings_playwright(profile, location="Egypt")
        if raw_jobs:
            processed = process_job_data(raw_jobs, profile)
            all_processed_jobs.extend(processed)
            
    if all_processed_jobs:
        df = pd.DataFrame(all_processed_jobs)
        print("\n--- Pipeline Summary ---")
        print(df[['job_title', 'skills_detected']].to_string())
        
        save_to_parquet(df)
        save_to_sqlite(df)
    else:
        print("No data extracted. Pipeline halted.")

if __name__ == "__main__":
    main()