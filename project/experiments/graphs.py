import random

def example_graph():
    # Structure du graphe orienté pondéré
    graph = {
        "A": [("B", 2), ("C", 4)],
        "B": [("D", 1), ("E", 5)],
        "C": [("F", 3)],
        "D": [("G", 2)],
        "E": [("G", 1)],
        "F": [("G", 2)],
        "G": []
    }
    # Heuristique admissible et cohérente (de base)
    h = {"A": 6, "B": 4, "C": 4, "D": 2, "E": 1, "F": 2, "G": 0}
    
    # Coordonnées (x, y) pour la visualisation des chemins
    pos = {
        "A": (0, 1), "B": (1, 2), "C": (1, 0),
        "D": (2, 2), "E": (2, 1), "F": (2, 0),
        "G": (3, 1)
    }
    return graph, h, pos

def get_heuristic_variations():
    """Répond à la question II.5 du cahier des charges"""
    # 1. Heuristique admissible et cohérente (h <= h* et respecte l'inégalité triangulaire)
    h_admissible_coherente = {"A": 6, "B": 4, "C": 4, "D": 2, "E": 1, "F": 2, "G": 0}
    
    # 2. Heuristique admissible mais NON cohérente (ex: on sous-estime B fortement)
    h_admissible_non_coherente = {"A": 6, "B": 1, "C": 4, "D": 2, "E": 1, "F": 2, "G": 0}
    
    # 3. Heuristique NON admissible (ex: on surestime fortement B par rapport au coût réel)
    h_non_admissible = {"A": 6, "B": 15, "C": 4, "D": 2, "E": 1, "F": 2, "G": 0}
    
    return h_admissible_coherente, h_admissible_non_coherente, h_non_admissible

def generate_random_graph(n=10, p=0.3):
    nodes = [f"N{i}" for i in range(n)]
    graph = {node: [] for node in nodes}
    for node in nodes:
        for other in nodes:
            if node != other and random.random() < p:
                graph[node].append((other, random.randint(1, 10)))
    h = {node: random.randint(0, 10) for node in nodes}
    return graph, h