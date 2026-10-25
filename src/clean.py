import pandas as pd


ANALYSE_STARTJAHR = 2010
ANALYSE_ENDJAHR = 2024

# Amtlicher Gemeindestand 01.01.2026 (alte BFS-Nummer -> aktuelle BFS-Nummer).
BFS_MAPPING_2026 = {
    700: 6831,    # Moutier
    1057: 1065,   # Honau -> Root
    2016: 2056,   # Fétigny -> Fétigny-Ménières
    2027: 2056,   # Ménières -> Fétigny-Ménières
    2061: 2097,   # Auboranges -> Rue
    2066: 2097,   # Chapelle (Glâne) -> Rue
    2072: 2097,   # Ecublens (FR) -> Rue
    2089: 2097,   # Montet (Glâne) -> Rue
    2200: 2239,   # Grolley -> Grolley-Ponthaux
    2217: 2239,   # Ponthaux -> Grolley-Ponthaux
    2278: 2262,   # Ulmiz -> Gurmels
    2520: 2535,   # Halten -> Drei Höfe
    2529: 2535,   # Oekingen -> Drei Höfe
    3932: 3901,   # Tschiertschen-Praden -> Chur
    4122: 4095,   # Villnachern -> Brugg
    5064: 5073,   # Bodio -> Giornico
    5078: 5079,   # Prato (Leventina) -> Quinto
    5146: 5395,   # Astano -> Lema
    5149: 5395,   # Bedigliora -> Lema
    5181: 5395,   # Curio -> Lema
    5200: 5395,   # Miglieglia -> Lema
    5207: 5395,   # Novaggio -> Lema
    6453: 6513,   # Enges -> Laténa
    6454: 6513,   # Hauterive (NE) -> Laténa
    6459: 6513,   # Saint-Blaise -> Laténa
    6461: 6513,   # La Tène -> Laténa
}


def anfuehrungszeichen_entfernen(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.replace('"', "", regex=False)
    return df.replace('"', "", regex=True)


def bfs_nummern_hinzufügen(antrieb, einwohner, geo):
    antrieb = antrieb.copy()
    einwohner = einwohner.copy()
    geo = geo.copy()

    # Beispiel: "1 Aeugst am Albis"
    antrieb["gemeinde_nr"] = (
        antrieb["Gemeinde"]
        .str.extract(r"^(\d+)", expand=False)
        .astype("Int64")
    )
    antrieb["Gemeinde"] = (
        antrieb["Gemeinde"]
        .str.replace(r"^\d+\s*", "", regex=True)
        .str.strip()
    )

    gemeinde_spalte = "Kanton (-) / Bezirk (>>) / Gemeinde (......)"
    einwohner["gemeinde_nr"] = (
        einwohner[gemeinde_spalte]
        .str.extract(r"^\.{6}(\d+)", expand=False)
        .astype("Int64")
    )

    # GDENR ist in der Geografiedatei bereits die BFS-Nummer.
    geo["gemeinde_nr"] = (
        pd.to_numeric(geo["GDENR"], errors="coerce")
        .astype("Int64")
    )

    return antrieb, einwohner, geo


def gemeindestand_vereinheitlichen(antrieb, einwohner, geo):
    antrieb = antrieb.copy()
    einwohner = einwohner.copy()

    antrieb["gemeinde_nr"] = antrieb["gemeinde_nr"].replace(BFS_MAPPING_2026)
    einwohner["gemeinde_nr"] = einwohner["gemeinde_nr"].replace(BFS_MAPPING_2026)

    gemeindenamen = geo.set_index("gemeinde_nr")["GDENAME"]
    antrieb["Gemeinde"] = (
        antrieb["gemeinde_nr"]
        .map(gemeindenamen)
        .fillna(antrieb["Gemeinde"])
    )

    jahr_spalten = [
        spalte
        for spalte in antrieb.columns
        if str(spalte).isdigit()
        and ANALYSE_STARTJAHR <= int(spalte) <= ANALYSE_ENDJAHR
    ]
    antrieb[jahr_spalten] = antrieb[jahr_spalten].apply(
        pd.to_numeric,
        errors="coerce",
    )
    if antrieb[jahr_spalten].isna().any().any():
        raise ValueError("Antrieb enthält fehlende oder ungültige Jahreswerte.")

    gruppen = ["gemeinde_nr", "Gemeinde", "Fahrzeuggruppe", "Treibstoff"]
    antrieb = (
        antrieb
        .groupby(gruppen, as_index=False, dropna=False)[jahr_spalten]
        .sum()
    )
    antrieb = antrieb[
        ["Gemeinde", "Fahrzeuggruppe", "Treibstoff", *jahr_spalten, "gemeinde_nr"]
    ]

    return antrieb, einwohner, geo


def einwohner_umformen(einwohner: pd.DataFrame) -> pd.DataFrame:
    einwohner = einwohner.copy()
    einwohner["Jahr"] = pd.to_numeric(einwohner["Jahr"], errors="coerce")
    einwohner["Staatsangehörigkeit - Total"] = pd.to_numeric(
        einwohner["Staatsangehörigkeit - Total"],
        errors="coerce",
    )
    if einwohner.loc[einwohner["gemeinde_nr"].notna(), "Jahr"].isna().any():
        raise ValueError("Einwohner enthält fehlende oder ungültige Jahre.")
    einwohner = einwohner[
        einwohner["Jahr"].between(ANALYSE_STARTJAHR, ANALYSE_ENDJAHR)
    ]
    einwohner = einwohner.dropna(subset=["gemeinde_nr"])
    if einwohner["Staatsangehörigkeit - Total"].isna().any():
        raise ValueError("Einwohner enthält fehlende oder ungültige Zahlen.")

    return (
        einwohner
        .pivot_table(
            index="gemeinde_nr",
            columns="Jahr",
            values="Staatsangehörigkeit - Total",
            aggfunc="sum",
        )
        .rename(columns=lambda jahr: f"einwohner_{int(jahr)}")
        .rename_axis(columns=None)
        .reset_index()
    )


def daten_bereinigen(antrieb, einwohner, geo):
    antrieb = anfuehrungszeichen_entfernen(antrieb)
    einwohner = anfuehrungszeichen_entfernen(einwohner)
    geo = anfuehrungszeichen_entfernen(geo)

    antrieb, einwohner, geo = bfs_nummern_hinzufügen(
        antrieb,
        einwohner,
        geo,
    )
    antrieb, einwohner, geo = gemeindestand_vereinheitlichen(
        antrieb,
        einwohner,
        geo,
    )
    einwohner = einwohner_umformen(einwohner)

    return antrieb, einwohner, geo
