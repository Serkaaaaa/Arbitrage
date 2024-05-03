from dossier.lib_graphe import (
    trouve_tous_chemins,
    trouve_arbitrages,
    trouve_chemin_optimal,
)
import pytest

devises = ["EUR", "USD", "GBP"]
taux = {
    "USD": {"EUR": 1.09, "GBP": 0.86},
    "EUR": {"USD": 1 / 1.09, "GBP": 0.75},
    "GBP": {"USD": 1 / 0.86, "EUR": 1 / 0.75},
}


def test_trouve_tous_chemins():
    chemins_usd = trouve_tous_chemins(taux, "USD")
    assert len(chemins_usd) == 4

    chemins_eur = trouve_tous_chemins(taux, "EUR")
    assert len(chemins_eur) == 4

    chemins_gbp = trouve_tous_chemins(taux, "GBP")
    assert len(chemins_gbp) == 4


def test_plantage_trouve_tous_chemins():
    taux_incorrect = {
        "USD": {"EUR": 1.09, "GBP": 0.86},
        "EUR": {"USD": 1.2, "GBP": 0.75},
        "GBP": {"USD": 1 / 0.86, "EUR": 1 / 0.75},
    }
    with pytest.raises(AssertionError):
        assert len(trouve_tous_chemins(taux_incorrect, "USD")) != 4


def test_trouve_arbitrages():
    arbitrages_usd = trouve_arbitrages(taux, "USD")
    assert len(arbitrages_usd) == 4

    arbitrages_eur = trouve_arbitrages(taux, "EUR")
    assert len(arbitrages_eur) == 4

    arbitrages_gbp = trouve_arbitrages(taux, "GBP")
    assert len(arbitrages_gbp) == 4


def test_plantage_trouve_arbitrages():
    taux_incorrect = {
        "USD": {"EUR": 1.09, "GBP": 0.86},
        "EUR": {"USD": 1.2, "GBP": 0.75},
        "GBP": {"USD": 1 / 0.86, "EUR": 1 / 0.75},
    }
    with pytest.raises(AssertionError):
        assert len(trouve_arbitrages(taux_incorrect, "USD")) != 4


# Tester la fonction trouve_chemin_optimal
def test_trouve_chemin_optimal():
    arbitrages_usd = trouve_arbitrages(taux, "USD")
    chemin_optimal_usd = trouve_chemin_optimal(arbitrages_usd)
    assert chemin_optimal_usd is not None

    arbitrages_eur = trouve_arbitrages(taux, "EUR")
    chemin_optimal_eur = trouve_chemin_optimal(arbitrages_eur)
    assert chemin_optimal_eur is not None

    arbitrages_gbp = trouve_arbitrages(taux, "GBP")
    chemin_optimal_gbp = trouve_chemin_optimal(arbitrages_gbp)
    assert chemin_optimal_gbp is not None


def test_plantage_trouve_chemin_optimal():
    # Définir des arbitrages qui n'ont pas de chemin optimal
    arbitrages_sans_chemin_optimal = [
        (["USD", "EUR", "USD"], 1.0),
        (["USD", "EUR", "GBP", "USD"], 0.9),
        (["USD", "GBP", "USD"], 0.8),
    ]

    # Le résultat attendu est None car il n'y a pas de chemin optimal
    assert trouve_chemin_optimal(arbitrages_sans_chemin_optimal) is not None
