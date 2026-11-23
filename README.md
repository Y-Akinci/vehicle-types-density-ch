# Personenwagenbestand und Einwohnerdichte im Kanton Zürich

Die Pipeline analysiert den Personenwagenbestand, seine Antriebsarten und die Einwohnerdichte für die 160 politischen Gemeinden des Kantons Zürich von 2010 bis 2024. Sie erstellt 2024er Gemeindekarten mit GeoPandas.

## Ausführen

Python 3.11 oder neuer verwenden und im Projektverzeichnis ausführen:

```bash
python -m venv .venv
# Virtuelle Umgebung aktivieren; unter Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.pipeline
```

Die Pipeline speichert zwei Zeitreihen, acht Karten für 2024 und zwei Streudiagramme in `outputs/figures/`. Die Zeitreihen zeigen die kantonalen Antriebsanteile und die Bestände je Antriebsart in der Stadt Zürich von 2010 bis 2024. Die Streudiagramme vergleichen die beiden Eckjahre und zeigen, wie die Einwohnerdichte mit der PKW-Quote und den sechs Antriebsanteilen zusammenhängt.

Der Bericht in `outputs/eda_bericht.md` fasst die Kennzahlen zusammen und verlinkt die Streudiagramme.

## Definitionen

**Einwohnerdichte** ist die Einwohnerzahl geteilt durch die Gemeindefläche in km² (`AREA_HA / 100`). **PKW-Quote** ist die Anzahl Personenwagen je 1’000 Einwohner. Die Antriebskarten zeigen diese Quote jeweils für eine Antriebsart. Normal-Hybrid und Plug-in-Hybrid fassen je Benzin- und Dieselvarianten zusammen. «Sonstige» enthält Gas (mono- und bivalent), Wasserstoff und «Anderer».

## Geodaten und Zeitbezug

Die Karten verwenden `data/geo/zuerich_gemeinden_2026.gpkg` mit den 160 politischen Gemeinden aus [swissBOUNDARIES3D, Ausgabe 2026-01](https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d), © swisstopo. Quelle ist die amtliche Ebene `tlm_hoheitsgebiet`, gefiltert auf `kantonsnummer = 1` und `objektart = Gemeindegebiet`; enthalten sind BFS-Nummer, Name und Originalgeometrie in EPSG:2056. Der [Originaldownload](https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip) liegt wegen seiner Grösse nicht im Repository. Zürichsee und Greifensee sind keine politischen Gemeinden und werden nicht mitgezählt.

Die Fahrzeug- und Einwohnerzahlen reichen bis 2024. `src/clean.py` ordnet historische Gemeinden dem Stand 01.01.2026 zu. Deshalb verwenden die 2024er Karten 2026er Grenzen. Die Fläche aus `Geographische_Kennzahlen.csv` wird über alle Analysejahre konstant gehalten; historische Dichtewerte sind somit auf diesen Gemeindestand bezogen.
