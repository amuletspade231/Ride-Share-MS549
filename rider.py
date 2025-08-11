class Rider:
    def __init__(self, id, start_location, destination):
        self.id = id
        self.start_location = start_location
        self.destination = destination
        self.status = 'waiting'

    def __str__(self):
        return f"Rider {self.id} at {self.start_location} waiting for ride to {self.destination}"
    
    def __gt__(self, other):
        if(self.id > other.id):
            return True
        else:
            return False

# def main():
#     rider1 = Rider("rider1", (1,2), (9,8))
#     print(rider1)


# if __name__=="__main__":
#     main()