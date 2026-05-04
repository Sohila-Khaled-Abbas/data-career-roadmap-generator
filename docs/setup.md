# Setup Guide

This document outlines the steps required to configure the **Data & AI Career Roadmap Generator** for local development.

## Prerequisites

- **Python 3.11+**: Ensure Python is installed and accessible in your system PATH.
- **Google Gemini API Key**: An active API key from [Google AI Studio](https://aistudio.google.com/) with access to the `gemini-2.0-flash` model.

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd roadmap_webscraping
   ```

2. **Install Python Dependencies**
   It is highly recommended to use a virtual environment (Conda or venv).
   ```bash
   pip install -r requirements.txt
   pip install python-dotenv scrapling curl_cffi browserforge
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
