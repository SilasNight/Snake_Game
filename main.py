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

        self.game_window.create_rectangle(5, 5, 795, 795, width=10)


        self.window.mainloop()


if __name__ == "__main__":
    Game()
