# Data & AI Career Roadmap Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Scrapling-Automated_Scraping-green)](https://github.com/D4Vinci/Scrapling)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-purple)](https://aistudio.google.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Serverless_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-React_Framework-black?logo=next.js)](https://nextjs.org/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployment-black?logo=vercel&logoColor=white)](https://vercel.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

An end-to-end data engineering pipeline that scrapes real-time job market data, extracts technical skills using Gemini 2.0 Flash, and powers an interactive Serverless Next.js web application to generate sequential learning roadmaps bridging the gap between job seekers and market demand. Includes a GitHub Actions cron job for daily market data updates.

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

    A["Job Boards: LinkedIn"]:::scraper -->|Scrapling (Stealth Fetch)| B["Real Job Descriptions"]:::scraper
    B -->|Google GenAI API: Gemini 2.0 Flash| C["Dynamic Skill Extraction"]:::ai
    C -->|Structured Data| D["SQLite / Parquet"]:::database
    D -->|Aggregation| E["Top 15 In-Demand Skills"]:::database
    E -->|Roadmap Logic| F["Pedagogical Learning Roadmap"]:::ai
    F -->|Markdown Export| G["output/roadmap_data_engineer.md"]:::file
    E -->|Recharts Visualizations| H["Next.js Serverless Web Frontend (Vercel)"]:::ui
    F -->|Interactive UI| H
```

---

## Key Features

- **Multi-Source Scraping**: Utilizes `scrapling` to stealthily bypass bot protections and extract real job descriptions from LinkedIn.
- **Automated Daily Updates**: A GitHub Actions workflow automatically runs the pipeline every day at midnight (UTC) and redeploys the live Vercel app with fresh market data.
- **AI-Powered Extraction**: Leverages `gemini-2.0-flash` through the new `google-genai` SDK to identify technical tools and frameworks from unstructured text, avoiding brittle regex.
- **Smart Aggregation**: Ranks skills by frequency across different job profiles (Data Engineer, Analyst, ML Engineer, etc.).
- **Sequential Roadmaps**: Generates logical learning paths that explain *why* tools should be learned in a specific order (e.g., Python before Airflow).
- **Vercel Serverless Architecture**: The FastAPI backend and Next.js frontend are unified in a single monorepo deployed seamlessly to Vercel.
- **Clean Data Storage**: Exports structured data to high-performance **Parquet** files for lightning-fast serverless reads.
- **Interactive Web Dashboard**: Features a beautiful "Glassmorphism" Next.js application using Recharts for dynamic exploration of job market insights and 1-click roadmap generation.

---

## Project Structure

roadmap_webscraping/
├── .github/workflows/  # CI/CD Automation
│   └── daily_scraper.yml # Runs ETL pipeline automatically every day
├── data/               # Persistent storage for scraped data (Parquet)
├── docs/               # Detailed project documentation
├── output/             # Generated Markdown roadmaps
├── web/                # Vercel Monorepo Root
│   ├── api/            # FastAPI Serverless Backend
│   │   ├── src/        # Python Pipeline Components (Scrapling & Gemini)
│   │   ├── index.py    # Vercel Lambda Entry Point
│   │   └── requirements.txt
│   ├── src/app/        # React Next.js components and styling
│   ├── package.json    # Node dependencies
│   └── vercel.json     # Deployment configuration and API routing
├── .gitignore          # Environment & data exclusions
├── CONTRIBUTING.md     # Guidelines for contributing
├── LICENSE             # MIT License
└── README.md           # Primary overview
```

---

## Documentation

For detailed instructions on how to set up and use the project, please refer to the documentation:

- [Setup Guide](docs/setup.md): Instructions for installation, dependencies, and API configuration.
- [Usage Guide](docs/usage.md): Step-by-step guide on running the pipelines.
- [Architecture Details](docs/architecture.md): Deep dive into the pipeline logic and design decisions.

---

## Technical Stack

- **Orchestration**: GitHub Actions (Cron)
- **Automation**: Scrapling (Stealth Web Scraping)
- **AI/LLM Integration**: Google GenAI SDK (`gemini-2.0-flash`)
- **Data Processing**: Pandas, PyArrow
- **Storage**: Apache Parquet
- **Backend API**: FastAPI, Pydantic (Vercel Serverless Functions)
- **Web Frontend**: Next.js (React), Tailwind/Vanilla CSS
- **Data Visualization**: Recharts
- **Hosting / Deployment**: Vercel

---

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to report bugs, suggest features, and submit Pull Requests.

---

## License
Distributed under the MIT License. See `LICENSE` for more information.
