from dataclasses import dataclass
from collections import deque
from typing import List, Dict, Tuple, Optional


@dataclass
class Graphe:
    """Représente un graphe constitué de sommets et d'arêtes.

    Args:
        sommets (list): Liste des sommets du graphe.
        arretes (list): Liste des arêtes du graphe, représentées par des listes de poids.

    Raises:
        ValueError: Si un sommet de départ d'une arête n'appartient pas à la liste des sommets du graphe.
        ValueError: Si un sommet d'arrivée d'une arête n'appartient pas à la liste des sommets du graphe.
    """

    sommets: List[str]
    arretes: List[List[int]]

    def __post_init__(self) -> None:
        for i, depart in enumerate(self.sommets):
            for j, arrivee in enumerate(self.sommets):
                if i != j:
                    poids = self.arretes[i][j]
                    if poids != 0:
                        if depart not in self.sommets:
                            raise ValueError(
                                f"{depart=} n'est pas dans la liste des sommets!"
                            )
                        if arrivee not in self.sommets:
                            raise ValueError(
                                f"{arrivee=} n'est pas dans la liste des sommets!"
                            )

    def to_dictionnaire_taux(self) -> Dict[str, Dict[str, int]]:
        """Convertit le graphe en un dictionnaire de taux de change.

        Returns:
            dict: Un dictionnaire associant chaque devise à un dictionnaire contenant
                  les taux de change avec toutes les autres devises.
        """
        return dictionnaire_devise_taux(self.sommets, self.arretes)


def dictionnaire_devise_taux(
    devises: List[str], taux: List[List[int]]
) -> Dict[str, Dict[str, int]]:
    """Crée un dictionnaire associant chaque devise à ses taux de change.

    Args:
        devises (list): Une liste des devises disponibles.
        taux (list): Une liste des taux de change entre les devises.

    Returns:
        dict: Un dictionnaire associant chaque devise à un dictionnaire contenant
              les taux de change avec toutes les autres devises.
    """
    return {devise: dict(zip(devises, taux[i])) for i, devise in enumerate(devises)}


def trouve_tous_chemins(
    dictionnaire: Dict[str, Dict[str, int]], devise_initiale: str
) -> List[List[str]]:
    """Trouve tous les chemins possibles à partir d'une devise initiale.

    Args:
        dictionnaire (dict): Un dictionnaire représentant les relations de change entre devises.
        devise_initiale (str): La devise de départ pour trouver les chemins possibles.

    Returns:
        list: Une liste contenant tous les chemins possibles à partir de la devise initiale.
    """
    queue = deque([(devise_initiale, [devise_initiale])])
    chemins = []

    while queue:
        devise, chemin = queue.popleft()
        for voisin in dictionnaire[devise]:
            if voisin not in chemin:
                queue.append((voisin, chemin + [voisin]))
                chemins.append(chemin + [voisin] + [devise_initiale])
    return chemins


def trouve_arbitrages(
    dictionnaire: Dict[str, Dict[str, int]], devise_initiale: str
) -> List[Tuple[List[str], float]]:
    """Trouve des opportunités d'arbitrage entre les devises.

    Args:
        dictionnaire (dict): Un dictionnaire associant chaque devise à un dictionnaire contenant
                             les taux de change avec toutes les autres devises.
        devise_initiale (str): La devise de départ pour trouver les arbitrages.

    Returns:
        list: Une liste de tuples contenant les arbitrages possibles et leur rendement.
    """
    chemins = trouve_tous_chemins(dictionnaire, devise_initiale)
    arbitrages = []
    for chemin in chemins:
        rendement = 1.0
        for i in range(len(chemin) - 1):
            rendement *= dictionnaire[chemin[i]][chemin[i + 1]]
        arbitrages.append((chemin, rendement))
    return arbitrages


def trouve_chemin_optimal(
    arbitrages: List[Tuple[List[str], float]]
) -> Optional[Tuple[List[str], float]]:
    """Trouve le chemin optimal parmi les opportunités d'arbitrage.

    Args:
        arbitrages (list): Une liste de tuples contenant les arbitrages possibles et leur rendement.

    Returns:
        tuple: Le chemin optimal et son rendement, ou None si aucun chemin n'est trouvé.
    """
    chemin_optimal = None
    rendement_optimal = 0.0

    for chemin, rendement in arbitrages:
        if rendement > rendement_optimal:
            chemin_optimal = chemin
            rendement_optimal = rendement

    if chemin_optimal is None:
        return None
    else:
        return chemin_optimal, rendement_optimal
