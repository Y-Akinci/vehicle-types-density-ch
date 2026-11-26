# Personenwagen und Einwohnerdichte im Kanton Zürich

Fahren die Menschen in dicht besiedelten Gemeinden andere Autos als auf dem Land? Um das herauszufinden, schauen wir uns die 160 Gemeinden im Kanton Zürich von 2010 bis 2024 an. Für jede Gemeinde wissen wir, wie viele Personenwagen es gibt, welchen Antrieb sie haben und wie dicht die Gemeinde besiedelt ist. Daraus erstellt die Pipeline Grafiken, Karten und einen kurzen Bericht.

## Pipeline starten

Du brauchst Python 3.11 oder neuer. Führe diese Befehle im Projektordner aus.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.pipeline
```

Unter Windows aktivierst du die Umgebung mit `.venv\Scripts\Activate.ps1` statt mit `source`.

## Was dabei entsteht

Alle Grafiken landen im Ordner `outputs/figures/`. Das sind zwei Zeitreihen, acht Karten für 2024 und zwei Streudiagramme.

Die eine Zeitreihe zeigt, wie sich die Antriebsarten im ganzen Kanton entwickelt haben, die andere zeigt dasselbe für die Stadt Zürich. Die Karten zeigen für jede Gemeinde die Einwohnerdichte und wie viele Autos es pro 1'000 Einwohner gibt, einmal insgesamt und einmal pro Antriebsart. Die Streudiagramme vergleichen 2010 mit 2024. Sie zeigen, wie die Einwohnerdichte mit der Zahl der Autos und mit den Anteilen der Antriebsarten zusammenhängt.

Ausserdem schreibt die Pipeline den Bericht `outputs/analysebericht.md`. Er fasst die wichtigsten Zahlen zusammen und erklärt, wo die Auswertung an Grenzen stösst.

## Begriffe

Die **Einwohnerdichte** gibt an, wie viele Menschen auf einem Quadratkilometer wohnen. Wir teilen dafür die Einwohnerzahl durch die Fläche der Gemeinde.

Die **PKW-Quote** gibt an, wie viele Personenwagen es pro 1'000 Einwohner gibt.

Benzin- und Dieselhybride zählen wir zusammen und trennen nur zwischen Normal-Hybrid und Plug-in-Hybrid. Gas, Wasserstoff und andere Antriebe fassen wir unter «Sonstige» zusammen.

## Woher die Gemeindegrenzen kommen

Die Grenzen stammen aus [swissBOUNDARIES3D](https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d) von swisstopo und haben den Stand vom Januar 2026. Aus der Ebene `tlm_hoheitsgebiet` haben wir nur die Gemeindegebiete im Kanton Zürich behalten (`kantonsnummer = 1`). Sie liegen in `data/geo/zuerich_gemeinden_2026.gpkg`. Für jede Gemeinde stehen dort die BFS-Nummer, der Name und die Grenze im Koordinatensystem EPSG 2056.

Den [ganzen Download](https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip) haben wir nicht ins Repository gelegt, weil er zu gross ist. Zürichsee und Greifensee gehören zu keiner Gemeinde und zählen deshalb nicht mit.

## Gemeindestand

Seit 2010 haben sich einige Gemeinden zusammengeschlossen. Damit wir alle Jahre vergleichen können, rechnet `src/clean.py` alle Werte auf den Gemeindestand vom 1. Januar 2026 um. Deshalb zeigen auch die Karten für 2024 die Grenzen von 2026.

Die Fläche einer Gemeinde bleibt über alle Jahre gleich. Die Dichte früherer Jahre bezieht sich also immer auf die heutigen Grenzen.