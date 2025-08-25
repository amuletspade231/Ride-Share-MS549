import csv
import collections
import pathfinding
import argparse
import math

class Graph:
    """
    Represents a city map with both topological (edges) 
    and geometric (node coordinates) data.
    """
    def __init__(self):
        self.adjacency_list = collections.defaultdict(list) # {start node id: [neighbor node ids]}
        self.node_coordinates = {} # {node id: (x, y)}

    # load_map_data - creates graph based on csv file contents
    def load_map_data(self, filename):
        """
        Loads all map data from the single, unified 7-column CSV file.
        This method populates BOTH the adjacency_list and node_coordinates.
        """
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.strip().split(',')
                start_id, start_x, start_y, end_id, end_x, end_y, weight = parts
                
                # Store the coordinates for both nodes
                self.node_coordinates[start_id] = (float(start_x), float(start_y))
                self.node_coordinates[end_id] = (float(end_x), float(end_y))
                
                # Store the edge for the undirected graph
                self.adjacency_list[start_id].append((end_id, float(weight)))
                self.adjacency_list[end_id].append((start_id, float(weight)))

    # calculate_route - finds shortest route based on weighted graph
    # input: start - node id, end - node id
    # output: route_time
    def calculate_route(self, start, end, distance_to_beat=math.inf):
        route, route_time = pathfinding.find_shortest_path(self.adjacency_list, start, end, distance_to_beat)
        
        return route_time 

    def __str__(self):
        graph_str = "\n--- Graph Adjacency List ---"
        for vertex, neighbors in self.adjacency_list.items():
            neighbor_str = ", ".join([f"({n}, {w})" for n, w in neighbors])
            graph_str += f"\n{vertex} -> [{neighbor_str}]"
        graph_str += "\n----------------------------"
        return graph_str

def main(test):
    graph = Graph()
    graph.load_map_data("city_map_50.csv")
    print(graph)
    print(pathfinding.find_shortest_path(graph.adjacency_list, "N1", "N2"))


if __name__=="__main__":
    main()