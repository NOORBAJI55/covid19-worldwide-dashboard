# 🌍 COVID-19 Worldwide Dashboard

An **interactive Streamlit dashboard** for exploring COVID-19 data across the globe. Track **cases, deaths, vaccinations**, and see the **COVID Performance Index (CPI)** for each country.

## 🚀 Features

- **Date Filter:** Explore COVID-19 data up to any selected date.
- **Country Filter:** Compare multiple countries side by side.
- **COVID Performance Index (CPI):** A custom metric combining vaccination rates, testing, fatality rate, hospital capacity, and government stringency.
- **Interactive Visualizations:**
  - Line chart of **total cases** over time
  - Area chart of **vaccination progress**
  - Bar chart of **deaths over time**
  - Choropleth map showing **CPI by country**
  - Table of **top 10 countries** by CPI
- **Responsive and user-friendly design** using Streamlit and Plotly.

** visual flow diagram of code**
┌─────────────────────────────┐
│     Load CSV Dataset        │
│ covid_worldwide_compact.csv │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│   Data Cleaning & Prep      │
│ - Drop rows with no country │
│ - Convert 'date' column     │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│  User Inputs in Streamlit   │
│ - Select date               │
│ - Select countries          │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Filter Dataset by Date      │
│ df_date_filtered = df[df.date <= selected_date] │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Get Latest Data per Country │
│ latest_df = latest record   │
│ per country (up to date)    │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Feature Engineering / CPI   │
│ - VAX: Vaccination rate     │
│ - TEST: Tests normalized    │
│ - CFR_norm: Fatality rate   │
│ - HOSP: Hospital beds       │
│ - STRG_balanced: Policy     │
│ - CPI = weighted sum        │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Filter Data by Selected     │
│ Countries (if any)          │
└─────────────┬──────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Visualizations in Streamlit │
│ - Line Chart: Cases         │
│ - Area Chart: Vaccination   │
│ - Bar Chart: Deaths         │
│ - Table: CPI & Metrics      │
│ - Map: CPI by Country       │
│ - Table: Top 10 CPI         │
└─────────────────────────────┘
