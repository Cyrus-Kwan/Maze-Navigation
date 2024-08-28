from maze import Maze
from cell import *

import tkinter as tk
import time

class Navigation:
    def __init__(self, rows:int=None, cols:int=None, file_name:str=None):
        if file_name:
            self.maze = Maze(file_name=file_name)
        elif rows and cols:
            self.maze = Maze(rows=rows, cols=cols)
        else:
            raise AttributeError("Expected file_name or rows/cols dimensions")

        self.grid = self.maze.grid

        self.window = tk.Tk()
        self.canvas = tk.Canvas(master=self.window, width=self.maze.width, height=self.maze.height)
        self.canvas.pack()

    def breadth_first_search(self, start:tuple, stop:tuple):
        start_row:int = start[0]
        start_col:int = start[1]
        stop_row:int = stop[0]
        stop_col:int = stop[1]

        curr:Cell = self.grid[start_row][start_col]
        start_cell:Cell = self.grid[start_row][start_col]
        stop_cell:Cell = self.grid[stop_row][stop_col]

        if not (start_cell.path and stop_cell.path):
            raise AttributeError("Start and stop cells must be valid")

        frontier:list[Cell] = [curr]                # Stack/queue
        parents:list[Cell] = {}                     # Previously visited node for finding shortest path
        explored:list[Cell] = []                    # Do not repeat neighbours

        if curr == stop_cell:
            return curr
        
        while frontier != []:
            curr:Cell = frontier.pop(0)             # Pop from start of list FIFO
            explored.append(curr)

            # Animate window
            curr.colour = colour_set["explored"]
            start_cell.colour = colour_set["start"]
            stop_cell.colour = colour_set["stop"]
            self.window.update()
            self.maze.draw_grid(canvas=self.canvas)
            time.sleep(0.01)

            # Check surrounding current cell for neighbours
            for row, col in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_row, new_col = curr.row+row, curr.col+col
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                    neighbour = self.grid[new_row][new_col]

                    # Check the neighbouring cell is not a wall
                    if not neighbour.path:
                        continue

                    # Check the neighbouring cell has not been visited
                    if (neighbour not in frontier) and (neighbour not in explored):
                        parents[(neighbour.row, neighbour.col)] = curr
                        frontier.append(neighbour)

                    # Stop when solution has been found
                    if neighbour == stop_cell:
                        # Append goal cell to find parent
                        parents[(neighbour.row, neighbour.col)] = curr
                        path = self.shortest_path(start=start_cell, stop=stop_cell, parents=parents)
                        for cell in path[1:-1]:
                            # Animate solution
                            cell.colour = colour_set["solution"]
                            self.window.update()
                            self.maze.draw_grid(canvas=self.canvas)
                            time.sleep(0.01)
                        return path

            # Colour visualization for cells that are currently in the queue
            for cell in frontier:
                cell.colour = colour_set["frontier"]
        raise AttributeError("The given matrix has solution.")
        return 

    def shortest_path(self, start:Cell, stop:Cell, parents:dict):
        '''
        Returns the shortest path from a child:parent map
        '''
        path = []
        prev = stop
        while prev != start:
            path.append(self.grid[prev.row][prev.col])
            prev = parents[(prev.row, prev.col)]
        path.append(self.grid[start.row][start.col])
        path.reverse()
        return path

def main():
    nav = Navigation(file_name="maze.csv")
    path = nav.breadth_first_search(start=(10,2), stop=(12,19))
    short_path = [cell.__str__() for cell in path]
    print(short_path)
    nav.window.mainloop()

    return

if __name__ == "__main__":
    main()