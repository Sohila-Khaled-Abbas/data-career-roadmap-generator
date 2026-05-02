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

    # Step 2: Generate Default Roadmap
    print("[2/3] Generating Roadmap for default profile (Data Engineer)...")
    try:
        subprocess.run(["python", "src/roadmap_generator.py"], check=True)
        print("✅ Roadmap generation completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Roadmap generation failed with error: {e}")
        return

    # Step 3: Launch Streamlit Dashboard
    print("[3/3] Launching Streamlit Dashboard...")
    try:
        # Running streamlit dynamically and waiting for it to be interrupted by user
        print("ℹ️ The dashboard will open in your default browser. Press Ctrl+C to stop.")
        subprocess.run(["streamlit", "run", "streamlit_app/app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Pipeline stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit failed with error: {e}")

if __name__ == "__main__":
    run_pipeline()
