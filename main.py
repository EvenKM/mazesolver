from tkinter import Tk, BOTH, Canvas

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
    
    def update_walls(self):
        self.left_wall = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        self.right_wall = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        self.top_wall = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        self.bottom_wall = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

    def draw(self):
        if self.has_left_wall:
            self.window.draw_line(self.left_wall, "black")
        if self.has_right_wall:
            self.window.draw_line(self.right_wall, "black")
        if self.has_top_wall:
            self.window.draw_line(self.top_wall, "black")
        if self.has_bottom_wall:
            self.window.draw_line(self.bottom_wall, "black")
    
    def draw_move(self, dest_cell, undo=False):
        self_center = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        dest_center = Point((dest_cell.x1 + dest_cell.x2) / 2, (dest_cell.y1 + dest_cell.y2) / 2)
        if undo:
            self.window.draw_line(Line(self_center, dest_center), "red")
        else:
            self.window.draw_line(Line(self_center, dest_center), "black")

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
    line1 = Line(Point(200, 200), Point(400, 400))
    win.draw_line(line1, "black")
    cell1 = Cell(100, 140, 100, 140, win)
    cell1.draw()
    cell2 = Cell(200, 240, 200, 240, win)
    cell2.has_bottom_wall = False
    cell2.has_top_wall = False
    cell2.draw()
    cell1.draw_move(cell2)
    win.wait_for_close()

main()
