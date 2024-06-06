import os
import pandas as pd
import sqlite3
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

datasets = {
    "climate_change": ("goyaladi/climate-insights-dataset", "climate_change_data.csv"),
    "climate_risk": ("thedevastator/global-climate-risk-index-and-related-economic-l", "climate-risk-index-1.csv")
}

data_dir = "E:\FAU\MADE\exercise\main\made-paripurna\data"
sqlite_db_path = os.path.join(data_dir, "climate_data.db")

os.makedirs(data_dir, exist_ok=True)

def download_and_extract_kaggle_dataset(dataset, data_dir):
    api.dataset_download_files(dataset, path=data_dir, unzip=True)

download_and_extract_kaggle_dataset(datasets["climate_change"][0], data_dir)
download_and_extract_kaggle_dataset(datasets["climate_risk"][0], data_dir)

extracted_files = os.listdir(data_dir)
climate_change_path = [os.path.join(data_dir, f) for f in extracted_files if 'climate_change_data' in f][0]
climate_risk_path = [os.path.join(data_dir, f) for f in extracted_files if 'climate-risk-index-1' in f][0]

climate_change_df = pd.read_csv(climate_change_path)
climate_risk_df = pd.read_csv(climate_risk_path)

climate_change_df.dropna(inplace=True)
if climate_risk_df.dropna().empty:
    climate_risk_df.fillna(0, inplace=True)
else:
    climate_risk_df.dropna(inplace=True)

conn = sqlite3.connect(sqlite_db_path)
climate_change_df.to_sql("climate_change", conn, if_exists="replace", index=False)
climate_risk_df.to_sql("climate_risk", conn, if_exists="replace", index=False)
conn.close()

print("Data pipeline executed successfully. Data stored in:", sqlite_db_path)
