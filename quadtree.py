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
        self.points = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height

        # Create boundaries for the four new quadrants
        ne_rect = Rectangle(x + w / 2, y, w / 2, h / 2)
        self.northeast = Quadtree(ne_rect, self.capacity)

        nw_rect = Rectangle(x, y, w / 2, h / 2)
        self.northwest = Quadtree(nw_rect, self.capacity)

        se_rect = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = Quadtree(se_rect, self.capacity)

        sw_rect = Rectangle(x, y + h / 2, w / 2, h / 2)
        self.southwest = Quadtree(sw_rect, self.capacity)

        self.divided = True

        # Re-insert the points from this node into the new children
        for p in self.points:
            self.insert(p)
        self.points = [] # Clear points from parent node

    def insert(self, point):
        # If point is outside our boundary, do nothing
        if not self.boundary.contains(point):
            return False 

        # If there's space in this node and it's not divided, add the point
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
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
        
    def query(self, point, best_found_point, min_distance):
        # If this quadrant can't have a closer point, stop.
        if self.boundary.distance_sq_to_point(point) > min_distance:
            return

        # 2. Check points in this node if not divided
        for p in self.points:
            dist_sq = (p[0] - point[0])**2 + (p[1] - point[1])**2
            if dist_sq < min_distance:
                min_distance = dist_sq
                best_found_point = p

        # 3. Recursively search children, if divided
        if self.divided:
            children = [self.northeast, self.northwest, self.southeast, self.southwest]
            # Search closest children first
            children.sort(key=lambda child: child.boundary.distance_sq_to_point(point))

            for child in children:
                child.query(point, best_found_point, min_distance)

        return

class Quadtree:
    def __init__(self, boundary, root):
        self.boundary = boundary
        self.root = root

    def find_nearest(self, query_point):
        start = self.root
        best_found_point = None
        min_distance =  float('inf')

        # Check points in root if not divided
        for p in start.points:
            dist_sq = (p[0] - query_point[0])**2 + (p[1] - query_point[1])**2
            if dist_sq < min_distance:
                min_distance = dist_sq
                best_found_point = p

        # Recursively search children, if divided
        if start.divided:
            children = [self.northeast, self.northwest, self.southeast, self.southwest]
            # Search closest children first
            children.sort(key=lambda child: child.boundary.distance_sq_to_point(point))

            for child in children:
                child.query(point, best_found_point, min_distance)

        return best_found_point, min_distance