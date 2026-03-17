import tkinter as tk
from peg_game import PegSolitaireGame

class PegSolitaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire GUI")
        self.root.geometry("850x520")

        self.game = None
        self.selected = None

        self.board_size_var = tk.StringVar(value="7")
        self.board_type_var = tk.StringVar(value="English")
        self.status_var = tk.StringVar(value="Select board size/type, then click 'Start New Game'.")

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Solitaire Game", font=("Arial", 16)).place(x=10, y=10)

        tk.Label(self.root, text="Board size").place(x=600, y=15)
        tk.Spinbox(self.root, from_=5, to=15, increment=2,
                   textvariable=self.board_size_var, width=4).place(x=680, y=15)

        tk.Label(self.root, text="Board type").place(x=10, y=60)

        tk.Radiobutton(self.root, text="English",
                       variable=self.board_type_var, value="English").place(x=10, y=90)
        tk.Radiobutton(self.root, text="European",
                       variable=self.board_type_var, value="European").place(x=10, y=115)
        tk.Radiobutton(self.root, text="Triangle",
                       variable=self.board_type_var, value="Triangle").place(x=10, y=140)

        tk.Button(self.root, text="Start New Game",
                  command=self.start_new_game).place(x=10, y=180)

        self.status_label = tk.Label(self.root, textvariable=self.status_var)
        self.status_label.place(x=10, y=230)

        self.canvas = tk.Canvas(self.root, width=520, height=420, bg="white")
        self.canvas.place(x=280, y=70)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def start_new_game(self):
        size = int(self.board_size_var.get())
        btype = self.board_type_var.get()

        self.game = PegSolitaireGame(btype, size)
        self.selected = None
        self.render_board()

        self.status_var.set(f"New game started | Type: {btype} | Size: {size}")

    def render_board(self):
        self.canvas.delete("all")

        if not self.game:
            return

        cell = 40
        pad = 10

        for r in range(self.game.size):
            for c in range(self.game.size):
                val = self.game.board[r][c]
                if val == -1:
                    continue

                x0 = pad + c * cell
                y0 = pad + r * cell
                x1 = x0 + cell
                y1 = y0 + cell

                self.canvas.create_oval(x0+8, y0+8, x1-8, y1-8, outline="black")

                if val == 1:
                    self.canvas.create_oval(x0+12, y0+12, x1-12, y1-12, fill="blue")

    def on_canvas_click(self, event):
        if not self.game:
            return

        cell = 40
        pad = 10

        r = (event.y - pad) // cell
        c = (event.x - pad) // cell

        if not self.game.in_bounds(r, c):
            return

        if self.game.board[r][c] == 1:
            self.selected = (r, c)
            self.status_var.set(f"Selected peg at {r},{c}")
            return

        if self.game.board[r][c] == 0 and self.selected:
            sr, sc = self.selected
            if self.game.try_move(sr, sc, r, c):
                self.selected = None
                self.render_board()

                if self.game.is_game_over():
                    self.status_var.set("Game Over")
                else:
                    self.status_var.set("Move successful")
            else:
                self.status_var.set("Invalid move")

if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireApp(root)
    root.mainloop()