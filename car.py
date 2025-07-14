class Car:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.destination = None
        self.status = 'available'

    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"

# # Defining main function
# def main():
#     car1 = Car("car1", (1,2))
#     print(car1)


# # Using the special variable 
# # __name__
# if __name__=="__main__":
#     main()