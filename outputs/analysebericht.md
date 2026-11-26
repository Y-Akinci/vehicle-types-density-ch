# Analysebericht Kanton Zürich

## Daten

Wir betrachten die Personenwagen in den 160 Gemeinden des Kantons Zürich von 2010 bis 2024. Die Zahlen stammen aus den drei CSV-Dateien in `data/raw/`. Die Gemeindegrenzen kommen von [swisstopo](https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip) und haben den Stand vom 1. Januar 2026.

Die Einwohnerdichte gibt an, wie viele Menschen auf einem Quadratkilometer wohnen. Die PKW-Quote gibt an, wie viele Personenwagen es pro 1'000 Einwohner gibt. Jede Karte hat ihre eigene Farbskala, die Farben verschiedener Karten lassen sich also nicht direkt vergleichen.

Benzin- und Dieselhybride zählen wir zusammen und trennen nur zwischen Normal-Hybrid und Plug-in-Hybrid. Gas, Wasserstoff und andere Antriebe fassen wir unter «Sonstige» zusammen.

## Kanton Zürich 2024

Im Kanton wohnen 1'620'020 Menschen und es gibt 763'711 Personenwagen. Das sind 471 Autos pro 1'000 Einwohner.

Im [Streudiagramm zur PKW-Quote](figures/einwohnerdichte_und_pkw_2010_2024.png) steht jeder Punkt für eine Gemeinde. Es vergleicht 2010 und 2024 auf denselben Achsen.

Die [Grafik zu den Antriebsanteilen](figures/einwohnerdichte_und_antriebsanteile_2010_2024.png) zeigt für jede Antriebsart, wie gross ihr Anteil an den Autos einer Gemeinde ist. Die Linien zeigen den Trend. Sie sind mit einer linearen Regression auf die logarithmierte Dichte berechnet. Der Spearman-Wert ρ zeigt, wie gut die Reihenfolge der Gemeinden nach Dichte mit ihrer Reihenfolge nach Anteil übereinstimmt.

| Antriebsart | Personenwagen | Anteil |
| --- | --- | --- |
| Benzin | 441'458 | 57.8 % |
| Diesel | 194'083 | 25.4 % |
| Elektrisch | 40'959 | 5.4 % |
| Normal-Hybrid | 64'502 | 8.4 % |
| Plug-in-Hybrid | 18'720 | 2.5 % |
| Sonstige | 3'989 | 0.5 % |

## Stadt Zürich

In der Stadt Zürich gab es 137'225 Personenwagen im Jahr 2010 und 138'873 im Jahr 2024. Die [Stadtgrafik](figures/stadt_zuerich_antriebsarten_zeitreihe.png) zeigt, wie sich die einzelnen Antriebsarten entwickelt haben.

## Grenzen der Auswertung

- Alle früheren Werte sind auf den Gemeindestand 2026 umgerechnet. Die Fläche einer Gemeinde bleibt über alle Jahre gleich.
- Die Dichte bezieht sich auf die ganze Gemeindefläche, also auch auf Wald, Felder und kleinere Seen. Gemeinden mit viel Wald wirken dadurch weniger dicht, als sie im Siedlungsgebiet sind. Zürichsee und Greifensee gehören zu keiner Gemeinde und zählen nicht mit.
- Ein Auto ist dort eingelöst, wo der Halter wohnt oder seine Firma ihren Sitz hat, und nicht dort, wo es fährt. Miet-, Leasing- und Firmenwagen erklären die hohen Werte in Kloten, Opfikon und Rümlang rund um den Flughafen.
- In den ersten Jahren gab es kaum Elektroautos. 2010 hatten 124 von 160 Gemeinden kein einziges, Plug-in-Hybride gibt es erst ab 2012. Vor etwa 2015 sagen Zusammenhänge mit diesen beiden Antrieben deshalb wenig aus.
- Die Fahrzeugzahlen gelten für den 30. September, die Einwohnerzahlen für den 31. Dezember. Das betrifft nur die PKW-Quote und nicht die Anteile der Antriebsarten.
- Zürich und Winterthur haben zusammen 24 % aller Personenwagen im Kanton. Die Anteile für den ganzen Kanton hängen deshalb stark von diesen beiden Städten ab. Beim Vergleich der Gemeinden zählt dagegen jede Gemeinde gleich viel.
- Wir haben nur den Kanton Zürich untersucht. Für die ganze Schweiz können die Ergebnisse anders aussehen.
- Wir zählen, wie viele Autos es gibt, und nicht, wie viel sie fahren. Über Fahrleistung und Emissionen sagt die Auswertung nichts.
