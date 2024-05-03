import typer
from rich import print
from .lib_graphe import Graphe, trouve_arbitrages, trouve_chemin_optimal
import json

application = typer.Typer()


@application.command()
def auteurs():
    """Affiche les auteurs de cette magnifique application"""

    print("Auteurs : \n- Raphael MERCIER\n- Alexis SAVATON")


@application.command()
def devisee():
    """Permet à l'utilisateur de choisir une devise et affiche le chemin optimal pour cette devise si il y a un arbitrage possible"""
    with open("donnees.json", "r") as json_file:
        data = json.load(json_file)
        devises = data["devises"]

    print("Devises disponibles :")
    for i, devise in enumerate(devises, start=1):
        print(f"{i}. {devise}")

    while True:
        try:
            choix = int(input("Choisissez le numero de la devise : "))
            if choix < 1 or choix > len(devises):
                raise ValueError
            break
        except ValueError:
            print("Veuillez entrer un numero de devise valide.")

    devise_initiale = devises[choix - 1]

    graphe_devises = Graphe(devises, data["taux"])
    dictionnaire_taux = graphe_devises.to_dictionnaire_taux()

    arbitrages = trouve_arbitrages(dictionnaire_taux, devise_initiale)
    chemin_optimal = trouve_chemin_optimal(arbitrages)

    print(
        f"Le chemin optimal pour {devise_initiale} est : {chemin_optimal[0]} avec un rendement de {chemin_optimal[1]}"
    )

    while True:
        choix = input("Voulez-vous choisir un montant à convertir ? (o/n) : ")
        if choix == "o":
            while True:
                try:
                    montant = float(input("Entrez le montant à convertir : "))
                    break
                except ValueError:
                    print("Veuillez entrer un montant valide")

            montant_converti = montant * chemin_optimal[1]
            gain = montant_converti - montant
            print(
                f"Le montant converti grâce à cet arbitrage est : {montant_converti}, le gain est de {gain} {devise_initiale}"
            )
            break
        elif choix == "n":
            print("A+")
            break
        else:
            print("Veuillez entrer 'o' pour 'oui' ou 'n' pour 'non'")


@application.command()
def devises_disponibles(json_data=None):
    """Affiche les devises disponibles"""

    if json_data is None:
        with open("donnees.json", "r") as json_file:
            data = json.load(json_file)
    else:
        data = json.loads(json_data)

    print("Devises disponibles :")
    for devise in data["devises"]:
        print(devise)


@application.command()
def taux_de_change():
    """Renvoie le taux de change entre deux devises choisies par l'utilisateur"""

    with open("donnees.json", "r") as json_file:
        data = json.load(json_file)

    graphe_devises = Graphe(data["devises"], data["taux"])
    dictionnaire_taux = graphe_devises.to_dictionnaire_taux()

    while True:
        devise_source = input("Entrez la devise source : ").upper()
        if devise_source in data["devises"]:
            break
        else:
            print(
                "Vous devez entrer une devise valide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
            )

    while True:
        devise_cible = input("Entrez la devise cible : ").upper()
        if devise_cible in data["devises"]:
            break
        else:
            print(
                "Vous devez entrer une devise valide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
            )

    taux = dictionnaire_taux[devise_source][devise_cible]

    print(f"Taux de change entre {devise_source} et {devise_cible} : {taux}")


@application.command()
def convertir():
    """Convertit un montant d'une devise source vers la devise cible"""

    with open("donnees.json", "r") as json_file:
        data = json.load(json_file)

    graphe_devises = Graphe(data["devises"], data["taux"])
    dictionnaire_taux = graphe_devises.to_dictionnaire_taux()

    devise_source = ""
    while devise_source not in data["devises"]:
        devise_source = input("Entrez la devise source : ").upper()
        if devise_source not in data["devises"]:
            print(
                "Devise source invalide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
            )

    devise_cible = ""
    while devise_cible not in data["devises"]:
        devise_cible = input("Entrez la devise cible : ").upper()
        if devise_cible not in data["devises"]:
            print(
                "Devise cible invalide, vous pouvez consulter les devises disponibles avec la commande 'devises_disponibles'"
            )

    taux = dictionnaire_taux[devise_source][devise_cible]

    while True:
        try:
            montant_source = float(
                input(
                    f"Entrez le montant (en {devise_source}) à convertir en {devise_cible} : "
                )
            )
            break
        except ValueError:
            print("Veuillez entrer un montant valide.")

    montant_cible = montant_source * taux

    print(f"Montant converti en {devise_cible} : {montant_cible}")


if __name__ == "__main__":
    application()


# Commandes pour lancer le programme :
# python -m poetry run python -m dossier --help
# python -m poetry run python -m dossier auteurs
# python -m poetry run python -m dossier devisee
# python -m poetry run python -m dossier devises_disponibles
# python -m poetry run python -m dossier taux_de_change
# python -m poetry run python -m dossier convertir

# Commande pour lancer lancer puis installer les modules nécessaires :
# python -m poetry shell
# pip install poetry, rich, pyserde, typer

# $env:PYTHONWARNINGS = "ignore" pour ignorer les warnings


# Interface graphique hors poetry :
# Exécuter le programme avec la commande suivante :
# python -m dossier.interface_graphique
