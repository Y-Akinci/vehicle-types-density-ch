import csv
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_raw_data(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    antrieb = pd.read_csv(data_dir / "Antriebsarten_nach_Gemeinden.csv", encoding="latin1", sep=",", quoting=csv.QUOTE_NONE)
    einwohner = pd.read_csv(data_dir / "Einwohner_nach_Gemeinden.csv", encoding="latin1", quoting=csv.QUOTE_NONE)
    geo = pd.read_csv(data_dir / "Geographische_Kennzahlen.csv", encoding="utf-8", sep=";")
    return antrieb, einwohner, geo

