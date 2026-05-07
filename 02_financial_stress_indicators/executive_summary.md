# Executive Summary

## Project Objective

This project evaluates whether market-based financial indicators can improve short-horizon forecasts of U.S. financial stress. The target variable is the one-week-ahead change in the STLFSI4 financial stress index.

The project compares whether volatility, credit spreads, equity returns, Treasury yields, and yield-curve variables add useful forecasting information beyond the stress index’s own history.

## Data and Target

The final modeling dataset contains 516 weekly observations after cleaning, merging, lag construction, and removal of incomplete rows. The training set contains 412 observations from June 2016 through April 2024, and the test set contains 104 observations from April 2024 through April 2026.

Core variables include:

- STLFSI4 financial stress index
- VIX volatility index
- Baa corporate credit spread
- 2-year Treasury yield
- 10-year Treasury yield
- 10Y–2Y Treasury yield spread
- S&P 500 returns

The target is next-week financial stress change, not the stress level itself.

## Modeling Approach

The project compares baseline forecasts, ARIMA, ARIMAX, VAR, Random Forest, and XGBoost using a chronological train/test split.

The models are evaluated using:

- RMSE
- MAE
- Directional accuracy
- High-stress-week RMSE
- High-stress-week MAE

The high-stress metrics are important because average error can hide poor performance during the exact periods risk teams care about most.

## Key Results

ARIMAX was the strongest overall forecasting model. It achieved an RMSE of approximately 0.171 and MAE of approximately 0.123 on the chronological test set, outperforming ARIMA, VAR, Random Forest, and XGBoost on overall RMSE and high-stress-week forecast error.

ARIMA improved only modestly over the baseline. Its RMSE was approximately 0.196, MAE was approximately 0.141, and directional accuracy was approximately 55.8%. This shows that the stress-change series’ own history is not enough to produce strong forecasts.

Adding external financial-market predictors materially improved performance. ARIMAX reduced RMSE from approximately 0.196 to 0.171 and improved directional accuracy from approximately 55.8% to 64.4%.

Random Forest produced the strongest directional accuracy at approximately 70.2%, making it useful as a directional support model. However, it did not beat ARIMAX on high-stress-week errors.

XGBoost did not outperform ARIMAX, but its feature importance results were useful. It placed more weight on credit-spread variables, especially lagged credit spreads, supporting the interpretation that credit-market conditions are a key nonlinear stress channel.

VAR was useful for examining lead-lag relationships among volatility, credit, equity, rate, and stress variables, but it was the weakest forecasting model out of sample.

## Financial Interpretation

The strongest short-horizon stress signals came from volatility, credit spreads, stress persistence, and equity-market returns.

VIX and Baa credit spreads were the strongest contemporaneous stress-level channels, with correlations of approximately 0.71 and 0.74 with the official stress index. However, predicting stress changes was harder than explaining stress levels, since lagged predictor correlations with next-week stress changes were more modest.

The practical interpretation is that no single indicator works as a standalone early-warning rule. A better monitoring framework combines volatility, credit spreads, equity returns, and lagged stress behavior.

## Business Takeaway

For a financial risk or credit-monitoring workflow, ARIMAX should be treated as the primary forecasting model because it delivered the strongest overall and high-stress-week error performance.

Random Forest can be used as a secondary directional model because it was best at predicting whether stress would rise or fall.

XGBoost is most useful as a channel-ranking tool because it highlights the importance of credit-spread variables in nonlinear stress prediction.

The overall conclusion is that market-based indicators do improve financial stress forecasting, but the best-performing approach is not the most complex model. A controlled time-series model with carefully selected financial predictors performed better than unrestricted VAR and nonlinear tree models for this dataset.

## Limitations

The main limitation is that next-week stress changes are noisy and centered near zero, making the baseline difficult to beat. This explains why improvements must be judged by multiple metrics, especially high-stress-week performance rather than average RMSE alone.

The second limitation is that feature importance is model-specific, not causal. Random Forest emphasized VIX changes and current stress, while XGBoost emphasized credit-spread variables. These rankings help interpret channel relevance, but they do not prove causal relationships.

The third limitation is that Treasury-yield variables are highly correlated with each other, especially the 2-year and 10-year yields, which complicates coefficient interpretation in linear and multivariate models.
