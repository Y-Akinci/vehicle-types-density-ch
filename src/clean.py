import pandas as pd

EINWOHNER_REGION = "Kanton (-) / Bezirk (>>) / Gemeinde (......)"

# Geodaten: Gebiete ohne Einwohner
GEBIETE_OHNE_EINWOHNER = [2391, 5391, 5394]

def extract_gdenr(df: pd.DataFrame, name:str):
    """Trennt die Spalte 'name' ('1 Aeugst am Albis') in GDENR (int) und Gemeindename (str).

    Die ursprüngliche Spalte wird entfernt.
    """
    df = df.copy()

    df[['GDENR', 'Gemeindename']] = df[name].str.split(' ', n=1, expand=True)
    df['GDENR'] = df['GDENR'].astype(int)

    df = df.drop(columns=name)


    return df

def clean_antriebsarten(df: pd.DataFrame):
    """Cleaning des Antriebsarten DF: GDENR und Gemeindename trennen."""

    df = extract_gdenr(df, 'Gemeinde')

    return df

def clean_einwohner(df: pd.DataFrame):
    """Cleaning des Einwohner DF: nur Gemeinde-Zeilen, GDENR und Gemeindename trennen."""

    df = df[df[EINWOHNER_REGION].str.startswith('......')]
    df[EINWOHNER_REGION] = df[EINWOHNER_REGION].str.lstrip('.')

    df = extract_gdenr(df, EINWOHNER_REGION)

    df = df.reset_index(drop=True)

    return df

def clean_geo(df: pd.DataFrame):
    """Cleaning des Geo DF: Seen und Gebiete ohne Einwohner entfernen."""

    ist_see = df["GDENR"] >= 9000
    ohne_einwohner = df["GDENR"].isin(GEBIETE_OHNE_EINWOHNER)

    return df[~(ist_see | ohne_einwohner)].reset_index(drop=True)

if __name__ == "__main__":
    from load import load_antriebsarten, load_einwohner, load_geo

    antrieb = clean_antriebsarten(load_antriebsarten())
    einwohner = clean_einwohner(load_einwohner())
    geo = clean_geo(load_geo())

    print("Antriebsarten:", antrieb.shape, antrieb["GDENR"].nunique(), "Gemeinden")
    print("Einwohner:    ", einwohner.shape, einwohner["GDENR"].nunique(), "Gemeinden")
    print("Geo:          ", geo.shape)