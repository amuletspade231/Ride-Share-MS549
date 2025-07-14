class Rider:
    def __init__(self, id, start_location, destination):
        self.id = id
        self.start_location = start_location
        self.destination = destination
        self.status = 'waiting'

    def __str__(self):
        return f"Rider {self.id} at {self.start_location} waiting for ride to {self.destination}"

# # Defining main function
# def main():
#     rider1 = Rider("rider1", (1,2), (9,8))
#     print(rider1)


# # Using the special variable 
# # __name__
# if __name__=="__main__":
#     main()