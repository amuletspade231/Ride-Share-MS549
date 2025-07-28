import csv
import pathfinding

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start_node, end_node, weight):
        if start_node in self.adjacency_list:
            self.adjacency_list[start_node].append((end_node, weight))
        else:
            self.adjacency_list[start_node] = [(end_node, weight)]

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3: # Ensure row has 3 elements
                        start, end, weight = row
                        self.add_edge(start.strip(), end.strip(), int(weight.strip()))
            print(self)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def __str__(self):
        graph_str = "\n--- Graph Adjacency List ---"
        for vertex, neighbors in self.adjacency_list.items():
            neighbor_str = ", ".join([f"({n}, {w})" for n, w in neighbors])
            graph_str += f"\n{vertex} -> [{neighbor_str}]"
        graph_str += "\n----------------------------"
        return graph_str

def main():
    graph = Graph()
    graph.load_from_file("map.csv")
    print(pathfinding.find_shortest_path(graph.adjacency_list, "A", "D"))


if __name__=="__main__":
    main()