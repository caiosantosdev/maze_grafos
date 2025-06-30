import heapq
import time

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, end):
    start_time = time.time()

    open_set = []
    # f(n), h(n), current -> desempate por h(n)
    heapq.heappush(open_set, (0 + manhattan_distance(start, end), manhattan_distance(start, end), start))

    came_from = {}
    g_score = {start: 0}
    visited = set()
    in_open_set = {start}

    while open_set:
        _, _, current = heapq.heappop(open_set)
        in_open_set.discard(current)

        if current == end:
            break

        visited.add(current)

        # Ordenar vizinhos priorizando direção ao destino
        neighbors = list(graph.neighbors(current))
        neighbors.sort(key=lambda n: manhattan_distance(n, end))  # Prioriza mais próximos primeiro

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + graph.edges[current, neighbor].get('weight', 1)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h = manhattan_distance(neighbor, end)
                f = tentative_g + h

                if neighbor not in in_open_set:
                    heapq.heappush(open_set, (f, h, neighbor))  # f como prioridade principal, h como desempate
                    in_open_set.add(neighbor)

    elapsed = time.time() - start_time

    # Reconstrução do caminho
    path = []
    if end in came_from or start == end:
        node = end
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        path.reverse()

    return path, elapsed, visited