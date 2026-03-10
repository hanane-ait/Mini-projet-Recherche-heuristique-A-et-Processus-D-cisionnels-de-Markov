import heapq
import time
import os
import csv
from search.utils import reconstruct_path

def astar(graph, start, goal, h, w=1.0, save_trace=False):
    start_time = time.time()
    open_list = [(w * h[start], start)]
    g = {start: 0}
    parent = {start: None}
    closed_set = set()
    expanded_count = 0
    max_frontier = 0

    html_lines = []
    csv_data = []

    if save_trace:
        html_lines.append(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; color: #333; }}
        h2 {{ color: #8e44ad; border-bottom: 2px solid #9b59b6; padding-bottom: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px; border: 1px solid #ddd; text-align: center; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .code {{ font-family: Consolas, monospace; background-color: #f5eef8; padding: 4px; border-radius: 4px; color: #8e44ad;}}
        </style></head><body>""")
        
        html_lines.append(f"<h2>SIMULATION PAS À PAS : ALGORITHME A* (w={w})</h2>")
        html_lines.append("<p><em>Note : Pour A*, la fonction d'évaluation est f(n) = g(n) + h(n).</em></p>")
        html_lines.append("<table><tr><th>Étape</th><th>Nœud Extrait</th><th>g(n)</th><th>h(n)</th><th>f(n)</th><th>État de la Frontière (OPEN)</th></tr>")
        
        csv_data.append(["Étape", "Nœud Extrait", "g(n)", "h(n)", "f(n)", "État de la Frontière (OPEN)"])

    while open_list:
        max_frontier = max(max_frontier, len(open_list))
        
        if save_trace:
            open_str = ", ".join([f"{n}(f={f_val:.1f})" for f_val, n in sorted(open_list)])

        f_val, node = heapq.heappop(open_list)

        if save_trace:
            node_g = g.get(node, 0)
            node_h = h.get(node, 0)
            html_lines.append(f"<tr><td><b>{expanded_count}</b></td><td><b>{node}</b></td><td>{node_g}</td><td>{node_h}</td><td><b>{f_val:.1f}</b></td><td style='text-align:left;'><span class='code'>[{open_str}]</span></td></tr>")
            csv_data.append([expanded_count, node, node_g, node_h, round(f_val, 1), f"[{open_str}]"])

        if node == goal:
            execution_time = (time.time() - start_time) * 1000
            if save_trace:
                html_lines.append("</table>")
                html_lines.append("<h3 style='color: #27ae60;'>[SUCCÈS] Nœud BUT atteint !</h3>")
                path = reconstruct_path(parent, goal)
                html_lines.append(f"<h3>Chemin optimal trouvé : <span class='code'>{' &rarr; '.join(path)}</span></h3></body></html>")
                
                if not os.path.exists('data'):
                    os.makedirs('data')
                
                with open("data/trace_astar.html", "w", encoding="utf-8") as f:
                    f.write("\n".join(html_lines))
                    
                with open("data/trace_astar.csv", "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerows(csv_data)
                    
            return reconstruct_path(parent, goal), g[goal], expanded_count, execution_time, max_frontier

        if node in closed_set:
            continue
            
        closed_set.add(node)
        expanded_count += 1

        for neighbor, cost in graph.get(node, []):
            new_g = g[node] + cost
            
            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                parent[neighbor] = node
                f = new_g + (w * h.get(neighbor, 0))
                heapq.heappush(open_list, (f, neighbor))
                if neighbor in closed_set:
                    closed_set.remove(neighbor)

    return None, float('inf'), expanded_count, 0, max_frontier

def weighted_astar(graph, start, goal, h, w=1.5):
    open_list = []
    heapq.heappush(open_list, (0, start))
    g = {start: 0}
    parent = {start: None}
    expanded = 0

    while open_list:
        f, node = heapq.heappop(open_list)
        expanded += 1
        if node == goal:
            break
        for neighbor, cost in graph[node]:
            new_g = g[node] + cost
            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                parent[neighbor] = node
                f = new_g + w * h[neighbor]
                heapq.heappush(open_list, (f, neighbor))

    path = reconstruct_path(parent, goal)
    return path, g[goal], expanded