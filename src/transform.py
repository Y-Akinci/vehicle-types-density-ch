import pandas as pd


JAHRE = [str(jahr) for jahr in range(2010, 2025)]
DICHTEKLASSEN = ["tief", "mittel-tief", "mittel-hoch", "hoch"]

# Treibstoffe, die nicht vorkommen, werden zu "Andere"
ANTRIEBSARTEN = {
    "Elektrisch": "Elektro",
    "Benzin-elektrisch: Normal-Hybrid": "Hybrid",
    "Benzin-elektrisch: Plug-in-Hybrid": "Hybrid",
    "Diesel-elektrisch: Normal-Hybrid": "Hybrid",
    "Diesel-elektrisch: Plug-in-Hybrid": "Hybrid",
    "Benzin": "Benzin",
    "Diesel": "Diesel",
}


def personenwagen_long(df: pd.DataFrame) -> pd.DataFrame:
    """Personenwagen pro Gemeinde, Jahr und Antriebsart im Long-Format."""
    pw = df[df["Fahrzeuggruppe"] == "Personenwagen"]

    pw = pw.melt(
        id_vars=["gemeinde_nr", "Treibstoff"],
        value_vars=JAHRE,
        var_name="Jahr",
        value_name="Fahrzeuge",
    )
    pw["Jahr"] = pw["Jahr"].astype(int)
    pw["Antriebsart"] = pw["Treibstoff"].astype(str).map(ANTRIEBSARTEN).fillna("Andere")

    return pw.groupby(["gemeinde_nr", "Jahr", "Antriebsart"], as_index=False)["Fahrzeuge"].sum()


def gemeinden_long(df: pd.DataFrame) -> pd.DataFrame:
    """Einwohner, Fläche, Dichte und Dichteklasse pro Gemeinde und Jahr."""
    einwohner_spalten = [f"einwohner_{jahr}" for jahr in JAHRE]
    basis = ["gemeinde_nr", "GDENAME", "KTNAME", "AREA_HA"]

    gemeinden = df.drop_duplicates("gemeinde_nr")[basis + einwohner_spalten]
    gemeinden = gemeinden.melt(id_vars=basis, var_name="Jahr", value_name="Einwohner")
    gemeinden["Jahr"] = gemeinden["Jahr"].str.removeprefix("einwohner_").astype(int)

    gemeinden["Flaeche_km2"] = gemeinden["AREA_HA"] / 100
    gemeinden["Einwohnerdichte"] = gemeinden["Einwohner"] / gemeinden["Flaeche_km2"]

    # Feste Klassen nach der Dichte 2024, damit jede Gemeinde in allen Jahren in derselben Klasse bleibt
    dichte_2024 = gemeinden[gemeinden["Jahr"] == 2024].set_index("gemeinde_nr")["Einwohnerdichte"]
    klassen = pd.qcut(dichte_2024, q=4, labels=DICHTEKLASSEN)
    gemeinden["Dichteklasse"] = gemeinden["gemeinde_nr"].map(klassen)

    return (
        gemeinden
        .rename(columns={"GDENAME": "Gemeinde", "KTNAME": "Kanton"})
        .drop(columns="AREA_HA")
    )


def daten_transformieren(df: pd.DataFrame) -> pd.DataFrame:
    """Anteil jeder Antriebsart am Personenwagenbestand pro Gemeinde und Jahr."""
    pw = personenwagen_long(df)

    pw["Bestand"] = pw.groupby(["gemeinde_nr", "Jahr"])["Fahrzeuge"].transform("sum")
    pw = pw[pw["Bestand"] > 0].copy()
    pw["Anteil"] = pw["Fahrzeuge"] / pw["Bestand"] * 100

    return pw.merge(
        gemeinden_long(df),
        on=["gemeinde_nr", "Jahr"],
        how="left",
        validate="many_to_one",
    )