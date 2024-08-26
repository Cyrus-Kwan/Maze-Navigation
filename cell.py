import random

colour_set = {
    "wall":"black", 
    "path":"white", 
    "visited":"yellow", 
    "neighbour":"orange"
    }

class Cell():
    size:int = 25
    def __init__(self, row:int, col:int, wall:bool=None):
        self.row:int = row
        self.col:int = col

        if wall == None:
            self.wall:bool = True if random.random() < 0.2 else False
        else:
            self.wall:bool = wall
            
        if self.wall:
            self.colour = colour_set["wall"]
        else:
            self.colour = colour_set["path"]

def main():

    return

if __name__ == "__main__":
    main()