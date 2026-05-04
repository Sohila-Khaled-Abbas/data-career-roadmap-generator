# Data & AI Career Roadmap Generator

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Scrapling](https://img.shields.io/badge/Scrapling-Automated_Scraping-2ea44f?logo=python&logoColor=white)](https://github.com/D4Vinci/Scrapling)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-8E75B2?logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Serverless_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-React_Framework-black?logo=nextdotjs)](https://nextjs.org/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel&logoColor=white)](https://vercel.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

An end-to-end data engineering pipeline that scrapes real-time job market data across multiple platforms, extracts technical skills using Gemini 2.0 Flash, and powers an interactive Serverless Next.js web application to generate sequential learning roadmaps. Includes a GitHub Actions cron job for daily market data updates across 15+ job profiles.

---

## System Architecture

```mermaid
graph TD
    %% Modern Color Palette and Styles
    classDef scraper fill:#2563eb,stroke:#1e40af,stroke-width:2px,color:#fff,rx:8px,ry:8px
    classDef ai fill:#7c3aed,stroke:#5b21b6,stroke-width:2px,color:#fff,rx:8px,ry:8px
    classDef database fill:#059669,stroke:#047857,stroke-width:2px,color:#fff,rx:8px,ry:8px
    classDef ui fill:#db2777,stroke:#be185d,stroke-width:2px,color:#fff,rx:8px,ry:8px
    classDef file fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff,rx:8px,ry:8px

    subgraph "Scraping Engine (Scrapling)"
        A1["LinkedIn"]:::scraper
        A2["Wuzzuf"]:::scraper
        A3["Indeed (EG)"]:::scraper
        A4["Bayt.com"]:::scraper
    end

    A1 & A2 & A3 & A4 -->|Stealth Fetch| B["Real Job Descriptions"]:::scraper
    B -->|Gemini 2.0 Flash: Deep Skill Analysis| C["Dynamic Skill Extraction"]:::ai
    C -->|Structured Data| D["SQLite (.db) & Parquet"]:::database
    D -->|Aggregation| E["Top Skills per Profile"]:::database
    E -->|Intelligent Roadmap Logic| F["Pedagogical Learning Roadmap"]:::ai
    F -->|Markdown Export| G["output/roadmap_*.md"]:::file
    D -->|Vercel API| H["Next.js Web Frontend"]:::ui
```

---

## Key Features

- **Multi-Source Aggregation**: Scrapes and merges data from **LinkedIn, Wuzzuf, Indeed, and Bayt.com** to provide a comprehensive view of the Middle East and global data markets.
- **15+ Specialized Profiles**: Tracks demand for roles from Data Analyst and BI Developer to MLOps, NLP, and Computer Vision Engineers.
- **Deep AI Analysis**: Leverages `gemini-2.0-flash` with context-aware prompts to extract not just keywords, but essential technical concepts and related technologies.
- **Intelligent Roadmaps**: Generates sequential learning paths that identify "missing links" (prerequisite tools) and explain the logical dependency between technologies (e.g., Python → Airflow).
- **Dual-Storage Engine**: Uses **SQLite** for complex relational queries and **Apache Parquet** for high-performance serverless reads.
- **Automated Daily Pipeline**: GitHub Actions orchestrates the entire ETL process every midnight, committing fresh data and keeping the live dashboard up-to-date.
- **Serverless API**: A unified FastAPI backend deployed as Vercel Functions, serving both pre-aggregated insights and real-time AI roadmap generation.
- **Modern Web Dashboard**: An interactive Next.js application featuring glassmorphism design, Recharts visualizations, and 1-click personalized roadmaps.

---

## Project Structure

```text
roadmap_webscraping/
├── .github/workflows/  # CI/CD Automation (Daily Scraper)
├── .env                # Local environment variables (API Keys)
├── data/               # Local data storage (SQLite & Parquet)
├── docs/               # Detailed documentation & setup guides
├── output/             # Generated Markdown roadmaps
├── web/                # Vercel Monorepo Root
│   ├── api/            # FastAPI Serverless Backend
│   │   ├── src/        # Scraper Pipeline & Roadmap Logic
│   │   ├── data/       # Production data files (committed by CI)
│   │   └── index.py    # API Lambda entry point
│   └── src/app/        # React Next.js Frontend
├── requirements.txt    # Base python dependencies
├── vercel.json         # Deployment & routing config
└── README.md           # This file
```

---

## Technical Stack

- **Orchestration**: GitHub Actions (Cron)
- **Scraping Engine**: Scrapling (Stealth Fetching, curl_cffi, browserforge)
- **AI/LLM**: Google GenAI SDK (`gemini-2.0-flash`)
- **Data Engineering**: Pandas, PyArrow, SQLite
- **Environment**: python-dotenv
- **Backend API**: FastAPI, Pydantic (Vercel Serverless)
- **Web Frontend**: Next.js (React), Vanilla CSS
- **Visualization**: Recharts
- **Hosting**: Vercel

---

## Documentation

- [Setup Guide](docs/setup.md): Installation, API configuration, and Environment setup.
- [Usage Guide](docs/usage.md): How to run the scraper and generator locally.
- [Architecture Details](docs/architecture.md): Deep dive into the extraction and roadmap logic.

---

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs or submitting pull requests.

---

## License
Distributed under the MIT License. See `LICENSE` for more information.
