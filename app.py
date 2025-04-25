import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(layout="wide")
st.title("S&P 500 Overlay: Peaks Aligned")

@st.cache_data
def fetch_close(start: str, end: str) -> pd.Series:
    """
    Download S&P 500 (^GSPC) daily Close series between start and end dates.
    """
    df = yf.download("^GSPC", start=start, end=end, progress=False)
    return df["Close"]

# ——— Load two 1-year windows ———
s1 = fetch_close("2021-12-01", "2022-06-01")  # Dec ’21 → May ’22
s2 = fetch_close("2024-12-01", "2025-06-01")  # Dec ’24 → May ’25

# ——— Identify peaks and compute shift ———
peak1 = s1.idxmax()       # Timestamp of series A’s highest close
peak2 = s2.idxmax()       # Timestamp of series B’s highest close
shift  = peak2 - peak1    # pandas.Timedelta

# ——— Apply manual element-wise shift to series B ———
s2_shifted = s2.copy()
new_dates = [ts - shift for ts in s2_shifted.index]
s2_shifted.index = new_dates

# ——— Plot both series with aligned peak ———
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(s1.index,        s1.values,      label="Dec ’21–May ’22")
ax.plot(s2_shifted.index, s2_shifted.values, label="Dec ’24–May ’25 (shifted)")
ax.axvline(peak1, color="gray", linestyle="--", label="Aligned Peak")

ax.set_xlabel("Date")
ax.set_ylabel("S&P 500 Close")
ax.set_title("Overlay of Two 1-Year SPX Periods with Peaks Aligned")
ax.legend()
ax.grid(True)

st.pyplot(fig)
