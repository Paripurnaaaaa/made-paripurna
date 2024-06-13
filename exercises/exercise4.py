import requests
import zipfile
import os
import pandas as pd
import sqlite3
import logging

def configure_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(download_url, destination_path):
    logging.info(f"Fetching data from {download_url}")
    response = requests.get(download_url)
    with open(destination_path, 'wb') as file:
        file.write(response.content)

def unzip_file(zip_filepath, extract_to_folder):
    logging.info("Unzipping downloaded file")
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)

def load_csv_file(file_path, delimiter=';', quotechar='"'):
    logging.info(f"Loading CSV data from {file_path}")
    return pd.read_csv(file_path, delimiter=delimiter, quotechar=quotechar, on_bad_lines='skip')

def process_data_frame(data_frame, column_mapping):
    missing_cols = [col for col in column_mapping.keys() if col not in data_frame.columns]
    if missing_cols:
        logging.error(f"CSV is missing the following required columns: {missing_cols}")
        return None
    
    data_frame = data_frame[list(column_mapping.keys())].rename(columns=column_mapping)
    
    data_frame['temperature'] = data_frame['temperature'].astype(str).str.replace(',', '.').str.strip()
    data_frame['battery_temperature'] = data_frame['battery_temperature'].astype(str).str.replace(',', '.').str.strip()

    data_frame['temperature'] = pd.to_numeric(data_frame['temperature'], errors='coerce')
    data_frame['battery_temperature'] = pd.to_numeric(data_frame['battery_temperature'], errors='coerce')

    data_frame = data_frame.dropna(subset=['temperature', 'battery_temperature'])

    data_frame['temperature'] = data_frame['temperature'].apply(lambda x: (x * 9/5) + 32 if pd.notnull(x) else x)
    data_frame['battery_temperature'] = data_frame['battery_temperature'].apply(lambda x: (x * 9/5) + 32 if pd.notnull(x) else x)

    data_frame = data_frame[data_frame['id'].apply(lambda x: str(x).isdigit())]  # Ensure 'id' is numeric
    data_frame['id'] = data_frame['id'].astype(int)
    data_frame = data_frame[data_frame['id'] > 0]

    return data_frame

def save_data_to_sqlite(data_frame, sqlite_db, table='temperatures'):
    if not data_frame.empty:
        logging.info(f"Saving processed data to SQLite database: {sqlite_db}")
        conn = sqlite3.connect(sqlite_db)
        data_frame.to_sql(table, conn, if_exists='replace', index=False)
        conn.close()

def cleanup_resources(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                for filename in os.listdir(file_path):
                    os.remove(os.path.join(file_path, filename))
                os.rmdir(file_path)
            else:
                os.remove(file_path)

def main():
    configure_logging()

    data_source_url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
    zip_file_path = "temp_data.zip"
    extract_dir = "extracted_content"
    csv_file = os.path.join(extract_dir, "data.csv")

    fetch_data(data_source_url, zip_file_path)
    unzip_file(zip_file_path, extract_dir)
    
    data_frame = load_csv_file(csv_file)

    columns_mapping = {
        "Geraet": "id",
        "Hersteller": "producer",
        "Model": "model",
        "Monat": "month",
        "Temperatur in °C (DWD)": "temperature",
        "Batterietemperatur in °C": "battery_temperature"
    }
    
    processed_data = process_data_frame(data_frame, columns_mapping)
    if processed_data is not None:
        save_data_to_sqlite(processed_data, 'temperatures.sqlite')

    cleanup_resources([zip_file_path, csv_file, extract_dir])

if __name__ == "__main__":
    main()
