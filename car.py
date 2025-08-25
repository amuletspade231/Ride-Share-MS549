import pathfinding
from rider import Rider

TRAVEL_SPEED_FACTOR = 5

class Car:
    def __init__(self, id, location):
        self.id = id
        self.location = location # (node_id, (node x, node y))
        self.destination = None  # (node_id, (node x, node y))
        self.total_drive_time = 0
        self.status = 'available'

    def assign_rider(self, rider, request_time):
        # update car info
        self.destination = rider.start_location
        self.status = 'en route to pickup'

        # update rider info
        rider.request_time = request_time
        
        print(f"TIME {request_time:.2f}: {self.id} at {self.location} now {self.status} {rider.id} to {self.destination}")

    def pickup_rider(self, rider, pickup_time):
        # update car info
        self.location = self.destination
        self.destination = rider.destination
        self.status = 'en route to destination'

        # update rider info
        rider.pickup_time = pickup_time

        print(f"TIME {pickup_time:.2f}: {self.id} has picked up {rider.id} at {self.location} and is now {self.status} to {self.destination}")

    def dropoff_rider(self, rider, dropoff_time):
        # update car info
        self.location = self.destination
        self.status = 'available'
        self.total_drive_time += (dropoff_time - rider.request_time)

        # update rider info
        rider.dropoff_time = dropoff_time

        print(f"TIME {dropoff_time:.2f}: {self.id} has dropped off {rider.id} and is now {self.status} at {self.location}")

    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"

# def main():
#     car1 = Car("car1", (1,2))
#     print(car1)


# if __name__=="__main__":
#     main()