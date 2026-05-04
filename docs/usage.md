# Usage Guide

This guide explains how to execute the data pipelines and interact with the Career Roadmap system.

## 1. Local Scraper Pipeline (ETL)

The scraper pipeline searches for job listings across multiple platforms, extracts full job descriptions, and utilizes Gemini 2.0 Flash to identify technical skills.

**Execution:**
```bash
python web/api/src/scraper_pipeline.py
```

**What it does:**
-   **Multi-Board Fetching**: Scrapes LinkedIn, Wuzzuf, Indeed (EG), and Bayt.com.
-   **Deep Analysis**: Sends raw descriptions to Gemini for context-aware technical skill extraction.
-   **Data Persistence**: Saves results to both `data/egypt_data_skills.db` (SQLite) and `data/egypt_data_skills.parquet`.
-   **Vercel Sync**: Automatically populates the `web/api/data/` folder for serverless deployment.

---

## 2. Local Roadmap Generation

The roadmap generator reads the aggregated skills for a specific role and uses AI to reason about dependencies and learning paths.

**Execution:**
```bash
python web/api/src/roadmap_generator.py
```

**What it does:**
-   **Data Loading**: Reads from SQLite (primary) or Parquet (fallback).
-   **Frequency Ranking**: Identifies the Top 15 most in-demand skills for each profile.
-   **Pedagogical Logic**: Queries Gemini to build a sequential roadmap including "missing link" prerequisites.
-   **Markdown Export**: Saves professional roadmaps to the `output/` directory.

---

## 3. Local Web Development

You can run the interactive Next.js dashboard locally to explore the data and generate roadmaps through a GUI.

**Requirements:** Ensure your `.env` file contains your `GEMINI_API_KEY`.

**Execution:**
```bash
# Install dependencies
npm install

# Start the dev server (Frontend + API)
npm run dev
```
Navigate to `http://localhost:3000`.

**Features:**
-   **Dynamic Charts**: Interactive Recharts visualizations of the current job market trends.
-   **Live Roadmap Generation**: Click "Generate Roadmap" to trigger the serverless Gemini pipeline.
-   **Job Explorer**: Browse the raw jobs scraped from the various job boards via the `/api/v1/jobs` endpoint.

---

## 4. Automated Daily Updates (CI/CD)

The project is fully automated via GitHub Actions. You do not need to run the scraper manually once deployed.

**Workflow:**
-   **Cron Trigger**: Runs every day at 00:00 UTC.
-   **Execution**: Launches the Python pipeline in an Ubuntu container.
-   **Auto-Commit**: Fresh market data is automatically committed back to the repository.
-   **Vercel Deployment**: The commit triggers a fresh build on Vercel, ensuring your live app always shows today's data.

To trigger a manual update, go to the **Actions** tab in your GitHub repository and manually run the `Daily Job Market Scraper` workflow.
