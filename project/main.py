import os
import matplotlib.pyplot as plt
import networkx as nx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Imports des modules du projet
from experiments.graphs import example_graph, get_heuristic_variations, generate_random_graph
from experiments.benchmarks import run_comparative_study
from markov.absorbing_chain import compute_markov_analysis
from markov.simulation import monte_carlo
from search.astar import astar
from search.greedy import greedy

console = Console()

def print_professional_table(results):
    table = Table(title="[bold]Tableau Comparatif des Performances[/bold]", show_header=True, header_style="bold magenta", border_style="cyan")
    table.add_column("Algorithme", style="dim", width=15)
    table.add_column("Coût", justify="right")
    table.add_column("Explorés", justify="right", style="green")
    table.add_column("Frontière Max", justify="right", style="yellow")
    table.add_column("Temps (ms)", justify="right", style="blue")

    for algo, data in results.items():
        table.add_row(algo, f"{data['cost']:.1f}", f"{data['expanded']:.1f}", f"{data['max_frontier']:.1f}", f"{data['time_ms']:.4f}")
    console.print(table)

def save_comparative_histogram(search_results):
    algos = list(search_results.keys())
    expanded = [data['expanded'] for data in search_results.values()]
    frontier = [data['max_frontier'] for data in search_results.values()]

    plt.figure(figsize=(12, 6))
    x = range(len(algos))
    
    plt.bar(x, expanded, width=0.4, label='Nœuds Explorés', color='#3498DB', align='center')
    plt.bar([i + 0.4 for i in x], frontier, width=0.4, label='Taille Frontière (OPEN)', color='#2ECC71', align='center')

    plt.xlabel('Algorithmes', fontweight='bold')
    plt.ylabel('Nombre de Nœuds')
    plt.title('Analyse de l\'Efficacité et de la Complexité Spatiale')
    plt.xticks([i + 0.2 for i in x], algos)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('data/comparison_histogram.png', dpi=300)
    plt.close()

def visualize_optimal_path(graph, pos, path, title, filename):
    G = nx.DiGraph()
    for u in graph:
        for v, weight in graph[u]:
            G.add_edge(u, v, weight=weight)
    
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='#ECF0F1', node_size=2500, font_size=11, font_weight='bold', edge_color='#BDC3C7', arrows=True)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#E74C3C', node_size=2500)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#E74C3C', width=4)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title(title, fontsize=15, fontweight='bold', color='#2C3E50')
    plt.savefig(f'data/{filename}', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    if not os.path.exists('data'): 
        os.makedirs('data')
        
    console.rule("[bold red]MINI-PROJET ENSET : RECHERCHE HEURISTIQUE ET MDP")

    graph, h, pos = example_graph()
    
    console.print("\n[bold yellow][INFO][/bold yellow] Génération des traces pas à pas dans le dossier 'data/'...")
    
    # 1. Trace et Image pour GREEDY
    path_greedy, _, _ = greedy(graph, "A", "G", h, save_trace=True)
    visualize_optimal_path(graph, pos, path_greedy, "Chemin trouvé par l'algorithme Greedy (Glouton)", "greedy_path_pro.png")
    
    # 2. Trace et Image pour A*
    path_astar, cost_astar, _, _, _ = astar(graph, "A", "G", h, save_trace=True)
    visualize_optimal_path(graph, pos, path_astar, "Chemin optimal trouvé par l'algorithme A*", "astar_path_pro.png")
    
    console.print("[bold green][SUCCÈS][/bold green] Fichiers 'trace_greedy.html' et 'trace_astar.html' créés dans data/.")
    console.print("[bold green][SUCCÈS][/bold green] Images des graphes générées dans data/.\n")

    # 3. Tableau comparatif avec Greedy
    results = run_comparative_study(graph, h, "A", "G")
    print_professional_table(results)
    save_comparative_histogram(results)
    console.print("[bold green][INFO][/bold green] Histogramme 'comparison_histogram.png' généré dans data/.")


    # ==========================================================
    # MISE EN ÉVIDENCE DE L'EXTENSION E2 et III.5
    # ==========================================================
    console.print("\n")
    console.rule("[bold magenta]EXTENSION E2 & III.5 : TEST SUR GRAPHE ALÉATOIRE")
    console.print("[dim]Génération automatique d'un graphe de 20 nœuds...[/dim]")
    
    # On génère un graphe aléatoire de 20 nœuds
    rand_graph, rand_h = generate_random_graph(n=20, p=0.4)
    
    # On teste le benchmark sur ce nouveau graphe (de N0 vers N19)
    try:
        rand_results = run_comparative_study(rand_graph, rand_h, "N0", "N19")
        console.print("[bold green]Performances sur le graphe aléatoire généré :[/bold green]")
        print_professional_table(rand_results)
    except KeyError:
        console.print("[bold yellow]Chemin inaccessible sur ce graphe aléatoire spécifique.[/bold yellow]")
    # ==========================================================


    # --- PARTIE II : MARKOV ---
    console.print("\n")
    console.rule("[bold blue]SECTION MARKOV ET SIMULATION (RUINE DU JOUEUR)")
    
    # Analyse de base pour l'état 2 avec p=0.5 (Exigence V.1 à V.6)
    N, t, B = compute_markov_analysis(p=0.5)
    mc_win, mc_loss, mc_time = monte_carlo(2, trials=20000, p=0.5)
    
    markov_content = (
        f"[bold cyan]Résultats Analytiques pour l'état 2 (p=0.5):[/bold cyan]\n"
        f" • Probabilité de Ruine (0) : [bold red]{B[1,0]:.4f}[/bold red]\n"
        f" • Probabilité de Gain  (6) : [bold green]{B[1,1]:.4f}[/bold green]\n"
        f" • Espérance de temps      : [bold white]{t[1]:.2f} étapes[/bold white]\n\n"
        f"[bold cyan]Validation Monte Carlo (20 000 essais):[/bold cyan]\n"
        f" • P(gain) observé : {mc_win:.4f}\n"
        f" • P(perte) observé: {mc_loss:.4f}\n"
        f" • Temps moyen     : {mc_time:.4f} étapes"
    )
    console.print(Panel(markov_content, title="[bold magenta]ANALYSE DE BASE[/bold magenta]", border_style="green", expand=False))

    # ==========================================================
    # EXTENSIONS E4 ET E5
    # ==========================================================
    console.print("\n[bold yellow]Extensions de haut niveau (E4 et E5) :[/bold yellow]")
    
    # Sensibilité selon la fortune initiale (E5)
    table_e5 = Table(title="[bold]Sensibilité de l'espérance du temps (p=0.5)[/bold]", show_header=True, header_style="bold cyan")
    table_e5.add_column("Fortune Initiale")
    table_e5.add_column("Temps Analytique (étapes)")
    table_e5.add_column("Probabilité de Victoire")
    for i in range(1, 6):
        table_e5.add_row(f"État {i}", f"{t[i-1]:.2f}", f"{B[i-1,1]:.4f}")
    console.print(table_e5)

    # Probabilités asymétriques (E4) : Exemple p=0.4 (le joueur est désavantagé)
    N_asym, t_asym, B_asym = compute_markov_analysis(p=0.4)
    table_e4 = Table(title="[bold]Probabilités Asymétriques (Jeu déséquilibré : p=0.4)[/bold]", show_header=True, header_style="bold red")
    table_e4.add_column("Fortune Initiale")
    table_e4.add_column("Temps Analytique")
    table_e4.add_column("Probabilité de Victoire")
    for i in range(1, 6):
        table_e4.add_row(f"État {i}", f"{t_asym[i-1]:.2f}", f"{B_asym[i-1,1]:.4f}")
    console.print(table_e4)

if __name__ == "__main__":
    main()