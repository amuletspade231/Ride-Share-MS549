from car import Car
from rider import Rider

class Simulation:
    def __init__(self):
        self.cars = {}
        self.riders = {}

# Defining main function
def main():
    car1 = Car("car1", (1,2))
    rider1 = Rider("rider1", (1,2), (9,8))
    app = Simulation()

    app.cars[car1.id] = car1
    app.riders[rider1.id] = rider1

    for car in app.cars:
        print(app.cars[car])

    for rider in app.riders:
        print(app.riders[rider])



# Using the special variable 
# __name__
if __name__=="__main__":
    main()