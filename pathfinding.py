import heapq
import math

# find_shortest_path
# inputs: graph - graph object, start_node - node id, end_node - node id
# outputs: path - [node ids], path_distance - travel time
def find_shortest_path(graph, start_node, end_node, distance_to_beat=float(math.inf)):
    # if start and end are the same no need to find shortest path
    if (start_node == end_node):
        return ([], 0)

    distances_from_start = {node: distance_to_beat for node in graph}
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
    if shortest_predecessors[end_node] != None:
        current_node = end_node
    else:
        current_node = None
    while current_node is not None:
        path.insert(0, current_node)
        current_node = shortest_predecessors[current_node]

    if path_distance == float(math.inf):
        path = None
    
    return (path, path_distance)