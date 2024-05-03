# Projet en Python pour répondre à cette problématique :

Un arbitrage consiste à utiliser les différences entre les taux de changes pour gagner de l'argent en une monnaie par une série de conversion.

Par exemple si on échange

1 euro contre 49 roupies
1 roupie contre 2 yen
1 yen contre 0.0107 euros
Le chemin total permet de convertir 1 euro en 1.0486 euros.

On suppose données n devises et une table n x n pour les taux de change.

Déterminer si des séquences d'arbitrage existent. Lesquelles rapportent le plus et lesquelles ont le moins d'étapes.

**Graphe :**
-
- il faut un chemin qui passe max une fois par une devise
- calculer tous les chemins possibles:
    - exemple : 3 sommets : A,B,C
        - A-A
        - A-B-A
        - A-B-C-A
        - A-C-A
        - A-C-B-A

        ```mermaid
        graph TD;
            A[EUR]-->D[EUR];
            A-->B[USD];
            A-->C[YEN];
            B-->Y[EUR];
            B-->Z[YEN];
            C-->X[EUR];
            C-->W[USD];
            Z-->U[EUR];
            W-->V[EUR]
        ```
        
**tableau des devises :**
- 
| Devise |  EUR  |  USD  |  YEN  |
| :-----:|:-----:|:-----:|:-----:|
|  EUR   |   1   |  0.92 | 164.28|
|  USD   |  1.09 |   1   | 153.25|
|  YEN   | 0.0061| 0.0052|   1   |






