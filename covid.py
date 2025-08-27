# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import plotly.express as px

# # Load dataset
# @st.cache_data
# def load_data():
#     df = pd.read_csv("covid_worldwide_compact.csv")
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     df = df[df['continent'].notna()]  # drop aggregates
#     df = df.sort_values(['country','date'])
#     latest = df.drop_duplicates(subset=['country'], keep='last').reset_index(drop=True)

#     # Fill NaNs
#     numeric_cols = latest.select_dtypes(include=['number']).columns
#     latest[numeric_cols] = latest[numeric_cols].fillna(0)

#     # Derived metric
#     latest['CFR_percent'] = np.where(latest['total_cases']>0,
#                                      (latest['total_deaths']/latest['total_cases'])*100, 0.0)
#     return df, latest

# df, latest = load_data()

# # ----------------- Streamlit UI ----------------- #
# st.title("🌍 COVID-19 Worldwide Dashboard")
# st.markdown("Interactive global analysis with **COVID Performance Index (coming soon)**.")

# # --- Global overview ---
# global_cases = int(latest['total_cases'].sum())
# global_deaths = int(latest['total_deaths'].sum())
# global_vax_pct = round((latest['people_fully_vaccinated'].sum() / latest['population'].sum()) * 100, 2)

# col1, col2, col3 = st.columns(3)
# col1.metric("Total Cases", f"{global_cases:,}")
# col2.metric("Total Deaths", f"{global_deaths:,}")
# col3.metric("Global Vaccination %", f"{global_vax_pct}%")

# # --- Top 10 countries selection ---
# metric = st.selectbox(
#     "Choose metric for Top 10 chart:",
#     ["total_cases_per_million", "total_deaths_per_million", "people_fully_vaccinated_per_hundred"]
# )

# top10 = latest.sort_values(metric, ascending=False).head(10)

# fig = px.bar(top10, x="country", y=metric, color="country",
#              title=f"Top 10 Countries by {metric.replace('_',' ').title()}")
# st.plotly_chart(fig, use_container_width=True)

# # --- Country Drilldown ---
# country = st.selectbox("Select a country for detailed timeline:", latest['country'].unique())
# country_df = df[df['country'] == country]

# fig2 = px.line(country_df, x="date", y="total_cases", title=f"{country} - Total Cases Over Time")
# st.plotly_chart(fig2, use_container_width=True)

# fig3 = px.line(country_df, x="date", y="people_fully_vaccinated_per_hundred",
#                title=f"{country} - Vaccination % Over Time")
# st.plotly_chart(fig3, use_container_width=True)

# # --- Future: CPI Map ---
# st.info("🧮 COVID Performance Index map will be added in next step!")


# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # Load dataset
# df = pd.read_csv("covid_worldwide_compact.csv")

# # Drop rows with no country info
# df = df.dropna(subset=["country"])

# # Get the latest available data per country
# latest_df = df.sort_values("date").groupby("country").tail(1)

# # --- Handle missing values ---
# latest_df.fillna(0, inplace=True)

# # --- Feature Engineering for CPI ---
# # Vaccination coverage
# latest_df["VAX"] = latest_df["people_fully_vaccinated_per_hundred"] / 100

# # Testing capacity
# max_tests = latest_df["total_tests_per_thousand"].max()
# latest_df["TEST"] = latest_df["total_tests_per_thousand"] / max_tests

# # Case Fatality Rate (CFR)
# latest_df["CFR"] = latest_df["total_deaths"] / latest_df["total_cases"]
# latest_df["CFR"] = latest_df["CFR"].replace([np.inf, -np.inf], 0).fillna(0)
# latest_df["CFR_norm"] = latest_df["CFR"] / latest_df["CFR"].max()

# # Healthcare capacity
# max_hosp = latest_df["hospital_beds_per_thousand"].max()
# latest_df["HOSP"] = latest_df["hospital_beds_per_thousand"] / max_hosp

# # Government response (balanced: ideal around 50)
# latest_df["STRG_balanced"] = 1 - (abs(latest_df["stringency_index"] - 50) / 50)
# latest_df["STRG_balanced"] = latest_df["STRG_balanced"].clip(0, 1)

# # --- Final CPI Score ---
# latest_df["CPI"] = (
#     0.30 * latest_df["VAX"] +
#     0.20 * latest_df["TEST"] +
#     0.20 * (1 - latest_df["CFR_norm"]) +
#     0.20 * latest_df["HOSP"] +
#     0.10 * latest_df["STRG_balanced"]
# ) * 100

# # --- Streamlit App ---
# st.title("🧮 COVID Performance Index (CPI) Dashboard")
# st.markdown("A holistic score (0-100) that measures how well each country handled COVID-19 based on vaccines, testing, healthcare, and response.")

# # Sidebar
# continent_filter = st.sidebar.selectbox("🌍 Select Continent", options=["All"] + list(latest_df["continent"].dropna().unique()))

# if continent_filter != "All":
#     plot_df = latest_df[latest_df["continent"] == continent_filter]
# else:
#     plot_df = latest_df.copy()

# # Choropleth Map
# fig = px.choropleth(
#     plot_df,
#     locations="country",
#     locationmode="country names",
#     color="CPI",
#     hover_name="country",
#     hover_data=["CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"],
#     color_continuous_scale="RdYlGn",
#     title="COVID Performance Index (CPI) by Country"
# )

# st.plotly_chart(fig, use_container_width=True)

# # Top 10 Countries
# st.subheader("🏆 Top 10 Countries by CPI")
# top10 = plot_df.sort_values("CPI", ascending=False).head(10)[["country", "CPI"]]
# st.table(top10)
# # Bottom 10 Countries
# st.subheader("🔻 Bottom 10 Countries by CPI")


# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # Load dataset
# df = pd.read_csv("covid_worldwide_compact.csv")

# # Drop rows with no country info
# df = df.dropna(subset=["country"])



# # --- Sidebar Filters ---
# countries = st.sidebar.multiselect("🌍 Select Countries", options=sorted(df["country"].unique()), default=["India", "United States", "Brazil"])

# # --- Get latest available data per country ---
# latest_df = df.sort_values("date").groupby("country").tail(1)
# latest_df.fillna(0, inplace=True)

# # --- Feature Engineering for CPI ---
# latest_df["VAX"] = latest_df["people_fully_vaccinated_per_hundred"] / 100
# max_tests = latest_df["total_tests_per_thousand"].max()
# latest_df["TEST"] = latest_df["total_tests_per_thousand"] / max_tests
# latest_df["CFR"] = latest_df["total_deaths"] / latest_df["total_cases"]
# latest_df["CFR"] = latest_df["CFR"].replace([np.inf, -np.inf], 0).fillna(0)
# latest_df["CFR_norm"] = latest_df["CFR"] / latest_df["CFR"].max()
# max_hosp = latest_df["hospital_beds_per_thousand"].max()
# latest_df["HOSP"] = latest_df["hospital_beds_per_thousand"] / max_hosp
# latest_df["STRG_balanced"] = 1 - (abs(latest_df["stringency_index"] - 50) / 50)
# latest_df["STRG_balanced"] = latest_df["STRG_balanced"].clip(0, 1)

# latest_df["CPI"] = (
#     0.30 * latest_df["VAX"] +
#     0.20 * latest_df["TEST"] +
#     0.20 * (1 - latest_df["CFR_norm"]) +
#     0.20 * latest_df["HOSP"] +
#     0.10 * latest_df["STRG_balanced"]
# ) * 100

# # -------------------- STREAMLIT APP --------------------
# st.title("🌍 COVID-19 Worldwide Dashboard")
# st.markdown("Interactive analysis of worldwide COVID-19 data with a unique **COVID Performance Index (CPI)**.")

# # Filtered data for visualization
# if countries:
#     filtered_df = df[df["country"].isin(countries)]
#     filtered_latest = latest_df[latest_df["country"].isin(countries)]
# else:
#     filtered_df = df
#     filtered_latest = latest_df

# # 📈 Line Chart - Cases Trend
# st.subheader("📈 COVID-19 Cases Over Time")
# fig_cases = px.line(filtered_df, x="date", y="total_cases", color="country", title="Total Cases Over Time")
# st.plotly_chart(fig_cases, use_container_width=True)

# # 💉 Vaccination Progress
# st.subheader("💉 Vaccination Progress")
# fig_vax = px.line(filtered_df, x="date", y="people_fully_vaccinated_per_hundred", color="country",
#                   title="Vaccination Coverage (% of Population Fully Vaccinated)")
# st.plotly_chart(fig_vax, use_container_width=True)

# # ⚰️ Deaths Over Time
# st.subheader("⚰️ COVID-19 Deaths Over Time")
# fig_deaths = px.line(filtered_df, x="date", y="total_deaths", color="country", title="Total Deaths Over Time")
# st.plotly_chart(fig_deaths, use_container_width=True)

# # 📊 Selected Countries CPI
# st.subheader("📊 Selected Countries CPI Breakdown")
# st.dataframe(filtered_latest[["country", "CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"]].round(3))

# # 🧮 COVID Performance Index Map
# st.subheader("🧮 COVID Performance Index (CPI)")
# fig_cpi = px.choropleth(
#     latest_df,
#     locations="country",
#     locationmode="country names",
#     color="CPI",
#     hover_name="country",
#     hover_data=["CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"],
#     color_continuous_scale="RdYlGn",
#     title="COVID Performance Index (CPI) by Country"
# )
# st.plotly_chart(fig_cpi, use_container_width=True)

# # 🏆 Top 10 Countries
# st.subheader("🏆 Top 10 Countries by CPI")
# top10 = latest_df.sort_values("CPI", ascending=False).head(10)[["country", "CPI"]]
# st.table(top10)



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import numpy as np

# # -----------------------------
# # Load Data
# # -----------------------------
# @st.cache_data
# def load_data():
#     df = pd.read_csv("covid_worldwide_compact.csv")
#     df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
#     # Drop completely empty rows
#     df = df.dropna(how="all")
    
#     # Fill important metrics
#     fill_values = {
#         "total_cases": 0,
#         "new_cases": 0,
#         "total_deaths": 0,
#         "new_deaths": 0,
#         "total_tests": 0,
#         "people_vaccinated": 0,
#         "people_fully_vaccinated": 0,
#         "hospital_beds_per_thousand": df["hospital_beds_per_thousand"].mean(),
#         "stringency_index": df["stringency_index"].mean()
#     }
#     df = df.fillna(fill_values)

#     # Interpolate for missing values within each country
#     df = df.groupby("country").apply(lambda g: g.interpolate(method="linear")).reset_index(drop=True)

#     return df

# df = load_data()

# # -----------------------------
# # Sidebar Filters
# # -----------------------------
# st.sidebar.header("Filters")

# countries = df["country"].dropna().unique()
# selected_country = st.sidebar.selectbox("Choose a Country", sorted(countries))

# # Date range filter
# min_date = df["date"].min().date()
# max_date = df["date"].max().date()

# date_range = st.sidebar.date_input(
#     "Choose a date range",
#     [min_date, max_date],
#     min_value=min_date,
#     max_value=max_date
# )

# if len(date_range) == 2:
#     start_date = pd.to_datetime(date_range[0])
#     end_date = pd.to_datetime(date_range[1])
#     mask = (df["country"] == selected_country) & (df["date"].between(start_date, end_date))
#     filtered_data = df[mask]
# else:
#     filtered_data = df[df["country"] == selected_country]

# # -----------------------------
# # Main App
# # -----------------------------
# st.title("🌍 COVID-19 Worldwide Dashboard")

# st.markdown(f"### 📊 Country Selected: {selected_country}")

# # Total Cases Over Time
# fig_cases = px.line(filtered_data, x="date", y="total_cases", title=f"Total Cases in {selected_country}")
# st.plotly_chart(fig_cases, use_container_width=True)

# # Total Deaths Over Time
# fig_deaths = px.line(filtered_data, x="date", y="total_deaths", title=f"Total Deaths in {selected_country}")
# st.plotly_chart(fig_deaths, use_container_width=True)

# # Vaccinations Over Time
# fig_vax = px.line(filtered_data, x="date", y="people_vaccinated", title=f"People Vaccinated in {selected_country}")
# st.plotly_chart(fig_vax, use_container_width=True)

# # -----------------------------
# # COVID Performance Index (CPI)
# # -----------------------------
# st.subheader("🧮 COVID Performance Index (CPI)")

# def compute_cpi(data):
#     data["CPI"] = (
#         (1 / (1 + data["total_cases"])) * 0.3 +
#         (1 / (1 + data["total_deaths"])) * 0.3 +
#         (data["people_vaccinated"].fillna(0) / (data["people_vaccinated"].max() + 1)) * 0.2 +
#         (data["hospital_beds_per_thousand"].fillna(0) / (data["hospital_beds_per_thousand"].max() + 1)) * 0.1 +
#         (data["stringency_index"].fillna(0) / 100) * 0.1
#     )
#     return data

# df = compute_cpi(df)

# # Average CPI per country
# cpi_by_country = df.groupby("country")["CPI"].mean().reset_index().sort_values(by="CPI", ascending=False)

# # Show Top 10 Countries by CPI (at bottom)
# st.subheader("🏆 Top 10 Countries by CPI")
# fig_cpi = px.bar(cpi_by_country.head(10), x="country", y="CPI", title="Top 10 Performing Countries")
# st.plotly_chart(fig_cpi, use_container_width=True)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import datetime 

# # Load dataset
# df = pd.read_csv("covid_worldwide_compact.csv")

# # Drop rows with no country info
# df = df.dropna(subset=["country"])

# # Convert date column
# df["date"] = pd.to_datetime(df["date"], errors="coerce")

# # -------------------- STREAMLIT APP --------------------
# st.title("🌍 COVID-19 Worldwide Dashboard")
# st.markdown("Interactive analysis of worldwide COVID-19 data with a unique **COVID Performance Index (CPI)**.")

# # --- Date filter (TOP) ---
# min_date = df["date"].min().date()
# max_date = df["date"].max().date()

# selected_date = st.date_input(
#     "📅 Select a Date (Data up to this day will be shown)",
#     value=max_date,
#     min_value=min_date,
#     max_value=max_date
# )

# # Filter dataset by date
# df_date_filtered = df[df["date"] <= pd.to_datetime(selected_date)]

# # --- Sidebar Filters ---
# # countries = st.sidebar.multiselect("🌍 Select Countries", options=sorted(df["country"].unique()), default=["India", "United States", "Brazil"])
# # --- Sidebar Filters ---
# countries = st.sidebar.multiselect(
#     "🌍 Select Countries",
#     options=sorted(df["country"].unique()),
#     default=["India", "United States", "Brazil"],
#     key="sidebar_countries"
# )


# # --- Get latest available data per country (up to selected date) ---
# latest_df = df_date_filtered.sort_values("date").groupby("country").tail(1)
# latest_df.fillna(0, inplace=True)

# # --- Feature Engineering for CPI ---
# latest_df["VAX"] = latest_df["people_fully_vaccinated_per_hundred"] / 100
# max_tests = latest_df["total_tests_per_thousand"].max()
# latest_df["TEST"] = latest_df["total_tests_per_thousand"] / max_tests
# latest_df["CFR"] = latest_df["total_deaths"] / latest_df["total_cases"]
# latest_df["CFR"] = latest_df["CFR"].replace([np.inf, -np.inf], 0).fillna(0)
# latest_df["CFR_norm"] = latest_df["CFR"] / latest_df["CFR"].max()
# max_hosp = latest_df["hospital_beds_per_thousand"].max()
# latest_df["HOSP"] = latest_df["hospital_beds_per_thousand"] / max_hosp
# latest_df["STRG_balanced"] = 1 - (abs(latest_df["stringency_index"] - 50) / 50)
# latest_df["STRG_balanced"] = latest_df["STRG_balanced"].clip(0, 1)

# latest_df["CPI"] = (
#     0.30 * latest_df["VAX"] +
#     0.20 * latest_df["TEST"] +
#     0.20 * (1 - latest_df["CFR_norm"]) +
#     0.20 * latest_df["HOSP"] +
#     0.10 * latest_df["STRG_balanced"]
# ) * 100

# # Filtered data for visualization
# if countries:
#     filtered_df = df_date_filtered[df_date_filtered["country"].isin(countries)]
#     filtered_latest = latest_df[latest_df["country"].isin(countries)]
# else:
#     filtered_df = df_date_filtered
#     filtered_latest = latest_df


# # 📈 Line Chart - Cases Trend
# st.subheader("📈 COVID-19 Cases Over Time")
# fig_cases = px.line(filtered_df, x="date", y="total_cases", color="country", title="Total Cases Over Time")
# st.plotly_chart(fig_cases, use_container_width=True)

# # 💉 Vaccination Progress
# st.subheader("💉 Vaccination Progress")
# fig_vax = px.line(filtered_df, x="date", y="people_fully_vaccinated_per_hundred", color="country",
#                   title="Vaccination Coverage (% of Population Fully Vaccinated)")
# st.plotly_chart(fig_vax, use_container_width=True)

# # ⚰️ Deaths Over Time
# st.subheader("⚰️ COVID-19 Deaths Over Time")
# fig_deaths = px.line(filtered_df, x="date", y="total_deaths", color="country", title="Total Deaths Over Time")
# st.plotly_chart(fig_deaths, use_container_width=True)

# # 📊 Selected Countries CPI
# st.subheader("📊 Selected Countries CPI Breakdown")
# st.dataframe(filtered_latest[["country", "CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"]].round(3))

# # 🧮 COVID Performance Index Map
# st.subheader("🧮 COVID Performance Index (CPI)")
# fig_cpi = px.choropleth(
#     latest_df,
#     locations="country",
#     locationmode="country names",
#     color="CPI",
#     hover_name="country",
#     hover_data=["CPI", "VAX", "TEST", "CFR", "HOSP", "STRG_balanced"],
#     color_continuous_scale="RdYlGn",
#     title=f"COVID Performance Index (CPI) by Country as of {selected_date}"
# )
# st.plotly_chart(fig_cpi, use_container_width=True)

# # 🏆 Top 10 Countries
# st.subheader("🏆 Top 10 Countries by CPI")
# top10 = latest_df.sort_values("CPI", ascending=False).head(10)[["country", "CPI"]]
# st.table(top10)





import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime 

# Load dataset
# df = pd.read_csv("covid_worldwide_compact.csv")
df = pd.read_csv("https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv")

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

