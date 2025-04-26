import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title("S&P 500 Overlay: Peaks Aligned")

@st.cache_data
def fetch_close(start: str, end: str) -> pd.Series:
    """
    Downloads the daily closing prices for the S&P 500 (^GSPC) between two dates.
    """
    df = yf.download("^GSPC", start=start, end=end, progress=False)
    return df["Close"]

# Fetch two one-year periods
s1 = fetch_close("2021-12-01", "2022-06-01")  # Dec ’21 → May ’22
s2 = fetch_close("2024-12-01", "2025-06-01")  # Dec ’24 → May ’25

# Find each period's peak date and calculate the time shift
peak1 = s1.idxmax()
peak2 = s2.idxmax()
shift = peak2 - peak1  # pandas.Timedelta

# Manually shift the second period's dates
shifted_dates = [ts - shift for ts in s2.index]

# Plot both series on the same axes with the peaks aligned
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(s1.index,       s1.values,      label="Dec ’21–May ’22")
ax.plot(shifted_dates,  s2.values,      label="Dec ’24–May ’25 (shifted)")
ax.axvline(peak1, color="gray", linestyle="--", label="Aligned Peak")

# Formatting
ax.set_xlabel("Date")
ax.set_ylabel("S&P 500 Close")
ax.set_title("Overlay of Two 1-Year SPX Periods with Peaks Aligned")
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)
