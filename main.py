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

        self.small = 16
        self.medium = 21
        self.Large = 26

        self.move_direction = "Up"
        self.move_next = "Up"

        self.difficulty = self.small
        self.create_grid(10)
        self.block_size = 790/self.difficulty
        self.position = [0, 0]

        self.last_drawn = self.draw_block(self.position)

        self.tail_start_length = 10
        self.tail_segments = self.generate_tail()

        self.draw_grid()

        # Controls
        self.window.bind("<Right>", lambda a: self.right())
        self.window.bind("<Left>", lambda a: self.left())
        self.window.bind("<Up>", lambda a: self.up())
        self.window.bind("<Down>", lambda a: self.down())

        self.move()

        self.window.mainloop()

    def move_tail(self):
        reverse_list = reversed(list(range(len(self.tail_segments))))
        for i in reverse_list:
            if i == 0:
                self.tail_segments[i][0] = self.position.copy()
            else:
                self.tail_segments[i][0] = self.tail_segments[i - 1][0].copy()
            old = self.tail_segments[i]
            new = self.redraw_tail(old)
            self.tail_segments[i][1] = new

    def generate_tail(self):
        output = []
        for i in range(self.tail_length):
            x, y = self.position

            y += 1

            y += i
            print(x, y)
            temp = self.draw_block([x, y])
            output.append([[x, y], temp])
        return output

    def redraw(self):
        self.game_window.delete(self.last_drawn)
        self.last_drawn = self.draw_block(self.position)

    def redraw_tail(self, old):
        self.game_window.delete(old[1])
        new = self.draw_block(old[0])
        return new

    def draw_block(self, position: list, colour: str = "blue") -> int:
        x, y = position
        block = self.block_size
        # So that the grid corresponds to the size of the canvas
        x *= block
        y *= block

        # For the border... Should be more
        x += 5
        y += 5

        rectangle_id = self.game_window.create_rectangle(x + 2, y + 2, x + block - 2, y + block - 2, fill=colour)

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

    def move(self):
        horizontal = ["Left", "Right"]
        vertical = ["Up", "Down"]

        if self.move_direction != self.move_next:
            if self.move_direction in horizontal:
                if self.move_next not in horizontal:
                    self.move_direction = self.move_next
            else:
                if self.move_next not in vertical:
                    self.move_direction = self.move_next

        self.move_tail()

        match self.move_direction:
            case "Up":
                self.move_up()
            case "Down":
                self.move_down()
            case "Right":
                self.move_right()
            case "Left":
                self.move_left()

        self.window.after(ms=100, func=self.move)

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

    def up(self):
        self.move_next = "Up"

    def down(self):
        self.move_next = "Down"

    def right(self):
        self.move_next = "Right"

    def left(self):
        self.move_next = "Left"

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
