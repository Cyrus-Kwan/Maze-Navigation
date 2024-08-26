from cell import Cell
import tkinter as tk
import time

class Maze():
    def __init__(self, rows:int=None, cols:int=None, file_name:str=None):
        self.rows:int = rows
        self.cols:int = cols

        if file_name:
            print("importing")
            self.grid = self.import_grid(file=file_name)
        else:
            print("generating")
            self.grid = self.create_grid()

        self.width:int = self.cols * Cell.size
        self.height:int = self.rows * Cell.size
    
    def draw_grid(self, canvas:tk.Canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x1:int = col * Cell.size
                y1:int = row * Cell.size
                x2:int = x1 + Cell.size
                y2:int = y1 + Cell.size

                colour:str = self.grid[row][col].colour
                canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="black")

    def export_grid(self, file_name:str):
        with open(file=file_name, mode="w") as file:
            columns:str = ","+",".join([f"{i}" for i in range(len(self.grid))])
            matrix:list[str] = [columns]
            for r, row in enumerate(self.grid):
                items:list[str] = [f"{int(cell.wall)}" for cell in row]
                line:str = f"{r},"+",".join(items)
                matrix.append(line)
            lines:str = "\n".join(matrix)
            file.writelines(lines)

    def import_grid(self, file:str):
        with open(file=file, mode="r") as file:
            string:str = file.read()
            matrix:list = [row.split(",")[1:] for row in string.split("\n")[1:]]
            self.rows = len(matrix)
            self.cols = len(matrix[0])

        grid = [[] for line in matrix]
        for r, row in enumerate(matrix):
            for c, col in enumerate(matrix[r]):
                wall = True if int(matrix[r][c]) == 1 else False
                grid[r].append(Cell(row=r, col=c, wall=wall))

        return grid
    
    def create_grid(self):
        grid = [[Cell(row=row, col=col) for col in range(self.cols)] for row in range(self.rows)]
        return grid

def main():
    root = tk.Tk()
    maze = Maze(file_name="test")
    canvas = tk.Canvas(root, width=maze.width, height=maze.height)
    canvas.pack()

    maze.draw_grid(canvas=canvas)
    # while True:
    #     maze.new_grid()
    #     maze.draw_grid(canvas=canvas)
    #     root.update()
    #     time.sleep(1)

    root.mainloop()
    return

if __name__ == "__main__":
    main()