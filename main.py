import tkinter as tk


class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game - Python")
        self.window.geometry("800x800")
        self.window.config(bg="white")

        # Setup main Menu


        self.window.mainloop()


if __name__ == "__main__":
    Game()
