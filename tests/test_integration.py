from unittest.mock import patch
from dossier.__main__ import (
    convertir,
    devises_disponibles,
    taux_de_change,
    auteurs,
    devisee,
)


@patch("builtins.print")
def test_devises_disponibles_integration(mock_print, capsys):

    json_data = '{"devises": ["USD", "EUR", "GBP", "MUR", "YEN"]}'

    devises_disponibles(json_data=json_data)

    captured = capsys.readouterr().out
    assert captured == "Devises disponibles :\nUSD\nEUR\nGBP\nMUR\nYEN\n"


@patch("dossier.__main__.print")
def test_auteurs(mock_print):
    auteurs()
    mock_print.assert_called_with("Auteurs : \n- Raphael MERCIER\n- Alexis SAVATON")


@patch("builtins.input", side_effect=["EUR", "USD"])
@patch("dossier.__main__.print")
def test_taux_de_change_integration(mock_print, mock_input):
    taux_de_change()

    assert mock_print.call_count == 1

    mock_print.assert_called_once_with("Taux de change entre EUR et USD : 0.92")


@patch("builtins.input", side_effect=["NUL", "EUR", "USD"])
@patch("dossier.__main__.print")
def test_taux_de_change_invalide_integration(mock_print, mock_input):
    taux_de_change()

    assert mock_print.call_count == 2
    mock_print.assert_any_call(
        "Vous devez entrer une devise valide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
    )
    mock_print.assert_any_call("Taux de change entre EUR et USD : 0.92")


@patch("builtins.input", side_effect=["NUL", "EUR", "NUL", "USD"])
@patch("dossier.__main__.print")
def test_taux_de_change_invalide_2_integration(mock_print, mock_input):
    taux_de_change()

    assert mock_print.call_count == 3
    mock_print.assert_any_call(
        "Vous devez entrer une devise valide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
    )
    mock_print.assert_any_call("Taux de change entre EUR et USD : 0.92")


@patch("builtins.input", side_effect=["EUR", "USD", "1000"])
@patch("dossier.__main__.print")
def test_convertir_integration(mock_print, mock_input):
    convertir()
    mock_print.assert_called_once_with("Montant converti en USD : 920.0")


@patch("builtins.input", side_effect=["EUR", "NUL", "USD", 1000])
@patch("dossier.__main__.print")
def test_convertir_devise_invalide_integration(mock_print, mock_input):
    convertir()

    assert mock_print.call_count == 2

    mock_print.assert_any_call(
        "Devise cible invalide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
    )
    mock_print.assert_any_call("Montant converti en USD : 920.0")


@patch("builtins.input", side_effect=["NUL", "EUR", "NUL", "USD", 1000])
@patch("dossier.__main__.print")
def test_convertir_devise_invalide_2_integration(mock_print, mock_input):
    convertir()

    assert mock_print.call_count == 3

    mock_print.assert_any_call(
        "Devise cible invalide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
    )
    mock_print.assert_any_call("Montant converti en USD : 920.0")


@patch("builtins.input", side_effect=["7", "5", "n"])
@patch("dossier.__main__.print")
def test_affiche_devise_integration(mock_print, mock_input):
    devisee()

    assert mock_print.call_count == 9
    mock_print.assert_any_call("Veuillez entrer un numero de devise valide.")
    mock_print.assert_any_call("Devises disponibles :")
    mock_print.assert_any_call("1. USD")
    mock_print.assert_any_call("2. EUR")
    mock_print.assert_any_call("3. GBP")
    mock_print.assert_any_call("4. MUR")
    mock_print.assert_any_call("5. YEN")
    mock_print.assert_any_call(
        "Le chemin optimal pour YEN est : ['YEN', 'MUR', 'USD', 'GBP', 'EUR', 'YEN'] avec un rendement de 1.25084369088"
    )
    mock_print.assert_any_call("A+")


@patch("builtins.input", side_effect=["5", "o", "1000"])
@patch("dossier.__main__.print")
def test_affiche_devise_2_integration(mock_print, mock_input):
    devisee()

    assert mock_print.call_count == 8

    mock_print.assert_any_call("Devises disponibles :")
    mock_print.assert_any_call("1. USD")
    mock_print.assert_any_call("2. EUR")
    mock_print.assert_any_call("3. GBP")
    mock_print.assert_any_call("4. MUR")
    mock_print.assert_any_call(
        "Le chemin optimal pour YEN est : ['YEN', 'MUR', 'USD', 'GBP', 'EUR', 'YEN'] avec un rendement de 1.25084369088"
    )
    mock_print.assert_any_call(
        "Le montant converti grâce à cet arbitrage est : 1250.84369088, le gain est de 250.84369087999994 YEN"
    )


@patch("builtins.input", side_effect=["6", "5", "o", "1000"])
@patch("dossier.__main__.print")
def test_affiche_devise_3_integration(mock_print, mock_input):
    devisee()

    assert mock_print.call_count == 9

    mock_print.assert_any_call("Devises disponibles :")
    mock_print.assert_any_call("1. USD")
    mock_print.assert_any_call("2. EUR")
    mock_print.assert_any_call("3. GBP")
    mock_print.assert_any_call("4. MUR")
    mock_print.assert_any_call("Veuillez entrer un numero de devise valide.")
    mock_print.assert_any_call(
        "Le chemin optimal pour YEN est : ['YEN', 'MUR', 'USD', 'GBP', 'EUR', 'YEN'] avec un rendement de 1.25084369088"
    )
    mock_print.assert_any_call(
        "Le montant converti grâce à cet arbitrage est : 1250.84369088, le gain est de 250.84369087999994 YEN"
    )
