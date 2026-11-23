"""Gemeindewerte für die Zürcher Fahrzeuganalyse berechnen."""

import pandas as pd

from .clean import ANALYSE_ENDJAHR, ANALYSE_STARTJAHR


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


def _vorbereiten(verbunden: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Liefere die Personenwagen und die Gemeindedaten des Kantons Zürich."""
    zuerich = verbunden[verbunden["KTNR"] == 1]
    if zuerich["gemeinde_nr"].nunique() != 160:
        raise ValueError("Erwartet werden 160 politische Gemeinden im Kanton Zürich.")

    pkw = zuerich[zuerich["Fahrzeuggruppe"] == "Personenwagen"].copy()
    unbekannt = set(pkw["Treibstoff"]) - set(ANTRIEBSARTEN) - {"Ohne Motor"}
    if unbekannt:
        raise ValueError(f"Unbekannte Antriebsarten: {sorted(unbekannt)}")
    pkw["Antriebsart"] = pkw["Treibstoff"].map(ANTRIEBSARTEN)

    einwohner_spalten = [f"einwohner_{jahr}" for jahr in range(ANALYSE_STARTJAHR, ANALYSE_ENDJAHR + 1)]
    stamm = (
        zuerich[["gemeinde_nr", "GDENAME", "AREA_HA", *einwohner_spalten]]
        .drop_duplicates("gemeinde_nr")
        .set_index("gemeinde_nr")
    )
    zahlen = stamm[["AREA_HA", *einwohner_spalten]]
    if zahlen.isna().any().any() or (zahlen <= 0).any().any():
        raise ValueError("Gemeindeflächen und Einwohnerzahlen müssen vollständig und positiv sein.")
    return pkw, stamm


def _jahr_berechnen(pkw: pd.DataFrame, stamm: pd.DataFrame, jahr: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Zähle PKW je Antrieb und berechne Dichte und Quoten pro Gemeinde."""
    einwohner = stamm[f"einwohner_{jahr}"]
    flaeche_km2 = stamm["AREA_HA"] / 100
    antriebe = (
        pkw.groupby(["gemeinde_nr", "Antriebsart"])[str(jahr)]
        .sum()
        .unstack(fill_value=0)
        .reindex(index=stamm.index, columns=ANTRIEBS_SPALTEN, fill_value=0)
    )
    # Jede Zeile der Antriebstabelle gehört zur gleichen Gemeinde wie im Stamm.
    werte = pd.DataFrame(index=stamm.index)
    werte["Gemeinde"] = stamm["GDENAME"]
    werte["Jahr"] = jahr
    werte["flaeche_km2"] = flaeche_km2
    werte["einwohner"] = einwohner
    werte["einwohner_je_km2"] = einwohner / flaeche_km2
    werte["pkw"] = antriebe.sum(axis=1)
    werte["pkw_je_1000_einwohner"] = werte["pkw"] / einwohner * 1000
    for name, spalte in ANTRIEBS_SPALTEN.items():
        werte[spalte] = antriebe[name]
        werte[f"{spalte}_je_1000_einwohner"] = werte[spalte] / einwohner * 1000

    kanton = antriebe.sum().rename_axis("Antriebsart").reset_index(name="Fahrzeuge")
    kanton.insert(0, "Jahr", jahr)
    return werte.reset_index(), kanton


def berechne_kennzahlen(verbunden: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Erzeuge Gemeindekennzahlen und kantonale Antriebssummen für 2010–2024."""
    pkw, stamm = _vorbereiten(verbunden)
    gemeinde_jahre = []
    antrieb_jahre = []
    for jahr in range(ANALYSE_STARTJAHR, ANALYSE_ENDJAHR + 1):
        if (pkw[str(jahr)] < 0).any() or (pkw.loc[pkw["Treibstoff"] == "Ohne Motor", str(jahr)] != 0).any():
            raise ValueError(f"Ungültige PKW-Bestände im Jahr {jahr}.")
        gemeinden, antriebe = _jahr_berechnen(pkw, stamm, jahr)
        gemeinde_jahre.append(gemeinden)
        antrieb_jahre.append(antriebe)
    return pd.concat(gemeinde_jahre, ignore_index=True), pd.concat(antrieb_jahre, ignore_index=True)
