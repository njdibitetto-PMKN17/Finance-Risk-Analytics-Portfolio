# Credit Risk Detection & Monitoring Dashboard

This project builds a reproducible macro-credit risk monitoring dashboard using Python, SQLite, Streamlit, and public FRED data. The dashboard combines macroeconomic, interest-rate, market-volatility, financial-stress, credit-spread, delinquency, charge-off, and recession indicators into a monthly credit-risk scoring framework.

The final output is an interactive Streamlit dashboard that summarizes current macro-credit conditions, tracks risk-channel drivers, compares before-and-after monthly changes, displays historical risk regimes, provides a baseline ARIMA forward-risk outlook, and includes sensitivity controls for category weights and regime thresholds.

## Project Objective

This project is designed to answer eight practical macro-credit monitoring questions:

1. Are aggregate macro-credit conditions currently Normal, Watch, Elevated, or Stress?
2. Which risk channels are driving the current credit-risk score?
3. Are conditions improving, stabilizing, or deteriorating across 1-month, 3-month, and 6-month windows?
4. Is current risk broad-based across multiple channels or concentrated in one channel?
5. Did the score behave sensibly around historical recession and stress periods?
6. Do higher-risk regimes or regime transitions provide useful context for future S&P 500 returns?
7. How sensitive are dashboard conclusions to alternative category weights and regime thresholds?
8. What does the baseline forward outlook imply for near-term monitoring?

## Dashboard Screenshots

Click any screenshot to open the full-resolution image.

### Dashboard Overview and Category Driver Comparison

This view shows the main dashboard controls, selected before/after month comparison, current composite credit-risk score, current regime, trailing score changes, category-driver chart, and month-to-month category risk changes.

[![Dashboard Overview and Category Driver Comparison](assets/crd_shot1.png)](assets/crd_shot1.png)

### Category Feature Drilldown and Historical Composite Score

This view shows the category-level drilldown for the selected risk channel, including the underlying variables used to build the selected category score. It also shows the historical Composite Credit Risk Score with revised regime thresholds and recession shading.

[![Category Feature Drilldown and Historical Composite Score](assets/crd_shot2.png)](assets/crd_shot2.png)

### Forecast Outlook and Forward-Risk Tables

This view shows the historical score with the baseline ARIMA forecast and custom weighted component forecast. It also includes the forward credit-risk outlook table, showing projected scores and projected regime classifications across the current, 1-month, 3-month, and 6-month monitoring windows.

[![Forecast Outlook and Forward-Risk Tables](assets/crd_shot3.png)](assets/crd_shot3.png)

### Model Diagnostics and ARIMA Interpretation

This view shows the composite forecast range, ARIMA model selection summary, diagnostic statistics, and dashboard interpretation. These diagnostics are used to explain where the baseline forecast is useful and where the model should be interpreted cautiously.

[![Model Diagnostics and ARIMA Interpretation](assets/crd_shot4.png)](assets/crd_shot4.png)

## Full Analysis Report

A sanitized HTML report is included for readers who want to review the full project workflow, methodology, scoring logic, validation checks, forecast interpretation, limitations, and business conclusions.

The report documents the full analysis process behind the Streamlit dashboard while excluding local environment files, API keys, notebook checkpoints, raw API download artifacts, and development backups.

**Report:** [`reports/credit_risk_detection_monitoring_report.html`](reports/credit_risk_detection_monitoring_report.html)

**Viewing note:** GitHub may not preview this HTML file directly because it is a large exported notebook report. To view the full analysis, open the report file, click **Download raw file** or **Raw**, then open the downloaded `.html` file locally in a web browser.

## Methods Used

- FRED API data retrieval
- Python data cleaning and feature engineering
- SQLite database storage
- Monthly frequency alignment
- Expanding percentile risk scoring
- Category-level credit-risk scoring
- Composite risk-score construction
- Revised regime thresholds
- ARIMA baseline forecasting
- Forecast diagnostic checks
- Local Streamlit dashboard
- Interactive weight and threshold sensitivity analysis
- Market-context validation using S&P 500 forward returns
- Recession-context validation using historical recession indicators

## Risk Categories and Input Variables

The composite score is built from selected scoring inputs across four macro-credit risk channels. Each input is transformed into a comparable risk signal and converted into expanding percentile scores to avoid lookahead bias.

The project also includes additional context and validation variables, such as recession indicators and S&P 500 forward returns, but those variables are not used to calculate the composite score.

### Scoring Inputs

1. **Market / Financial Stress**
   - VIX 3-month average
   - VIX 3-month change
   - BAA-Treasury spread 3-month average
   - BAA-Treasury spread 3-month change
   - STLFSI4 financial stress index 3-month average
   - STLFSI4 financial stress index 3-month change

2. **Macro / Labor Risk**
   - Unemployment rate 3-month average
   - Unemployment rate 3-month change

3. **Rate / Yield-Curve Pressure**
   - 30-year Treasury yield 3-month average
   - 30-year Treasury yield 3-month change
   - Yield-curve inversion risk

4. **Realized Credit Performance**
   - All-loan delinquency rate
   - All-loan delinquency rate 3-month change
   - All-loan charge-off rate
   - All-loan charge-off rate 3-month change

### Context and Validation Variables

The project also uses several variables for interpretation and validation rather than direct scoring:

- **USREC recession indicator:** used to check whether the score behaves sensibly around recession periods.
- **S&P 500 forward returns:** used as a market-context outcome to evaluate whether credit-risk regimes or regime transitions provide useful equity-market context.
- **S&P 500 monthly values:** used for return calculations and market-context analysis, not for building the composite score.

### Feature Window Logic

The scoring framework uses 3-month averages and 3-month changes because the dashboard is built at a monthly frequency while the underlying data arrive at different frequencies. Daily market data are sampled or aggregated into monthly form, monthly macro data update once per month, and quarterly credit-performance data are forward-filled monthly.

The 3-month average captures the recent level of pressure, while the 3-month change captures short-term deterioration or improvement. This creates a cleaner monitoring signal than using only one-month movements, which can be noisy.

### Category Weighting

The baseline model uses equal 25% category weights for transparency:

```text
Composite Score =
25% Market / Financial Stress
+ 25% Macro / Labor Risk
+ 25% Rate / Yield-Curve Pressure
+ 25% Realized Credit Performance
```

The Streamlit dashboard allows users to test custom category-weight assumptions without changing the saved baseline model. These custom weights are used for sensitivity analysis and scenario comparison, not for replacing the official baseline score.

## Dashboard Features

The `streamlit_app/app.py` file contains the Streamlit dashboard code. It reads the cleaned SQLite database, loads the saved dashboard tables, builds the interactive charts, and powers the weight/threshold sensitivity controls.

The Streamlit dashboard includes:

- Latest composite credit-risk score and regime
- Before/after month comparison
- 1-month, 3-month, and 6-month trailing score changes
- Category-driver comparison chart
- Category score-change chart
- Feature drilldown by risk category
- Historical composite score with recession shading
- Custom-weight sensitivity layer
- Adjustable regime thresholds
- Baseline ARIMA forecast outlook
- Custom-weighted forecast recombination
- ARIMA model selection and diagnostics

## Forecast and Sensitivity Interpretation

The dashboard includes two forward-looking forecast views:

1. **Baseline ARIMA Forecast**
2. **Custom Weighted Component Forecast**

The **Baseline ARIMA Forecast** is the official saved forecast from the notebook. It is produced by fitting an ARIMA model directly to the final Composite Credit Risk Score. In other words, the baseline model first uses the already-created composite score series, then forecasts that composite score as one time series.

The **Custom Weighted Component Forecast** is a sensitivity layer. It does not refit ARIMA. Instead, it takes the separately saved category-level forecasts and recombines them using the current category weights selected in the Streamlit sidebar.

Conceptually, the two approaches differ:

```text
Baseline ARIMA Forecast:
Composite Credit Risk Score -> ARIMA model -> projected composite score

Custom Weighted Component Forecast:
Category forecasts -> custom category weights -> recombined projected score
```

Because these are different forecasting methods, the two forecast lines can differ even when the custom weights are set to 25% each. Forecasting the already-averaged composite score is not necessarily the same as forecasting each category separately and then averaging the category forecasts. Each category has its own historical pattern, ARIMA order, persistence, volatility, and residual behavior.

The custom-weight controls affect the custom historical score and the custom weighted forecast line. They do not change the saved baseline ARIMA forecast, selected ARIMA orders, AIC/BIC values, diagnostic statistics, or SQLite model outputs. The custom-weight layer should therefore be interpreted as a scenario and sensitivity tool, not as a full model retraining system.

The threshold sliders adjust how score levels are classified into Normal, Watch, Elevated, and Stress regimes. Changing thresholds can alter regime labels and visual interpretation, but it does not change the underlying score values or the saved forecast model.

## Key Interpretation

The latest dashboard output classifies macro-credit conditions as **Normal**, but close to the Watch threshold. The most elevated category is Rate / Yield-Curve Pressure, while Market / Financial Stress and Macro / Labor Risk show meaningful recent movement. Realized Credit Performance remains slower-moving, consistent with delinquency and charge-off indicators being lagging credit-performance measures.

The ARIMA forecast is treated as a transparent baseline monitoring layer, not a precision forecasting engine. Model diagnostics show that some category-level forecasts, especially Macro / Labor Risk, require cautious interpretation due to residual autocorrelation and stationarity concerns.

## Main Questions Answered

### 1. Current Macro-Credit Regime

The latest dashboard output classifies macro-credit conditions as **Normal**, but close to the Watch threshold. This indicates that the current environment does not show broad-based macro-credit stress, although some risk channels remain elevated.

### 2. Primary Risk Drivers

The highest current risk contribution comes from **Rate / Yield-Curve Pressure**, while **Market / Financial Stress** and **Macro / Labor Risk** show meaningful recent movement. **Realized Credit Performance** remains slower-moving because delinquency and charge-off measures typically update less frequently and tend to lag market-based stress indicators.

### 3. Recent Direction of Risk

The dashboard compares the selected after-month against a before-month and also reports trailing 1-month, 3-month, and 6-month changes. Positive score changes indicate rising macro-credit risk, while negative changes indicate improving or easing risk conditions.

### 4. Broad-Based Versus Concentrated Risk

The dashboard helps distinguish whether risk is broad-based across multiple categories or concentrated in one channel. In the latest reading, risk is not broad-based across all four categories. The main pressure is concentrated in Rate / Yield-Curve Pressure, with additional movement in Market / Financial Stress and Macro / Labor Risk.

### 5. Historical Recession and Stress Behavior

The historical validation checks show that the composite score and category scores generally behave sensibly around recession and stress periods. Market stress, labor risk, and realized credit performance tend to rise around major deterioration periods, while rate and yield-curve pressure can behave differently because yield-curve inversion and rate pressure often appear before realized credit losses or recession confirmation.

### 6. S&P 500 Market-Context Evaluation

The project also tested whether macro-credit regimes and regime transitions provided useful context for future S&P 500 returns. The S&P 500 variables were used as market-context validation outcomes, not as inputs into the composite credit-risk score.

The results did not support a mechanical S&P 500 forecasting or trading rule. Higher-risk regimes did not consistently lead to weaker forward S&P 500 returns in the available sample. However, the transition analysis showed that moving from Normal to Watch was the most useful early-warning transition because it was associated with weaker downside context in the available transition sample.

The main limitation is that there were not enough regime-transition observations to support a statistically conclusive market-timing strategy. The S&P 500 analysis should therefore be interpreted as exploratory market-context evidence, not as a standalone investment signal.

### 7. Weight and Threshold Sensitivity

The Streamlit dashboard allows users to adjust category weights and regime thresholds. This does not retrain the saved model. Instead, it shows how dashboard interpretation changes when the user applies different assumptions to the existing category scores and saved component forecasts.

### 8. Baseline Forward Outlook

The ARIMA forecast provides a baseline near-term monitoring path. It is most useful as a transparent 1-month to 3-month directional monitoring tool. The 6-month projection should be interpreted more cautiously because macro-credit conditions can change quickly when new market, policy, or economic information arrives.

## How to Run Locally

Clone or download the repository and navigate to this project folder.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
python -m streamlit run streamlit_app/app.py
```

The app reads from the included SQLite database:

```text
data/cleaned/credit_risk_detection_monitoring.db
```

## Reproducibility Note

This public version is designed to reproduce the finished Streamlit dashboard, not the full raw API ingestion pipeline.

The dashboard runs from the included SQLite database:

```text
data/cleaned/credit_risk_detection_monitoring.db
```

This database contains cleaned public FRED data and saved dashboard output tables. Because the database is included, users can run the dashboard locally without needing the original FRED API key.

The original development workflow used a local `.env` file for API retrieval. The real `.env` file and API key are not included in this repository. The `.env.example` file is provided only as a template for future users who want to rebuild the raw data pipeline with their own FRED API key.

## Environment Variables

The original data pipeline used a FRED API key stored locally in a `.env` file.

A real API key is **not included** in this repository.

Use `.env.example` as a template:

```text
FRED_API_KEY=your_fred_api_key_here
```

The included Streamlit dashboard runs from the cleaned SQLite database and does not require the API key for dashboard viewing.

## Repository Structure

```text
01_credit_risk_detection_monitoring_dashboard/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── streamlit_app/
│   └── app.py
├── data/
│   └── cleaned/
│       └── credit_risk_detection_monitoring.db
├── assets/
│   ├── crd_shot1.png
│   ├── crd_shot2.png
│   ├── crd_shot3.png
│   └── crd_shot4.png
└── reports/
    ├── README.md
    └── credit_risk_detection_monitoring_report.html
```

The public repository includes the finished Streamlit dashboard, cleaned SQLite database, dashboard screenshots, project README, requirements file, environment-variable template, and sanitized HTML analysis report.

## Limitations

- The ARIMA layer is a baseline monitoring forecast, not a fully validated production forecast.
- Some category-level diagnostics are mixed, especially Macro / Labor Risk.
- The Streamlit custom-weight forecast recombines saved category forecasts but does not retrain ARIMA live.
- The baseline composite forecast and custom weighted component forecast can differ even at equal weights because they are produced through different forecasting workflows.
- The S&P 500 market-context analysis is exploratory and not sufficient for standalone trading decisions.
- Quarterly credit-performance variables are forward-filled to monthly frequency, which makes them slower-moving than market-based indicators.

## Version 2 Enhancements

Future improvements could include:

- Rolling-origin forecast validation for 1-month, 3-month, and 6-month horizons
- Benchmark comparison against naive, moving-average, random-walk, and exponential-smoothing models
- More formal stationarity and transformation workflow for each score series, including level models, first-difference models, retesting after transformation, and rolling-origin comparison of transformed versus untransformed forecasts
- ARIMAX / SARIMAX models using inflation, policy-rate, lending-standard, and credit-supply variables
- Direct inclusion of CPI, core CPI, real rates, Federal Funds Rate, SLOOS lending standards, SLOOS loan demand, MOVE index, and broader labor-market variables
- Alternative empirical category-weighting schemes tested against recession alignment, realized credit deterioration, credit-spread widening, and forecast accuracy
- Forecast interval coverage validation to determine whether uncertainty bands are too narrow, too wide, or reasonably calibrated
- Regime-probability forecasting for Watch, Elevated, and Stress transitions
- Scenario saving inside the Streamlit dashboard for custom weights and custom thresholds
- Expanded market-context validation using longer S&P 500 history and additional risk assets
