import heapq
import time

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, end):
    start_time = time.time()

    visited = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}

    queue = [(f_score[start], start)]

    while queue:
        _, current = heapq.heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + graph.edges[current, neighbor].get('weight', 1)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + manhattan_distance(neighbor, end)
                heapq.heappush(queue, (f_score[neighbor], neighbor))

    elapsed = time.time() - start_time

    # Reconstruir o caminho
    path = []
    if end in came_from or start == end:
        node = end
        while node != start:
            path.append(node)
            node = came_from[node]
        path.append(start)
        path.reverse()

    return path, elapsed, visited