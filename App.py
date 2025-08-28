import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime 

# Load dataset
# df = pd.read_csv("https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv")

# df = pd.read_csv("covid_worldwide_compact.csv")  # use this if u download the dataset

df = pd.read_csv("covid_worldwide_compact.csv", sep=",", engine="python")

# Drop rows with no country info
df = df.dropna(subset=["country"])

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -------------------- STREAMLIT APP --------------------
st.title("🌍 COVID-19 Worldwide Dashboard")
st.markdown("Interactive analysis of worldwide COVID-19 data with a unique **COVID Performance Index (CPI)**.")
st.image("https://cdn.pixabay.com/photo/2020/02/01/12/31/coronavirus-4810201_1280.jpg", width=1000)
# --- Date filter (TOP) ---
min_date = df["date"].min().date()
max_date = df["date"].max().date()

# ✅ Set default date as 18th April 2020
default_date = datetime.date(2020, 4, 18)
if default_date < min_date or default_date > max_date:
    default_date = max_date  # fallback if dataset doesn’t include Apr 18, 2020

selected_date = st.date_input(
    "📅 Select a Date (Data up to this day will be shown)",
    value=default_date,
    min_value=min_date,
    max_value=max_date
)

# Filter dataset by date
df_date_filtered = df[df["date"] <= pd.to_datetime(selected_date)]

# --- Sidebar Filters ---
countries = st.sidebar.multiselect(
    "🌍 Select Countries",
    options=sorted(df["country"].unique()),
    default=["India", "United States", "Brazil"],
    key="sidebar_countries",
    
)
st.sidebar.image(
    "https://cdn.pixabay.com/animation/2022/08/06/11/56/11-56-57-681_512.gif",
    width=1000
)

# --- Get latest available data per country (up to selected date) ---
latest_df = df_date_filtered.sort_values("date").groupby("country").tail(1)
latest_df.fillna(0, inplace=True)

# --- Feature Engineering for CPI ---
latest_df["VAX"] = latest_df["people_fully_vaccinated_per_hundred"] / 100
max_tests = latest_df["total_tests_per_thousand"].max()
latest_df["TEST"] = latest_df["total_tests_per_thousand"] / max_tests
latest_df["CFR"] = latest_df["total_deaths"] / latest_df["total_cases"]
latest_df["CFR"] = latest_df["CFR"].replace([np.inf, -np.inf], 0).fillna(0)
latest_df["CFR_norm"] = latest_df["CFR"] / latest_df["CFR"].max()
max_hosp = latest_df["hospital_beds_per_thousand"].max()
latest_df["HOSP"] = latest_df["hospital_beds_per_thousand"] / max_hosp
latest_df["STRG_balanced"] = 1 - (abs(latest_df["stringency_index"] - 50) / 50)
latest_df["STRG_balanced"] = latest_df["STRG_balanced"].clip(0, 1)

latest_df["CPI"] = (
    0.30 * latest_df["VAX"] +
    0.20 * latest_df["TEST"] +
    0.20 * (1 - latest_df["CFR_norm"]) +
    0.20 * latest_df["HOSP"] +
    0.10 * latest_df["STRG_balanced"]
) * 100

# Filtered data for visualization
if countries:
    filtered_df = df_date_filtered[df_date_filtered["country"].isin(countries)]
    filtered_latest = latest_df[latest_df["country"].isin(countries)]
else:
    filtered_df = df_date_filtered
    filtered_latest = latest_df

# 📈 Line Chart - Cases Trend
st.subheader("📈 COVID-19 Cases Over Time")
fig_cases = px.line(filtered_df, x="date", y="total_cases", color="country", title="Total Cases Over Time")
st.plotly_chart(fig_cases, use_container_width=True)


# 💉 Vaccination Progress
st.subheader("💉 Vaccination Progress")
fig_vax = px.area(filtered_df, x="date", y="people_fully_vaccinated_per_hundred", color="country",
                  title="Vaccination Coverage (% of Population Fully Vaccinated)")
st.plotly_chart(fig_vax, use_container_width=True)

# ⚰️ Deaths Over Time
st.subheader("⚰️ COVID-19 Deaths Over Time")
fig_deaths = px.bar(filtered_df, x="date", y="total_deaths", color="country", title="Total Deaths Over Time")
st.plotly_chart(fig_deaths, use_container_width=True)

# 📊 Selected Countries CPI
st.subheader("📊 Selected Countries CPI Breakdown")
st.dataframe(filtered_latest[["country", "CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"]].round(3))

# 🧮 COVID Performance Index Map
st.subheader("🧮 COVID Performance Index (CPI)")
fig_cpi = px.choropleth(
    latest_df,
    locations="country",
    locationmode="country names",
    color="CPI",
    hover_name="country",
    hover_data=["CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"],
    color_continuous_scale="RdYlGn",
    title=f"COVID Performance Index (CPI) by Country as of {selected_date}"
)
st.plotly_chart(fig_cpi, use_container_width=True)

# 🏆 Top 10 Countries
st.subheader("🏆 Top 10 Countries by CPI")
top10 = latest_df.sort_values("CPI", ascending=False).head(10)[["country", "CPI"]]
st.table(top10)
