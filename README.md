# Data & AI Career Roadmap Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated_Scraping-green?logo=playwright)](https://playwright.dev/)
[![AgentRouter](https://img.shields.io/badge/AgentRouter-API-purple)](https://agentrouter.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Interactive_Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

An end-to-end data engineering pipeline that scrapes real-time job market data, extracts technical skills using Claude AI (via AgentRouter), and powers an interactive Streamlit dashboard to generate sequential learning roadmaps bridging the gap between job seekers and market demand.

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

    A["Job Boards: LinkedIn, Wuzzuf, Indeed, Glassdoor"]:::scraper -->|"Playwright Scraping"| B("Raw Job Descriptions"):::scraper
    B -->|"AgentRouter API: Claude Haiku"| C{"Dynamic Skill Extraction"}:::ai
    C -->|"Structured Data"| D[("SQLite / Parquet")]:::database
    D -->|"Aggregation"| E["Top 15 In-Demand Skills"]:::database
    E -->|"Roadmap Logic"| F["Pedagogical Learning Roadmap"]:::ai
    F -->|"Markdown Export"| G["output/roadmap_data_engineer.md"]:::file
    E -->|"Plotly Visualizations"| H{"Streamlit Web Dashboard"}:::ui
    F -->|"Interactive UI"| H
```

---

## Key Features

- **Multi-Source Scraping**: Utilizes Playwright to navigate complex DOM structures of major job boards (LinkedIn, Wuzzuf, Indeed, Glassdoor).
- **AI-Powered Extraction**: Leverages `claude-haiku-4-5-20251001` through the AgentRouter API to identify technical tools and frameworks from unstructured text, avoiding brittle regex.
- **Smart Aggregation**: Ranks skills by frequency across different job profiles (Data Engineer, Analyst, ML Engineer, etc.).
- **Sequential Roadmaps**: Generates logical learning paths that explain *why* tools should be learned in a specific order (e.g., Python before Airflow).
- **Clean Data Storage**: Exports structured data to both high-performance **Parquet** files and queryable **SQLite** databases.
- **Interactive Web Dashboard**: Features a beautiful Streamlit application with Plotly charts for dynamic exploration of job market insights and 1-click roadmap generation.

---

## Project Structure

```text
roadmap_webscraping/
├── data/               # Persistent storage for scraped data (Parquet, SQLite)
├── docs/               # Detailed project documentation
├── src/                # Core Python pipeline components
│   ├── scraper_pipeline.py    # ETL: Extract, AI-Transform, Load
│   ├── roadmap_generator.py   # Analysis & Roadmap Generation
│   └── api/                   # REST API Layer
│       └── main.py            # FastAPI Application
├── docker-compose.yml    # Docker services config
├── Dockerfile          # Container build instructions
├── automate.py         # 1-Click Pipeline Orchestrator
├── notebooks/          # Interactive Jupyter Notebooks
│   └── Data_Career_Roadmap.ipynb
├── streamlit_app/      # Interactive Web Dashboard
│   ├── app.py
│   └── .streamlit/config.toml
├── output/             # Generated Markdown roadmaps
├── .gitignore          # Environment & data exclusions
├── CONTRIBUTING.md     # Guidelines for contributing
├── LICENSE             # MIT License
├── requirements.txt    # Python dependencies
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

- **Orchestration**: Python
- **Automation**: Playwright (Headless Chromium)
- **AI/LLM Integration**: AgentRouter API (`claude-haiku-4-5-20251001`)
- **Data Processing**: Pandas, PyArrow
- **Database**: SQLite3
- **Storage**: Apache Parquet
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Web Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Interactive Environment**: Jupyter Notebook
- **Containerization**: Docker & Docker Compose

---

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to report bugs, suggest features, and submit Pull Requests.

---

## License
Distributed under the MIT License. See `LICENSE` for more information.
