import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("S&P 500 Overlay: Peaks Aligned")

# --- Fetch two 1-year slices of SPX ---
@st.cache_data
def fetch_close(start: str, end: str) -> pd.Series:
    df = yf.download("^GSPC", start=start, end=end, progress=False)
    return df["Close"]

# hard-coded windows (you can make these configurable if you like)
s1 = fetch_close("2021-12-01", "2022-06-01")
s2 = fetch_close("2024-12-01", "2025-06-01")

# --- Find peaks and shift second series to align ---
peak1 = s1.idxmax()
peak2 = s2.idxmax()
shift = peak2 - peak1

s2_shifted = s2.copy()
s2_shifted.index = s2_shifted.index - shift

# --- Plotting ---
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
