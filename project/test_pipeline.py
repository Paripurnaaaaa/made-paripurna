import os
import subprocess
import sys

def verify_input_files(data_dir, input_files):
    missing_files = [f for f in input_files if not os.path.exists(f)]
    if missing_files:
        for file in missing_files:
            print(f"Test failed: Input file {file} does not exist.")
        sys.exit(1)
    print("Test passed: All input files exist.")

def run_pipeline_script():
    result = subprocess.run([sys.executable, 'pipeline.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Test failed: Pipeline execution failed: {result.stderr}")
        sys.exit(1)
    print("Test passed: Pipeline executed successfully.")

def check_output_file(data_dir, db_filename):
    db_path = os.path.join(data_dir, db_filename)
    if not os.path.exists(db_path):
        print(f"Test failed: SQLite database {db_path} does not exist.")
        sys.exit(1)
    print(f"Test passed: SQLite database {db_path} exists.")

def test_pipeline_execution():
    data_dir = r"E:\FAU\MADE\exercise\main\made-paripurna\data"
    input_files = [
        os.path.join(data_dir, 'climate_change_data.csv'),
        os.path.join(data_dir, 'climate-risk-index-1.csv')
    ]
    db_filename = 'climate_data.db'

    verify_input_files(data_dir, input_files)
    run_pipeline_script()
    check_output_file(data_dir, db_filename)
    print("All tests passed.")

if __name__ == "__main__":
    test_pipeline_execution()
