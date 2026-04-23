import tkinter as tk
import random
import time


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
        self.autopilot = True
        self.tail_length = 4
        self.game_speed = 50
        self.food_colour = "red4"
        self.snake_colour = "lawn green"

        self.game_window = tk.Canvas(self.window, bg="white", height=800, width=800)

        # Pause screen setup
        colour = "gray90"
        self.pause = False
        self.pause_screen = tk.Canvas(self.game_window, bg=colour, height=600, width=200, highlightthickness=1,
                                      highlightbackground="black")

        self.title = tk.Label(self.pause_screen, bg=colour, text="Options", font=("Helvetica", 12, "bold"))

        self.food_title = tk.Label(self.pause_screen, bg=colour, text="Food Amount")
        self.food_box = tk.Entry(self.pause_screen, bg="white")

        self.tail_title = tk.Label(self.pause_screen, bg=colour, text="Tail Start Length")
        self.tail_box = tk.Entry(self.pause_screen, bg="white")

        self.speed_title = tk.Label(self.pause_screen, bg=colour, text="Game Speed")
        self.speed_box = tk.Entry(self.pause_screen, bg="white")

        self.growth_toggle = tk.Button(self.pause_screen, text="Growth", bg=colour, fg="green", width=16,
                                       command=self.growth_button)
        self.death_toggle = tk.Button(self.pause_screen, text="Death", bg=colour, fg="green", width=16,
                                      command=self.death_button)
        self.autopilot_toggle = tk.Button(self.pause_screen, text="Auto Pilot", bg=colour, fg="red", width=16,
                                          command=self.auto_pilot_button)

        self.unpause_active = tk.Button(self.pause_screen, text="Unpause", bg=colour, width=16,
                                        command=self.unpause_button)
        self.restart_active = tk.Button(self.pause_screen, text="Restart", bg=colour, width=16,
                                        command=self.restart_button)

        self.title.pack(pady=20)
        self.food_title.pack()
        self.food_box.pack(padx=20)
        self.tail_title.pack()
        self.tail_box.pack()
        self.speed_title.pack()
        self.speed_box.pack()
        self.growth_toggle.pack()
        self.death_toggle.pack()
        self.autopilot_toggle.pack()
        self.restart_active.pack()
        self.unpause_active.pack(padx=20, pady=20)

        self.window.bind("<Escape>", lambda a: self.pause_menu())
        # Pause screen end

        self.game_window.place(x=-1, y=-1)
        self.restart_button = tk.Button(self.game_window, text="Restart", command=self.restart)
        self.game_end_id = []

        self.small = 16
        self.medium = 21
        self.large = 26

        self.move_direction = "Up"
        self.move_next = "Up"

        self.map_size = 16
        self.create_grid(10)
        self.block_size = 790/self.map_size
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
        total_blocks = self.map_size * self.map_size
        half = int(total_blocks/2)
        blocks_used = 1 + len(self.tail_segments) + len(self.food) + self.tail_start_length

        if blocks_used > half:
            coordinate = self.find_via_grid()
        else:
            coordinate = self.find_via_random()

        if coordinate[1]:
            food_id = self.draw_block(coordinate[0], "red4")
            food_item = [coordinate[0], food_id]
            self.food.append(food_item)
        else:
            if len(self.food) == 0:
                self.game_won()

    def find_via_random(self):
        while True:
            # Choose a random place on the map
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
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

        return [coordinate, True]

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
        map_grid = self.create_grid(self.map_size)

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
                return ["gg", False]
            return ["gg", False]
        else:
            free_spot = random.choice(available_co_ordinates)
            return [free_spot, True]

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
        index = len(self.tail_segments) - 1
        segment = self.tail_segments[index]
        x, y = segment[0]
        co_ordinates = [x, y]
        block_id = self.draw_block(co_ordinates, self.snake_colour)
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
        size = self.map_size
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

    def auto_move(self):
        x, y = self.position
        if y == 0:
            if x % 2 == 0:
                self.move_next = "Right"
            else:
                self.move_next = "Down"

        if y == self.map_size - 1:
            if x % 2 == 1:
                self.move_next = "Right"
            else:
                self.move_next = "Up"

    def update_menu(self):
        self.food_box.delete(0, tk.END)
        self.food_box.insert(0, str(self.food_amount))
        self.food_box.update()

        self.tail_box.delete(0, tk.END)
        self.tail_box.insert(0, str(self.tail_start_length))
        self.tail_box.update()

        self.speed_box.delete(0, tk.END)
        self.speed_box.insert(0, str(self.game_speed))
        self.speed_box.update()

        if self.growth:
            self.growth_toggle.config(fg="green")
        else:
            self.growth_toggle.config(fg="red")

        if self.death:
            self.death_toggle.config(fg="green")
        else:
            self.death_toggle.config(fg="red")

        if self.autopilot:
            self.autopilot_toggle.config(fg="green")
        else:
            self.autopilot_toggle.config(fg="red")

    def pause_menu(self):
        self.pause = True
        self.update_menu()
        self.pause_screen.place(x=200, y=200)

    def growth_button(self):
        if self.growth:
            self.growth = False
            self.growth_toggle.config(fg="red")
            self.growth_toggle.update()
        else:
            self.growth = True
            self.growth_toggle.config(fg="green")
            self.growth_toggle.update()

    def death_button(self):
        if self.death:
            self.death = False
            self.death_toggle.config(fg="red")
            self.death_toggle.update()
        else:
            self.death = True
            self.death_toggle.config(fg="green")
            self.death_toggle.update()

    def auto_pilot_button(self):
        if self.autopilot:
            self.autopilot = False
            self.autopilot_toggle.config(fg="red")
            self.autopilot_toggle.update()
        else:
            self.autopilot = True
            self.autopilot_toggle.config(fg="green")
            self.autopilot_toggle.update()

    def restart_button(self):
        self.update_settings()
        self.pause = False
        self.restart()

    def unpause_button(self):
        # food tail speed
        self.update_settings()
        self.pause = False
        self.pause_screen.place_forget()
        self.count_down_start()

    def update_settings(self):
        food = int(self.food_box.get())
        self.food_amount = food

        tail = int(self.tail_box.get())
        self.tail_start_length = tail

        speed = int(self.speed_box.get())
        self.game_speed = speed

    def hide_menu(self):
        self.pause_screen.place_forget()

    def count_down_start(self):
        temp = self.game_window.create_text(400, 425, text="3", fill="red", font=("Arial", 100))
        self.game_window.update()
        time.sleep(1)
        self.game_window.delete(temp)
        temp = self.game_window.create_text(400, 425, text="2", fill="red", font=("Arial", 100))
        self.game_window.update()
        time.sleep(1)
        self.game_window.delete(temp)
        temp = self.game_window.create_text(400, 425, text="1", fill="red", font=("Arial", 100))
        self.game_window.update()
        time.sleep(1)
        self.game_window.delete(temp)
        self.move()

    def move(self):
        if self.autopilot:
            self.auto_move()

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
        if not self.pause:
            if not self.game_over:
                # noinspection PyTypeChecker
                self.window.after(ms=self.game_speed, func=self.move)
            else:
                print(f"Game Over\nScore: {self.score}")

    def move_right(self):
        if self.position[0] == self.map_size - 1:
            self.position[0] = 0
        else:
            self.position[0] += 1
        self.redraw()

    def move_left(self):
        if self.position[0] == 0:
            self.position[0] = self.map_size - 1
        else:
            self.position[0] -= 1
        self.redraw()

    def move_up(self):
        if self.position[1] == 0:
            self.position[1] = self.map_size - 1
        else:
            self.position[1] -= 1
        self.redraw()

    def move_down(self):
        if self.position[1] == self.map_size - 1:
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
