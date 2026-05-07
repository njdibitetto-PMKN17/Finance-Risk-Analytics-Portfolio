# Financial Stress Indicators Forecasting

## Objective

This project forecasts short-horizon changes in U.S. financial stress using market-based indicators such as volatility, Treasury yields, yield-curve spreads, credit spreads, and equity returns.

## Business Question

Which financial market channels provide useful signal for forecasting changes in U.S. financial stress?

## Methods

The project compares classical time-series models and machine learning models, including:

- ARIMA
- ARIMAX
- VAR
- Random Forest
- XGBoost

## Skills Demonstrated

- Python data analysis
- Financial time-series feature engineering
- Lagged variable creation
- Time-ordered train/test validation
- Forecast evaluation using RMSE and MAE
- Financial stress and credit-market interpretation
- Machine learning model comparison

## Files

- `01_data_cleaning_and_merging.ipynb`: data collection, cleaning, merging, and feature preparation
- `02_modeling_and_analysis.ipynb`: forecasting models, evaluation metrics, and interpretation
- `executive_summary.md`: recruiter-facing business summary
- `data_sources.md`: data source and variable documentation
- `requirements.txt`: Python package list
- `.html` files: supplemental rendered notebook exports
- `time_series_full_academic_report.pdf`: full academic report
