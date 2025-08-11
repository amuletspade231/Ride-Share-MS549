import heapq
import math
import random
from car import Car
from rider import Rider
from graph import Graph

TRAVEL_SPEED_FACTOR = 5

class Simulation:
    # Graph ver
    '''
    def __init__(self, map_filename):
        self.cars = {}
        self.riders = {}
        self.map = Graph()
        self.map.load_from_file(map_filename)
    '''
    # Coordinate ver
    def __init__(self):
        self.time = 0
        self.events = []
        self.cars = {}
        self.riders = {}

    def add_event(self, delay, event_type, data):
        heapq.heappush(self.events, (self.time + delay, event_type, data))

    def run(self):

        while self.events:
            self.time, event_type, data = heapq.heappop(self.events)

            print(f"Current time is: {self.time}")
            if(self.time > 499):
                print("Simulation timedout.")
                return

            print(f"Processing {event_type} for {data}")

            if event_type == "RIDER_REQUEST":
                self.handle_rider_request(data)
            elif event_type == "ARRIVAL":
                self.handle_arrival(data)

    def handle_rider_request(self, rider):
        car = self.find_closest_car_brute_force(rider.start_location)
        if car.status == "available":
            car.assign_rider(rider)
            eta = self.calculate_travel_time(car.location, car.destination)
            self.add_event(eta, "ARRIVAL", (car, rider))
            print(f"ETA: {eta}s.")
        else:
            eta = self.calculate_travel_time(car.location, car.destination)
            self.add_event(eta + 5, "RIDER_REQUEST", (rider)) # wait after car has moved to find next closest
            print(f"{car.id} is unavailable. Resubmitting request in {eta + 5}s.")

    def handle_arrival(self, data):
        car, rider = data
        if car.status == "en route to pickup":
            car.pickup_rider(rider)
            eta = self.calculate_travel_time(car.location, car.destination)
            self.add_event(eta, "ARRIVAL", (car, rider))
            print(f"ETA: {eta}s.")
        elif car.status == "en route to destination":
            car.dropoff_rider(rider)

    def find_closest_car_brute_force(self, rider_location):
        closest_car = None
        min_dist_sq = float('inf')
        for car in self.cars:
            car = self.cars[car]
            dist_sq = (car.location[0] - rider_location[0])**2 + (car.location[1] - rider_location[1])**2
            #print(f"current shortest: {min_dist_sq}, contending shortest: {dist_sq}")
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_car = car
        return closest_car

    def calculate_travel_time(self, start_location, end_location):
        dx = abs(start_location[0] - end_location[0])
        dy = abs(start_location[1] - end_location[1])
        return (dx + dy) * TRAVEL_SPEED_FACTOR

# Coordinate Ver
def main():
    app = Simulation()
    num_cars = 2
    num_riders = 3
    num_events = 3

    for i in range(num_cars):
        car = Car("car" + str(i), (random.randint(0, 10), random.randint(0, 10)))
        app.cars[car.id] = car

    for i in range(num_riders):
        rider = Rider("rider" + str(i), (random.randint(0, 10), random.randint(0, 10)), (random.randint(0, 10), random.randint(0, 10)))
        app.riders[rider.id] = rider

    for i in range(num_riders):
        app.add_event(random.randint(0, 10) * 10, "RIDER_REQUEST", app.riders["rider" + str(i)])

    for car in app.cars:
        print(app.cars[car])

    for rider in app.riders:
        print(app.riders[rider])

    for event in app.events:
        print(event)

    app.run()

# Graph Ver
'''
def main():
    car1 = Car("car1", ('A'))
    rider1 = Rider("rider1", ('D'), ('B'))
    app = Simulation("map.csv")

    app.cars[car1.id] = car1
    app.riders[rider1.id] = rider1

    for car in app.cars:
        print(app.cars[car])

    for rider in app.riders:
        print(app.riders[rider])

    car1.assign_rider(rider1)

    car1.calculate_route(app.map.adjacency_list)

    car1.pickup_rider(rider1)

    car1.calculate_route(app.map.adjacency_list)
'''

if __name__=="__main__":
    main()