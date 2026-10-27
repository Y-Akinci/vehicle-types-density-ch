import pandas as pd


STARTJAHR = 2010
ENDJAHR = 2024
ZUERICH_KANTONSNUMMER = 1
SEEN_BEZIRKSNUMMER = 100

GEBIET_SPALTE = (
    "Kanton (-) / Bezirk (>>) / Gemeinde (......)"
)

EINWOHNER_SPALTE = "Staatsangehörigkeit - Total"


def _export_anfuehrungszeichen_entfernen(daten):
    bereinigt = daten.copy()
    bereinigt.columns = bereinigt.columns.str.strip('"')

    for spalte in bereinigt.columns:
        if pd.api.types.is_string_dtype(
            bereinigt[spalte]
        ):
            bereinigt[spalte] = (
                bereinigt[spalte]
                .str.strip('"')
            )

    return bereinigt


def geodaten_bereinigen(daten):
    bereinigt = daten.rename(
        columns={
            "GDENR": "gemeinde_nr",
            "GDENAME": "amtlicher_gemeindename",
        }
    ).copy()

    zuerich = bereinigt.loc[
        (bereinigt["KTNR"] == ZUERICH_KANTONSNUMMER)
        & (bereinigt["BEZNR"] != SEEN_BEZIRKSNUMMER),
        [
            "gemeinde_nr",
            "amtlicher_gemeindename",
            "AREA_HA",
            "BEZNR",
            "BEZNAME",
        ],
    ].copy()

    if zuerich["gemeinde_nr"].duplicated().any():
        raise ValueError(
            "Die Geodaten enthalten doppelte Gemeindenummern."
        )

    return (
        zuerich
        .sort_values("gemeinde_nr")
        .reset_index(drop=True)
    )


def fahrzeugdaten_bereinigen(
    daten,
    gemeindenummern,
):
    bereinigt = _export_anfuehrungszeichen_entfernen(
        daten
    )

    bereinigt["gemeinde_nr"] = (
        bereinigt["Gemeinde"]
        .str.extract(
            r"^(\d+)",
            expand=False,
        )
        .astype("Int64")
    )

    bereinigt["Gemeinde"] = (
        bereinigt["Gemeinde"]
        .str.replace(
            r"^\d+\s*",
            "",
            regex=True,
        )
        .str.strip()
    )

    bereinigt = bereinigt[
        bereinigt["gemeinde_nr"].isin(
            set(gemeindenummern)
        )
    ].copy()

    jahresspalten = [
        spalte
        for spalte in bereinigt.columns
        if str(spalte).isdigit()
        and STARTJAHR <= int(spalte) <= ENDJAHR
    ]

    bereinigt[jahresspalten] = (
        bereinigt[jahresspalten].apply(
            pd.to_numeric,
            errors="coerce",
        )
    )

    if bereinigt[jahresspalten].isna().any().any():
        raise ValueError(
            "Die Fahrzeugdaten enthalten ungültige Jahreswerte."
        )

    gruppenspalten = [
        "gemeinde_nr",
        "Gemeinde",
        "Fahrzeuggruppe",
        "Treibstoff",
    ]

    bereinigt = (
        bereinigt.groupby(
            gruppenspalten,
            as_index=False,
            dropna=False,
        )[jahresspalten]
        .sum()
    )

    return (
        bereinigt[
            [
                "gemeinde_nr",
                "Gemeinde",
                "Fahrzeuggruppe",
                "Treibstoff",
                *jahresspalten,
            ]
        ]
        .sort_values(
            [
                "gemeinde_nr",
                "Fahrzeuggruppe",
                "Treibstoff",
            ]
        )
        .reset_index(drop=True)
    )


def einwohnerdaten_bereinigen(
    daten,
    gemeindenummern,
):
    bereinigt = _export_anfuehrungszeichen_entfernen(
        daten
    )

    bereinigt["gemeinde_nr"] = bereinigt[
        GEBIET_SPALTE
    ].str.extract(
        r"^\.{6}(\d+)",
        expand=False,
    )

    bereinigt = bereinigt.dropna(
        subset=["gemeinde_nr"]
    )

    bereinigt["gemeinde_nr"] = (
        bereinigt["gemeinde_nr"]
        .astype("Int64")
    )

    bereinigt = bereinigt[
        bereinigt["gemeinde_nr"].isin(
            set(gemeindenummern)
        )
    ].copy()

    bereinigt["Jahr"] = pd.to_numeric(
        bereinigt["Jahr"],
        errors="coerce",
    )

    bereinigt[EINWOHNER_SPALTE] = pd.to_numeric(
        bereinigt[EINWOHNER_SPALTE],
        errors="coerce",
    )

    if bereinigt["Jahr"].isna().any():
        raise ValueError(
            "Die Einwohnerdaten enthalten ungültige Jahre."
        )

    if bereinigt[EINWOHNER_SPALTE].isna().any():
        raise ValueError(
            "Die Einwohnerdaten enthalten ungültige Werte."
        )

    bereinigt = bereinigt[
        bereinigt["Jahr"].between(
            STARTJAHR,
            ENDJAHR,
        )
    ]

    return (
        bereinigt.pivot_table(
            index="gemeinde_nr",
            columns="Jahr",
            values=EINWOHNER_SPALTE,
            aggfunc="sum",
        )
        .rename(
            columns=lambda jahr: (
                f"einwohner_{int(jahr)}"
            )
        )
        .rename_axis(columns=None)
        .reset_index()
    )