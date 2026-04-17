import tkinter as tk
import random


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
        self.food = []

        # Controls
        self.window.bind("<Right>", lambda a: self.right())
        self.window.bind("<Left>", lambda a: self.left())
        self.window.bind("<Up>", lambda a: self.up())
        self.window.bind("<Down>", lambda a: self.down())
        self.window.bind("<f>", lambda a: self.spawn_food())

        self.move()

        self.window.mainloop()

    def spawn_food(self):
        tries = 0
        while True:
            tries += 1
            print(tries)
            x = random.randint(0, self.difficulty - 1)
            y = random.randint(0, self.difficulty - 1)

            coordinate = [x, y]
            free = True

            if coordinate != self.position:
                for segment in self.tail_segments:
                    position, draw_id = segment
                    if coordinate == position:
                        free = False
            else:
                free = False

            if free:
                break

        food_id = self.draw_block(coordinate, "red")
        food_item = [coordinate, food_id]
        self.food.append(food_item)

    def food_check(self):
        food_found = False
        food_index = "Bad"
        for index, food in enumerate(self.food):
            co_ordinate, block_id = food
            if self.position == co_ordinate:
                food_found = True
                food_index = index
                break

        if food_found:
            self.eat_food(food_index)

    def eat_food(self, index: int):
        co_ordinate, block_id = self.food[index]
        self.game_window.delete(block_id)
        self.food.pop(index)

    def move_tail(self):
        index = len(self.tail_segments) - 1
        last_segment = self.tail_segments[index].copy()
        self.tail_segments.pop(index)
        last_segment[0] = self.position.copy()
        new_segment = self.redraw_tail(last_segment)
        self.tail_segments.insert(0, new_segment)

    def generate_tail(self):
        output = []
        for i in range(self.tail_length):
            x, y = self.position

            y += 1

            y += i
            temp = self.draw_block([x, y])
            output.append([[x, y], temp])
        return output

    def redraw(self):
        self.game_window.delete(self.last_drawn)
        self.last_drawn = self.draw_block(self.position)

    def redraw_tail(self, segment):
        self.game_window.delete(segment[1])
        new = self.draw_block(segment[0])
        segment[1] = new
        return segment

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

        self.food_check()

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
