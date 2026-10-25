def merge_dfs(antrieb, einwohner, geo):
    verbunden = antrieb.merge(
        einwohner,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_einwohner_merge",
    )
    if (verbunden["_einwohner_merge"] == "left_only").any():
        raise ValueError("Für einige Antriebszeilen fehlen Einwohnerdaten.")

    verbunden = verbunden.merge(
        geo,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_geo_merge",
    )
    if (verbunden["_geo_merge"] == "left_only").any():
        raise ValueError("Für einige Antriebszeilen fehlen Geografiedaten.")

    return verbunden
