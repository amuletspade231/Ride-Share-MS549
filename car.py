import pathfinding
from rider import Rider

class Car:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.destination = None
        self.status = 'available'

    def assign_rider(self, rider):
        self.destination = rider.start_location
        self.status = 'en route to pickup'
        print(f"{self.id} now {self.status} {rider.id} at {self.destination}")

    def pickup_rider(self, rider):
        self.location = self.destination
        self.destination = rider.destination
        self.status = 'en route to destination'
        print(f"{self.id} has picked up {rider.id} and is now {self.status} at {self.destination}")

    def dropoff_rider(self, rider):
        self.location = self.destination
        self.status = 'available'
        print(f"{self.id} has dropped up {rider.id} and is now {self.status} at {self.destination}")

    def calculate_route(self, map):
        route, route_time = pathfinding.find_shortest_path(map, self.location, self.destination)

        print(f"\nShortest path to '{self.destination}': {' -> '.join(route)}")
        print(f"Total time: {route_time} minutes")        

    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"

# def main():
#     car1 = Car("car1", (1,2))
#     print(car1)


# if __name__=="__main__":
#     main()