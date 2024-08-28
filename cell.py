import random

colour_set = {
    "wall":"black", 
    "path":"white", 
    "start":"red",
    "stop":"limegreen",
    "explored":"yellow", 
    "frontier":"orange",
    "solution":"blue"
    }

class Cell:
    size:int = 25
    def __init__(self, row:int, col:int, path:bool=None):
        self.row:int = row
        self.col:int = col

        if path == None:
            self.path:bool = False if random.random() < 0.2 else True
        else:
            self.path:bool = path
            
        if self.path:
            self.colour:str = colour_set["path"]
        else:
            self.colour:str = colour_set["wall"]

    def __eq__(self, other):
        row = (self.row == other.row)
        col = (self.col == other.col)
        path = (self.path == other.path)
        colour = (self.colour == other.colour)

        return row and col and path and colour
    
    def __str__(self):
        return f"row:{self.row}, col:{self.col}"

def main():

    return

if __name__ == "__main__":
    main()