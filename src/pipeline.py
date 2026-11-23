"""Vollständige Datenpipeline und explorative Auswertung.

Aufruf: python -m src.pipeline
"""

from .clean import daten_bereinigen
from .exploration import erstelle_exploration
from .load import load_raw_data
from .merge import merge_dfs
from .transform import berechne_kennzahlen


def run_pipeline():
    antrieb, einwohner, geo = load_raw_data()
    antrieb, einwohner, geo = daten_bereinigen(antrieb, einwohner, geo)
    verbunden = merge_dfs(antrieb, einwohner, geo)
    gemeinden, antriebe = berechne_kennzahlen(verbunden)
    output_dir = erstelle_exploration(gemeinden, antriebe)
    return gemeinden, antriebe, output_dir


def main():
    gemeinden, antriebe, output_dir = run_pipeline()
    print(f"Analyse abgeschlossen: {gemeinden['gemeinde_nr'].nunique()} Zuercher Gemeinden, "
          f"{gemeinden['Jahr'].nunique()} Jahre, {antriebe['Antriebsart'].nunique()} Antriebsarten.")
    print(f"Ergebnisse: {output_dir}")


if __name__ == "__main__":
    main()
