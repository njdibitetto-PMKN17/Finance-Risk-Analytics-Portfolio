# Data Sources

This project uses publicly available financial and macroeconomic time-series data. The data were cleaned, merged by date, transformed into weekly observations where needed, and used to forecast one-week-ahead changes in the STLFSI4 financial stress index.

## Core Data Sources

### Federal Reserve Economic Data (FRED)

Primary source for macroeconomic, interest-rate, credit-spread, and financial stress indicators.

Series used include:

- `STLFSI4` — St. Louis Fed Financial Stress Index
- `DGS2` — 2-Year Treasury Constant Maturity Rate
- `DGS10` — 10-Year Treasury Constant Maturity Rate
- `T10Y2Y` — 10-Year Treasury minus 2-Year Treasury Spread
- Corporate credit spread series, including Baa/high-yield style spread indicators where applicable

### Market Volatility Data

Volatility indicators were used to capture market risk and stress sensitivity.

Series used include:

- `VIXCLS` — CBOE Volatility Index

### Equity Market Data

Equity market data were used to measure broad market return behavior.

Series used include:

- S&P 500 index or return-derived features

## Target Variable

The main target variable is:

- `stress_change_next` — one-week-ahead change in STLFSI4

This target was used to evaluate whether current and lagged financial-market indicators could forecast future changes in financial stress.

## Feature Engineering

The project includes engineered predictors such as:

- Lagged financial stress variables
- Lagged volatility indicators
- Lagged credit-spread indicators
- Treasury-yield variables
- Yield-curve spread variables
- S&P 500 return variables
- Weekly stress-change variables

## Modeling Dataset

The final modeling dataset contains weekly observations after:

- Date alignment
- Missing-value handling
- Lag construction
- Target construction
- Removal of incomplete rows

The final dataset was split chronologically into training and test periods to avoid lookahead bias.

## Notes

Raw data files are not included in full unless needed for reproducibility. Data source documentation is included so the project workflow can be reviewed and replicated using the same public series.
