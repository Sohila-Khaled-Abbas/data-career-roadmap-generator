"""
Real-Time Job Market Scraper & Skill ETL Pipeline
====================================================
Sources: LinkedIn, Wuzzuf, Indeed (via job key), Bayt.com
AI:      Google Gemini 2.0 Flash for skill extraction
Storage: SQLite (.db) + Apache Parquet
"""

import pandas as pd
import sqlite3
import re
from datetime import datetime
import time
import os
import json
from urllib.parse import urlencode, quote_plus

from google import genai
from scrapling import Fetcher

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── API Key ────────────────────────────────────────────────────────────────
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "CRITICAL ERROR: GEMINI_API_KEY is not set. "
        "Set it via environment variable or a .env file."
    )

client = genai.Client(api_key=API_KEY)

# ── Target Profiles ────────────────────────────────────────────────────────
TARGET_PROFILES = [
    "Data Analyst", "Data Engineer", "Analytics Engineer",
    "Data Scientist", "Machine Learning Engineer",
    "BI Developer", "Business Intelligence Developer",
    "Product Analyst", "Real Time Analyst", "WFM Analyst",
    "Data Architect", "MLOps Engineer", "NLP Engineer",
    "Computer Vision Engineer", "Reporting Analyst",
]

# ── Scraper ────────────────────────────────────────────────────────────────
class RealJobScraper:
    def __init__(self):
        self.fetcher = Fetcher()

    # ── LinkedIn ───────────────────────────────────────────────────────────
    def fetch_linkedin_jobs(self, job_title: str, location: str = "Egypt") -> list:
        print(f"  [LinkedIn] {job_title}")
        query = quote_plus(job_title)
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}"
        try:
            page = self.fetcher.get(url, allow_redirects=True)
            cards = page.css("div.base-card")
            return self._parse_linkedin_cards(cards, limit=4)
        except Exception as e:
            print(f"    [ERROR] LinkedIn fetch failed: {e}")
            return []

    def _parse_linkedin_cards(self, cards, limit: int = 4) -> list:
        extracted = []
        for card in cards[:limit]:
            title_el   = card.css(".base-search-card__title")
            company_el = card.css(".base-search-card__subtitle")
            link_el    = card.css(".base-card__full-link")

            title = title_el[0].text.strip()   if title_el   else ""
            link  = link_el[0].attrib.get("href", "") if link_el else ""

            company = ""
            if company_el:
                a_tags = company_el[0].css("a")
                company = a_tags[0].text.strip() if a_tags else company_el[0].text.strip()

            description = self._fetch_linkedin_description(link, title, company)

            if title:
                extracted.append({
                    "source": "LinkedIn",
                    "title": title,
                    "company": company or "Unknown Company",
                    "url": link,
                    "description": description,
                })
        return extracted

    def _fetch_linkedin_description(self, url: str, title: str, company: str) -> str:
        if not url:
            return f"Job Title: {title}. Company: {company}."
        try:
            time.sleep(1.2)
            p = self.fetcher.get(url, allow_redirects=True)
            el = p.css(".show-more-less-html__markup")
            return el[0].text.strip() if el else f"Job Title: {title}. Company: {company}."
        except Exception:
            return f"Job Title: {title}. Company: {company}."

    # ── Wuzzuf ─────────────────────────────────────────────────────────────
    def fetch_wuzzuf_jobs(self, job_title: str, location: str = "Egypt") -> list:
        print(f"  [Wuzzuf]   {job_title}")
        query = job_title.replace(" ", "+")
        url = f"https://wuzzuf.net/search/jobs/?q={query}&a=hpb"
        try:
            page  = self.fetcher.get(url, allow_redirects=True)
            cards = page.css("div.css-pkv5jc")
            extracted = []
            for card in cards[:4]:
                title_el   = card.css("h2 a")
                company_el = card.css(".css-d7j1kk a")
                title   = title_el[0].text.strip()  if title_el   else ""
                company = (
                    company_el[0].text.strip().replace("-", "").strip()
                    if company_el else ""
                )
                href = title_el[0].attrib.get("href", "") if title_el else ""
                job_url = ("https://wuzzuf.net" + href) if href and not href.startswith("http") else href

                description = self._fetch_wuzzuf_description(job_url, title, company)

                if title:
                    extracted.append({
                        "source": "Wuzzuf",
                        "title": title,
                        "company": company or "Unknown Company",
                        "url": job_url,
                        "description": description,
                    })
            return extracted
        except Exception as e:
            print(f"    [ERROR] Wuzzuf fetch failed: {e}")
            return []

    def _fetch_wuzzuf_description(self, url: str, title: str, company: str) -> str:
        if not url:
            return f"Job Title: {title}. Company: {company}."
        try:
            time.sleep(1.2)
            p = self.fetcher.get(url, allow_redirects=True)
            # Wuzzuf renders description text in multiple paragraphs inside the card
            paras = p.css(".css-o1vzmt, .css-4c4ojb, .css-0, article p")
            text  = " ".join(e.text.strip() for e in paras if e.text.strip())
            return text if text else f"Job Title: {title}. Company: {company}."
        except Exception:
            return f"Job Title: {title}. Company: {company}."

    # ── Indeed (Egypt) ─────────────────────────────────────────────────────
    def fetch_indeed_jobs(self, job_title: str, location: str = "Egypt") -> list:
        print(f"  [Indeed]   {job_title}")
        query = quote_plus(job_title)
        url = f"https://eg.indeed.com/jobs?q={query}&l={quote_plus(location)}"
        try:
            page  = self.fetcher.get(url, allow_redirects=True)
            cards = page.css(".job_seen_beacon, .resultContent")
            extracted = []
            for card in cards[:4]:
                # Get job key from href
                a_tags  = card.css("a")
                title_h = card.css("h2")
                title   = title_h[0].text.strip() if title_h else ""
                if not title and a_tags:
                    title = a_tags[0].text.strip()

                # Company name is usually in a span
                spans = card.css("span")
                company = ""
                for s in spans:
                    t = s.text.strip()
                    if t and len(t) < 60 and t != title:
                        company = t
                        break

                # Extract job key from rc/clk href
                href = ""
                for a in a_tags:
                    h = a.attrib.get("href", "")
                    if "jk=" in h or h.startswith("/rc/clk"):
                        href = h
                        break

                jk = re.search(r"jk=([a-f0-9]+)", href)
                job_url = f"https://eg.indeed.com/viewjob?jk={jk.group(1)}" if jk else ""

                description = self._fetch_indeed_description(job_url, title, company)

                if title:
                    extracted.append({
                        "source": "Indeed",
                        "title": title,
                        "company": company or "Unknown Company",
                        "url": job_url,
                        "description": description,
                    })
            return extracted
        except Exception as e:
            print(f"    [ERROR] Indeed fetch failed: {e}")
            return []

    def _fetch_indeed_description(self, url: str, title: str, company: str) -> str:
        if not url:
            return f"Job Title: {title}. Company: {company}."
        try:
            time.sleep(1.2)
            p = self.fetcher.get(url, allow_redirects=True)
            # Try known selectors, then fall back to full page text
            for sel in ["#jobDescriptionText", ".jobsearch-jobDescriptionText",
                        "[id*=JobDescription]", "#mosaic-vjJobDetails"]:
                el = p.css(sel)
                if el and el[0].text.strip():
                    return el[0].text.strip()[:3000]
            # Last resort: raw page text (better than nothing for Gemini)
            raw = p.text.strip()
            return raw[:3000] if raw else f"Job Title: {title}. Company: {company}."
        except Exception:
            return f"Job Title: {title}. Company: {company}."

    # ── Bayt ───────────────────────────────────────────────────────────────
    def fetch_bayt_jobs(self, job_title: str, location: str = "egypt") -> list:
        print(f"  [Bayt]     {job_title}")
        slug = job_title.lower().replace(" ", "-") + "-jobs"
        url  = f"https://www.bayt.com/en/{location}/jobs/{slug}/"
        try:
            page  = self.fetcher.get(url, allow_redirects=True)
            # Bayt lists job hrefs as /en/egypt/jobs/<slug>-<id>/
            seen  = set()
            links = []
            for a in page.css("a"):
                href = a.attrib.get("href", "")
                # Only individual job posting pages: /en/egypt/jobs/<job-slug>-<numeric-id>/
                if (re.match(r"/en/egypt/jobs/[^/]+-\d+/$", href)
                        and href not in seen):
                    seen.add(href)
                    links.append(href)

            extracted = []
            for href in links[:4]:
                full_url = "https://www.bayt.com" + href
                title, company, description = self._fetch_bayt_detail(full_url)
                if title:
                    extracted.append({
                        "source": "Bayt",
                        "title": title,
                        "company": company or "Unknown Company",
                        "url": full_url,
                        "description": description,
                    })
            return extracted
        except Exception as e:
            print(f"    [ERROR] Bayt fetch failed: {e}")
            return []

    def _fetch_bayt_detail(self, url: str):
        try:
            time.sleep(1.2)
            p = self.fetcher.get(url, allow_redirects=True)
            # Title
            title_el = p.css("h1, h2.t-default")
            title    = title_el[0].text.strip() if title_el else ""
            # Company
            co_el   = p.css("[class*=company], [itemprop=name]")
            company = co_el[0].text.strip() if co_el else ""
            # Description — Bayt uses DL/DD or article body
            desc_el = p.css("dl dd, article, [class*=description], main p")
            description = " ".join(e.text.strip() for e in desc_el if e.text.strip())
            if not description:
                description = p.text.strip()[:3000]
            return title, company, description[:3000]
        except Exception:
            return "", "", ""


# ── Gemini Skill Extraction ────────────────────────────────────────────────
def extract_skills_dynamically(description_text: str) -> list:
    """Use Gemini 2.0 Flash to extract technical skills from a job description."""
    if not description_text.strip():
        return []
    try:
        prompt = (
            "Extract ONLY technical tools, programming languages, libraries, "
            "platforms, and frameworks from this job description. "
            "Return a JSON array of lowercase strings ONLY — no explanation, no markdown. "
            f"Description: {description_text[:2500]}"
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        skills = json.loads(text.strip())
        # Deduplicate + lowercase
        return list(dict.fromkeys(s.lower().strip() for s in skills if s.strip()))
    except Exception as e:
        print(f"    [WARN] Skill extraction failed: {e}")
        return []


# ── Process Jobs → Structured Records ─────────────────────────────────────
def process_job_data(jobs: list, profile: str) -> list:
    records    = []
    crawl_date = datetime.now().strftime("%Y-%m-%d")
    for job in jobs:
        print(f"    [Gemini] {job['title']} @ {job['company']} ({job['source']})")
        skills = extract_skills_dynamically(job["description"])
        records.append({
            "crawl_date":       crawl_date,
            "searched_profile": profile,
            "source":           job.get("source", "Unknown"),
            "job_title":        job.get("title", ""),
            "company":          job.get("company", ""),
            "job_url":          job.get("url", ""),
            "raw_description":  job.get("description", "")[:500] + "…",
            "skills_detected":  ", ".join(skills),
            "skill_count":      len(skills),
        })
        time.sleep(0.8)
    return records


# ── Storage: Parquet + SQLite ──────────────────────────────────────────────
def save_to_parquet(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"  [Parquet] Saved → {path}")


def save_to_sqlite(df: pd.DataFrame, db_path: str, table: str = "job_skills"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = sqlite3.connect(db_path)
    # Append new rows; create table on first run
    df.to_sql(table, con, if_exists="append", index=False)
    con.close()
    print(f"  [SQLite]  Saved → {db_path}  (table: {table})")


def parquet_to_sqlite(parquet_path: str, db_path: str, table: str = "job_skills"):
    """Convert an existing Parquet file to a SQLite DB (full replace)."""
    if not os.path.exists(parquet_path):
        print(f"  [WARN] Parquet not found: {parquet_path}")
        return
    df = pd.read_parquet(parquet_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = sqlite3.connect(db_path)
    df.to_sql(table, con, if_exists="replace", index=False)
    con.close()
    print(f"  [SQLite]  Converted Parquet → {db_path}  ({len(df)} rows)")


# ── Main Pipeline ──────────────────────────────────────────────────────────
def main():
    scraper          = RealJobScraper()
    all_records: list = []

    for profile in TARGET_PROFILES:
        print(f"\n[Profile] {profile}")
        jobs: list = []
        jobs += scraper.fetch_linkedin_jobs(profile)
        jobs += scraper.fetch_wuzzuf_jobs(profile)
        jobs += scraper.fetch_indeed_jobs(profile)
        jobs += scraper.fetch_bayt_jobs(profile)

        if jobs:
            records = process_job_data(jobs, profile)
            all_records.extend(records)
            print(f"  Collected {len(records)} records for '{profile}'")
        else:
            print(f"  No jobs found for '{profile}' — skipping")

    if not all_records:
        print("\n[ERROR] No data extracted at all. Check connectivity / blocking.")
        return

    df = pd.DataFrame(all_records)

    # ── Save Parquet (for Vercel API) ──────────────────────────────────────
    save_to_parquet(df, "web/api/data/egypt_data_skills.parquet")
    save_to_parquet(df, "data/egypt_data_skills.parquet")

    # ── Save SQLite (for local analytics & the API) ────────────────────────
    save_to_sqlite(df, "web/api/data/egypt_data_skills.db")
    save_to_sqlite(df, "data/egypt_data_skills.db")

    print(
        f"\n[SUCCESS] Pipeline complete — {len(all_records)} records "
        f"across {len(TARGET_PROFILES)} profiles from 4 job boards."
    )


if __name__ == "__main__":
    main()
