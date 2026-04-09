import tkinter as tk


class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game - Python")
        self.window.geometry("800x800")
        self.window.resizable(False, False)
        self.window.config(bg="white")

        # Setup main Menu
        # self.settings_canvas = tk.Canvas(self.window)

        self.tail_length = 4
        self.game_window = tk.Canvas(self.window, bg="white", height=800, width=800)
        self.game_window.place(x=-1, y=-1)

        self.easy = 16
        self.medium = 21
        self.hard = 26
        self.difficulty = self.easy
        self.create_grid(10)
        self.block_size = 790/self.difficulty
        self.position = [0, 0]

        self.last_drawn = self.draw_block(self.position)

        self.draw_grid()

        # Controls
        self.window.bind("<Right>", lambda a: self.move_right())
        self.window.bind("<Left>", lambda a: self.move_left())
        self.window.bind("<Up>", lambda a: self.move_up())
        self.window.bind("<Down>", lambda a: self.move_down())

        self.window.mainloop()

    def redraw(self):
        self.game_window.delete(self.last_drawn)
        self.last_drawn = self.draw_block(self.position)

    def draw_block(self, position: list, colour: str = "blue") -> int:
        x, y = position
        block = self.block_size
        # So that the grid corresponds to the size of the canvas
        x *= block
        y *= block

        # For the border... Should be more
        x += 8
        y += 8

        rectangle_id = self.game_window.create_rectangle(x + 1, y + 1, x + block - 6, y + block - 6, fill=colour)

        return rectangle_id

    def draw_grid(self):
        size = self.difficulty
        block = self.block_size
        x = 5
        y = 5
        for i in range(size + 1):
            self.game_window.create_line(x, y, x + 790, y, fill="grey")
            y += block

        x = 5
        y = 5
        for i in range(size + 1):
            self.game_window.create_line(x, y, x, y + 790, fill="grey")
            x += block

    def move_right(self):
        if self.position[0] == self.difficulty - 1:
            self.position[0] = 0
        else:
            self.position[0] += 1
        self.redraw()

    def move_left(self):
        if self.position[0] == 0:
            self.position[0] = self.difficulty - 1
        else:
            self.position[0] -= 1
        self.redraw()

    def move_up(self):
        if self.position[1] == 0:
            self.position[1] = self.difficulty - 1
        else:
            self.position[1] -= 1
        self.redraw()

    def move_down(self):
        if self.position[1] == self.difficulty - 1:
            self.position[1] = 0
        else:
            self.position[1] += 1
        self.redraw()

    @staticmethod
    def create_grid(size: int) -> list:
        line = list(range(size))
        line = [x-x for x in line]
        grid = []
        for i in range(size):
            grid.append(line)

        return grid


if __name__ == "__main__":
    Game()
