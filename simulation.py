from car import Car
from rider import Rider
from graph import Graph

class Simulation:
    def __init__(self, map_filename):
        self.cars = {}
        self.riders = {}
        self.map = Graph()
        self.map.load_from_file(map_filename)

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


if __name__=="__main__":
    main()