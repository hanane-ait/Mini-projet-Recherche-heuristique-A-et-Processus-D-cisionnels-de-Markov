# Mini-Projet ENSET : Recherche Heuristique & Processus de Markov

Ce dépôt contient l'implémentation du mini-projet du module **Prise de Décision et Intelligence Artificielle** du **Master SDIA – ENSET Mohammedia**.

Le projet combine deux axes principaux de l'intelligence artificielle :

* **Recherche heuristique sur graphe**
* **Modélisation probabiliste avec les chaînes de Markov**

L'objectif est d'étudier et comparer les performances d'algorithmes de recherche (**A***, **Greedy**, **Weighted A*** ) et d'analyser un processus stochastique classique : **le problème de la ruine du joueur**.

Le projet inclut également plusieurs **extensions avancées (E2, E3, E4, E5)** pour approfondir l'analyse expérimentale.

---

# Objectifs du projet

Les principaux objectifs de ce mini-projet sont :

* Comprendre le fonctionnement des **algorithmes de recherche heuristique**
* Implémenter **A*** et **Greedy Best-First Search**
* Comparer leurs performances sur différents graphes
* Modéliser un problème stochastique avec **les chaînes de Markov**
* Calculer les **probabilités d'absorption et le temps moyen avant absorption**
* Vérifier les résultats théoriques par **simulation Monte Carlo**
* Étudier l'impact de différents paramètres sur le système

---

# Organisation du projet

Le projet est structuré de manière modulaire pour séparer les différentes composantes :

```
projet_ia/
├── main.py                  # Point d'entrée principal (orchestre l'ensemble des tests)
├── README.md                # Documentation du projet
├── data/                    # Dossier généré automatiquement (images, histogrammes, traces)

├── experiments/             # Module d'expérimentation
│   ├── benchmarks.py        # Comparaison des algorithmes (temps, mémoire, nœuds explorés)
│   └── graphs.py            # Graphes de test + générateur aléatoire (Extension E2)

├── markov/                  # Modélisation stochastique
│   ├── absorbing_chain.py   # Calculs matriciels (matrice fondamentale, probabilités)
│   └── simulation.py        # Simulation Monte Carlo

└── search/                  # Recherche heuristique
    ├── astar.py             # Algorithmes A* et Weighted A* (Extension E3)
    └── greedy.py            # Greedy Best-First Search
```

Cette organisation permet de **séparer clairement la logique du projet** :

* `search` → algorithmes de recherche
* `markov` → modélisation probabiliste
* `experiments` → comparaison et tests
* `data` → résultats générés

---

# Installation

## Prérequis

Avant d'exécuter le projet, assurez-vous d'avoir installé :

* **Python 3.8 ou supérieur**

Vérifier la version :

```bash
python --version
```

---

## Installation des dépendances

Dans le dossier du projet (là où se trouve `main.py`), exécutez :

```bash
pip install numpy matplotlib networkx rich
```

### Description des bibliothèques

| Bibliothèque | Rôle                                              |
| ------------ | ------------------------------------------------- |
| numpy        | Calculs matriciels pour les chaînes de Markov     |
| matplotlib   | Génération des graphiques et histogrammes         |
| networkx     | Manipulation et visualisation des graphes         |
| rich         | Affichage de tableaux structurés dans le terminal |

---

# Exécution du projet

Le projet est conçu pour s'exécuter **à partir d'un seul script principal**.

Dans le terminal, exécutez :

```bash
python main.py
```

Le fichier `main.py` orchestre toutes les parties du projet.

---

# Résultats lors de l'exécution

## Résultats dans le terminal

Lors de l'exécution, le programme affiche :

* Un **tableau comparatif des algorithmes**
* Le **coût du chemin trouvé**
* Le **nombre de nœuds explorés**
* La **taille de la frontière**
* Le **temps d'exécution**

Le programme exécute également :

* Test sur un **graphe aléatoire** (Extension E2)
* Analyse de la **chaîne de Markov**
* Comparaison **résultats théoriques vs simulation**
* Analyse de sensibilité des paramètres

---

## Résultats générés dans le dossier `data/`

Le dossier `data/` est créé automatiquement et contient :

```
data/

astar_path_pro.png
Visualisation du chemin trouvé par A*

greedy_path_pro.png
Visualisation du chemin trouvé par Greedy

comparison_histogram.png
Histogramme comparant les performances des algorithmes

traces/
Fichiers détaillant l'évolution des structures OPEN et CLOSED
```

Ces visualisations facilitent l'analyse des résultats.

---

# Extensions réalisées

## Extension E2 : Génération de graphe aléatoire

Un générateur permet de créer automatiquement un graphe de test :

* environ **20 nœuds**
* poids aléatoires
* heuristique générée automatiquement

Cela permet de tester les algorithmes sur des graphes plus réalistes.

---

## Extension E3 : Weighted A*

Une variante de l'algorithme **A*** est implémentée :

```
f(n) = g(n) + w × h(n)
```

où :

* `g(n)` : coût réel du chemin
* `h(n)` : heuristique
* `w` : poids (>1)

Objectif :

* accélérer la recherche
* au prix d'une solution parfois moins optimale.

---

## Extension E4 : Jeu biaisé (Markov)

Dans le problème de la ruine du joueur, la probabilité de gagner peut être modifiée.

Exemple :

```
P(gagner) = 0.6
P(perdre) = 0.4
```

Cela permet d'étudier comment un biais influence :

* la probabilité de ruine
* la durée moyenne du jeu.

---

## Extension E5 : Analyse de sensibilité

Cette extension analyse l'effet de plusieurs paramètres :

* capital initial
* capital cible
* probabilité de gain

L'objectif est d'observer leur influence sur :

* la probabilité d'absorption
* le temps moyen avant absorption.

---

# Méthodes utilisées

## Recherche heuristique

Les algorithmes implémentés sont :

* **A***
* **Greedy Best-First Search**
* **Weighted A***

Les performances sont comparées selon :

* coût du chemin
* nombre de nœuds explorés
* taille de la frontière
* temps d'exécution

---

## Chaînes de Markov

Le problème de la **ruine du joueur** est modélisé comme une **chaîne de Markov absorbante**.

Les étapes de calcul sont :

1. Construction de la matrice de transition
2. Extraction de la sous-matrice **Q**
3. Calcul de la matrice fondamentale

```
N = (I - Q)^(-1)
```

4. Calcul des probabilités d'absorption
5. Simulation **Monte Carlo** pour validation

---

# Conclusion

Ce projet permet d'explorer deux aspects importants de l'intelligence artificielle :

* les **algorithmes de recherche heuristique**
* la **modélisation probabiliste**

Les expérimentations montrent les différences de performance entre les algorithmes et illustrent la validité des modèles théoriques grâce aux simulations.

---


