from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import sqlite3
import re
from datetime import datetime
import time
import os
import json
import google.generativeai as genai
from abc import ABC, abstractmethod

# API Key loaded from Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# Target profiles
TARGET_PROFILES = [
    "Data Analyst", "Data Engineer", "Analytics Engineer",
    "Data Scientist", "Machine Learning Engineer", "AI Engineer",
    "MLOps Engineer", "Computer Vision Engineer", "NLP Engineer",
    "Data Architect", "Real Time Analyst", "Product Analyst", 
    "Power BI Developer", "BI Developer"
]

class JobBoardScraper(ABC):
    @abstractmethod
    def fetch(self, job_title, location, page):
        pass

class LinkedInScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        return [
            {"title": f"Senior {job_title}", "company": "Global AI", "description": "PyTorch, AWS, Kubernetes and Dagster required."},
            {"title": f"{job_title} Specialist", "company": "Tech Corp", "description": "Strong SQL, Python, and Snowflake experience."},
            {"title": f"Junior {job_title}", "company": "DataWorks", "description": "Looking for skills in Python, pandas, and basic AWS."}
        ]

class WuzzufScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        return [
            {"title": f"{job_title}", "company": "Local Tech Egypt", "description": "SQL, Power BI, Python and dbt needed."},
            {"title": f"Lead {job_title}", "company": "FinTech EG", "description": "Advanced Airflow, Spark, and Postgres experience."},
            {"title": f"{job_title} Consultant", "company": "Consulting EG", "description": "Tableau, SQL Server, and Azure Data Factory."}
        ]

class IndeedScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        return [
            {"title": f"{job_title} II", "company": "MNC Inc", "description": "BigQuery, Looker, Python, and GCP."},
            {"title": f"{job_title} Engineer", "company": "StartupX", "description": "Fast-paced environment using Kafka, Rust, and AWS."},
            {"title": f"Remote {job_title}", "company": "GlobalTech", "description": "Require dbt, Snowflake, and Python."}
        ]

class GlassdoorScraper(JobBoardScraper):
    def fetch(self, job_title, location, page):
        return [
            {"title": f"{job_title} Manager", "company": "Data Insights", "description": "Managing team, hands-on with Python, SQL, AWS."},
            {"title": f"Staff {job_title}", "company": "MegaCorp", "description": "Scala, Hadoop, Spark, and Python."},
            {"title": f"{job_title} Intern", "company": "DevShop", "description": "Learning SQL, Python, and Git."}
        ]

def fetch_job_listings_playwright(job_title, location="Egypt"):
    extracted_jobs = []
    target_boards = [LinkedInScraper(), WuzzufScraper(), IndeedScraper(), GlassdoorScraper()] 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0")
        page = context.new_page()
        for board in target_boards:
            try:
                jobs = board.fetch(job_title, location, page)
                extracted_jobs.extend(jobs)
            except: pass
        browser.close()
    return extracted_jobs

def extract_skills_dynamically(description_text):
    """
    Uses Gemini 2.0 Flash to extract technical skills from job descriptions for free.
    """
    if not API_KEY:
        return []

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"Extract only technical tools and frameworks from this job description as a JSON list: {description_text}"
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up potential markdown formatting
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        return json.loads(text.strip())
    except Exception as e:
        print(f"❌ Skill Extraction failed: {e}")
        return []

def process_job_data(jobs, profile):
    processed_data = []
    crawl_date = datetime.now().strftime("%Y-%m-%d")
    
    for job in jobs:
        print(f"    [Gemini Flash] Analyzing: {job['title']}...")
        skills = extract_skills_dynamically(job['description'])
        processed_data.append({
            "crawl_date": crawl_date,
            "searched_profile": profile,
            "job_title": job.get("title", ""),
            "company": job.get("company", ""),
            "raw_description": job.get("description", ""),
            "skills_detected": ", ".join(skills),
            "skill_count": len(skills)
        })
        time.sleep(0.5) 
    return processed_data

def save_to_parquet(df, filename="data/egypt_data_skills.parquet"):
    os.makedirs('data', exist_ok=True)
    df.to_parquet(filename, index=False)

def save_to_sqlite(df, db_name="data/market_trends.db"):
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(db_name)
    df.to_sql('job_skills', conn, if_exists='append', index=False)
    conn.close()

def main():
    all_processed_jobs = []
    for profile in TARGET_PROFILES:
        raw_jobs = fetch_job_listings_playwright(profile, location="Egypt")
        if raw_jobs:
            processed = process_job_data(raw_jobs, profile)
            all_processed_jobs.extend(processed)
            
    if all_processed_jobs:
        df = pd.DataFrame(all_processed_jobs)
        save_to_parquet(df)
        save_to_sqlite(df)
        print("✅ ETL Pipeline Completed Successfully.")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()