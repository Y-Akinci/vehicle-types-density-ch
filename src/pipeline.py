if __package__:
    from .clean import daten_bereinigen
    from .load import load_raw_data
    from .merge import merge_dfs
else:
    from clean import daten_bereinigen
    from load import load_raw_data
    from merge import merge_dfs


def run_pipeline():
    antrieb, einwohner, geo = load_raw_data()
    antrieb, einwohner, geo = daten_bereinigen(antrieb, einwohner, geo)
    return merge_dfs(antrieb, einwohner, geo)


def main():
    verbunden = run_pipeline()

    print("Ergebnis (Zeilen, Spalten):", verbunden.shape)
    print("\nEinwohner-Merge:")
    print(verbunden["_einwohner_merge"].value_counts())
    print("\nGeografie-Merge:")
    print(verbunden["_geo_merge"].value_counts())
    print("\nErste Zeilen:")
    print(verbunden.head())


if __name__ == "__main__":
    main()
