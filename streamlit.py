import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Weather Dashboard", layout="wide")

PLOT_HEIGHT = 270  # compact height like matplotlib figsize=(6,3)

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("weather.csv")
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
c5.metric("Max Wind (km/h)", round(year_df["wind"].max(), 1))
c6.metric("Min Wind (km/h)", round(year_df["wind"].min(), 1))

st.divider()

# ----------------------------
# Row 1: Temperature
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperature Trend")
    fig = px.line(
        year_df,
        x="date",
        y="temperature",
        labels={"date": "Date", "temperature": "Temperature (°C)"}
    )
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Temperature Dot Plot (Hover for Date)")
    fig = px.scatter(
        year_df,
        x="date",
        y="temperature",
        hover_data=["date", "temperature"],
        labels={"date": "Date", "temperature": "Temperature (°C)"}
    )
    fig.update_traces(marker=dict(size=6, opacity=0.6))
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Row 2: Wind + Weather distribution
# ----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Wind Trend")
    fig = px.line(
        year_df,
        x="date",
        y="wind",
        labels={"date": "Date", "wind": "Wind Speed (km/h)"}
    )
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Weather Distribution")
    wc = year_df["weather"].value_counts().reset_index()
    wc.columns = ["weather", "count"]
    fig = px.pie(wc, names="weather", values="count")
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Row 3: Precipitation + Monthly weather
# ----------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Monthly Precipitation")
    mp = year_df.groupby("month", as_index=False)["precipitation"].sum()
    fig = px.bar(
        mp,
        x="month",
        y="precipitation",
        labels={"month": "Month", "precipitation": "Precipitation (mm)"}
    )
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Monthly Weather Breakdown")
    mw = (
        year_df.groupby(["month", "weather"])
        .size()
        .reset_index(name="count")
    )
    fig = px.bar(
        mw,
        x="month",
        y="count",
        color="weather",
        barmode="stack",
        labels={"month": "Month", "count": "Days"}
    )
    fig.update_layout(height=PLOT_HEIGHT, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Raw data
# ----------------------------
st.subheader("Raw Data")
st.dataframe(year_df.reset_index(drop=True), height=300)
