import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from datetime import date

# Page configuration
st.set_page_config(layout="wide")
st.title("S&P 500 Overlay: Peaks Aligned and Normalized")

# Sidebar inputs for two 1-year windows
today = date.today()
col1, col2 = st.sidebar.columns(2)
with col1:
    start_a = st.date_input(
        "Series A start date", value=date(2021, 12, 1), max_value=today
    )
with col2:
    start_b = st.date_input(
        "Series B start date", value=date(2024, 12, 1), max_value=today
    )

# Compute end dates one year later
df1_start = pd.to_datetime(start_a)
df1_end = df1_start + pd.DateOffset(years=1)
df2_start = pd.to_datetime(start_b)
df2_end = df2_start + pd.DateOffset(years=1)

@st.cache_data
def fetch_close(start: str, end: str) -> pd.Series:
    """
    Download daily closing prices for S&P 500 (^GSPC) between start and end.
    """
    df = yf.download("^GSPC", start=start, end=end, progress=False)
    return df["Close"]

# Fetch data for both periods
s1 = fetch_close(df1_start.strftime('%Y-%m-%d'), df1_end.strftime('%Y-%m-%d'))
s2 = fetch_close(df2_start.strftime('%Y-%m-%d'), df2_end.strftime('%Y-%m-%d'))

# Normalize series to percent-from-peak
s1_norm = s1 / s1.max() * 100
s2_norm = s2 / s2.max() * 100

# Align peaks by computing shift
peak1 = s1_norm.idxmax()
peak2 = s2_norm.idxmax()
shift = peak2 - peak1

# Shift series B dates
shifted_dates = [ts - shift for ts in s2_norm.index]

# Build DataFrames for plotting
# Series A
df_a = s1_norm.to_frame(name='value').reset_index().rename(columns={'index': 'date'})
df_a['series'] = 'A'
# Series B
df_b = pd.DataFrame({'date': shifted_dates, 'value': s2_norm.values})
df_b['series'] = 'B'

# Combine and sort
df_all = pd.concat([df_a, df_b], ignore_index=True)
df_all = df_all.sort_values('date')

# Create interactive Altair chart
tooltip = ['date:T', 'value:Q', 'series:N']
chart = (
    alt.Chart(df_all)
        .mark_line()
        .encode(
            x='date:T',
            y='value:Q',
            color='series:N',
            tooltip=tooltip
        )
        .properties(width='container', height=400)
        .interactive()
)

st.altair_chart(chart, use_container_width=True)
