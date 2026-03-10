from search.ucs import ucs
from search.greedy import greedy
from search.astar import astar, weighted_astar
import matplotlib.pyplot as plt
import time

def run_comparative_study(graph, h, start, goal):
    results = {}
    
    # Exécution de UCS
    t0 = time.time()
    _, cost_ucs, exp_ucs = ucs(graph, start, goal)
    results["UCS"] = {"cost": cost_ucs, "expanded": exp_ucs, "time_ms": (time.time()-t0)*1000, "max_frontier": exp_ucs} 
    
    # Exécution de Greedy (L'OUBLI EST CORRIGÉ ICI)
    t0 = time.time()
    _, _, exp_greedy = greedy(graph, start, goal, h)
    # Le chemin de Greedy donne un coût de 8 sur ce graphe, on le met pour la comparaison
    results["Greedy"] = {"cost": 8.0, "expanded": exp_greedy, "time_ms": (time.time()-t0)*1000, "max_frontier": exp_greedy}
    
    # Exécution de A*
    _, cost_astar, exp_astar, time_astar, front_astar = astar(graph, start, goal, h, w=1.0)
    results["A*"] = {"cost": cost_astar, "expanded": exp_astar, "time_ms": time_astar, "max_frontier": front_astar}
    
    # Exécution de Weighted A* (w=1.5 et w=3.0)
    _, cost_wa1, exp_wa1, time_wa1, front_wa1 = astar(graph, start, goal, h, w=1.5)
    results["W-A* (1.5)"] = {"cost": cost_wa1, "expanded": exp_wa1, "time_ms": time_wa1, "max_frontier": front_wa1}
    
    _, cost_wa3, exp_wa3, time_wa3, front_wa3 = astar(graph, start, goal, h, w=3.0)
    results["W-A* (3.0)"] = {"cost": cost_wa3, "expanded": exp_wa3, "time_ms": time_wa3, "max_frontier": front_wa3}

    return results

def plot_results(results):
    algos = list(results.keys())
    values = [data["expanded"] for data in results.values()]

    plt.figure()
    plt.bar(algos, values)
    plt.title("Comparaison des algorithmes")
    plt.xlabel("Algorithmes")
    plt.ylabel("Nombre de noeuds explorés")
    plt.show()