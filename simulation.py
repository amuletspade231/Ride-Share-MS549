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
import matplotlib.pyplot as plt

# determines frequency of rider requests
MEAN_ARRIVAL_TIME = 100

class Simulation:
    def __init__(self, map_filename, num_cars, max_dim):
        self.max_dim = max_dim
        self.time = 0
        self.events = [] # [(time, event_type, car and/or rider)]
        self.riders = {} # {rider_id : rider_object}
        self.cars = {} # {car_id : car_object}
        self.trip_log = []

        # generate map graph
        self.map = Graph()
        self.map.load_map_data(map_filename)

        # generate cars at a random position in the graph
        for i in range(num_cars):
            car = Car("Car" + str(i), random.choice(list(self.map.node_coordinates.items())))
            self.cars[car.id] = car
        
        # add cars to a quadtree
        map_boundary = Rectangle(0, 0, max_dim, max_dim)
        self.qt = Quadtree(map_boundary, QuadtreeNode(map_boundary, capacity=4))
        for car in self.cars:
            # insert only location coordinates
            self.qt.root.insert((car, self.cars[car].location[1]))

    # generate_rider_request - generate a new rider at a random position in the graph and add a request to the event tracker
    def generate_rider_request(self, delay):
        rider = Rider("Rider" + str(len(self.riders)), random.choice(list(self.map.node_coordinates.items())), random.choice(list(self.map.node_coordinates.items())))
        self.riders[rider.id] = rider

        self.add_event(delay, "RIDER_REQUEST", rider)

    def add_event(self, delay, event_type, data):
        heapq.heappush(self.events, (self.time + delay, event_type, data))

    def run(self, max_riders):
        # start the simulation with one request
        self.generate_rider_request(0)

        print("SIMULATION START")

        while self.events:
            # check for rider limit
            if(len(self.riders) > max_riders):
                print("Simulation timed-out.\n")
                return

            self.time, event_type, data = heapq.heappop(self.events)

            if event_type == "RIDER_REQUEST":
                self.handle_rider_request(data)
            elif event_type == "ARRIVAL":
                self.handle_arrival(data)

    # handle_rider_request - assigns the closest car with the fastest eta to a given rider 
    def handle_rider_request(self, rider):
        # find 5 closest cars using rider coordinates
        best_k_qt = self.qt.find_nearest_k(rider.start_location[1])

        # pick car with shortest travel time using location node
        best_car_graph = ("None", float('inf'))
        for car_id in best_k_qt.values():
            if car_id != "None":
                car = self.cars[car_id]
                start = car.location[0]
                end = rider.start_location[0]
                # use current best travel time to calculate potential routes to save some time
                travel_time = self.map.calculate_route(start,end, best_car_graph[1])
                if travel_time < best_car_graph[1]:
                    best_car_graph = (car_id, travel_time)
                # no need to continue if current best is 0s
                if travel_time == 0:
                    break

        # get car id and eta from best car calc
        car_id, eta = best_car_graph

        if car_id != "None":
            # assign rider to car
            car = self.cars[car_id]
            car.assign_rider(rider, self.time)
            # remove car from quadtree using car coordinates
            self.qt.root.remove((car.id, car.location[1]))
            # generate arrival event and a new request with eta from best car calc
            self.add_event(eta, "ARRIVAL", (car, rider))
            print(f"ETA: {eta}s.")
            self.generate_rider_request(random.expovariate(1.0/MEAN_ARRIVAL_TIME))
        # if no cars are available, resubmit the request later
        else:
            delay = MEAN_ARRIVAL_TIME
            self.add_event(delay, "RIDER_REQUEST", (rider)) # wait after cars have moved to find next closest
            print(f"All cars are unavailable. Resubmitting request in {delay}s.")

    # handle_arrival - either picks up or drops off a rider and makes necessary updates
    def handle_arrival(self, data):
        car, rider = data
        # update car and rider status
        if car.status == "en route to pickup":
            car.pickup_rider(rider, self.time)
            start = car.location[0]
            end = rider.destination[0]
            eta = self.map.calculate_route(start,end)
            self.add_event(eta, "ARRIVAL", (car, rider))
            print(f"ETA: {eta}s.")
        # if at destination, make car available again and log rider's trip
        elif car.status == "en route to destination":
            car.dropoff_rider(rider, self.time)
            self.qt.root.insert((car.id, car.location[1]))
            self.log_trip_data(rider)

    # log_trip_data - logs a rider's trip
    def log_trip_data(self, rider):
        trip_record = {
            'rider_id': rider.id,
            'request_time': rider.request_time,
            'pickup_time': rider.pickup_time,
            'dropoff_time': rider.dropoff_time,
            'wait_time': rider.pickup_time - rider.request_time,
            'trip_duration': rider.dropoff_time - rider.pickup_time,
            'trip_distance': math.sqrt((rider.start_location[1][0] - rider.destination[1][0])**2 + (rider.start_location[1][1] - rider.destination[1][1])**2)
        }
        self.trip_log.append(trip_record)
        print(f"Trip for {rider.id} completed and logged.")
        self.plot_current_state()
    
    # plot_current_state - plots current locations and status of all cars
    def plot_current_state(self):
        available_locations = []
        busy_locations = []

        for car in self.cars:
            if self.cars[car].status == 'available':
                available_locations.append(self.cars[car].location[1])
            else:
                busy_locations.append(self.cars[car].location[1])

        # Unzip the coordinates for plotting
        available_x = [loc[0] for loc in available_locations]
        available_y = [loc[1] for loc in available_locations]
        busy_x = [loc[0] for loc in busy_locations]
        busy_y = [loc[1] for loc in busy_locations]

        # Create a figure and an axes object
        plt.figure(figsize=(8, 8))

        # Plot the available cars in blue
        plt.scatter(available_x, available_y, c='green', label='Available Cars', marker='o', s=100) # s is marker size

        # Plot the rider request in red with a different marker
        plt.scatter(busy_x, busy_y, c='gray', label='Busy Cars', marker='s', s=100)

        # Set plot boundaries, title, and labels
        plt.xlim(0, self.max_dim)
        plt.ylim(0, self.max_dim)
        plt.title("Current State of Car Fleet")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend() # Display the labels
        plt.grid(True) # Add a grid for readability

        # Save the plot to a file
        plt.savefig("simulation_summary.png")

        plt.close()


def main(max_riders):
    # simulation settings

    # 50 node map
    # map_file = "city_map_50.csv"
    # num_cars = 5
    # max_dim = 7
    
    # 1000 node map
    map_file = "city_map_1000.csv"
    num_cars = 100
    max_dim = 1000

    app = Simulation(map_file, num_cars, max_dim)

    app.run(int(max_riders))

    available_locations = []
    busy_locations = []

    total_driver_utilization = 0

    for car in app.cars:
        if app.cars[car].status == 'available':
            available_locations.append(app.cars[car].location[1])
        else:
            busy_locations.append(app.cars[car].location[1])
        
        total_driver_utilization += (app.cars[car].total_drive_time / app.time)

    # Unzip the coordinates for plotting
    available_x = [loc[0] for loc in available_locations]
    available_y = [loc[1] for loc in available_locations]
    busy_x = [loc[0] for loc in busy_locations]
    busy_y = [loc[1] for loc in busy_locations]

    # calcaulate total wait and travel time
    total_wait_time = sum(log["wait_time"] for log in app.trip_log)
    total_travel_time = sum(log["trip_duration"] for log in app.trip_log)
    total_travel_dist = sum(log["trip_distance"] for log in app.trip_log)
    num_trips = len(app.trip_log)

    avg_wait_time = total_wait_time / num_trips
    avg_travel_time = total_travel_time / num_trips
    avg_travel_dist = total_travel_dist / num_trips
    driver_utilization = (total_driver_utilization) / len(app.cars) * 100

    # Create a figure and an axes object
    plt.figure(figsize=(8, 8))

    # Plot the available cars in blue
    plt.scatter(available_x, available_y, c='green', label='Available Cars', marker='o', s=100) # s is marker size

    # Plot the rider request in red with a different marker
    plt.scatter(busy_x, busy_y, c='gray', label='Busy Cars', marker='s', s=100)

    # Set plot boundaries, title, and labels
    plt.xlim(0, max_dim)
    plt.ylim(0, max_dim)
    plt.title("Simulation Summary")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    textstr = '\n'.join((
    f"# of Trips Completed: {num_trips}",
    f"Average Wait Time: {avg_wait_time:.2f}s",
    f"Overall Driver Utilization: {driver_utilization:.2f}%"))
    plt.text(-.15*max_dim, -.15*max_dim, f"# of Trips Completed: {num_trips}   Overall Driver Utilization: {driver_utilization:.2f}%")
    plt.text(-.15*max_dim, -.25*max_dim, f"Average Wait Time: {avg_wait_time:.2f}s   Average Travel Time: {avg_travel_time:.2f}s")
    plt.text(-.15*max_dim, -.35*max_dim, f"Average Travel Distance: {avg_travel_dist:.2f} units")
    plt.subplots_adjust(bottom=0.25)
    plt.legend() # Display the labels
    plt.grid(True) # Add a grid for readability

    # Save the plot to a file
    plt.savefig("simulation_summary.png")
    print("Plot saved to simulation_summary.png")

if __name__=="__main__":
    # get max riders from user
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_riders")
    args = parser.parse_args()
    max_riders = args.max_riders
    main(max_riders)