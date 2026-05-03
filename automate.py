import os
import subprocess
import time

def run_pipeline():
    print("==================================================")
    print("🚀 Starting Automated Data & AI Roadmap Pipeline")
    print("==================================================\n")

    # Step 1: Run the Scraper
    print("[1/3] Running Scraper Pipeline to gather market data...")
    try:
        subprocess.run(["python", "src/scraper_pipeline.py"], check=True)
        print("✅ Scraping completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Scraper failed with error: {e}")
        return

    # Step 2: Generate Roadmaps for all profiles
    print("[2/3] Generating individual roadmaps for each identified job profile...")
    try:
        subprocess.run(["python", "src/roadmap_generator.py"], check=True)
        print("✅ All roadmaps generated successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Roadmap generation failed with error: {e}")
        return

    # Step 3: Launch Full Stack
    print("[3/3] The pipeline is now decoupled.")
    print("ℹ️ To launch the FastAPI backend and Next.js frontend, please use Docker:")
    print("    docker-compose up --build")
    print("    - API available at: http://localhost:8000")
    print("    - Web App available at: http://localhost:3000")

if __name__ == "__main__":
    run_pipeline()
