import pandas as pd


STARTJAHR = 2010
ENDJAHR = 2024


def daten_transformieren(
    daten: pd.DataFrame,
) -> pd.DataFrame:
    transformiert = daten.copy()

    jahresspalten = [
        str(jahr)
        for jahr in range(STARTJAHR, ENDJAHR + 1)
    ]

    einwohnerspalten = [
        f"einwohner_{jahr}"
        for jahr in range(STARTJAHR, ENDJAHR + 1)
    ]

    benoetigte_spalten = [
        *jahresspalten,
        *einwohnerspalten,
        "AREA_HA",
    ]

    fehlende_spalten = [
        spalte
        for spalte in benoetigte_spalten
        if spalte not in transformiert.columns
    ]

    if fehlende_spalten:
        raise ValueError(
            f"Folgende Spalten fehlen: {fehlende_spalten}"
        )

    hilfsspalten = [
        "_einwohner_merge",
        "_geo_merge",
    ]

    grundspalten = [
        spalte
        for spalte in transformiert.columns
        if spalte not in jahresspalten
        and spalte not in einwohnerspalten
        and spalte not in hilfsspalten
    ]

    jahresdaten = []

    for jahr in range(STARTJAHR, ENDJAHR + 1):
        jahr_daten = transformiert[grundspalten].copy()
        jahr_daten["Jahr"] = jahr
        jahr_daten["Fahrzeuge"] = pd.to_numeric(
            transformiert[str(jahr)],
            errors="coerce",
        )
        jahr_daten["Einwohner"] = pd.to_numeric(
            transformiert[f"einwohner_{jahr}"],
            errors="coerce",
        )
        jahresdaten.append(jahr_daten)

    transformiert = pd.concat(
        jahresdaten,
        ignore_index=True,
    )

    transformiert["Flaeche_km2"] = (
        pd.to_numeric(
            transformiert["AREA_HA"],
            errors="coerce",
        )
        / 100
    )

    pruefspalten = [
        "Fahrzeuge",
        "Einwohner",
        "Flaeche_km2",
    ]

    if transformiert[pruefspalten].isna().any().any():
        raise ValueError(
            "Die Daten enthalten ungültige Zahlen."
        )

    if (transformiert["Einwohner"] <= 0).any():
        raise ValueError(
            "Die Einwohnerzahl muss grösser als null sein."
        )

    if (transformiert["Flaeche_km2"] <= 0).any():
        raise ValueError(
            "Die Fläche muss grösser als null sein."
        )

    transformiert["Messdatum_Fahrzeuge"] = pd.to_datetime(
        transformiert["Jahr"].astype(str) + "-09-30"
    )

    transformiert.loc[
        transformiert["Jahr"] == 2022,
        "Messdatum_Fahrzeuge",
    ] = pd.Timestamp("2022-10-15")

    transformiert["Messdatum_Einwohner"] = pd.to_datetime(
        transformiert["Jahr"].astype(str) + "-12-31"
    )

    transformiert["Einwohnerdichte"] = (
        transformiert["Einwohner"]
        / transformiert["Flaeche_km2"]
    )

    transformiert["Fahrzeuge_pro_1000_Einwohner"] = (
        transformiert["Fahrzeuge"]
        / transformiert["Einwohner"]
        * 1000
    )

    transformiert["Fahrzeuge_pro_km2"] = (
        transformiert["Fahrzeuge"]
        / transformiert["Flaeche_km2"]
    )

    sortierspalten = [
        "gemeinde_nr",
        "Fahrzeuggruppe",
        "Treibstoff",
        "Jahr",
    ]

    transformiert = transformiert.sort_values(
        sortierspalten
    )

    transformiert["Bestandsveraenderung_zum_Vorjahr"] = (
        transformiert.groupby(
            [
                "gemeinde_nr",
                "Fahrzeuggruppe",
                "Treibstoff",
            ]
        )["Fahrzeuge"]
        .diff()
    )

    return transformiert.reset_index(drop=True)
