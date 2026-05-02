# Usage Guide

This guide explains how to execute the data pipelines and generate learning roadmaps.

## 1. Automated Pipeline (Recommended)

The easiest way to execute the core ETL process is to use the automation script.

**Execution:**
```bash
python automate.py
```
This script will sequentially run the scraper and generate the default roadmaps. To view the UI, you must launch the Docker containers (see section 2).

---

## 2. Docker Execution

You can run the entire pipeline in an isolated container without installing dependencies locally.

**Execution:**
```bash
docker-compose up --build
```
This will build the images, run the `etl-worker` pipeline internally, host the `api-backend`, and map the Next.js frontend to `http://localhost:3000`.

---

## 3. Manual Data Extraction Pipeline

The scraper pipeline searches for job listings, extracts the job descriptions, and utilizes the AgentRouter API to dynamically identify technical skills.

**Execution:**
```bash
python src/scraper_pipeline.py
```

**Process:**
- Launches headless Playwright browser instances.
- Targets specific profiles defined in `TARGET_PROFILES` (e.g., Data Engineer, ML Engineer).
- Sends raw job descriptions to the `claude-haiku-4-5-20251001` model for strict JSON array extraction of tools.
- Saves the aggregated data into `data/egypt_data_skills.parquet` and `data/market_trends.db`.

## 4. Manual Roadmap Generation Pipeline

The roadmap generator reads the processed data, calculates frequency distributions for a specific role, and prompts the LLM to build a sequential learning path.

**Execution:**
```bash
python src/roadmap_generator.py
```

**Process:**
- Reads `data/egypt_data_skills.parquet`.
- Filters for the target profile (configured in the `main` function).
- Identifies the top 15 most frequently mentioned tools.
- Queries the LLM to logically sequence the tools into a pedagogical roadmap.
- Saves the output as a Markdown file in the `output/` directory.

**Changing Target Profiles:**
To generate a roadmap for a different role, modify the `target_profile` variable in `src/roadmap_generator.py`:
```python
def main():
    target_profile = "Machine Learning Engineer" 
    # ...
```

## 5. Next.js Web Frontend

For a more user-friendly experience, you can use the Next.js web application. This interface allows you to visually explore the top skills and generate roadmaps with a single click.

**Execution:**
Ensure the FastAPI backend is running, then start the development server:
```bash
cd web
npm install
npm run dev
```
Navigate to `http://localhost:3000` in your browser.

**Features:**
- Visually configure target profiles from the sidebar.
- Visualize the top 15 most requested skills via an interactive Recharts bar chart.
- Generate and view Claude AI roadmaps rendered cleanly via react-markdown.

## 6. Jupyter Notebook Walkthrough

For learners and developers who want to understand the code execution step-by-step, the project includes an interactive Jupyter Notebook (`Data_Career_Roadmap.ipynb`).

**Execution:**
```bash
jupyter notebook notebooks/Data_Career_Roadmap.ipynb
```

**Features:**
- Step-by-step execution of the scraping logic.
- Real-time interaction with the AgentRouter Claude AI model for skill extraction.
- Inline preview of the Pandas DataFrame.
- Saving Parquet, SQLite, and Markdown roadmap files directly to the `output/` folder.

## 7. FastAPI Backend Server

A decoupled FastAPI backend has been implemented to serve the ETL data via REST APIs, paving the way for distinct web frontends (like Next.js).

**Execution:**
```bash
uvicorn src.api.main:app --reload --port 8000
```

**Features:**
- **Interactive API Docs:** Automatically generated Swagger UI available at `http://localhost:8000/docs`.
- **Decoupled Architecture:** Cleanly separates the data layer (Parquet/SQLite) from the presentation layer.
- **Robust Endpoints:** Fetch aggregated skills, market insights, and trigger Claude AI generation securely via REST calls.
