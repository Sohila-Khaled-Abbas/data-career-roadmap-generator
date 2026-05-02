# System Architecture

The Data & AI Career Roadmap Generator is designed as a two-phase Extract, Transform, Load (ETL) and Analysis pipeline. 

## Phase 1: Data Acquisition & Transformation

### Headless Web Scraping
The project utilizes **Playwright** to interact with modern, Javascript-heavy web applications (job boards). It uses an abstract class pattern (`JobBoardScraper`) to handle the unique Document Object Model (DOM) structures of different platforms, allowing easy extension for new job boards.

### Dynamic Skill Extraction via LLM
Traditional skill extraction relies on static regex lists (e.g., `(?i)\b(python|sql|aws)\b`), which quickly become outdated and miss context. 
This system replaces regex with dynamic LLM inference. It sends the raw job description to the **AgentRouter API** utilizing the `claude-haiku-4-5-20251001` model. 

The prompt strictly enforces a JSON array output consisting solely of technical skills, filtering out soft skills and irrelevant text. Exponential backoff is implemented to respect API rate limits.

### Dual Storage Strategy
- **Apache Parquet**: Used for fast read operations during the analysis phase. It provides columnar storage which is highly efficient for analytical workloads in Pandas.
- **SQLite3**: Used as a persistent, queryable data warehouse. This allows for historical trend analysis using standard SQL.

## Phase 2: Analysis & Synthesis

### Frequency Distribution
The `roadmap_generator.py` script reads the Parquet data and isolates records matching a specific job title. It splits the comma-separated skill lists and uses `collections.Counter` to determine the top 15 most in-demand tools.

### Pedagogical Synthesis
A list of tools alone is not a roadmap. The system sends the aggregated top skills back to the LLM with a system instruction to act as a "senior technical lead". The model is tasked with arranging the disconnected skills into a logical learning sequence (e.g., Prerequisites -> Core -> Advanced), explaining the dependencies between tools before outputting a formatted Markdown document.
