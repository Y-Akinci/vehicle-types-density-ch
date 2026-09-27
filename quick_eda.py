import pandas as pd
import numpy as np
import seaborn as sns
from  pathlib import Path

data_dir = Path("data")

antrieb = pd.read_csv(
    data_dir / "Antriebsarten nach Gemeinden.csv",
    encoding="latin1"
)

einwohner = pd.read_csv(
    data_dir / "Einwohner nach Gemeinden.csv",
    encoding="latin1"
)
geo = pd.read_excel(data_dir / "Geographische_Kennzahlen.xlsx")

print("Antrieb Shape:", antrieb.shape)
print("Einwohner Shape:", einwohner.shape)
print("Geo Shape:", geo.shape)

# Missing Data
print("\n--- Missing Data (%) ---")

print("\nAntrieb:")
print((antrieb.isna().mean() * 100).round(2))

print("\nEinwohner:")
print((einwohner.isna().mean() * 100).round(2))

print("\nGeo:")
print((geo.isna().mean() * 100).round(2))


# Summary Statistics
print("\n--- Summary Statistics ---")

print("\nAntrieb:")
print(antrieb.describe())

print("\nEinwohner:")
print(einwohner.describe())

print("\nGeo:")
print(geo.describe())


# Notable Patterns / Correlations
print("\n--- Correlations ---")

print("\nAntrieb:")
print(antrieb.select_dtypes(include="number").corr().round(2))

print("\nEinwohner:")
print(einwohner.select_dtypes(include="number").corr().round(2))

print("\nGeo:")
print(geo.select_dtypes(include="number").corr().round(2))
