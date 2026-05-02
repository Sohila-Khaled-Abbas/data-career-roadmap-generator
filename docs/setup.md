# Setup Guide

This document outlines the steps required to configure the Data & AI Career Roadmap Generator on your local machine.

## Prerequisites

- **Python 3.9+**: Ensure Python is installed and accessible in your system PATH.
- **AgentRouter API Key**: An active API key from AgentRouter with access to the `claude-haiku-4-5-20251001` model.

## Installation

1. **Clone the Repository**
   Navigate to your desired directory and clone the project repository.
   ```bash
   git clone <repository-url>
   cd roadmap_webscraping
   ```

2. **Install Python Dependencies**
   Install the required libraries listed in `requirements.txt`. It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**
   The scraping pipeline requires Chromium to function in headless mode.
   ```bash
   playwright install chromium
   ```

## Configuration

The project utilizes the AgentRouter API for LLM inference. The API key is configured directly within the source code.

**Updating the API Key**
If you need to change the API key, update the `API_KEY` variable at the top of the following files:
- `scripts/scraper_pipeline.py`
- `scripts/roadmap_generator.py`

```python
# AgentRouter API Key
API_KEY = "your_agentrouter_api_key_here"
```

*Security Note: Hardcoding API keys is not recommended for production environments. Consider migrating to environment variables before deploying to version control.*
