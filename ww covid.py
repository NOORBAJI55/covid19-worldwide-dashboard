import pandas as pd

url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

# Read and save locally
df = pd.read_csv(url)
df.to_csv("covid_worldwide_compact.csv", index=False)

print("CSV saved as covid_worldwide_compact.csv")
