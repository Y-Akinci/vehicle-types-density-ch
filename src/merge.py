import pandas as pd
def merge_dfs(antrieb, einwohner, geo):
    verbunden = antrieb.merge(
        einwohner,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_einwohner_merge",
    )

    verbunden = verbunden.merge(
        geo,
        on="gemeinde_nr",
        how="left",
        validate="many_to_one",
        indicator="_geo_merge",
    )

    return verbunden
