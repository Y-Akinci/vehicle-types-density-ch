import pandas as pd

from .clean import ANALYSE_ENDJAHR, ANALYSE_STARTJAHR


KANTON_ZUERICH = 1
ANZAHL_GEMEINDEN = 160
JAHRE = [str(jahr) for jahr in range(ANALYSE_STARTJAHR, ANALYSE_ENDJAHR + 1)]
DICHTEKLASSEN = ["tief", "mittel-tief", "mittel-hoch", "hoch"]

ANTRIEBSARTEN = {
    "Benzin": "Benzin",
    "Diesel": "Diesel",
    "Elektrisch": "Elektrisch",
    "Benzin-elektrisch: Normal-Hybrid": "Normal-Hybrid",
    "Diesel-elektrisch: Normal-Hybrid": "Normal-Hybrid",
    "Benzin-elektrisch: Plug-in-Hybrid": "Plug-in-Hybrid",
    "Diesel-elektrisch: Plug-in-Hybrid": "Plug-in-Hybrid",
    "Gas (mono- und bivalent)": "Sonstige",
    "Wasserstoff": "Sonstige",
    "Anderer": "Sonstige",
}
ANTRIEBS_SPALTEN = {
    "Benzin": "antrieb_benzin",
    "Diesel": "antrieb_diesel",
    "Elektrisch": "antrieb_elektrisch",
    "Normal-Hybrid": "antrieb_normal_hybrid",
    "Plug-in-Hybrid": "antrieb_plugin_hybrid",
    "Sonstige": "antrieb_sonstige",
}


def berechne_kennzahlen(verbunden: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Kennzahlen pro Gemeinde und Jahr sowie Summen pro Antriebsart für den Kanton Zürich."""
    zuerich = verbunden[verbunden["KTNR"] == KANTON_ZUERICH]
    if zuerich["gemeinde_nr"].nunique() != ANZAHL_GEMEINDEN:
        raise ValueError(f"Erwartet werden {ANZAHL_GEMEINDEN} Gemeinden im Kanton Zürich.")
    pkw = zuerich[zuerich["Fahrzeuggruppe"] == "Personenwagen"]

    # Fahrzeuge vom Wide- ins Long-Format, dann pro Gemeinde, Jahr und Antriebsart summieren
    fahrzeuge = pkw.melt(id_vars=["gemeinde_nr", "Treibstoff"], value_vars=JAHRE,
                         var_name="Jahr", value_name="Fahrzeuge")
    fahrzeuge["Jahr"] = fahrzeuge["Jahr"].astype(int)
    fahrzeuge["Antriebsart"] = fahrzeuge["Treibstoff"].map(ANTRIEBSARTEN)
    antriebe_breit = (
        fahrzeuge.pivot_table(index=["gemeinde_nr", "Jahr"], columns="Antriebsart",
                              values="Fahrzeuge", aggfunc="sum", fill_value=0)
        [list(ANTRIEBS_SPALTEN)]
        .rename(columns=ANTRIEBS_SPALTEN)
        .reset_index()
    )

    # Einwohner vom Wide- ins Long-Format
    stamm = zuerich.drop_duplicates("gemeinde_nr")
    einwohner = stamm.melt(id_vars=["gemeinde_nr", "GDENAME", "AREA_HA"],
                           value_vars=[f"einwohner_{jahr}" for jahr in JAHRE],
                           var_name="Jahr", value_name="einwohner")
    einwohner["Jahr"] = einwohner["Jahr"].str.removeprefix("einwohner_").astype(int)

    gemeinden = einwohner.merge(antriebe_breit, on=["gemeinde_nr", "Jahr"], validate="one_to_one")
    gemeinden = gemeinden.rename(columns={"GDENAME": "Gemeinde"})
    gemeinden["flaeche_km2"] = gemeinden["AREA_HA"] / 100
    gemeinden["einwohner_je_km2"] = gemeinden["einwohner"] / gemeinden["flaeche_km2"]
    gemeinden["pkw"] = gemeinden[list(ANTRIEBS_SPALTEN.values())].sum(axis=1)
    gemeinden["pkw_je_1000_einwohner"] = gemeinden["pkw"] / gemeinden["einwohner"] * 1000
    for spalte in ANTRIEBS_SPALTEN.values():
        gemeinden[f"{spalte}_je_1000_einwohner"] = gemeinden[spalte] / gemeinden["einwohner"] * 1000
        gemeinden[f"{spalte}_anteil"] = gemeinden[spalte] / gemeinden["pkw"] * 100

    # Feste Dichteklassen nach der Dichte im letzten Jahr, je ein Viertel der Gemeinden
    dichte = gemeinden[gemeinden["Jahr"] == ANALYSE_ENDJAHR].set_index("gemeinde_nr")["einwohner_je_km2"]
    klassen = pd.qcut(dichte, q=4, labels=DICHTEKLASSEN)
    gemeinden["dichteklasse"] = gemeinden["gemeinde_nr"].map(klassen)

    antriebe = fahrzeuge.groupby(["Jahr", "Antriebsart"], as_index=False)["Fahrzeuge"].sum()
    return gemeinden, antriebe


def ausreisser_finden(werte: pd.Series) -> pd.Series:
    """Gibt die Werte zurück, die nach der Boxplot-Regel (1.5 x IQR) auffallen."""
    q1, q3 = werte.quantile([0.25, 0.75])
    grenze = 1.5 * (q3 - q1)
    return werte[(werte < q1 - grenze) | (werte > q3 + grenze)]