import pandas as pd
import pytest

from src.pipeline import run_pipeline
from src.transform import ANTRIEBS_SPALTEN, ANZAHL_GEMEINDEN, DICHTEKLASSEN, JAHRE, ausreisser_finden


@pytest.fixture(scope="module")
def daten():
    """Die Pipeline läuft nur einmal für alle Tests."""
    return run_pipeline()


def test_alle_gemeinden_in_jedem_jahr(daten):
    gemeinden, _ = daten
    assert (gemeinden.groupby("Jahr")["gemeinde_nr"].nunique() == ANZAHL_GEMEINDEN).all()
    assert gemeinden["Jahr"].nunique() == len(JAHRE)


def test_gemeinde_und_jahr_sind_eindeutig(daten):
    gemeinden, _ = daten
    assert not gemeinden.duplicated(["gemeinde_nr", "Jahr"]).any()


def test_keine_fehlenden_oder_negativen_werte(daten):
    gemeinden, _ = daten
    zahlen = gemeinden[["einwohner", "flaeche_km2", "pkw", *ANTRIEBS_SPALTEN.values()]]
    assert zahlen.notna().all().all()
    assert (zahlen >= 0).all().all()


def test_anteile_ergeben_100_prozent(daten):
    gemeinden, _ = daten
    summe = gemeinden[[f"{spalte}_anteil" for spalte in ANTRIEBS_SPALTEN.values()]].sum(axis=1)
    assert summe.round(6).eq(100).all()


def test_kantonssumme_passt_zu_gemeinden(daten):
    gemeinden, antriebe = daten
    pro_jahr_gemeinden = gemeinden.groupby("Jahr")["pkw"].sum()
    pro_jahr_kanton = antriebe.groupby("Jahr")["Fahrzeuge"].sum()
    assert pro_jahr_gemeinden.equals(pro_jahr_kanton)


def test_dichteklassen_gleich_gross(daten):
    gemeinden, _ = daten
    letztes_jahr = gemeinden[gemeinden["Jahr"] == gemeinden["Jahr"].max()]
    anzahl = letztes_jahr["dichteklasse"].value_counts()
    assert set(anzahl.index) == set(DICHTEKLASSEN)
    assert (anzahl == ANZAHL_GEMEINDEN / 4).all()


def test_ausreisser_finden():
    werte = pd.Series([10, 11, 12, 13, 14, 100])
    assert ausreisser_finden(werte).tolist() == [100]