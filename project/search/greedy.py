import heapq
import os
import csv
from search.utils import reconstruct_path

def greedy(graph, start, goal, h, save_trace=False):
    open_list = []
    heapq.heappush(open_list, (h[start], start))
    parent = {start: None}
    visited = set()
    g = {start: 0}
    expanded = 0

    html_lines = []
    csv_data = []
    
    if save_trace:
        # Entête HTML avec du style CSS professionnel
        html_lines.append("""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; color: #333; }
        h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: center; }
        th { background-color: #34495e; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .code { font-family: Consolas, monospace; background-color: #e8f4f8; padding: 4px; border-radius: 4px; color: #2980b9;}
        </style></head><body>""")
        
        html_lines.append("<h2>SIMULATION PAS À PAS : GREEDY BEST-FIRST SEARCH</h2>")
        html_lines.append("<p><em>Note : Pour Greedy, la fonction d'évaluation f(n) = h(n). Le coût g(n) est affiché à titre informatif.</em></p>")
        html_lines.append("<table><tr><th>Étape</th><th>Nœud Extrait</th><th>g(n)</th><th>h(n)</th><th>f(n)</th><th>État de la Frontière (OPEN)</th></tr>")
        
        csv_data.append(["Étape", "Nœud Extrait", "g(n)", "h(n)", "f(n)", "État de la Frontière (OPEN)"])

    while open_list:
        if save_trace:
            open_str = ", ".join([f"{n}(h={val})" for val, n in sorted(open_list)])

        val_h, node = heapq.heappop(open_list)
        
        if save_trace:
            node_g = g.get(node, 0)
            html_lines.append(f"<tr><td><b>{expanded}</b></td><td><b>{node}</b></td><td>{node_g}</td><td>{val_h}</td><td><b>{val_h}</b></td><td style='text-align:left;'><span class='code'>[{open_str}]</span></td></tr>")
            csv_data.append([expanded, node, node_g, val_h, val_h, f"[{open_str}]"])

        expanded += 1

        if node == goal:
            if save_trace:
                html_lines.append("</table>")
                html_lines.append("<h3 style='color: #27ae60;'>[SUCCÈS] Nœud BUT atteint !</h3>")
            break

        visited.add(node)

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                if neighbor not in [n for _, n in open_list]:
                    parent[neighbor] = node
                    g[neighbor] = g.get(node, 0) + cost
                    heapq.heappush(open_list, (h[neighbor], neighbor))

    path = reconstruct_path(parent, goal)
    
    if save_trace:
        html_lines.append(f"<h3>Chemin final trouvé : <span class='code'>{' &rarr; '.join(path)}</span></h3></body></html>")
        
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Sauvegarde au format HTML (Beauté visuelle)
        with open("data/trace_greedy.html", "w", encoding="utf-8") as f:
            f.write("\n".join(html_lines))
            
        # Sauvegarde au format CSV (Pour Excel)
        with open("data/trace_greedy.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(csv_data)

    return path, None, expanded