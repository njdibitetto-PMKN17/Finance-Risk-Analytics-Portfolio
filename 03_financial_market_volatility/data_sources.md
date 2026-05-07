# Data Sources

This project uses publicly available financial market time-series data to forecast S&P 500 realized volatility.

## Core Data Sources

### Federal Reserve Economic Data (FRED)

Primary source for daily financial market series.

Series used include:

- `SP500` — S&P 500 Index
- `VIXCLS` — CBOE Volatility Index

### Gold Volatility Indicator

The project also uses a gold-volatility indicator to test whether cross-asset volatility information improves S&P 500 realized-volatility forecasts.

Series used include:

- `GVZCLS` or equivalent GVZ gold volatility series, depending on data availability

## Target Variable

The main target variable is:

- 21-day annualized S&P 500 realized volatility

This target is constructed from daily S&P 500 log returns using a rolling 21-day window.

## Feature Engineering

The project includes engineered variables such as:

- S&P 500 log returns
- Squared log returns
- 21-day realized volatility
- Lagged realized-volatility features
- VIX features
- GVZ features
- Rolling volatility features

## Modeling Dataset

The final modeling dataset was created after:

- Date alignment
- Missing-value handling
- Log return construction
- Rolling realized-volatility construction
- Lagged feature creation
- Removal of incomplete rows

The final dataset was split chronologically into training and test periods to avoid lookahead bias.

## Notes

Raw data files are not included in full. The notebooks document the data collection, cleaning, feature engineering, and modeling workflow.
