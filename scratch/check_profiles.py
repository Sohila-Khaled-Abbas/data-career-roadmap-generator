import pandas as pd
import os

parquet_file = r"d:\courses\Data Science\Data Engineering\Projects\roadmap_webscarping\data\egypt_data_skills.parquet"

if os.path.exists(parquet_file):
    df = pd.read_parquet(parquet_file)
    print(f"Columns: {df.columns.tolist()}")
    print(f"Unique profiles: {df['searched_profile'].unique().tolist()}")
else:
    print(f"File not found: {parquet_file}")
