import tkinter as tk
import random


class Game:
    def __init__(self):

        # Set up the basic window
        self.window = tk.Tk()
        self.window.title("Snake Game - Python (Score: 0)")
        self.window.geometry("800x800")
        self.window.resizable(False, False)
        self.window.config(bg="white")

        # Setup main Menu
        # self.settings_canvas = tk.Canvas(self.window)

        # Setting up basic game states
        self.score = 0
        self.game_over = False
        self.food_amount = 3
        self.growth = True
        self.death = True
        self.tail_length = 4
        self.game_speed = 200
        self.food_colour = "red4"
        self.snake_colour = "lawn green"
        self.game_window = tk.Canvas(self.window, bg="white", height=800, width=800)
        self.game_window.place(x=-1, y=-1)
        self.restart_button = tk.Button(self.game_window, text="Restart", command=self.restart)
        self.game_end_id = []

        self.small = 16
        self.medium = 21
        self.large = 26

        self.move_direction = "Up"
        self.move_next = "Up"

        self.difficulty = 16
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

        self.move()

        self.window.mainloop()

    def restart(self):
        self.move_direction = "Up"
        self.move_next = "Up"
        self.game_over = False
        self.score = 0
        self.position = [0, 0]
        self.clear_tail()
        self.clear_food()
        self.clear_words()
        self.restart_button.place_forget()
        self.move()

    def clear_words(self):
        for words in self.game_end_id:
            self.game_window.delete(words)

    def clear_food(self):
        for food in self.food:
            self.game_window.delete(food[1])

        self.food = []

    def clear_tail(self):
        for segment in self.tail_segments:
            self.game_window.delete(segment[1])

        self.tail_segments = self.generate_tail()

    def spawn_food(self):
        """
        Spawns a single piece of food somewhere on the map
        """
        total_blocks = self.difficulty * self.difficulty
        half = int(total_blocks/2)
        blocks_used = 1 + len(self.tail_segments) + len(self.food) + self.tail_start_length
        print(blocks_used)

        if blocks_used > half:
            coordinate = self.find_via_grid()
        else:
            coordinate = self.find_via_random()

        food_id = self.draw_block(coordinate, "red4")
        food_item = [coordinate, food_id]
        self.food.append(food_item)

    def find_via_random(self):
        while True:
            # Choose a random place on the map
            x = random.randint(0, self.difficulty - 1)
            y = random.randint(0, self.difficulty - 1)
            coordinate = [x, y]

            free = True

            if coordinate != self.position:
                # Make sure it doesn't spawn on top of a piece of the tail
                for segment in self.tail_segments:
                    position, draw_id = segment
                    if coordinate == position:
                        free = False
                        break

                # Make sure the food doesn't spawn on top of food
                for food in self.food:
                    co_ordinate, block_id = food
                    if coordinate == co_ordinate:
                        free = False
                        break

            else:
                free = False

            if free:
                break

        return coordinate

    def find_via_grid(self) -> list:
        """
        Sometimes the amount of tries is just too many. This is to handle those conditions.
        This will regulate the amount of resources the game uses. This is more intense than
        a possible one off random selection.

        This function goes through the snake and the food lists and checks to see where the gaps are.
        it then picks one of the open spots at random and returns that.
        :return:
        """
        # Create a grid that can be used to map out the game space
        map_grid = self.create_grid(self.difficulty)

        # Map the tail-pieces
        for piece in self.tail_segments:
            co_ordinates, block_id = piece
            x, y = co_ordinates
            map_grid[x][y] = 1

        # Map food pieces
        for food in self.food:
            co_ordinates, block_id = food
            x, y = co_ordinates
            map_grid[x][y] = 1

        # Map snake head position
        x, y = self.position
        map_grid[x][y] = 1

        # Find all available spots on the map
        available_co_ordinates = []
        for x, x_line in enumerate(map_grid):
            for y, y_item in enumerate(x_line):
                if y_item == 0:
                    temp = [x, y]
                    available_co_ordinates.append(temp.copy())

        # If there are available spots return one random one.
        if len(available_co_ordinates) == 0:
            if len(self.food) == 0:
                self.game_won()
                return [-2, -2]
            return [-2, -2]
        else:
            free_spot = random.choice(available_co_ordinates)
            return free_spot

    def game_won(self):
        pass

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

    def tail_check(self):
        for co_ordinate, block_id in self.tail_segments:
            if self.position == co_ordinate:
                self.game_over = True
                display_colour = "Red"
                temp = self.game_window.create_text(400, 150, text="Game Over", fill=display_colour,
                                                    font=("Arial", 100))
                self.game_end_id.append(temp)
                temp = self.game_window.create_text(400, 275, text="Score:", fill=display_colour, font=("Arial", 100))
                self.game_end_id.append(temp)
                temp = self.game_window.create_text(400, 425, text=self.score, fill=display_colour, font=("Arial", 100))
                self.game_end_id.append(temp)
                self.restart_button.place(x=400, y=500)

    def eat_food(self, index: int):
        co_ordinate, block_id = self.food[index]
        self.game_window.delete(block_id)
        self.food.pop(index)

        if self.growth:
            self.grow_tail()

        self.score += 1
        self.window.title(f"Snake Game - Python (Score: {self.score})")

    def grow_tail(self):
        x = y = self.difficulty * 2
        co_ordinates = [x, y]
        block_id = self.draw_block(co_ordinates)
        new_tail_piece = [co_ordinates, block_id]
        self.tail_segments.append(new_tail_piece)

    def move_tail(self):
        index = len(self.tail_segments) - 1
        last_segment = self.tail_segments[index].copy()
        self.tail_segments.pop(index)
        last_segment[0] = self.position.copy()
        new_segment = self.redraw_tail(last_segment)
        self.tail_segments.insert(0, new_segment)

    def generate_tail(self):
        output = []
        x, y = self.position
        y += 1
        for i in range(self.tail_length):
            y += i
            temp = self.draw_block([x, y], self.snake_colour)
            output.append([[x, y], temp])
        return output

    def redraw(self):
        self.game_window.delete(self.last_drawn)
        self.last_drawn = self.draw_block(self.position, self.snake_colour)

    def redraw_tail(self, segment):
        self.game_window.delete(segment[1])
        new = self.draw_block(segment[0], self.snake_colour)
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
        if len(self.food) < self.food_amount:
            self.spawn_food()

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

        if self.death:
            self.tail_check()

        # Pycharm my IDE is putting a type error on this.
        # But it works, so I am suppressing the error
        if not self.game_over:
            # noinspection PyTypeChecker
            self.window.after(ms=self.game_speed, func=self.move)
        else:
            print(f"Game Over\nScore: {self.score}")

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
            grid.append(line.copy())

        return grid


if __name__ == "__main__":
    Game()
