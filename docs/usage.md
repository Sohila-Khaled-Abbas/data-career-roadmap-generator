# Usage Guide

This guide explains how to execute the data pipelines and generate learning roadmaps.

## 1. Data Extraction Pipeline

The scraper pipeline searches for job listings, extracts the job descriptions, and utilizes the AgentRouter API to dynamically identify technical skills.

**Execution:**
```bash
python scripts/scraper_pipeline.py
```

**Process:**
- Launches headless Playwright browser instances.
- Targets specific profiles defined in `TARGET_PROFILES` (e.g., Data Engineer, ML Engineer).
- Sends raw job descriptions to the `claude-haiku-4-5-20251001` model for strict JSON array extraction of tools.
- Saves the aggregated data into `data/egypt_data_skills.parquet` and `data/market_trends.db`.

## 2. Roadmap Generation Pipeline

The roadmap generator reads the processed data, calculates frequency distributions for a specific role, and prompts the LLM to build a sequential learning path.

**Execution:**
```bash
python scripts/roadmap_generator.py
```

**Process:**
- Reads `data/egypt_data_skills.parquet`.
- Filters for the target profile (configured in the `main` function).
- Identifies the top 15 most frequently mentioned tools.
- Queries the LLM to logically sequence the tools into a pedagogical roadmap.
- Saves the output as a Markdown file in the `output/` directory.

**Changing Target Profiles:**
To generate a roadmap for a different role, modify the `target_profile` variable in `scripts/roadmap_generator.py`:
```python
def main():
    target_profile = "Machine Learning Engineer" 
    # ...
```
