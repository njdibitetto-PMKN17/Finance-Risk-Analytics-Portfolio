# Financial Market Volatility Forecasting

## Objective

This project forecasts short-horizon financial market volatility, with a focus on S&P 500 realized volatility. The analysis compares classical time-series models and machine learning models to evaluate which approaches perform best for market-risk forecasting.

## Business Question

Can S&P 500 realized volatility be forecast using lagged market returns, volatility indicators, and related financial-market variables?

## Methods

The project compares several model families, including:

- ARIMA
- ARIMAX
- GARCH
- EGARCH
- Random Forest
- XGBoost

## Skills Demonstrated

- Python data analysis
- Financial return calculation
- Realized-volatility feature engineering
- Lagged market indicator creation
- Time-ordered train/test validation
- Forecast evaluation using RMSE and MAE
- Volatility clustering interpretation
- Market-risk analysis
- Classical model and machine learning benchmark comparison

## Files

- `01_data_cleaning_and_merging.ipynb`: data collection, cleaning, merging, and feature preparation
- `02_modeling_and_analysis.ipynb`: forecasting models, evaluation metrics, and interpretation
- `executive_summary.md`: recruiter-facing business summary
- `data_sources.md`: data source and variable documentation
- `requirements.txt`: Python package list
- `.html` files: supplemental rendered notebook exports
- `time_series_full_academic_report.pdf`: full academic report
