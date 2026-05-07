# Finance Risk Analytics Portfolio

This repository contains applied finance and risk analytics projects focused on credit risk monitoring, financial stress forecasting, and financial market volatility forecasting. The projects use Python, SQL, statistical modeling, machine learning, and financial interpretation to convert market and macroeconomic data into risk-focused insights.

## Projects

### 1. Credit Risk Early-Warning Dashboard

A SQL and Python-based project designed to monitor deterioration in credit conditions using macroeconomic, credit, interest-rate, and market-risk indicators.

**Status:** In development  
**Folder:** `01_credit_risk_early_warning_dashboard/`

Planned skills demonstrated:

- SQL table creation and querying
- SQL joins and date alignment
- Python data cleaning and analysis
- Credit-risk feature engineering
- Dashboard-style reporting
- Business-focused risk interpretation

---

### 2. Financial Stress Indicators Forecasting

This project forecasts one-week-ahead changes in the STLFSI4 financial stress index using volatility, Treasury yields, yield-curve spreads, corporate credit spreads, and S&P 500 returns.

**Folder:** `02_financial_stress_indicators/`

Methods used:

- ARIMA
- ARIMAX
- VAR
- Random Forest
- XGBoost

Key focus areas:

- Financial stress forecasting
- Credit-spread and volatility signal interpretation
- Time-ordered train/test validation
- RMSE, MAE, directional accuracy, and high-stress-week evaluation

---

### 3. Financial Market Volatility Forecasting

This project forecasts 21-day annualized S&P 500 realized volatility using realized-volatility features, VIX, GVZ, and market return data.

**Folder:** `03_financial_market_volatility/`

Methods used:

- ARIMA
- ARIMAX
- GARCH
- EGARCH
- Random Forest
- XGBoost

Key focus areas:

- Market-risk forecasting
- Realized-volatility modeling
- Volatility clustering analysis
- Classical model and machine learning benchmark comparison

---

## Skills Demonstrated

- Python data analysis
- SQL-based data preparation
- Data cleaning and merging
- Financial feature engineering
- Time-series forecasting
- Regression and machine learning model comparison
- Forecast validation using chronological train/test splits
- Credit-risk and market-risk interpretation
- Executive summary writing
- GitHub project organization

## Repository Structure

Each project folder includes some or all of the following:

- `README.md`: project overview
- `executive_summary.md`: business-facing project summary
- `data_sources.md`: data source and variable documentation
- `requirements.txt`: Python package list
- `.ipynb` notebooks: technical analysis and modeling workflow
- `.html` exports: supplemental rendered notebook files
- `full_academic_report.pdf`: full academic report where applicable

## Notes

The two completed forecasting projects were developed as applied finance analytics projects using public market and macroeconomic data. The credit risk project is being developed as a practical SQL and Python analyst workflow to complement the more model-heavy forecasting projects.
