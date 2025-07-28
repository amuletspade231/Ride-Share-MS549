import heapq
import math

def find_shortest_path(graph, start_node, end_node):
    distances_from_start = {node: math.inf for node in graph}
    distances_from_start[start_node] = 0
    shortest_predecessors = {node: None for node in graph}
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances_from_start[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            neighbor_distance = current_distance + weight
            if neighbor_distance < distances_from_start[neighbor]:
                distances_from_start[neighbor] = neighbor_distance
                shortest_predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (neighbor_distance, neighbor))

    path = []
    path_distance = distances_from_start[end_node]
    current_node = end_node
    while current_node is not None:
        path.insert(0, current_node)
        current_node = shortest_predecessors[current_node]

    if path_distance == math.inf:
        path = None
    
    return (path, path_distance)