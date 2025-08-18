import pathfinding
from rider import Rider

TRAVEL_SPEED_FACTOR = 5

class Car:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.destination = None
        self.eta = 0
        self.status = 'available'

    def assign_rider(self, rider):
        self.destination = rider.start_location
        self.status = 'en route to pickup'
        self.eta = self.calculate_travel_time()
        print(f"{self.id} now {self.status} {rider.id} at {self.destination}")

    def pickup_rider(self, rider):
        self.location = self.destination
        self.destination = rider.destination
        self.status = 'en route to destination'
        self.eta = self.calculate_travel_time()
        print(f"{self.id} has picked up {rider.id} and is now {self.status} at {self.destination}")

    def dropoff_rider(self, rider):
        self.location = self.destination
        self.status = 'available'
        print(f"{self.id} has dropped off {rider.id} and is now {self.status} at {self.destination}")

    def calculate_route(self, map):
        route, route_time = pathfinding.find_shortest_path(map, self.location, self.destination)

        print(f"\nShortest path to '{self.destination}': {' -> '.join(route)}")
        print(f"Total time: {route_time} minutes")     
        return route_time  
    
    def calculate_travel_time(self):
        dx = abs(self.location[0] - self.destination[0])
        dy = abs(self.location[1] - self.destination[1])
        return (dx + dy) * TRAVEL_SPEED_FACTOR 

    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"

# def main():
#     car1 = Car("car1", (1,2))
#     print(car1)


# if __name__=="__main__":
#     main()