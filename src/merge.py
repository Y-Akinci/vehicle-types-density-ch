import pandas as pd


def datensaetze_verbinden(
    antrieb: pd.DataFrame,
    einwohner: pd.DataFrame,
    geodaten: pd.DataFrame,
) -> pd.DataFrame:
    anzahl_antriebszeilen = len(antrieb)

    verbunden = antrieb.merge(
        einwohner,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_einwohner_verbindung",
    )

    if (
        verbunden["_einwohner_verbindung"]
        == "left_only"
    ).any():
        raise ValueError(
            "Für einige Fahrzeugzeilen fehlen Einwohnerdaten."
        )

    verbunden = verbunden.drop(
        columns="_einwohner_verbindung"
    )

    verbunden = verbunden.merge(
        geodaten,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_geo_verbindung",
    )

    if (
        verbunden["_geo_verbindung"]
        == "left_only"
    ).any():
        raise ValueError(
            "Für einige Fahrzeugzeilen fehlen Geografiedaten."
        )

    verbunden = verbunden.drop(
        columns="_geo_verbindung"
    )

    if len(verbunden) != anzahl_antriebszeilen:
        raise ValueError(
            "Beim Verbinden hat sich die Anzahl "
            "der Fahrzeugzeilen verändert."
        )

    einwohnerspalten = [
        f"einwohner_{jahr}"
        for jahr in range(2010, 2025)
    ]

    pflichtspalten = [
        *einwohnerspalten,
        "amtlicher_gemeindename",
        "AREA_HA",
    ]

    if verbunden[pflichtspalten].isna().any().any():
        raise ValueError(
            "Nach dem Verbinden fehlen Werte."
        )

    return verbunden