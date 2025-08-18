import heapq
import math
import random
import argparse
from car import Car
from rider import Rider
from graph import Graph
from quadtree import QuadtreeNode
from quadtree import Quadtree
from quadtree import Rectangle

MEAN_ARRIVAL_TIME = 50

class Simulation:
    def __init__(self, map_filename, num_cars, max_dim):
        self.max_dim = max_dim
        self.time = 0
        self.events = []
        self.riders = {}
        self.cars = {}

        for i in range(num_cars):
            car = Car("car" + str(i), (random.randint(0, max_dim), random.randint(0, max_dim)))
            self.cars[car.id] = car

        self.map = Graph()
        self.map.load_map_data(map_filename)
        
        map_boundary = Rectangle(0, 0, max_dim, max_dim)
        self.qt = Quadtree(map_boundary, QuadtreeNode(map_boundary, capacity=4))
        for car in self.cars:
            self.qt.root.insert(self.cars[car].location)

    def generate_rider_request(self, delay):
        rider = Rider("Rider" + str(len(self.riders)), (random.randint(0, self.max_dim), random.randint(0, self.max_dim)), (random.randint(0, self.max_dim), random.randint(0, self.max_dim)))
        self.riders[rider.id] = rider

        self.add_event(delay, "RIDER_REQUEST", rider)

    def add_event(self, delay, event_type, data):
        heapq.heappush(self.events, (self.time + delay, event_type, data))

    def run(self, max_time):
        self.generate_rider_request(0)

        while self.events:
            self.time, event_type, data = heapq.heappop(self.events)

            print(f"\nCurrent time is: {self.time}")
            if(self.time > max_time):
                print("Simulation timedout.")
                return

            print(f"Processing {event_type} for {data}")

            if event_type == "RIDER_REQUEST":
                self.handle_rider_request(data)
            elif event_type == "ARRIVAL":
                self.handle_arrival(data)

    def handle_rider_request(self, rider):
        # best_k_qt = self.qt.find_nearest_k(rider.start_location)
        # car_id = best_k_qt[min(best_k_qt)].id
        # car = self.cars[car_id]
        car = self.find_closest_car_brute_force(rider.start_location)
        if car:
            car.assign_rider(rider)
            self.qt.root.remove(car.location)
            self.add_event(car.eta, "ARRIVAL", (car, rider))
            print(f"ETA: {car.eta}s.")
            self.generate_rider_request(random.expovariate(1.0/MEAN_ARRIVAL_TIME))
        else:
            delay = MEAN_ARRIVAL_TIME
            self.add_event(delay, "RIDER_REQUEST", (rider)) # wait after cars have moved to find next closest
            print(f"All cars are unavailable. Resubmitting request in {delay}s.")

    def handle_arrival(self, data):
        car, rider = data
        if car.status == "en route to pickup":
            car.pickup_rider(rider)
            self.add_event(car.eta, "ARRIVAL", (car, rider))
            print(f"ETA: {car.eta}s.")
        elif car.status == "en route to destination":
            car.dropoff_rider(rider)
            self.qt.root.insert(car.location)

    def find_closest_car_brute_force(self, rider_location):
        closest_car = None
        min_dist_sq = float('inf')
        for car in self.cars:
            car = self.cars[car]
            if car.status != "available":
                continue
            dist_sq = (car.location[0] - rider_location[0])**2 + (car.location[1] - rider_location[1])**2
            #print(f"current shortest: {min_dist_sq}, contending shortest: {dist_sq}")
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_car = car
        return closest_car

def main(max_time):
    app = Simulation("city_map_50.csv", 5, 7)

    for car in app.cars:
        print(app.cars[car])

    app.run(int(max_time))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_time")
    args = parser.parse_args()
    max_time = args.max_time
    main(max_time)