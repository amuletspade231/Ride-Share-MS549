import collections

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (self.x <= point[0] < self.x + self.width and
                self.y <= point[1] < self.y + self.height)

    def distance_sq_to_point(self, point):
        dx = max(0, self.x - point[0], point[0] - (self.x + self.width))
        dy = max(0, self.y - point[1], point[1] - (self.y + self.height))
        return dx*dx + dy*dy

class QuadtreeNode:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = {} # {car_id : (car x, car y)}
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    # subdivide - divides node into 4 sub nodes and redistributes any points to sub nodes
    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height

        # Create boundaries for the four new quadrants
        ne_rect = Rectangle(x + w / 2, y, w / 2, h / 2)
        self.northeast = QuadtreeNode(ne_rect, self.capacity)

        nw_rect = Rectangle(x, y, w / 2, h / 2)
        self.northwest = QuadtreeNode(nw_rect, self.capacity)

        se_rect = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = QuadtreeNode(se_rect, self.capacity)

        sw_rect = Rectangle(x, y + h / 2, w / 2, h / 2)
        self.southwest = QuadtreeNode(sw_rect, self.capacity)

        self.divided = True

        # Re-insert the points from this node into the new children
        for p in self.points:
            self.insert((p,self.points[p]))
        self.points = {} # Clear points from parent node

    # remove - removes a point from the quad tree
    # inputs: point - (car, (car x, car y))
    def remove(self, point):
        if not self.boundary.contains(point[1]):
            return False 
        if not self.divided:
            self.points.pop(point[0])
        else:
            if self.northwest.remove(point): return True
            if self.northeast.remove(point): return True
            if self.southwest.remove(point): return True
            if self.southeast.remove(point): return True
        
        return False

    # insert - inserts a point from the quad tree
    # inputs: point - (car, (car x, car y))
    def insert(self, point):
        # If point is outside our boundary, do nothing
        if not self.boundary.contains(point[1]):
            return False 

        # If there's space in this node and it's not divided, add the point
        if len(self.points) < self.capacity and not self.divided:
            self.points[point[0]] = point[1]
            return True

        # If node reached capacity and is not yet divided, subdivide it
        if not self.divided:
            self.subdivide()

        # Node is divided; pass the point down to the correct child quadrant
        if self.northwest.insert(point): return True
        if self.northeast.insert(point): return True
        if self.southwest.insert(point): return True
        if self.southeast.insert(point): return True

        return False

    # query
    # inputs: point - (rider x, rider y), k - number of neighbors
    # outputs: best_k_qt - {dist_sq_num_1 : car_id_str_1, ... dist_sq_num_k : car_id_str_k}    
    def query(self, point, best_k_qt, k):
        # If this quadrant can't have a closer point, stop.
        if self.boundary.distance_sq_to_point(point) > max(best_k_qt):
            return

        # 2. Check points in this node if not divided
        for p in self.points:
            dist_sq = (self.points[p][0] - point[0])**2 + (self.points[p][1] - point[1])**2
            if len(best_k_qt) == k:
                kth_best = max(best_k_qt)
                if dist_sq < kth_best:
                    best_k_qt.pop(kth_best)
                    best_k_qt[dist_sq] = p
            else:
                best_k_qt[dist_sq] = p

        # 3. Recursively search children, if divided
        if self.divided:
            children = [self.northeast, self.northwest, self.southeast, self.southwest]
            # Search closest children first
            children.sort(key=lambda child: child.boundary.distance_sq_to_point(point))

            for child in children:
                child.query(point, best_k_qt, k)

        return

    def __str__(self, level=0):
        """A simple string representation for visualization."""
        ret = "\t" * level + f"Level {level}, Boundary: {self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height}\n"
        ret += "\t" * level + f"Points: {self.points}\n"
        if self.divided:
            ret += self.northeast.__str__(level + 1)
            ret += self.northwest.__str__(level + 1)
            ret += self.southeast.__str__(level + 1)
            ret += self.southwest.__str__(level + 1)
        return ret



class Quadtree:
    def __init__(self, boundary, root):
        self.boundary = boundary
        self.root = root

    # find_nearest_k - finds k nearest neighbors based on coordinates
    # inputs: query_point - (rider x, rider y), k - number of neighbors
    # outputs: best_k_qt - {dist_sq_num_1 : car_id_str_1, ... dist_sq_num_k : car_id_str_k}
    def find_nearest_k(self, query_point, k = 5):
        start = self.root
        best_k_qt = {float('inf'): "None"}

        # Check points in root if not divided
        for p in start.points:
            dist_sq = (start.points[p][0] - query_point[0])**2 + (start.points[p][1] - query_point[1])**2
            if len(best_k_qt) == 5:
                kth_best = max(best_k_qt)
                if dist_sq < kth_best:
                    best_k_qt.pop(kth_best)
                    best_k_qt[dist_sq] = p
            else:
                best_k_qt[dist_sq] = p

        # Recursively search children, if divided
        if start.divided:
            children = [start.northeast, start.northwest, start.southeast, start.southwest]
            # Search closest children first
            children.sort(key=lambda child: child.boundary.distance_sq_to_point(query_point))

            for child in children:
                child.query(query_point, best_k_qt, k)

        

        return collections.OrderedDict(sorted(best_k_qt.items()))