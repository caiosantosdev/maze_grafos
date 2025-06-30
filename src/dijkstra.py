import heapq
import time

def dijkstra_custom(graph, start, end):
    start_time = time.time()

    visited = set()
    came_from = {}
    distances = {start: 0}
    queue = [(0, start)]

    while queue:
        current_dist, current = heapq.heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        for neighbor in graph.neighbors(current):
            if neighbor in visited:
                continue

            new_dist = current_dist + graph.edges[current, neighbor].get('weight', 1)
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                came_from[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))

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