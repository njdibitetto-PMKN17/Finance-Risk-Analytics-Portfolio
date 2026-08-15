# Finance Risk Analytics Portfolio

This repository contains applied finance and risk analytics projects focused on credit risk monitoring, financial stress forecasting, and financial market volatility forecasting. The projects use Python, SQL (SQLite), Streamlit, statistical modeling, machine learning, and financial interpretation to convert market and macroeconomic data into risk-focused insights.

## Projects

### 1. Credit Risk Detection & Monitoring Dashboard

A Python, SQL (SQLite), and Streamlit dashboard designed to monitor macro-credit conditions using public FRED data across market stress, labor risk, interest-rate pressure, yield-curve pressure, and realized credit performance.

**Folder:** `01_credit_risk_detection_monitoring_dashboard/`

**Key features:**

- Macro-credit risk scoring framework
- Four-channel category driver analysis
- Composite risk regime classification
- Before/after monthly risk comparison
- Historical recession-context visualization
- Baseline ARIMA forward-risk outlook
- Interactive Streamlit dashboard
- Custom category-weight sensitivity
- Adjustable regime thresholds
- Category feature drilldown
- ARIMA model diagnostics and limitations

**Tools / methods used:**

- Python
- pandas
- SQL (SQLite)
- Streamlit
- Altair
- ARIMA
- FRED public economic data
- Expanding percentile scoring
- Composite risk regime classification
- Interactive dashboard sensitivity analysis

**Primary focus areas:**

- Credit-risk monitoring
- Macro-financial risk interpretation
- Interest-rate and yield-curve pressure
- Financial-stress dashboarding
- Forecast interpretation and model diagnostics

---

### 2. Financial Stress Indicators Forecasting

This project forecasts one-week-ahead changes in the STLFSI4 financial stress index using volatility, Treasury yields, yield-curve spreads, corporate credit spreads, and S&P 500 returns.

**Folder:** `02_financial_stress_indicators/`

**Tools / methods used:**

- Python
- pandas
- Time-series feature engineering
- ARIMA
- ARIMAX
- VAR
- Random Forest
- XGBoost
- Chronological train/test validation
- RMSE, MAE, and directional accuracy evaluation

Key focus areas:

- Financial stress forecasting
- Credit-spread and volatility signal interpretation
- Time-ordered train/test validation
- RMSE, MAE, directional accuracy, and high-stress-week evaluation

---

### 3. Financial Market Volatility Forecasting

This project forecasts 21-day annualized S&P 500 realized volatility using realized-volatility features, VIX, GVZ, and market return data.

**Folder:** `03_financial_market_volatility/`

**Tools / methods used:**

- Python
- pandas
- Realized-volatility feature engineering
- ARIMA
- ARIMAX
- GARCH
- EGARCH
- Random Forest
- XGBoost
- Classical model and machine-learning benchmark comparison

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

#### Note

The tools and methods listed above summarize the main technologies and modeling approaches used across the portfolio. Individual projects may include additional Python libraries for data processing, visualization, statistical modeling, machine learning, and diagnostic evaluation. Package-level details are documented within each project folder where applicable.
