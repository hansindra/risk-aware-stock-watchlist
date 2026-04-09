# Risk-Aware Stock Watchlist System (CSE)

## Overview
This project builds a risk-aware anomaly detection system for the Sri Lankan stock market to help investors identify abnormal stock behavior and market stress periods.

## Project Structure
Capstone/
├── notebooks/
├── src/
├── data/ (auto-created)
├── README.md
├── requirements.txt
├── .gitignore


- notebooks/ → Analysis workflow
- src/ → Data download script
- data/ → Generated after running script

## Requirements (Note: Tested on Python 3.11)

- Python 3.10 – 3.11 recommended  
- Tested on Python 3.11  

Install dependencies:

pip install -r requirements.txt

## How to Run

Install dependencies using one of the following:

### macOS / Linux
python3 -m pip install -r requirements.txt
### Windows
python -m pip install -r requirements.txt

1. Run data download script:
   
## macOS / Linux
python3 src/01_download_data.py
## Windows
python src/01_download_data.py

This will create the data/ folder and download the required raw and processed datasets.

2. Run Notebooks (IN ORDER)

Open Jupyter Notebook or VS Code and run:

1. notebooks/01_data_audit.ipynb  
2. notebooks/02_aspi_eda.ipynb  
3. notebooks/03_stock_feature_engineering.ipynb  
4. notebooks/04_anomaly_detection.ipynb  
5. notebooks/05_evaluation_and_baselines.ipynb  


## Outputs

Main generated outputs are saved in:
Saved in:

data/processed/

### Processed Files

- ensemble_anomaly_evaluation.csv → Evaluation results of anomaly detection methods  
- monthly_market_regime.csv → Monthly classification (Normal / Elevated / Crisis)  
- risk_aware_daily_watchlist.csv → Final sector-diversified stock recommendations  
- stock_features_daily.csv → Engineered feature dataset  
- stock_metadata.csv → Stock-sector mapping  
- stocks_master_2014_2024.csv → Cleaned master dataset  


## Methods Used

- Baseline (3-sigma)
- Isolation Forest
- Local Outlier Factor (LOF)
- Ensemble (≥2 models agree)


## Results

Baseline: 7.07%  
Isolation Forest: 2.00%  
LOF: 2.00%  
Ensemble: 2.17%  


## Key Design Decisions

 **No forecasting used** — system focuses on anomaly detection  
- Proxy market index used (due to ASPI limitation)  
- dropna() used only for rolling calculations  
- Evaluation done on full dataset  


## Author
L R M H N Rajapaksha
258735U  
MDSAI – University of Moratuwa