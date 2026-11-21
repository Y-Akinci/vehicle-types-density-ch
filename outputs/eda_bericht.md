# Explorative Datenanalyse: Kanton Zürich

## Daten und Definitionen

Die Analyse betrachtet Personenwagen in den 160 Zürcher Gemeinden von 2010 bis 2024. Grundlage sind die drei CSV-Dateien unter `data/raw/` und die Gemeindegrenzen aus [swissBOUNDARIES3D, Stand 01.01.2026](https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip) (© swisstopo).

- Die Einwohnerdichte entspricht Einwohnern je km².
- Die PKW-Quote gibt die Zahl der Personenwagen je 1’000 Einwohner an. Die PKW- und Antriebskarten zeigen diese Quote mit jeweils eigener Farbskala.
- Normal-Hybrid und Plug-in-Hybrid bündeln je Benzin- und Dieselvarianten. Sonstige umfasst Gas, Wasserstoff und «Anderer».

## Kanton Zürich 2024

1,620,020 Einwohner und 763,711 Personenwagen ergeben 471.4 PKW je 1’000 Einwohner.

Das [Streudiagramm zur PKW-Quote](figures/einwohnerdichte_und_pkw_2010_2024.png) vergleicht beide Jahre auf gleichen Achsen. Jeder Punkt steht für eine Gemeinde.

Die [Grafik zu den Antriebsanteilen](figures/einwohnerdichte_und_antriebsanteile_2010_2024.png) zeigt pro Antrieb den prozentualen Anteil am PKW-Bestand der Gemeinde. Die Trendlinien sind lineare Regressionen auf log10(Einwohnerdichte). Spearman ρ beschreibt den Zusammenhang zwischen den Rangfolgen der Gemeinden.

| Antriebsart | PKW | Anteil am PKW-Bestand |
| --- | ---: | ---: |
| Benzin | 441,458 | 57.8% |
| Diesel | 194,083 | 25.4% |
| Elektrisch | 40,959 | 5.4% |
| Normal-Hybrid | 64,502 | 8.4% |
| Plug-in-Hybrid | 18,720 | 2.5% |
| Sonstige | 3,989 | 0.5% |

## Stadt Zürich

Die Stadt Zürich zählte 137,225 Personenwagen im Jahr 2010 und 138,873 im Jahr 2024. Die [Stadtgrafik](figures/stadt_zuerich_antriebsarten_zeitreihe.png) zeigt die absoluten Bestände je Antriebsart.

## Grenzen der Auswertung

Die historischen Werte wurden dem Gemeindestand 2026 zugeordnet. Die Gemeindefläche bleibt für alle Jahre konstant. Fahrzeugbestände messen weder Fahrleistung noch Emissionen.
