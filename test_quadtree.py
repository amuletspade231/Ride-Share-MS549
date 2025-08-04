if __name__ == "__main__":
    import math
    import random
    from quadtree import QuadtreeNode
    from quadtree import Quadtree
    from quadtree import Rectangle

    def find_closest_brute_force(query_point, all_points):
        best_p = None
        min_dist_sq = float('inf')
        for p in all_points:
            dist_sq = (p[0] - query_point[0])**2 + (p[1] - query_point[1])**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                best_p = p
        return best_p, min_dist_sq

    map_boundary = Rectangle(0, 0, 1000, 1000)
    qt = Quadtree(map_boundary, QuadtreeNode(map_boundary, capacity=4))

    # Populate random points
    num_points = 5000
    points = [(random.uniform(0, 1000), random.uniform(0, 1000))]
    for p in points:
        qt.root.insert(p)

    query_point = (512, 512)

    print(f"--- Searching for nearest to {query_point} among {num_points} points ---\n")

    best_point_qt, best_dist_sq_qt = qt.find_nearest(query_point)
    print(f"Quadtree Search found: {best_point_qt} at distance {math.sqrt(best_dist_sq_qt):.2f}")

    best_point_bf, best_dist_sq_bf = find_closest_brute_force(query_point, points)
    print(f"Brute-Force Search found: {best_point_bf} at distance {math.sqrt(best_dist_sq_bf):.2f}")
