"""Automatische explorative Auswertung und Karten des Kantons Zürich."""

from pathlib import Path

import geopandas as gpd
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .clean import ANALYSE_ENDJAHR, ANALYSE_STARTJAHR
from .transform import ANTRIEBS_SPALTEN


PROJEKTVERZEICHNIS = Path(__file__).resolve().parents[1]
GRENZEN = PROJEKTVERZEICHNIS / "data" / "geo" / "zuerich_gemeinden_2026.gpkg"
GRENZEN_QUELLE = (
    "https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/"
    "swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip"
)


def _speichern(fig: plt.Figure, ziel: Path) -> None:
    fig.savefig(ziel, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _kantonale_antriebsanteile(antriebe: pd.DataFrame, ziel: Path) -> None:
    anteile = antriebe.pivot(index="Jahr", columns="Antriebsart", values="Fahrzeuge")
    anteile = anteile[list(ANTRIEBS_SPALTEN)]
    anteile = anteile.div(anteile.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.stackplot(anteile.index, *[anteile[spalte] for spalte in anteile], labels=anteile.columns)
    ax.set(title="Anteile der Antriebsarten bei Personenwagen", xlabel="Jahr", ylabel="Anteil (%)", ylim=(0, 100))
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    _speichern(fig, ziel / "zeitreihe_antriebsarten.png")


def _stadt_zuerich_zeitreihen(gemeinden: pd.DataFrame, ziel: Path) -> None:
    """Zeige die PKW-Bestände je Antriebsart in der Stadt Zürich."""
    stadt = gemeinden[gemeinden["gemeinde_nr"] == 261].sort_values("Jahr")
    jahre = list(range(ANALYSE_STARTJAHR, ANALYSE_ENDJAHR + 1))
    if stadt["Jahr"].tolist() != jahre:
        raise ValueError("Für die Stadt Zürich wird genau ein Wert pro Analysejahr erwartet.")

    fig, achsen = plt.subplots(2, 3, figsize=(12, 7), sharex=True, layout="constrained")
    for ax, (name, spalte) in zip(achsen.flat, ANTRIEBS_SPALTEN.items()):
        ax.plot(stadt["Jahr"], stadt[spalte], marker="o", markersize=3)
        ax.set_title(name)
        ax.ticklabel_format(axis="y", style="plain", useOffset=False)
        ax.grid(alpha=0.2)
    fig.suptitle("Antriebsarten der Personenwagen in der Stadt Zürich")
    fig.supxlabel("Jahr")
    fig.supylabel("Anzahl PKW")
    _speichern(fig, ziel / "stadt_zuerich_antriebsarten_zeitreihe.png")


def _punkte_mit_trend(ax, dichte, werte, jahr, farbe):
    """Zeichne die Gemeindewerte und eine Gerade auf der logarithmischen Achse."""
    ax.scatter(dichte, werte, s=14, alpha=0.35, color=farbe, edgecolors="none")

    # Wir passen die Gerade an log10(Dichte) an, passend zur gezeichneten Achse.
    steigung, achsenabschnitt = np.polyfit(np.log10(dichte), werte, 1)
    linie_x = np.array([dichte.min(), dichte.max()])
    linie_y = steigung * np.log10(linie_x) + achsenabschnitt

    # Spearman vergleicht die Rangfolge der Gemeinden.
    rho = dichte.rank().corr(werte.rank()) if werte.nunique() > 1 else None
    korrelation = f"p = {rho:+.2f}".replace(".", ",") if rho is not None else "p nicht definiert"
    ax.plot(linie_x, linie_y, color=farbe, linewidth=2, label=f"{jahr} · {korrelation}")
    ax.set_xscale("log")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=8)


def _dichtevergleich(gemeinden: pd.DataFrame, ziel: Path) -> None:
    """Vergleiche die Gemeinden im ersten und letzten Jahr auf gleichen Achsen."""
    fig, achsen = plt.subplots(1, 2, figsize=(11, 5), sharex=True, sharey=True, layout="constrained")
    for ax, jahr in zip(achsen, [ANALYSE_STARTJAHR, ANALYSE_ENDJAHR]):
        werte = gemeinden[gemeinden["Jahr"] == jahr]
        _punkte_mit_trend(ax, werte["einwohner_je_km2"], werte["pkw_je_1000_einwohner"], jahr, "#17608b")
        ax.set_title(str(jahr))
    fig.suptitle("Einwohnerdichte und PKW-Quote im Kanton Zürich")
    fig.supxlabel("Einwohner je km² (logarithmische Skala)")
    fig.supylabel("PKW je 1'000 Einwohner")
    _speichern(fig, ziel / f"einwohnerdichte_und_pkw_{ANALYSE_STARTJAHR}_{ANALYSE_ENDJAHR}.png")


def _antriebsanteile_und_dichte(gemeinden: pd.DataFrame, ziel: Path) -> None:
    """Vergleiche die Anteile der sechs Antriebsarten je Gemeinde."""
    start = gemeinden[(gemeinden["Jahr"] == ANALYSE_STARTJAHR) & (gemeinden["pkw"] > 0)]
    ende = gemeinden[(gemeinden["Jahr"] == ANALYSE_ENDJAHR) & (gemeinden["pkw"] > 0)]

    fig, achsen = plt.subplots(2, 3, figsize=(12, 8), sharex=True, layout="constrained")
    for ax, (name, spalte) in zip(achsen.flat, ANTRIEBS_SPALTEN.items()):
        ax.set_title(name)
        for werte, jahr, farbe in [(start, ANALYSE_STARTJAHR, "#17608b"), (ende, ANALYSE_ENDJAHR, "#ad511c")]:
            anteil = werte[spalte] / werte["pkw"] * 100
            _punkte_mit_trend(ax, werte["einwohner_je_km2"], anteil, jahr, farbe)

    fig.suptitle("Einwohnerdichte und Antriebsanteile bei Personenwagen")
    fig.supxlabel("Einwohner je km² (logarithmische Skala)")
    fig.supylabel("Anteil am PKW-Bestand der Gemeinde (%)")
    _speichern(fig, ziel / f"einwohnerdichte_und_antriebsanteile_{ANALYSE_STARTJAHR}_{ANALYSE_ENDJAHR}.png")


def _gemeindekarte(karte, spalte, titel, einheit, datei):
    """Färbe die Gemeinden nach einer Spalte und speichere die Karte."""
    fig, ax = plt.subplots(figsize=(8, 8))
    karte.plot(
        column=spalte, ax=ax, cmap="YlGnBu", legend=True,
        edgecolor="#52636d", linewidth=0.25,
        legend_kwds={"label": einheit, "shrink": 0.65},
    )
    ax.set_title(titel, fontsize=12)
    ax.set_axis_off()
    ax.text(0, -0.02, "Gemeindestand 01.01.2026 · Quellen: CSV-Rohdaten und © swisstopo",
            transform=ax.transAxes, fontsize=8)
    _speichern(fig, datei)


def _karten(gemeinden_2024: pd.DataFrame, ziel: Path, grenzen_pfad: Path) -> None:
    if not grenzen_pfad.exists():
        raise FileNotFoundError(f"Gemeindegrenzen fehlen: {grenzen_pfad}")
    grenzen = gpd.read_file(grenzen_pfad, layer="gemeinden")
    if grenzen.crs is None or grenzen.crs.to_epsg() != 2056:
        raise ValueError("Gemeindegrenzen müssen im Koordinatensystem EPSG:2056 vorliegen.")
    if len(grenzen) != 160 or grenzen["bfs_nummer"].nunique() != 160 or not grenzen.geometry.is_valid.all():
        raise ValueError("Gemeindegrenzen müssen 160 eindeutige und gültige Polygone enthalten.")
    karte = grenzen.merge(gemeinden_2024, left_on="bfs_nummer", right_on="gemeinde_nr", how="left", validate="one_to_one")
    if karte["einwohner"].isna().any() or set(karte["bfs_nummer"]) != set(gemeinden_2024["gemeinde_nr"]):
        raise ValueError("Nicht alle 160 Zürcher Gemeinden konnten kartiert werden.")

    _gemeindekarte(
        karte, "einwohner_je_km2", f"Einwohnerdichte nach Zürcher Gemeinde, {ANALYSE_ENDJAHR}",
        "Einwohner je km²", ziel / f"karte_einwohnerdichte_{ANALYSE_ENDJAHR}.png",
    )

    karten = {"Personenwagen": "pkw", **ANTRIEBS_SPALTEN}
    for titel, name in karten.items():
        _gemeindekarte(
            karte, f"{name}_je_1000_einwohner", f"{titel} nach Zürcher Gemeinde, {ANALYSE_ENDJAHR}",
            "PKW je 1'000 Einwohner", ziel / f"karte_{name}_{ANALYSE_ENDJAHR}.png",
        )


def _zahl(wert) -> str:
    """Schreibt eine Zahl mit Schweizer Tausendertrennzeichen, z. B. 1'620'020."""
    return f"{int(wert):,}".replace(",", "'")


def _bericht(gemeinden: pd.DataFrame, antriebe: pd.DataFrame, ziel: Path) -> None:
    """Schreibe die wichtigsten Kennzahlen und Links zu den Grafiken."""
    aktuell = gemeinden[gemeinden["Jahr"] == ANALYSE_ENDJAHR]
    gesamt = int(aktuell["pkw"].sum())
    einwohner = int(aktuell["einwohner"].sum())
    stadt = gemeinden[gemeinden["gemeinde_nr"] == 261].set_index("Jahr")
    antrieb_2024 = antriebe[antriebe["Jahr"] == ANALYSE_ENDJAHR]
    zeilen = "\n".join(
        f"| {row.Antriebsart} | {_zahl(row.Fahrzeuge)} | {row.Fahrzeuge / gesamt * 100:.1f} % |"
        for row in antrieb_2024.itertuples(index=False)
    )
    text = f"""# Analysebericht Kanton Zürich

## Daten

Wir betrachten die Personenwagen in den 160 Gemeinden des Kantons Zürich von {ANALYSE_STARTJAHR} bis {ANALYSE_ENDJAHR}. Die Zahlen stammen aus den drei CSV-Dateien in `data/raw/`. Die Gemeindegrenzen kommen von [swisstopo]({GRENZEN_QUELLE}) und haben den Stand vom 1. Januar 2026.

Die Einwohnerdichte gibt an, wie viele Menschen auf einem Quadratkilometer wohnen. Die PKW-Quote gibt an, wie viele Personenwagen es pro 1'000 Einwohner gibt. Jede Karte hat ihre eigene Farbskala, die Farben verschiedener Karten lassen sich also nicht direkt vergleichen.

Benzin- und Dieselhybride zählen wir zusammen und trennen nur zwischen Normal-Hybrid und Plug-in-Hybrid. Gas, Wasserstoff und andere Antriebe fassen wir unter «Sonstige» zusammen.

## Kanton Zürich {ANALYSE_ENDJAHR}

Im Kanton wohnen {_zahl(einwohner)} Menschen und es gibt {_zahl(gesamt)} Personenwagen. Das sind {gesamt / einwohner * 1000:.0f} Autos pro 1'000 Einwohner.

Im [Streudiagramm zur PKW-Quote](figures/einwohnerdichte_und_pkw_{ANALYSE_STARTJAHR}_{ANALYSE_ENDJAHR}.png) steht jeder Punkt für eine Gemeinde. Es vergleicht {ANALYSE_STARTJAHR} und {ANALYSE_ENDJAHR} auf denselben Achsen.

Die [Grafik zu den Antriebsanteilen](figures/einwohnerdichte_und_antriebsanteile_{ANALYSE_STARTJAHR}_{ANALYSE_ENDJAHR}.png) zeigt für jede Antriebsart, wie gross ihr Anteil an den Autos einer Gemeinde ist. Die Linien zeigen den Trend. Sie sind mit einer linearen Regression auf die logarithmierte Dichte berechnet. Der Spearman-Wert ρ zeigt, wie gut die Reihenfolge der Gemeinden nach Dichte mit ihrer Reihenfolge nach Anteil übereinstimmt.

| Antriebsart | Personenwagen | Anteil |
| --- | --- | --- |
{zeilen}

## Stadt Zürich

In der Stadt Zürich gab es {_zahl(stadt.loc[ANALYSE_STARTJAHR, 'pkw'])} Personenwagen im Jahr {ANALYSE_STARTJAHR} und {_zahl(stadt.loc[ANALYSE_ENDJAHR, 'pkw'])} im Jahr {ANALYSE_ENDJAHR}. Die [Stadtgrafik](figures/stadt_zuerich_antriebsarten_zeitreihe.png) zeigt, wie sich die einzelnen Antriebsarten entwickelt haben.

## Grenzen der Auswertung

- Alle früheren Werte sind auf den Gemeindestand 2026 umgerechnet. Die Fläche einer Gemeinde bleibt über alle Jahre gleich.
- Die Dichte bezieht sich auf die ganze Gemeindefläche, also auch auf Wald, Felder und kleinere Seen. Gemeinden mit viel Wald wirken dadurch weniger dicht, als sie im Siedlungsgebiet sind. Zürichsee und Greifensee gehören zu keiner Gemeinde und zählen nicht mit.
- Ein Auto ist dort eingelöst, wo der Halter wohnt oder seine Firma ihren Sitz hat, und nicht dort, wo es fährt. Miet-, Leasing- und Firmenwagen erklären die hohen Werte in Kloten, Opfikon und Rümlang rund um den Flughafen.
- In den ersten Jahren gab es kaum Elektroautos. 2010 hatten 124 von 160 Gemeinden kein einziges, Plug-in-Hybride gibt es erst ab 2012. Vor etwa 2015 sagen Zusammenhänge mit diesen beiden Antrieben deshalb wenig aus.
- Die Fahrzeugzahlen gelten für den 30. September, die Einwohnerzahlen für den 31. Dezember. Das betrifft nur die PKW-Quote und nicht die Anteile der Antriebsarten.
- Zürich und Winterthur haben zusammen 24 % aller Personenwagen im Kanton. Die Anteile für den ganzen Kanton hängen deshalb stark von diesen beiden Städten ab. Beim Vergleich der Gemeinden zählt dagegen jede Gemeinde gleich viel.
- Wir haben nur den Kanton Zürich untersucht. Für die ganze Schweiz können die Ergebnisse anders aussehen.
- Wir zählen, wie viele Autos es gibt, und nicht, wie viel sie fahren. Über Fahrleistung und Emissionen sagt die Auswertung nichts.
"""
    ziel.write_text(text, encoding="utf-8")


def erstelle_exploration(gemeinden: pd.DataFrame, antriebe: pd.DataFrame, output_dir: Path | None = None) -> Path:
    """Speichere die Grafiken und den EDA-Bericht in outputs/."""
    output_dir = Path(output_dir) if output_dir is not None else PROJEKTVERZEICHNIS / "outputs"
    figuren = output_dir / "figures"
    figuren.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    aktuell = gemeinden[gemeinden["Jahr"] == ANALYSE_ENDJAHR]
    _kantonale_antriebsanteile(antriebe, figuren)
    _stadt_zuerich_zeitreihen(gemeinden, figuren)
    _dichtevergleich(gemeinden, figuren)
    _antriebsanteile_und_dichte(gemeinden, figuren)
    _karten(aktuell, figuren, GRENZEN)
    _bericht(gemeinden, antriebe, output_dir / "analysebericht.md")
    return output_dir
