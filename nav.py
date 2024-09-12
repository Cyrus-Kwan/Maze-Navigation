from maze import Maze
from cell import *

import tkinter as tk
import numpy as np
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

    def heuristic(self, cell:Cell, stop_cell:Cell, metric:str="euclidean"):
        x_dist:int = abs(cell.row - stop_cell.row)
        y_dist:int = abs(cell.col - stop_cell.col)
        dist:float = None
        match metric:
            case "euclidean":
                sum_of_squares:int = (x_dist**2) + (y_dist**2)
                dist:float = np.sqrt(sum_of_squares)

                return dist
            case "manhattan":
                dist:float = sum((x_dist, y_dist))

        return dist

    
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
    
    # Pathfinding Algorithms
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
        explored:list[Cell] = []                    # Do not repeat neighbours
        parents:dict[tuple] = {}                    # Previously visited node for finding shortest path

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

            # Stop when solution has been found
            if curr == stop_cell:
                # Append goal cell to find parent
                path = self.shortest_path(start=start_cell, stop=stop_cell, parents=parents)
                expanded = len(explored)
                for cell in path[1:-1]:
                    # Animate solution
                    cell.colour = colour_set["solution"]
                    self.window.update()
                    self.maze.draw_grid(canvas=self.canvas)
                return path, expanded

            # Check surrounding current cell for neighbours
            # Add neighbours starting from top clockwise
            for row, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
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

            # Colour visualization for cells that are currently in the queue
            for cell in frontier:
                cell.colour = colour_set["frontier"]
        raise AttributeError("The given matrix has no solution.")
    
        return 
    
    def depth_first_search(self, start:tuple, stop:tuple):
        start_row:int = start[0]
        start_col:int = start[1]
        stop_row:int = stop[0]
        stop_col:int = stop[1]

        curr:Cell = self.grid[start_row][start_col]
        start_cell:Cell = self.grid[start_row][start_col]
        stop_cell:Cell = self.grid[stop_row][stop_col]

        # Must be valid cell for start and stop
        if not (start_cell.path and stop_cell.path):
            raise AttributeError("Start and stop cells must be valid")
        
        frontier:list[Cell] = [curr]            # Stack/queue FILO
        explored:list[Cell] = []                # Do not repeat neighbours
        parents:dict[tuple] = {}                # Previously visited node for finding shortest path

        while frontier != []:
            curr:Cell = frontier.pop(-1)        # Pop from end of frontier
            explored.append(curr)

            # Animate window
            curr.colour = colour_set["explored"]
            start_cell.colour = colour_set["start"]
            stop_cell.colour = colour_set["stop"]
            self.window.update()
            self.maze.draw_grid(canvas=self.canvas)

            # Stop when solution has been found
            if curr == stop_cell:
                # Append goal cell to find parent
                path = self.shortest_path(start=start_cell, stop=stop_cell, parents=parents)
                expanded = len(explored)
                for cell in path[1:-1]:
                    # Animate solution
                    cell.colour = colour_set["solution"]
                    self.window.update()
                    self.maze.draw_grid(canvas=self.canvas)
                    
                return path, expanded

            # Add neighbours starting from top clockwise
            for row, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_row, new_col = curr.row+row, curr.col+col
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                    neighbour:Cell = self.grid[new_row][new_col]

                    # Check the neighbour is not a wall
                    if not neighbour.path:
                        continue
                    
                    # Check the neighbour has not been visited
                    # if (neighbour not in frontier) and (neighbour not in explored):
                    if (neighbour not in frontier) and (neighbour not in explored):
                        parents[(neighbour.row, neighbour.col)] = curr
                        frontier.append(neighbour)

            # Colour visualization for cells that are currently in the queue
            for cell in frontier:
                cell.colour = colour_set["frontier"]
        raise AttributeError("The given matrix has no solution.")
    
        return

    def a_star_search(self, start:tuple, stop:tuple, metric:str="euclidean"):
        start_row:int = start[0]
        start_col:int = start[1]
        stop_row:int = stop[0]
        stop_col:int = stop[1]

        curr:Cell = self.grid[start_row][start_col]
        start_cell:Cell = self.grid[start_row][start_col]
        stop_cell:Cell = self.grid[stop_row][stop_col]

        # Must be valid cell for start and stop
        if not (start_cell.path and stop_cell.path):
            raise AttributeError("Start and stop cells must be valid")

        frontier:list[Cell] = [curr]        # Priority queue
        explored:list[Cell] = []            # Do not repeat neighbours
        parents:dict[tuple] = {
            (curr.row,curr.col):curr
        }                                   # Previously visited node for finding shortest path

        while frontier != []:
            heuristic = lambda cell:self.heuristic(
                cell=cell, stop_cell=stop_cell, metric=metric
            )
            cost = lambda cell: len(
                self.shortest_path(
                    start=start_cell, 
                    stop=cell, 
                    parents=parents
                )
            )
            a_star_score = lambda cell: cost(cell=cell)+heuristic(cell=cell)
            frontier.sort(key=a_star_score)
            curr = frontier.pop(0)          # Pop cell with lowest a* score
            explored.append(curr)
            
            # Animate window
            curr.colour = colour_set["explored"]
            start_cell.colour = colour_set["start"]
            stop_cell.colour = colour_set["stop"]
            self.window.update()
            self.maze.draw_grid(canvas=self.canvas)

            # Stop when solution has been found
            if curr == stop_cell:
                # Append goal cell to find parent
                path = self.shortest_path(start=start_cell, stop=stop_cell, parents=parents)
                expanded = len(explored)
                for cell in path[1:-1]:
                    # Animate solution
                    cell.colour = colour_set["solution"]
                    self.window.update()
                    self.maze.draw_grid(canvas=self.canvas)
                    
                return path, expanded

            # Add neighbours starting from top clockwise
            for row, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                new_row, new_col = curr.row+row, curr.col+col
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                    neighbour:Cell = self.grid[new_row][new_col]

                    # Check the neighbour is not a wall
                    if not neighbour.path:
                        continue
                    
                    # Check the neighbour has not been visited
                    if (neighbour not in frontier) and (neighbour not in explored):
                        parents[(neighbour.row, neighbour.col)] = curr
                        frontier.append(neighbour)

            # Colour visualization for cells that are currently in the queue
            for cell in frontier:
                cell.colour = colour_set["frontier"]
        raise AttributeError("The given matrix has no solution.")
        return

def main():
    nav = Navigation(file_name="maze.csv")
    # nav = Navigation(rows=25, cols=50)
    # nav.grid[24][49].path = True
    # path, expanded = nav.breadth_first_search(start=(0,0), stop=(19,19))
    # short_path = [cell.__str__() for cell in path]
    # print("distance:", len(short_path))
    # print("expanded:", expanded)
    
    # for row in nav.grid:
    #     for cell in row:
    #         if cell.path:
    #             cell.colour = colour_set["path"]
    #         else:
    #             cell.colour = colour_set["wall"]

    path, expanded = nav.iterative_deepening_dfs(start=(0,0), stop=(19,19))
    short_path = [cell.__str__() for cell in path]
    print("distance:", len(short_path))
    print("expanded:", expanded)

    # for row in nav.grid:
    #     for cell in row:
    #         if cell.path:
    #             cell.colour = colour_set["path"]
    #         else:
    #             cell.colour = colour_set["wall"]

    # path, expanded = nav.a_star_search(start=(0,0), stop=(19,19), metric="manhattan")
    # short_path = [cell.__str__() for cell in path]
    # print("distance:", len(short_path))
    # print("expanded:", expanded)

    nav.window.mainloop()
    return

if __name__ == "__main__":
    main()