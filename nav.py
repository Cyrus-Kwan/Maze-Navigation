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
        self.breadth_first_search(start=(0,0), stop=(19,19))
        self.window.mainloop()


    def breadth_first_search(self, start:tuple, stop:tuple):
        start_row:int = start[0]
        start_col:int = start[1]
        stop_row:int = stop[0]
        stop_col:int = stop[1]

        curr:Cell = self.grid[start_row][start_col]
        start_cell:Cell = self.grid[start_row][start_col]
        stop_cell:Cell = self.grid[stop_row][stop_col]

        frontier:list[Cell] = [curr]
        explored:list[Cell] = []

        if curr == stop_cell:
            return curr
        
        while frontier != []:
            curr = frontier.pop(0)  # Pop from start of list FIFO
            explored.append(curr)
            self.window.update()
            curr.colour = colour_set["visited"]
            start_cell.colour = colour_set["start"]
            stop_cell.colour = colour_set["stop"]
            self.maze.draw_grid(canvas=self.canvas)

            queue = []

            for row, col in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_row, new_col = curr.row+row, curr.col+col
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                    if self.grid[new_row][new_col] in queue:
                        continue
                    if self.grid[new_row][new_col].path:
                        self.grid[new_row][new_col].colour = colour_set["neighbour"]
                        queue.append(self.grid[new_row][new_col])

            for cell in queue:
                if cell == stop_cell:
                    return cell
                if (cell not in frontier) and (cell not in explored):
                    frontier.append(cell)
            
            for _ in explored:
                _.colour = colour_set["visited"]
        return

def main():
    nav = Navigation(file_name="maze.csv")
    # result = nav.breadth_first_search(start=(0,0), stop=(19,19))

    return

if __name__ == "__main__":
    main()