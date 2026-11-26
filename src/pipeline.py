from .clean import daten_bereinigen
from .exploration import erstelle_exploration
from .load import DATA_DIR, load_raw_data
from .merge import merge_dfs
from .transform import berechne_kennzahlen


def run_pipeline(data_dir=DATA_DIR):
    """Liest die Rohdaten ein und gibt die Kennzahlen pro Gemeinde und pro Antriebsart zurück."""
    antrieb, einwohner, geo = load_raw_data(data_dir)
    antrieb, einwohner, geo = daten_bereinigen(antrieb, einwohner, geo)
    verbunden = merge_dfs(antrieb, einwohner, geo)
    return berechne_kennzahlen(verbunden)


def main():
    gemeinden, antriebe = run_pipeline()
    output_dir = erstelle_exploration(gemeinden, antriebe)
    print(f"Analyse abgeschlossen: {gemeinden['gemeinde_nr'].nunique()} Zuercher Gemeinden, "
          f"{gemeinden['Jahr'].nunique()} Jahre, {antriebe['Antriebsart'].nunique()} Antriebsarten.")
    print(f"Ergebnisse: {output_dir}")


if __name__ == "__main__":
    main()