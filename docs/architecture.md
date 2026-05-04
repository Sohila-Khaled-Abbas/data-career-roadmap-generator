# System Architecture

The **Data & AI Career Roadmap Generator** is a production-grade, serverless data pipeline designed to bridge the gap between job market demand and technical education.

## 1. Data Ingestion Layer

### Stealth Scraping Engine (Scrapling)
The system leverages **Scrapling**, a modern scraping framework, to bypass bot protections on major job boards. 
-   **Multi-Source Agnostic**: Implements specific handlers for **LinkedIn, Wuzzuf, Indeed (EG), and Bayt.com**.
-   **Deep Crawling**: Unlike basic search-result scrapers, this system navigates to individual job postings to capture the full job description, providing high-fidelity data for the AI.
-   **Stealth Features**: Uses `curl_cffi` and `browserforge` to emulate realistic browser signatures and avoid IP blocking.

### AI-Driven Skill Extraction (Gemini 2.0 Flash)
Instead of brittle keyword matching (Regex), we use **Gemini 2.0 Flash** for "Semantic Extraction":
-   **Analytical Prompting**: The AI analyzes the *context* of the description to identify tools, frameworks, and related technologies.
-   **Filtering**: It intelligently ignores common soft skills to focus exclusively on technical proficiencies.
-   **Efficiency**: Utilizing the `google-genai` SDK for low-latency, high-throughput processing of hundreds of jobs daily.

---

## 2. Storage & Analysis Layer

### Hybrid Data Strategy
The project implements a dual-format storage system to maximize flexibility:
-   **SQLite (.db)**: The primary relational data store. It enables complex SQL queries for historical trend analysis and powers the FastAPI backend.
-   **Apache Parquet**: A high-performance columnar format used as a secondary data mirror for fast analytical reads and serverless compatibility.

### Intelligence Engine (Roadmap Synthesis)
The `roadmap_generator.py` component performs the "Synthesis" phase:
1.  **Aggregation**: Ranks skills by frequency across aggregated market data.
2.  **Dependency Logic**: Gemini analyzes the identified skills to determine pedagogical order (e.g., Learning Spark requires prior knowledge of Python/Java).
3.  **Missing Link Discovery**: The AI infers foundational technologies that might be missing from job descriptions but are required to master the stack.

---

## 3. Presentation Layer

### Vercel Serverless Architecture
The entire application is unified in a monorepo structure optimized for **Vercel**:
-   **FastAPI Backend**: Deployed as Serverless Functions (`/api/v1/`). Handles data filtering, skill ranking, and on-demand AI roadmap generation.
-   **Next.js Frontend**: A responsive, modern dashboard built with React and Tailwind CSS.
-   **CI/CD Orchestration**: **GitHub Actions** runs the Python ETL pipeline on a daily cron schedule. It commits fresh data directly to the repository, triggering an automatic rebuild and redeployment of the web app.
