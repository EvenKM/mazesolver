from tkinter import Tk, BOTH, Canvas
import time
import random

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, x1, x2, y1, y2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.window = window
        self.left_wall = Line(Point(x1, y1), Point(x1, y2))
        self.right_wall = Line(Point(x2, y1), Point(x2, y2))
        self.top_wall = Line(Point(x1, y1), Point(x2, y1))
        self.bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        self.visited = False
    
    def update_walls(self):
        self.left_wall = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        self.right_wall = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        self.top_wall = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        self.bottom_wall = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

    def draw(self):
        if self.has_left_wall:
            self.window.draw_line(self.left_wall, "black")
        else:
            self.window.draw_line(self.left_wall, "#d9d9d9")
        if self.has_right_wall:
            self.window.draw_line(self.right_wall, "black")
        else:
            self.window.draw_line(self.right_wall, "#d9d9d9")
        if self.has_top_wall:
            self.window.draw_line(self.top_wall, "black")
        else:
            self.window.draw_line(self.top_wall, "#d9d9d9")
        if self.has_bottom_wall:
            self.window.draw_line(self.bottom_wall, "black")
        else:
            self.window.draw_line(self.bottom_wall, "#d9d9d9")
    
    def draw_move(self, dest_cell, undo=False):
        self_center = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        dest_center = Point((dest_cell.x1 + dest_cell.x2) / 2, (dest_cell.y1 + dest_cell.y2) / 2)
        if undo:
            self.window.draw_line(Line(self_center, dest_center), "red")
        else:
            self.window.draw_line(Line(self_center, dest_center), "black")

class Maze():
    def __init__(self, x1, y1, num_cols, num_rows, cell_size_x, cell_size_y, win, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        random.seed(self.seed)

        
        self.create_cells()

    def create_cells(self):
        self.cells = []
        for x in range(0, self.num_cols):
            column = []
            for y in range(0, self.num_rows):
                new_cell = Cell(self.x1 + x*self.cell_size_x,
                                self.x1 + (x+1)*self.cell_size_x,
                                self.y1 + y*self.cell_size_y,
                                self.y1 + (y+1)*self.cell_size_y,
                                self.win)
                column.append(new_cell)
            self.cells.append(column)
        
        self.draw_cells()


    def draw_cells(self):
        for col in self.cells:
            for cell in col:
                cell.draw()
        self.animate()
    
    def break_entrance_and_exit(self):
        self.cells[0][0].has_left_wall = False
        self.cells[-1][-1].has_right_wall = False
        self.draw_cells()

    def break_walls_r(self, x, y):
        current_cell = self.cells[x][y]
        current_cell.visited = True
        while True:
            to_visit = []
            if (y > 0 and not self.cells[x][y-1].visited):
                to_visit.append([x, y-1, "up"])
            if (x < (self.num_cols-1) and not self.cells[x+1][y].visited):
                to_visit.append([x+1, y, "right"])
            if (y < (self.num_rows-1) and not self.cells[x][y+1].visited):
                to_visit.append([x, y+1, "down"])
            if (x > 0 and not self.cells[x-1][y].visited):
                to_visit.append([x-1, y, "left"])
            if len(to_visit) == 0:
                self.cells[x][y].draw()
                return
            dir = to_visit[random.randrange(len(to_visit))]
            next_cell = self.cells[dir[0]][dir[1]]
            match dir[2]:
                case "up":
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                case "right":
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                case "down":
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                case "left":
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
            self.break_walls_r(dir[0], dir[1])


    def reset_cells_visited(self):
        for column in self.cells:
            for cell in column:
                cell.visited = False
    
    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, x, y):
        self.animate()
        current_cell = self.cells[x][y]
        current_cell.visited = True
        if current_cell == self.cells[-1][-1]:
            return True
        if (y > 0 and not current_cell.has_top_wall and not self.cells[x][y-1].visited):
            current_cell.draw_move(self.cells[x][y-1])
            if self.solve_r(x, y-1):
                return True
            current_cell.draw_move(self.cells[x][y-1], undo=True)
        if (x < (self.num_cols-1) and not current_cell.has_right_wall and not self.cells[x+1][y].visited):
            current_cell.draw_move(self.cells[x+1][y])
            if self.solve_r(x+1, y):
                return True
            current_cell.draw_move(self.cells[x+1][y], undo=True)
        if (y < (self.num_rows-1) and not current_cell.has_bottom_wall and not self.cells[x][y+1].visited):
            current_cell.draw_move(self.cells[x][y+1])
            if self.solve_r(x, y+1):
                return True
            current_cell.draw_move(self.cells[x][y+1], undo=True)
        if (x > 0 and not current_cell.has_left_wall and not self.cells[x-1][y].visited):
            current_cell.draw_move(self.cells[x-1][y])
            if self.solve_r(x-1, y):
                return True
            current_cell.draw_move(self.cells[x-1][y], undo=True)
        return False

    def animate(self):
        self.win.redraw()
        time.sleep(0.05)

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Mazesolver")
        self.canvas = Canvas(width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True
        while (self.running):
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

def main():
    win = Window(800, 600)
    maze = Maze(50, 50, 12, 12, 40, 40, win)
    maze.break_entrance_and_exit()
    maze.break_walls_r(0, 0)
    maze.reset_cells_visited()
    maze.solve()
    win.wait_for_close()

main()
