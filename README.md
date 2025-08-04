Ride Share Simulator
---------------------

This is a practice project intended to refamiliarize myself with python OOP, data structures, and algorithms.
Specifically, I will be using Dijkstra’s algorithm to allow our Car class to calculate the best route to its riders and their destinations.

Map Data Format: The map.csv should contain three columns: start_node, end_node, and travel_time. Each row represents a directed road (an edge) between two locations (nodes) with an associated travel time (weight).

How to Run:
1) Clone the repository
2) Tweak map.csv as desired according to the above format
3) Run 'python3 simulation.py'

Dependencies: None

Nearest Neighbor: Quadtree Implementation
------------------------------------------
In the ride share simulator we will eventually select the closest car pick up a rider.
To do so, we will be utilizing Quadtrees to find the nearest neighbor or "car" based on a rider's coordinates.
By using Quadtrees to exponentially shrink our search area for the nearest neighbor, our search algorithm will perform at a O(logN) complexity versus a burte forced O(N) solution.

How to Run:
1) Clone the repository
3) Run 'python3 test_quadtree.py'

Dependencies: None

