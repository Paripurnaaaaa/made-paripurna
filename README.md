# Analyzing Climate Risk and Insights for Predicting Economic Losses

## Project Overview

This project aims to analyze the relationship between climate risk indices and various climate metrics to understand how climate risks influence economic losses due to climate-related events. By integrating datasets that include climate change data and the Global Climate Risk Index, we explore patterns and trends to provide a comprehensive understanding of how different regions are affected by climate risks. This analysis helps in identifying the most vulnerable regions and the key factors contributing to economic instability caused by climate change.

## Data Sources

### Climate Change Dataset
- **Metadata URL:** [Climate Insights Dataset](https://www.kaggle.com/datasets/goyaladi/climate-insights-dataset/data)
- **Data URL:** [Climate Change Data](https://www.kaggle.com/datasets/goyaladi/climate-insights-dataset/data?select=climate_change_data.csv)
- **Data Type:** CSV, historical climate metrics including temperature, CO2 emissions, and sea level rise.

### Climate Risk Index Dataset
- **Metadata URL:** [Global Climate Risk Index](https://www.kaggle.com/datasets/thedevastator/global-climate-risk-index-and-related-economic-l/data)
- **Data URL:** [Climate Risk Index Data](https://www.kaggle.com/datasets/thedevastator/global-climate-risk-index-and-related-economic-l/data?select=climate-risk-index-1.csv)
- **Data Type:** CSV, climate risk index and economic loss data due to extreme weather events.

## Data Pipeline Overview

The data pipeline extracts, processes, and stores datasets from Kaggle using Python, Kaggle API, pandas, and SQLite. The steps are as follows:
1. **Download and Extract:** Datasets are downloaded from Kaggle and extracted to a specified folder.
2. **Identify Files:** The pipeline lists files in the folder to find the relevant datasets.
3. **Load Data:** The datasets are loaded into pandas DataFrames.
4. **Clean Data:**
    - For `climate_change_df`: Rows with missing data are removed.
    - For `climate_risk_df`: If removing rows with missing data results in an empty DataFrame, NaN values are filled with 0; otherwise, rows with missing data are dropped.
5. **Store Data:** The cleaned data is saved in a SQLite database.

## How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Kaggle API
- pandas
- SQLite
- matplotlib
- seaborn
- statsmodels

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Paripurnaaaaa/made-paripurna.git
    cd made-paripurna
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the data pipeline script:
    ```bash
    python pipeline.py
    ```
4. Open and run the Jupyter notebook for analysis:
    ```bash
    jupyter notebook insight-analysis.ipynb
    ```

## Repository Structure

```plaintext
project/
│
├── .gitignore
├── .gitkeep
├── analysis-report.pdf
├── insight-analysis.ipynb
├── pipeline.py
├── pipeline.sh
├── project-plan.md
├── report.pdf
├── test.sh
└── test_pipeline.py
```

## License

This project is licensed under the [MIT License](https://github.com/Paripurnaaaaa/made-paripurna/blob/main/LICENSE).

## Authors

- Paripurna Dutta

For any questions or issues, please open an issue on GitHub.


