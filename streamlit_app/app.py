import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from collections import Counter

# Add scripts directory to path to import roadmap generator
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(ROOT_DIR, 'scripts'))
from roadmap_generator import generate_roadmap_with_llm

# Page Configuration
st.set_page_config(
    page_title="Egypt Data & AI Career Roadmap",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #8A2BE2;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
    }
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 40px;
    }
    .stButton>button {
        width: 100%;
        background-color: #8A2BE2;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #7B24C3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚀 Data & AI Career Roadmap Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Discover the most in-demand technical skills in the Egyptian market and generate a personalized, AI-driven learning roadmap.</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    parquet_path = os.path.join(ROOT_DIR, "data", "egypt_data_skills.parquet")
    if os.path.exists(parquet_path):
        return pd.read_parquet(parquet_path)
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("No data found! Please run the scraper pipeline first to populate the market data.")
    st.info("Run `python scripts/scraper_pipeline.py` in your terminal.")
    st.stop()

# Sidebar Configuration
st.sidebar.header("🎯 Configuration")
profiles = df['searched_profile'].dropna().unique().tolist()
selected_profile = st.sidebar.selectbox("Select Target Role:", sorted(profiles))

if selected_profile:
    st.header(f"Market Insights: {selected_profile}")
    
    # Filter data for the selected profile
    profile_df = df[df['searched_profile'].str.lower() == selected_profile.lower()]
    
    # Show high-level metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Analyzed Job Postings", value=len(profile_df))
    with col2:
        latest_date = profile_df['crawl_date'].max()
        st.metric(label="Latest Data Update", value=latest_date)
    with col3:
        avg_skills = round(profile_df['skill_count'].mean(), 1) if not profile_df.empty else 0
        st.metric(label="Avg Skills per Posting", value=avg_skills)
        
    st.markdown("---")
    
    # Process skills dynamically
    all_skills = []
    for skills_string in profile_df['skills_detected']:
        if pd.notna(skills_string) and skills_string.strip():
            skills = [s.strip() for s in skills_string.split(',')]
            all_skills.extend(skills)
            
    skill_counts = Counter(all_skills)
    top_skills_data = skill_counts.most_common(15)
    
    if not top_skills_data:
        st.warning(f"No skills found for {selected_profile}. Try another profile.")
    else:
        # Create a dataframe for plotting
        skills_df = pd.DataFrame(top_skills_data, columns=['Skill', 'Frequency'])
        top_skills_list = skills_df['Skill'].tolist()
        
        # Main Dashboard Layout
        col_chart, col_roadmap = st.columns([1.2, 1])
        
        with col_chart:
            st.subheader("Top 15 Most Requested Skills")
            fig = px.bar(
                skills_df, 
                x='Frequency', 
                y='Skill', 
                orientation='h',
                color='Frequency',
                color_continuous_scale='Purples',
                title=f"Most Demanded Tools for {selected_profile}s"
            )
            # Ensure the highest frequency is at the top
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
        with col_roadmap:
            st.subheader("AI Roadmap Generation")
            st.write("Click the button below to synthesize the market data into a logical, step-by-step learning path using Claude AI via AgentRouter.")
            
            if st.button(f"Generate Roadmap for {selected_profile}"):
                with st.spinner("Analyzing pedagogical dependencies and generating roadmap..."):
                    try:
                        roadmap_md = generate_roadmap_with_llm(selected_profile, top_skills_list)
                        if roadmap_md:
                            st.success("Roadmap Generated Successfully!")
                            
                            # Save to output folder
                            filename = os.path.join(ROOT_DIR, "output", f"roadmap_{selected_profile.replace(' ', '_').lower()}.md")
                            os.makedirs(os.path.join(ROOT_DIR, "output"), exist_ok=True)
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(roadmap_md)
                            
                            # Display the markdown inside an expander
                            with st.expander("View Full Roadmap", expanded=True):
                                st.markdown(roadmap_md)
                            
                            # Provide Download button
                            st.download_button(
                                label="⬇️ Download Roadmap as Markdown",
                                data=roadmap_md,
                                file_name=f"roadmap_{selected_profile.replace(' ', '_').lower()}.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate roadmap. Please check your API key and connection.")
                    except Exception as e:
                        st.error(f"An error occurred during generation: {e}")
