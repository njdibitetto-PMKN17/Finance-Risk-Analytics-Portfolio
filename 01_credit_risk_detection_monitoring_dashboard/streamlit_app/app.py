import sqlite3
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Credit Risk Dashboard",
    layout="wide"
)


# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "cleaned" / "credit_risk_detection_monitoring.db"


# Constants
CATEGORY_ORDER = [
    "Market / Financial Stress",
    "Macro / Labor Risk",
    "Rate / Yield-Curve Pressure",
    "Realized Credit Performance",
]

CATEGORY_COLUMNS = {
    "Market / Financial Stress": "market_financial_stress_score",
    "Macro / Labor Risk": "macro_labor_risk_score",
    "Rate / Yield-Curve Pressure": "rate_yield_curve_pressure_score",
    "Realized Credit Performance": "realized_credit_performance_score",
}

OPTIONAL_FEATURE_TABLES = [
    "credit_risk_scoring_inputs",
    "credit_risk_percentile_features",
    "credit_risk_monthly_features",
    "fred_monthly_analysis_core_final",
    "fred_monthly_analysis_core",
]

FEATURE_DETAILS = {
    "Market / Financial Stress": [
        {
            "feature": "VIX 3-Month Average",
            "columns": ["vixcls_3m_avg", "vix_3m_avg"],
            "meaning": "Tracks recent equity-market volatility pressure. Higher values indicate greater market stress."
        },
        {
            "feature": "VIX 3-Month Change",
            "columns": ["vixcls_3m_change", "vix_3m_change"],
            "meaning": "Tracks whether volatility is rising or falling over the recent 3-month window."
        },
        {
            "feature": "BAA-Treasury Spread 3-Month Average",
            "columns": ["baa10y_3m_avg", "baa_spread_3m_avg"],
            "meaning": "Tracks corporate credit-spread pressure. Higher spreads indicate investors require more compensation for credit risk."
        },
        {
            "feature": "BAA-Treasury Spread 3-Month Change",
            "columns": ["baa10y_3m_change", "baa_spread_3m_change"],
            "meaning": "Tracks whether corporate spread pressure is widening or easing."
        },
        {
            "feature": "Financial Stress Index 3-Month Average",
            "columns": ["stlfsi4_3m_avg", "financial_stress_3m_avg"],
            "meaning": "Tracks broad financial-system stress using the STLFSI4 stress index."
        },
        {
            "feature": "Financial Stress Index 3-Month Change",
            "columns": ["stlfsi4_3m_change", "financial_stress_3m_change"],
            "meaning": "Tracks whether broad financial stress is increasing or decreasing."
        },
    ],
    "Macro / Labor Risk": [
        {
            "feature": "Unemployment Rate 3-Month Average",
            "columns": ["unrate_3m_avg", "unemployment_3m_avg"],
            "meaning": "Tracks labor-market weakness. Higher unemployment pressure usually confirms macro deterioration."
        },
        {
            "feature": "Unemployment Rate 3-Month Change",
            "columns": ["unrate_3m_change", "unemployment_3m_change"],
            "meaning": "Tracks whether labor-market conditions are worsening or improving over the recent 3-month window."
        },
    ],
    "Rate / Yield-Curve Pressure": [
        {
            "feature": "30-Year Treasury Yield 3-Month Average",
            "columns": ["dgs30_3m_avg", "treasury_30y_3m_avg"],
            "meaning": "Tracks long-rate pressure. Higher long-term yields can increase borrowing and refinancing pressure."
        },
        {
            "feature": "30-Year Treasury Yield 3-Month Change",
            "columns": ["dgs30_3m_change", "treasury_30y_3m_change"],
            "meaning": "Tracks whether long-term interest-rate pressure is rising or falling."
        },
        {
            "feature": "Yield-Curve Inversion Risk",
            "columns": ["yield_curve_inversion_risk", "t10y2y_inversion_risk"],
            "meaning": "Tracks yield-curve inversion pressure. This feature was directionally transformed so higher values represent greater risk."
        },
    ],
    "Realized Credit Performance": [
        {
            "feature": "All-Loan Delinquency Rate",
            "columns": ["delinquency_all_loans", "dralacbs"],
            "meaning": "Tracks realized borrower credit stress through delinquency rates on bank loans."
        },
        {
            "feature": "All-Loan Delinquency Rate 3-Month Change",
            "columns": ["delinquency_all_loans_3m_change", "dralacbs_3m_change"],
            "meaning": "Tracks whether realized delinquency pressure is worsening or improving."
        },
        {
            "feature": "All-Loan Charge-Off Rate",
            "columns": ["chargeoff_all_loans", "coralacbs"],
            "meaning": "Tracks realized credit losses through charge-off rates on bank loans."
        },
        {
            "feature": "All-Loan Charge-Off Rate 3-Month Change",
            "columns": ["chargeoff_all_loans_3m_change", "coralacbs_3m_change"],
            "meaning": "Tracks whether realized credit-loss pressure is worsening or improving."
        },
    ],
}


# Data loading helpers
@st.cache_data
def list_tables(db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
            """,
            conn
        )


@st.cache_data
def load_table(db_path: str, table_name: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(f"SELECT * FROM {table_name};", conn)


def load_optional_tables(db_path, available_tables):
    optional_tables = {}

    for table_name in OPTIONAL_FEATURE_TABLES:
        if table_name in available_tables:
            optional_tables[table_name] = load_table(str(db_path), table_name)

    return optional_tables


# Formatting helpers
def safe_number(value):
    try:
        return float(value)
    except Exception:
        return None


def format_score(value):
    value = safe_number(value)
    if value is None:
        return "N/A"
    return f"{value:.2f}"


def format_delta(value):
    value = safe_number(value)
    if value is None:
        return None
    return f"{value:+.2f}"


def format_feature_value(value):
    value = safe_number(value)
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.4f}"


# Model helpers
def classify_regime(score, watch_threshold, elevated_threshold, stress_threshold):
    if pd.isna(score):
        return "N/A"
    if score < watch_threshold:
        return "Normal"
    if score < elevated_threshold:
        return "Watch"
    if score < stress_threshold:
        return "Elevated"
    return "Stress"


def normalize_weights(raw_weights):
    total = sum(raw_weights.values())
    if total == 0:
        return {key: 0 for key in raw_weights}
    return {key: value / total for key, value in raw_weights.items()}


def initialize_state():
    defaults = {
        "market_weight": 25,
        "macro_weight": 25,
        "rate_weight": 25,
        "realized_weight": 25,
        "watch_threshold": 45,
        "elevated_threshold": 55,
        "stress_threshold": 70,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_weights():
    st.session_state["market_weight"] = 25
    st.session_state["macro_weight"] = 25
    st.session_state["rate_weight"] = 25
    st.session_state["realized_weight"] = 25


def reset_thresholds():
    st.session_state["watch_threshold"] = 45
    st.session_state["elevated_threshold"] = 55
    st.session_state["stress_threshold"] = 70


def prepare_score_history(score_history):
    score_history = score_history.copy()
    score_history["month_end"] = pd.to_datetime(score_history["month_end"], errors="coerce")

    numeric_cols = [
        "composite_credit_risk_score",
        "market_financial_stress_score",
        "macro_labor_risk_score",
        "rate_yield_curve_pressure_score",
        "realized_credit_performance_score",
    ]

    for col in numeric_cols:
        score_history[col] = pd.to_numeric(score_history[col], errors="coerce")

    score_history = (
        score_history
        .dropna(subset=["month_end"])
        .sort_values("month_end")
        .reset_index(drop=True)
    )

    score_history["composite_change_1m_calc"] = score_history["composite_credit_risk_score"].diff(1)
    score_history["composite_change_3m_calc"] = score_history["composite_credit_risk_score"].diff(3)
    score_history["composite_change_6m_calc"] = score_history["composite_credit_risk_score"].diff(6)

    return score_history


def build_custom_forecast(forward_outlook, weights, watch_threshold, elevated_threshold, stress_threshold):
    forecast = forward_outlook.copy()
    forecast["projected_score"] = pd.to_numeric(forecast["projected_score"], errors="coerce")

    component_rows = forecast[
        forecast["score_component"].isin(CATEGORY_ORDER)
    ].copy()

    if component_rows.empty:
        return pd.DataFrame()

    forecast_pivot = component_rows.pivot_table(
        index="outlook_window",
        columns="score_component",
        values="projected_score",
        aggfunc="first"
    ).reset_index()

    missing_components = [
        component for component in CATEGORY_ORDER
        if component not in forecast_pivot.columns
    ]

    if missing_components:
        return pd.DataFrame()

    forecast_pivot["custom_weighted_forecast_score"] = (
        forecast_pivot["Market / Financial Stress"] * weights["Market / Financial Stress"]
        + forecast_pivot["Macro / Labor Risk"] * weights["Macro / Labor Risk"]
        + forecast_pivot["Rate / Yield-Curve Pressure"] * weights["Rate / Yield-Curve Pressure"]
        + forecast_pivot["Realized Credit Performance"] * weights["Realized Credit Performance"]
    )

    forecast_pivot["custom_forecast_regime"] = forecast_pivot["custom_weighted_forecast_score"].apply(
        lambda score: classify_regime(
            score,
            watch_threshold,
            elevated_threshold,
            stress_threshold
        )
    )

    return forecast_pivot


def add_forecast_dates(forecast_df, latest_month, latest_month_col_name="month_end"):
    df = forecast_df.copy()

    horizon_offsets = {
        "Current": 0,
        "Projected 1-month": 1,
        "Projected 3-month": 3,
        "Projected 6-month": 6,
    }

    df[latest_month_col_name] = df["outlook_window"].map(
        lambda window: latest_month + pd.DateOffset(months=horizon_offsets.get(window, 0))
    )

    df["horizon_order"] = df["outlook_window"].map(horizon_offsets)

    return df


# Chart helpers
def make_threshold_layers(watch_threshold, elevated_threshold, stress_threshold):
    watch_line = (
        alt.Chart(pd.DataFrame({"threshold": [watch_threshold]}))
        .mark_rule(color="#00ff66", strokeDash=[6, 4], size=2)
        .encode(
            y="threshold:Q",
            tooltip=[alt.Tooltip("threshold:Q", title="Watch Threshold")]
        )
    )

    elevated_line = (
        alt.Chart(pd.DataFrame({"threshold": [elevated_threshold]}))
        .mark_rule(color="#ffff00", strokeDash=[6, 4], size=2)
        .encode(
            y="threshold:Q",
            tooltip=[alt.Tooltip("threshold:Q", title="Elevated Threshold")]
        )
    )

    stress_line = (
        alt.Chart(pd.DataFrame({"threshold": [stress_threshold]}))
        .mark_rule(color="#ff3333", strokeDash=[6, 4], size=2)
        .encode(
            y="threshold:Q",
            tooltip=[alt.Tooltip("threshold:Q", title="Stress Threshold")]
        )
    )

    return watch_line + elevated_line + stress_line


def get_y_domain(values, lower_buffer=5, upper_buffer=5):
    clean_values = pd.Series(values).dropna()

    if clean_values.empty:
        return [0, 100]

    lower = max(0, clean_values.min() - lower_buffer)
    upper = min(100, clean_values.max() + upper_buffer)

    if upper - lower < 10:
        upper = min(100, upper + 5)
        lower = max(0, lower - 5)

    return [float(lower), float(upper)]


def build_recession_periods(score_history, y_domain):
    if "usrec" not in score_history.columns:
        return pd.DataFrame()

    recession_df = score_history[["month_end", "usrec"]].copy()
    recession_df["usrec"] = pd.to_numeric(recession_df["usrec"], errors="coerce").fillna(0)

    recession_months = recession_df[recession_df["usrec"] == 1].copy()

    if recession_months.empty:
        return pd.DataFrame()

    recession_months = recession_months.sort_values("month_end").reset_index(drop=True)
    recession_months["month_gap"] = recession_months["month_end"].diff().dt.days.fillna(31)
    recession_months["group"] = (recession_months["month_gap"] > 45).cumsum()

    periods = (
        recession_months
        .groupby("group")
        .agg(
            start=("month_end", "min"),
            end=("month_end", "max")
        )
        .reset_index(drop=True)
    )

    periods["end"] = periods["end"] + pd.DateOffset(months=1)
    periods["ymin"] = y_domain[0]
    periods["ymax"] = y_domain[1]

    return periods


def make_recession_layer(recession_periods, legend_domain, legend_range):
    if recession_periods.empty:
        return alt.Chart(pd.DataFrame({"x": []})).mark_rect()

    recession_periods = recession_periods.copy()
    recession_periods["score_type"] = "NBER Recession Shading"

    return (
        alt.Chart(recession_periods)
        .mark_rect(opacity=0.22)
        .encode(
            x="start:T",
            x2="end:T",
            y="ymin:Q",
            y2="ymax:Q",
            color=alt.Color(
                "score_type:N",
                title="Score Type",
                legend=alt.Legend(title="Score Type", orient="right"),
                scale=alt.Scale(
                    domain=legend_domain,
                    range=legend_range
                ),
            ),
            tooltip=[
                alt.Tooltip("start:T", title="Recession Start"),
                alt.Tooltip("end:T", title="Recession End"),
            ],
        )
    )


# Feature drilldown helpers
def find_date_column(df):
    candidates = [
        "month_end",
        "date",
        "observation_date",
        "month",
        "period",
    ]

    for col in candidates:
        if col in df.columns:
            return col

    return None


def find_first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col

    return None


def get_month_row(df, target_month):
    date_col = find_date_column(df)

    if date_col is None:
        return pd.DataFrame()

    temp_df = df.copy()
    temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors="coerce")

    return temp_df[temp_df[date_col].dt.date == target_month]


def build_feature_detail_table(optional_tables, category, before_month, after_month):
    feature_specs = FEATURE_DETAILS.get(category, [])
    rows = []

    for feature_spec in feature_specs:
        feature_name = feature_spec["feature"]
        column_candidates = feature_spec["columns"]
        meaning = feature_spec["meaning"]

        source_table = "Not found"
        source_column = "Not found"
        before_value = None
        after_value = None

        for table_name, table_df in optional_tables.items():
            source_col = find_first_existing_column(table_df, column_candidates)

            if source_col is None:
                continue

            before_rows = get_month_row(table_df, before_month)
            after_rows = get_month_row(table_df, after_month)

            if before_rows.empty or after_rows.empty:
                continue

            before_value = before_rows.iloc[0].get(source_col)
            after_value = after_rows.iloc[0].get(source_col)
            source_table = table_name
            source_column = source_col
            break

        before_num = safe_number(before_value)
        after_num = safe_number(after_value)

        if before_num is not None and after_num is not None:
            change = after_num - before_num
        else:
            change = None

        rows.append({
            "feature": feature_name,
            "source_table": source_table,
            "source_column": source_column,
            "before_value": before_num,
            "after_value": after_num,
            "change": change,
            "meaning": meaning,
        })

    return pd.DataFrame(rows)


# App Header
st.title("Credit Risk Detection & Monitoring Dashboard")
st.caption("Macro-credit risk monitoring with market-context and forward-risk overlay")

if not DB_PATH.exists():
    st.error("Database not found.")
    st.write("Expected database path:")
    st.code(str(DB_PATH))
    st.stop()


# Load Data
tables = list_tables(str(DB_PATH))
available_tables = set(tables["name"].tolist())

score_history = load_table(str(DB_PATH), "dashboard_credit_risk_score")
forward_outlook = load_table(str(DB_PATH), "dashboard_forward_credit_risk_outlook")
forecast_range = load_table(str(DB_PATH), "dashboard_composite_forward_outlook_range")
model_summary = load_table(str(DB_PATH), "dashboard_arima_selected_models")
diagnostics = load_table(str(DB_PATH), "dashboard_arima_diagnostic_summary")
optional_tables = load_optional_tables(DB_PATH, available_tables)


# Prepare Data
required_score_columns = [
    "month_end",
    "composite_credit_risk_score",
    "composite_credit_risk_regime_revised",
    "market_financial_stress_score",
    "macro_labor_risk_score",
    "rate_yield_curve_pressure_score",
    "realized_credit_performance_score",
]

missing_score_columns = [
    col for col in required_score_columns
    if col not in score_history.columns
]

if missing_score_columns:
    st.error("The score history table is missing required columns:")
    st.write(missing_score_columns)
    st.dataframe(score_history.head(10), width="stretch")
    st.stop()

score_history = prepare_score_history(score_history)
latest_month = score_history["month_end"].max()


# Sidebar Controls
initialize_state()

st.sidebar.header("Dashboard Controls")

available_months = score_history["month_end"].dt.date.sort_values(ascending=False).tolist()

before_default_index = 1 if len(available_months) > 1 else 0
after_default_index = 0

before_month = st.sidebar.selectbox(
    "Before month",
    available_months,
    index=before_default_index
)

after_month = st.sidebar.selectbox(
    "After month",
    available_months,
    index=after_default_index
)

if before_month > after_month:
    st.sidebar.warning("Before month is later than after month. Changes will still calculate, but interpretation may be reversed.")

min_date = score_history["month_end"].dt.date.min()
max_date = score_history["month_end"].dt.date.max()

date_range = st.sidebar.slider(
    "Historical chart date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

forecast_chart_min_date = score_history["month_end"].min().date()
forecast_chart_max_date = (latest_month + pd.DateOffset(months=6)).date()

forecast_chart_range = st.sidebar.slider(
    "Forecast chart date range",
    min_value=forecast_chart_min_date,
    max_value=forecast_chart_max_date,
    value=(forecast_chart_min_date, forecast_chart_max_date)
)

st.sidebar.header("Custom Weight Sensitivity")
st.sidebar.caption("Baseline model remains 25% / 25% / 25% / 25%.")

st.sidebar.button(
    "Reset weights to 25%",
    on_click=reset_weights
)

raw_weights = {
    "Market / Financial Stress": st.sidebar.slider(
        "Market / Financial Stress weight",
        min_value=0,
        max_value=100,
        step=1,
        key="market_weight"
    ),
    "Macro / Labor Risk": st.sidebar.slider(
        "Macro / Labor Risk weight",
        min_value=0,
        max_value=100,
        step=1,
        key="macro_weight"
    ),
    "Rate / Yield-Curve Pressure": st.sidebar.slider(
        "Rate / Yield-Curve Pressure weight",
        min_value=0,
        max_value=100,
        step=1,
        key="rate_weight"
    ),
    "Realized Credit Performance": st.sidebar.slider(
        "Realized Credit Performance weight",
        min_value=0,
        max_value=100,
        step=1,
        key="realized_weight"
    ),
}

weights = normalize_weights(raw_weights)

with st.sidebar.expander("Applied normalized weights"):
    for label, weight in weights.items():
        st.write(f"{label}: {weight:.1%}")

st.sidebar.header("Regime Thresholds")

st.sidebar.button(
    "Reset thresholds",
    on_click=reset_thresholds
)

watch_threshold = st.sidebar.slider(
    "Watch threshold",
    min_value=35,
    max_value=60,
    step=1,
    key="watch_threshold"
)

elevated_threshold = st.sidebar.slider(
    "Elevated threshold",
    min_value=50,
    max_value=75,
    step=1,
    key="elevated_threshold"
)

stress_threshold = st.sidebar.slider(
    "Stress threshold",
    min_value=60,
    max_value=90,
    step=1,
    key="stress_threshold"
)

if not (watch_threshold < elevated_threshold < stress_threshold):
    st.sidebar.error("Thresholds must satisfy: Watch < Elevated < Stress.")
    st.stop()

show_raw_tables = st.sidebar.checkbox("Show raw dashboard tables", value=False)


# Custom Weighted Score
custom_score_history = score_history.copy()
custom_score_history["custom_weighted_score"] = 0.0

for label, col in CATEGORY_COLUMNS.items():
    custom_score_history["custom_weighted_score"] += (
        custom_score_history[col] * weights[label]
    )

custom_score_history["custom_regime"] = custom_score_history["custom_weighted_score"].apply(
    lambda score: classify_regime(
        score,
        watch_threshold,
        elevated_threshold,
        stress_threshold
    )
)


# Before and After Month Data
before_rows = custom_score_history[
    custom_score_history["month_end"].dt.date == before_month
]

after_rows = custom_score_history[
    custom_score_history["month_end"].dt.date == after_month
]

if before_rows.empty:
    st.error("Before month not found in score history.")
    st.stop()

if after_rows.empty:
    st.error("After month not found in score history.")
    st.stop()

before_row = before_rows.iloc[0]
after_row = after_rows.iloc[0]

baseline_score = after_row["composite_credit_risk_score"]
baseline_regime = after_row["composite_credit_risk_regime_revised"]
custom_score = after_row["custom_weighted_score"]
custom_regime = after_row["custom_regime"]

before_baseline_score = before_row["composite_credit_risk_score"]
before_custom_score = before_row["custom_weighted_score"]

baseline_change = baseline_score - before_baseline_score
custom_change = custom_score - before_custom_score

change_1m = after_row["composite_change_1m_calc"]
change_3m = after_row["composite_change_3m_calc"]
change_6m = after_row["composite_change_6m_calc"]


# Selected Dashboard Reading
st.subheader("Selected Dashboard Reading")

st.caption(
    f"Change calculations use: after month minus before month. "
    f"Current comparison: {after_month} minus {before_month}. "
    f"Positive changes mean higher macro-credit risk. Negative changes mean lower macro-credit risk."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Before Month", str(before_month))
col2.metric("After Month", str(after_month))
col3.metric(
    "Baseline Score",
    format_score(baseline_score),
    delta=format_delta(baseline_change),
    delta_color="inverse"
)
col4.metric("Baseline Regime", str(baseline_regime))

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Custom Weighted Score",
    format_score(custom_score),
    delta=format_delta(custom_change),
    delta_color="inverse"
)
col6.metric("Custom Regime", str(custom_regime))
col7.metric("After-Month 1M Change", format_score(change_1m))
col8.metric("After-Month 3M Change", format_score(change_3m))

st.metric("After-Month 6M Change", format_score(change_6m))

st.caption(
    "The Baseline Score and Custom Weighted Score deltas compare After Month minus Before Month. "
    "The 1M, 3M, and 6M changes are trailing historical changes in the baseline composite score ending at the After Month. "
    "They are not forecasts and they do not depend on the manually selected Before Month."
)


# Category Driver Comparison Data
category_rows = []

for label, col in CATEGORY_COLUMNS.items():
    after_score = after_row[col]
    before_score = before_row[col]
    score_change = after_score - before_score

    category_rows.append({
        "category": label,
        "after_score": after_score,
        "before_score": before_score,
        "score_change": score_change,
        "change_start": min(after_score, before_score),
        "change_end": max(after_score, before_score),
        "change_direction": (
            "Risk Increased" if score_change > 0
            else "Risk Decreased" if score_change < 0
            else "No Change"
        ),
        "weight": weights[label],
        "weighted_contribution": after_score * weights[label],
    })

category_df = pd.DataFrame(category_rows)
category_df["zero"] = 0


# Category Drivers
st.subheader("Category Drivers for After Month")

st.caption(
    "Light blue shows the before-month score. "
    "Red shows added risk from before month to after month. "
    "Green shows risk reduction from before month to after month."
)

comparison_base_chart = (
    alt.Chart(category_df)
    .mark_bar(color="#7ec8ff", stroke="#ffffff", strokeWidth=0.7)
    .encode(
        x=alt.X("zero:Q", title="Category Risk Score"),
        x2="before_score:Q",
        y=alt.Y("category:N", sort=CATEGORY_ORDER, title="Category"),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("before_score:Q", title="Before Score", format=".2f"),
            alt.Tooltip("after_score:Q", title="After Score", format=".2f"),
            alt.Tooltip("score_change:Q", title="Change", format="+.2f"),
            alt.Tooltip("change_direction:N", title="Direction"),
            alt.Tooltip("weight:Q", title="Applied Weight", format=".1%"),
            alt.Tooltip("weighted_contribution:Q", title="Weighted Contribution", format=".2f"),
        ],
    )
)

change_overlay_chart = (
    alt.Chart(category_df)
    .mark_bar(stroke="#ffffff", strokeWidth=1.2)
    .encode(
        x=alt.X("change_start:Q", title="Category Risk Score"),
        x2="change_end:Q",
        y=alt.Y("category:N", sort=CATEGORY_ORDER, title="Category"),
        color=alt.Color(
            "change_direction:N",
            scale=alt.Scale(
                domain=["Risk Increased", "Risk Decreased", "No Change"],
                range=["#ff3333", "#00cc66", "#bfbfbf"]
            ),
            title="Change Direction"
        ),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("before_score:Q", title="Before Score", format=".2f"),
            alt.Tooltip("after_score:Q", title="After Score", format=".2f"),
            alt.Tooltip("score_change:Q", title="Change", format="+.2f"),
            alt.Tooltip("change_direction:N", title="Direction"),
        ],
    )
)

category_driver_chart = (
    comparison_base_chart + change_overlay_chart
).properties(height=260)

st.altair_chart(category_driver_chart, width="stretch")


# Category Score Change
st.subheader("Category Score Change Between Before and After Months")

change_chart = (
    alt.Chart(category_df)
    .mark_bar(stroke="#ffffff", strokeWidth=0.8)
    .encode(
        x=alt.X("score_change:Q", title="Score Change"),
        y=alt.Y("category:N", sort=CATEGORY_ORDER, title="Category"),
        color=alt.Color(
            "change_direction:N",
            scale=alt.Scale(
                domain=["Risk Increased", "Risk Decreased", "No Change"],
                range=["#ff3333", "#00cc66", "#bfbfbf"]
            ),
            title="Direction"
        ),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("before_score:Q", title="Before Score", format=".2f"),
            alt.Tooltip("after_score:Q", title="After Score", format=".2f"),
            alt.Tooltip("score_change:Q", title="Change", format="+.2f"),
            alt.Tooltip("change_direction:N", title="Direction"),
        ],
    )
    .properties(height=260)
)

zero_line = (
    alt.Chart(pd.DataFrame({"x": [0]}))
    .mark_rule(color="#ffffff", size=1)
    .encode(x="x:Q")
)

st.altair_chart(change_chart + zero_line, width="stretch")

category_display_df = category_df.drop(columns=["zero"], errors="ignore")

st.dataframe(
    category_display_df.sort_values("after_score", ascending=False),
    width="stretch"
)


# Category Feature Drilldown
st.subheader("Category Feature Drilldown")

st.write(
    "Select a risk category to inspect the underlying variables used to build that category. "
    "Values are shown for the selected before and after months when the underlying feature table is available."
)

selected_category_detail = st.selectbox(
    "Select category to inspect",
    CATEGORY_ORDER
)

selected_category_score_row = category_df[
    category_df["category"] == selected_category_detail
].iloc[0]

detail_col1, detail_col2, detail_col3 = st.columns(3)

detail_col1.metric(
    "Before Category Score",
    format_score(selected_category_score_row["before_score"])
)

detail_col2.metric(
    "After Category Score",
    format_score(selected_category_score_row["after_score"])
)

detail_col3.metric(
    "Category Score Change",
    format_score(selected_category_score_row["score_change"]),
    delta=format_delta(selected_category_score_row["score_change"]),
    delta_color="inverse"
)

feature_detail_df = build_feature_detail_table(
    optional_tables=optional_tables,
    category=selected_category_detail,
    before_month=before_month,
    after_month=after_month
)

if feature_detail_df.empty:
    st.warning("No feature details were available for this category.")
else:
    feature_detail_display = feature_detail_df.copy()
    feature_detail_display["before_value"] = feature_detail_display["before_value"].apply(format_feature_value)
    feature_detail_display["after_value"] = feature_detail_display["after_value"].apply(format_feature_value)
    feature_detail_display["change"] = feature_detail_display["change"].apply(format_feature_value)

    st.dataframe(
        feature_detail_display,
        width="stretch"
    )

    missing_features = feature_detail_df[
        feature_detail_df["source_table"] == "Not found"
    ]

    if not missing_features.empty:
        st.info(
            "Some feature values were not found in the available SQLite feature tables. "
            "The category score is still valid because it comes from the saved dashboard score table, "
            "but the raw feature drilldown depends on whether the intermediate feature tables were saved."
        )


# Historical Composite Score
st.subheader("Historical Composite Credit Risk Score")

chart_data = custom_score_history[
    (custom_score_history["month_end"].dt.date >= date_range[0])
    & (custom_score_history["month_end"].dt.date <= date_range[1])
].copy()

chart_long = chart_data[
    ["month_end", "composite_credit_risk_score", "custom_weighted_score"]
].melt(
    id_vars="month_end",
    value_vars=["composite_credit_risk_score", "custom_weighted_score"],
    var_name="score_type",
    value_name="score"
)

chart_long["score_type"] = chart_long["score_type"].replace({
    "composite_credit_risk_score": "Baseline 25% Equal-Weight Score",
    "custom_weighted_score": "Custom Weighted Score",
})

historical_y_domain = get_y_domain(chart_long["score"], lower_buffer=8, upper_buffer=8)

historical_color_domain = [
    "Baseline 25% Equal-Weight Score",
    "Custom Weighted Score",
    "NBER Recession Shading",
]

historical_color_range = [
    "#4da3ff",
    "#ffffff",
    "#8a94a6",
]

historical_recession_periods = build_recession_periods(chart_data, historical_y_domain)

historical_recession_layer = make_recession_layer(
    historical_recession_periods,
    historical_color_domain,
    historical_color_range
)

historical_chart = (
    alt.Chart(chart_long)
    .mark_line()
    .encode(
        x=alt.X("month_end:T", title="Month"),
        y=alt.Y(
            "score:Q",
            title="Composite Risk Score",
            scale=alt.Scale(domain=historical_y_domain),
            axis=alt.Axis(tickCount=12)
        ),
        color=alt.Color(
            "score_type:N",
            title="Score Type",
            legend=alt.Legend(title="Score Type", orient="right"),
            scale=alt.Scale(
                domain=historical_color_domain,
                range=historical_color_range,
            ),
        ),
        tooltip=[
            alt.Tooltip("month_end:T", title="Month"),
            alt.Tooltip("score_type:N", title="Score Type"),
            alt.Tooltip("score:Q", title="Score", format=".2f"),
        ],
    )
    .properties(height=440)
)

threshold_lines = make_threshold_layers(
    watch_threshold,
    elevated_threshold,
    stress_threshold
)

st.altair_chart(
    historical_recession_layer + historical_chart + threshold_lines,
    width="stretch"
)


# Forecast Chart
st.subheader("Historical Score with Baseline and Custom Forecast Outlook")

st.write(
    "This chart shows the score history from the selected forecast chart range, followed by the saved baseline ARIMA forecast "
    "and a custom-weighted forecast that recombines the existing category-level forecasts. "
    "Changing weights affects the custom historical score and the custom forecast line by recombining saved category scores "
    "and saved category forecasts. It does not retrain ARIMA, recalculate BIC/AIC, update diagnostics, or change the saved notebook model."
)

historical_forecast_lines = custom_score_history[
    ["month_end", "composite_credit_risk_score", "custom_weighted_score"]
].melt(
    id_vars="month_end",
    value_vars=["composite_credit_risk_score", "custom_weighted_score"],
    var_name="score_type",
    value_name="score"
)

historical_forecast_lines["score_type"] = historical_forecast_lines["score_type"].replace({
    "composite_credit_risk_score": "Baseline Historical Score",
    "custom_weighted_score": "Custom Weighted Historical Score",
})

forecast_range_clean = forecast_range.copy()
forecast_range_clean["projected_score"] = pd.to_numeric(
    forecast_range_clean["projected_score"],
    errors="coerce"
)

baseline_forecast = forecast_range_clean[
    ["outlook_window", "projected_score", "projected_regime"]
].copy()

baseline_forecast = add_forecast_dates(
    baseline_forecast,
    latest_month=latest_month,
    latest_month_col_name="month_end"
)

baseline_forecast["score_type"] = "Baseline ARIMA Forecast"
baseline_forecast = baseline_forecast.rename(
    columns={
        "projected_score": "score",
        "projected_regime": "regime",
    }
)

custom_forecast = build_custom_forecast(
    forward_outlook,
    weights,
    watch_threshold,
    elevated_threshold,
    stress_threshold
)

if not custom_forecast.empty:
    custom_forecast_chart_data = custom_forecast[
        ["outlook_window", "custom_weighted_forecast_score", "custom_forecast_regime"]
    ].copy()

    custom_forecast_chart_data = add_forecast_dates(
        custom_forecast_chart_data,
        latest_month=latest_month,
        latest_month_col_name="month_end"
    )

    custom_forecast_chart_data["score_type"] = "Custom Weighted Component Forecast"
    custom_forecast_chart_data = custom_forecast_chart_data.rename(
        columns={
            "custom_weighted_forecast_score": "score",
            "custom_forecast_regime": "regime",
        }
    )

    forecast_lines = pd.concat(
        [
            baseline_forecast[["month_end", "score_type", "score"]],
            custom_forecast_chart_data[["month_end", "score_type", "score"]],
        ],
        ignore_index=True
    )
else:
    forecast_lines = baseline_forecast[["month_end", "score_type", "score"]].copy()

forecast_chart_data = pd.concat(
    [
        historical_forecast_lines[["month_end", "score_type", "score"]],
        forecast_lines[["month_end", "score_type", "score"]],
    ],
    ignore_index=True
)

forecast_chart_data = forecast_chart_data.dropna(subset=["month_end", "score"])

forecast_chart_data = forecast_chart_data[
    (forecast_chart_data["month_end"].dt.date >= forecast_chart_range[0])
    & (forecast_chart_data["month_end"].dt.date <= forecast_chart_range[1])
].copy()

forecast_y_domain = get_y_domain(forecast_chart_data["score"], lower_buffer=6, upper_buffer=6)

forecast_recession_periods = build_recession_periods(
    custom_score_history[
        (custom_score_history["month_end"].dt.date >= forecast_chart_range[0])
        & (custom_score_history["month_end"].dt.date <= forecast_chart_range[1])
    ],
    forecast_y_domain
)

forecast_color_domain = [
    "Baseline Historical Score",
    "Custom Weighted Historical Score",
    "Baseline ARIMA Forecast",
    "Custom Weighted Component Forecast",
    "NBER Recession Shading",
]

forecast_color_range = [
    "#4da3ff",
    "#ffffff",
    "#b266ff",
    "#ff66cc",
    "#8a94a6",
]

forecast_recession_layer = make_recession_layer(
    forecast_recession_periods,
    forecast_color_domain,
    forecast_color_range
)

forecast_chart = (
    alt.Chart(forecast_chart_data)
    .mark_line(point=True)
    .encode(
        x=alt.X("month_end:T", title="Month"),
        y=alt.Y(
            "score:Q",
            title="Composite Risk Score",
            scale=alt.Scale(domain=forecast_y_domain),
            axis=alt.Axis(tickCount=12)
        ),
        color=alt.Color(
            "score_type:N",
            title="Score Type",
            legend=alt.Legend(title="Score Type", orient="right"),
            scale=alt.Scale(
                domain=forecast_color_domain,
                range=forecast_color_range,
            ),
        ),
        strokeDash=alt.StrokeDash(
            "score_type:N",
            scale=alt.Scale(
                domain=[
                    "Baseline Historical Score",
                    "Custom Weighted Historical Score",
                    "Baseline ARIMA Forecast",
                    "Custom Weighted Component Forecast",
                    "NBER Recession Shading",
                ],
                range=[
                    [1, 0],
                    [1, 0],
                    [8, 4],
                    [8, 4],
                    [1, 0],
                ],
            ),
            legend=alt.Legend(title="Line Style", orient="right"),
        ),
        tooltip=[
            alt.Tooltip("month_end:T", title="Month"),
            alt.Tooltip("score_type:N", title="Score Type"),
            alt.Tooltip("score:Q", title="Score", format=".2f"),
        ],
    )
    .properties(height=500)
)

three_month_cutoff = latest_month + pd.DateOffset(months=3)

late_forecast_segments = forecast_chart_data[
    (forecast_chart_data["month_end"] >= three_month_cutoff)
    & (
        forecast_chart_data["score_type"].isin([
            "Baseline ARIMA Forecast",
            "Custom Weighted Component Forecast",
        ])
    )
].copy()

late_forecast_caution_layer = (
    alt.Chart(late_forecast_segments)
    .mark_line(point=True, color="#a87945", strokeDash=[8, 4], size=4)
    .encode(
        x=alt.X("month_end:T", title="Month"),
        y=alt.Y(
            "score:Q",
            title="Composite Risk Score",
            scale=alt.Scale(domain=forecast_y_domain),
            axis=alt.Axis(tickCount=12)
        ),
        detail="score_type:N",
        tooltip=[
            alt.Tooltip("month_end:T", title="Month"),
            alt.Tooltip("score_type:N", title="Score Type"),
            alt.Tooltip("score:Q", title="Score", format=".2f"),
        ],
    )
)

st.altair_chart(
    forecast_recession_layer + forecast_chart + threshold_lines + late_forecast_caution_layer,
    width="stretch"
)

st.caption(
    "Brown overlay highlights the 3-month to 6-month forecast segment, "
    "which should be interpreted more cautiously than the 1-month and 3-month monitoring windows."
)

forecast_table = forecast_lines.copy()
forecast_table["month_end"] = pd.to_datetime(forecast_table["month_end"]).dt.date

st.dataframe(
    forecast_table.sort_values(["month_end", "score_type"]),
    width="stretch"
)


# Baseline Forward Outlook
st.subheader("Baseline Forward Credit-Risk Outlook Table")
st.dataframe(forward_outlook, width="stretch")


# Composite Forecast Range
st.subheader("Composite Forecast Range")

st.write(
    "The Current row has no lower or upper forecast range because it is an observed score. "
    "Forecast ranges begin with the projected 1-month, 3-month, and 6-month rows."
)

st.dataframe(forecast_range, width="stretch")


# Model Transparency
st.subheader("ARIMA Model Selection Summary")
st.dataframe(model_summary, width="stretch")

st.subheader("ARIMA Diagnostic Summary")
st.dataframe(diagnostics, width="stretch")

st.markdown(
    """
    **Diagnostic interpretation**

    The ARIMA diagnostic table evaluates whether the saved baseline forecasts are reasonable monitoring tools.

    - **ADF p-value:** tests for a unit root. A value below 0.05 suggests the series is more likely stationary.
    - **KPSS p-value:** tests whether the series is stationary. A value above 0.05 is preferred because it means stationarity is not rejected.
    - **Ljung-Box p-value at lag 6:** tests whether residual autocorrelation remains after fitting the ARIMA model. A value above 0.05 is preferred.
    - **Residual mean:** measures average model error. Values closer to zero are preferred.
    - **Residual standard error:** measures the typical size of the model residuals. Larger values imply more forecast uncertainty.

    A clean diagnostic profile generally has ADF p-value below 0.05, KPSS p-value above 0.05, Ljung-Box p-value above 0.05, and residual mean close to zero. Mixed ADF/KPSS results do not automatically invalidate the model, but they indicate that the forecast should be interpreted with caution.
    """
)

st.markdown(
    """
    **Dashboard interpretation**

    The Composite Credit Risk Score forecast is retained as a transparent baseline monitoring path. Most model residual checks are acceptable, but the Macro / Labor Risk model shows weaker diagnostics because its Ljung-Box p-value indicates remaining residual autocorrelation. This means the Macro / Labor Risk forecast should be interpreted more cautiously than the Market / Financial Stress or Realized Credit Performance forecasts.

    These diagnostics do not change when Streamlit weight sliders are adjusted. The sliders only recombine the saved category scores and saved category forecasts. They do not rerun ARIMA model selection, recalculate BIC/AIC, or refit model diagnostics.
    """
)


# Optional Raw Tables
if show_raw_tables:
    st.subheader("SQLite Tables Found")
    st.dataframe(tables, width="stretch")

    st.subheader("Raw Score History")
    st.dataframe(
        score_history.sort_values("month_end", ascending=False),
        width="stretch"
    )

    st.subheader("Custom Weighted Score History")
    st.dataframe(
        custom_score_history.sort_values("month_end", ascending=False),
        width="stretch"
    )

    if optional_tables:
        for table_name, table_df in optional_tables.items():
            st.subheader(f"Optional Feature Table: {table_name}")
            st.dataframe(table_df.head(100), width="stretch")