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

## Antriebsanteile nach Dichteklasse

Wir teilen die Gemeinden nach ihrer Einwohnerdichte im Jahr 2024 in vier gleich grosse Gruppen ein. Jede Gemeinde bleibt in allen Jahren in derselben Gruppe. Die Tabelle zeigt für jede Gruppe den Median der Antriebsanteile im Jahr 2024. Wir nehmen den Median statt des Durchschnitts, weil einzelne Ausreisser ihn kaum verschieben.

| Dichteklasse | Benzin | Diesel | Elektrisch | Normal-Hybrid | Plug-in-Hybrid | Sonstige |
| --- | --- | --- | --- | --- | --- | --- |
| tief | 61.5 % | 26.5 % | 4.4 % | 5.5 % | 1.7 % | 0.5 % |
| mittel-tief | 60.8 % | 24.1 % | 5.8 % | 6.8 % | 1.9 % | 0.5 % |
| mittel-hoch | 60.0 % | 24.8 % | 5.3 % | 7.3 % | 2.0 % | 0.5 % |
| hoch | 59.6 % | 24.7 % | 5.1 % | 8.3 % | 2.5 % | 0.5 % |

## Ausreisser

Als Ausreisser zählt eine Gemeinde, wenn ihr Wert mehr als das 1.5-fache des Interquartilsabstands unter dem ersten oder über dem dritten Quartil liegt. Das ist dieselbe Regel, die auch ein Boxplot verwendet. Im Jahr 2024 fallen diese Gemeinden auf.

| Kennzahl | Auffällige Gemeinden |
| --- | --- |
| Einwohnerdichte | Zürich, Opfikon, Kilchberg (ZH), Thalwil, Oberengstringen, Schlieren, Dietikon, Wallisellen, Geroldswil |
| PKW-Quote | Kloten, Zürich |
| Anteil Benzin | Schleinikon, Truttikon, Dietikon, Otelfingen, Dielsdorf, Urdorf, Schwerzenbach, Kloten, Wallisellen, Schlieren, Rümlang, Opfikon |
| Anteil Diesel | Schlieren |
| Anteil Elektrisch | Aesch (ZH) |
| Anteil Normal-Hybrid | Rümlang, Opfikon, Kloten, Dietlikon |
| Anteil Plug-in-Hybrid | Opfikon, Erlenbach (ZH), Uitikon, Küsnacht (ZH), Zumikon, Kloten, Zollikon, Herrliberg |
| Anteil Sonstige | Flurlingen, Dorf, Dättlikon |

Wir behalten alle Ausreisser, weil es echte Werte und keine Fehler sind. Gerade die dichten Gemeinden sind für unsere Frage wichtig. Damit sie das Ergebnis nicht verzerren, arbeiten wir mit dem Median und mit Spearman ρ, das nur die Reihenfolge der Gemeinden vergleicht. Zur Kontrolle berechnen wir ρ einmal mit allen Gemeinden und einmal ohne die Flughafengemeinden Kloten, Opfikon, Rümlang.

| Antriebsart | ρ mit allen Gemeinden | ρ ohne Flughafengemeinden |
| --- | --- | --- |
| Benzin | -0.32 | -0.30 |
| Diesel | -0.14 | -0.16 |
| Elektrisch | +0.15 | +0.14 |
| Normal-Hybrid | +0.67 | +0.66 |
| Plug-in-Hybrid | +0.48 | +0.47 |
| Sonstige | -0.06 | -0.04 |

Die grösste Abweichung beträgt 0.02. Die Ausreisser verändern das Ergebnis also kaum.


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
