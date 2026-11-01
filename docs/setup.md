# Setup Guide

This document outlines the steps required to configure the **Data & AI Career Roadmap Generator** for local development.

## Prerequisites

- **Python 3.11+**: Ensure Python is installed and accessible in your system PATH.
- **Google Gemini API Key**: An active API key from [Google AI Studio](https://aistudio.google.com/) with access to the `gemini-3.8-flash` model.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sohila-Khaled-Abbas/data-career-roadmap-generator.git
   cd data-career-roadmap-generator
   ```

2. **Install Python Dependencies**
   It is highly recommended to use a virtual environment (Conda or venv).
   ```bash
   python -m pip install pandas pyarrow google-genai scrapling curl_cffi browserforge python-dotenv
   ```

## Configuration

The project uses a `.env` file to manage sensitive API keys securely.

1. **Create a .env file**
   Create a file named `.env` in the root of the project (copying from `.env.example`).
   ```bash
   cp .env.example .env
   ```

2. **Add your API Key**
   Open the `.env` file and paste your Gemini API key:
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running Locally

Once configured, you can run the pipeline components:

- **ETL Scraper**: `python web/api/src/scraper_pipeline.py`
- **Roadmap Generator**: `python web/api/src/roadmap_generator.py`

*Note: The scripts automatically detect the `.env` file at the root and load your credentials.*

### Scheduled refresh requirements

Set the repository Actions secret `GEMINI_API_KEY` and optionally repository variable `GEMINI_MODEL` (default: `gemini-3.8-flash`). The model must be supported by your own Gemini API key and plan. The workflow skips refresh when no secret exists, and fails rather than overwriting data when extraction returns no usable records. Root `data/*.db` / `data/*.parquet` files are ignored; the API reads the committed `web/api/data/` snapshots.
