import pandas as pd
import numpy as np
import seaborn as sns
import pathlib as Path

data_dir = Path("data")

antrieb = pd.read_csv(data_dir / "Antriebsarten nach Gemeinden.csv")
einwohner = pd.read_csv(data_dir / "Einwohner nach Gemeinden.csv")
geo = pd.read_excel(data_dir / "Geographische_Kennzahlen.xlsx")

antrieb.shape
einwohner.shape
geo.shape

antrieb.head()
einwohner.head()
geo.head()

