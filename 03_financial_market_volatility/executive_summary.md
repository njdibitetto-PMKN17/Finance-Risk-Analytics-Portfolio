# Executive Summary

## Project Objective

This project forecasts short-horizon S&P 500 realized volatility using classical time-series models, conditional-volatility models, and machine-learning benchmarks.

The primary target is 21-day annualized S&P 500 realized volatility, constructed from daily S&P 500 log returns.

## Business Relevance

Volatility forecasting is relevant for market-risk monitoring, portfolio risk review, drawdown preparation, and stress-period analysis.

The project evaluates whether realized volatility is mainly driven by its own persistence or whether external volatility indicators such as VIX and GVZ materially improve forecast accuracy.

## Data Used

The project uses daily financial market data including:

- S&P 500 levels
- S&P 500 log returns
- Squared log returns
- 21-day annualized realized volatility
- VIX equity volatility index
- GVZ gold volatility index

The analysis removes missing observations caused by return construction, rolling-window calculations, and lagged feature creation.

## Modeling Approach

The project compares:

- ARIMA
- ARIMAX
- GARCH
- EGARCH
- Random Forest
- XGBoost

Models are evaluated using chronological out-of-sample testing to avoid lookahead leakage.

## Key Findings

Rolling ARIMA produced the strongest out-of-sample forecast accuracy for the 21-day realized-volatility target. The rolling ARIMA model achieved an MAE of approximately 0.0061 and RMSE of approximately 0.0132 on the test period.

ARIMAX, Random Forest, and XGBoost tracked the realized-volatility path reasonably well, but did not outperform ARIMA. This suggests that recent realized volatility contained more useful forecasting signal than the added external volatility indicators.

GARCH and EGARCH confirmed volatility clustering in S&P 500 returns, but they performed worse when compared against the smoother 21-day realized-volatility target.

The final RMSE ranking was:

1. ARIMA
2. ARIMAX
3. Random Forest
4. XGBoost
5. GARCH
6. EGARCH

## Financial Interpretation

The S&P 500 return series showed weak linear autocorrelation but strong autocorrelation in squared returns. This supports the presence of volatility clustering.

The 21-day realized-volatility series was highly persistent, which explains why a direct ARIMA model on realized volatility performed best.

VIX contributed secondary information, while GVZ contributed relatively little. The machine-learning feature-importance results showed that recent realized volatility and rolling realized-volatility features dominated the nonlinear feature set.

## Business Takeaway

For this target, the best-performing model was not the most complex model. A rolling ARIMA model on realized volatility outperformed conditional-volatility models and machine-learning benchmarks.

The practical takeaway is that model choice must match the target. GARCH-family models are useful for modeling conditional return volatility, but a smooth 21-day realized-volatility target may be better forecast directly using realized-volatility persistence.

## Limitations

The analysis uses baseline model specifications rather than fully optimized production models.

The target is 21-day realized volatility, not next-day conditional return variance. This target definition naturally favors models that capture persistence in realized volatility.

Future extensions could test HAR-RV models, richer lag structures, rolling machine-learning retraining, and additional volatility-regime indicators.
