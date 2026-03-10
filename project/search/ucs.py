import heapq
from search.utils import reconstruct_path

def ucs(graph, start, goal):

    open_list = []
    heapq.heappush(open_list, (0, start))

    g = {start: 0}
    parent = {start: None}

    expanded = 0

    while open_list:

        cost, node = heapq.heappop(open_list)
        expanded += 1

        if node == goal:
            break

        for neighbor, c in graph[node]:

            new_cost = g[node] + c

            if neighbor not in g or new_cost < g[neighbor]:

                g[neighbor] = new_cost
                parent[neighbor] = node

                heapq.heappush(open_list, (new_cost, neighbor))

    path = reconstruct_path(parent, goal)

    return path, g[goal], expanded