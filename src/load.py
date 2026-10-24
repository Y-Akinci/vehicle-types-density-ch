import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

def _read_bfs_csv(path: Path) -> pd.DataFrame:
    """Liest eine BFS-CSV, jede Zeile steht in Anführungszeichen."""

    df = pd.read_csv(path, sep=',', encoding='latin1')

    # CSV formatieren
    df_split = df.iloc[:, 0].str.split(',', expand=True)

    # Spaltennamen setzen
    spaltennamen = df.columns[0].split(',')
    df_split.columns = spaltennamen

    # Anführungszeichen entfernen
    df_split.columns = df_split.columns.str.strip('"')
    for col in df_split.columns:
        df_split[col]= df_split[col].str.strip('"')

    return df_split


def load_antriebsarten(path: Path = RAW_DIR / "Antriebsarten_nach_Gemeinden.csv") -> pd.DataFrame:
    """Liest das CSV Antriebsarten nach Gemeinden ein."""

    # CSV einlesen
    df = _read_bfs_csv(path)

    # Datentypen ändern
    df = df.astype({'Fahrzeuggruppe': 'category', 'Treibstoff': 'category'})

    # Jahresspalten in int umwandeln
    jahre = df.columns[3:]
    df[jahre] = df[jahre].astype(int)

    return df


def load_einwohner(path: Path = RAW_DIR / "Einwohner_nach_Gemeinden.csv") -> pd.DataFrame:
    """Liest das CSV Einwohner nach Gemeinden ein."""

    # CSV einlesen
    df = _read_bfs_csv(path)

    # Datentypen ändern
    df = df.astype({'Jahr': int, 'Bevölkerungstyp': 'category', 'Staatsangehörigkeit - Total': int})

    return df


def load_geo(path: Path = RAW_DIR / "Geographische_Kennzahlen.csv") -> pd.DataFrame:
    """Liest das CSV Geographische Kennzahlen ein."""

    # CSV einlesen
    df = pd.read_csv(path, sep=';')

    # Datentypen ändern
    df = df.astype({'KTNAME': 'category'})

    return df