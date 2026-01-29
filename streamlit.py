import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("./weather.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    return df

df = load_data()

# ----------------------------
# Sidebar – Year selection
# ----------------------------
st.sidebar.title("Weather Dashboard")
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

year_df = df[df["year"] == selected_year]

# ----------------------------
# Year summary
# ----------------------------
st.title(f"{selected_year} Summary")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Max Temp (°C)", round(year_df["temperature"].max(), 1))
c2.metric("Min Temp (°C)", round(year_df["temperature"].min(), 1))
c3.metric("Max Precip (mm)", round(year_df["precipitation"].max(), 1))
c4.metric("Min Precip (mm)", round(year_df["precipitation"].min(), 1))
c5.metric("Max Wind", round(year_df["wind"].max(), 1))
c6.metric("Min Wind", round(year_df["wind"].min(), 1))

st.divider()

# ----------------------------
# Row 1: Temperature line + Dot plot
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperature Trend")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(year_df["date"], year_df["temperature"], linewidth=1)
    ax.set_ylabel("°C")
    ax.set_xlabel("Date")
    st.pyplot(fig)

with col2:
    st.subheader("Temperature Dot Plot")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.scatter(
        year_df["date"],
        year_df["temperature"],
        s=8,        # dot size (smaller)
        alpha=0.6
    )
    ax.set_ylabel("°C")
    ax.set_xlabel("Date")
    st.pyplot(fig)

# ----------------------------
# Row 2: Wind + Weather distribution
# ----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Wind Trend")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(year_df["date"], year_df["wind"], linewidth=1)
    ax.set_ylabel("km/h")
    ax.set_xlabel("Date")
    st.pyplot(fig)

with col4:
    st.subheader("Weather Distribution")
    weather_counts = year_df["weather"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(
        weather_counts,
        labels=weather_counts.index,
        autopct="%1.0f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

# ----------------------------
# Row 3: Precipitation + Monthly weather
# ----------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Monthly Precipitation")
    monthly_precip = year_df.groupby("month")["precipitation"].sum()
    fig, ax = plt.subplots(figsize=(6, 3))
    monthly_precip.plot(kind="bar", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("mm")
    st.pyplot(fig)

with col6:
    st.subheader("Monthly Weather Breakdown")
    monthly_weather = (
        year_df.groupby(["month", "weather"])
        .size()
        .unstack(fill_value=0)
    )
    st.bar_chart(monthly_weather, height=250)

# ----------------------------
# Raw data
# ----------------------------
st.subheader("Raw Data")
st.dataframe(year_df.reset_index(drop=True), height=250)
