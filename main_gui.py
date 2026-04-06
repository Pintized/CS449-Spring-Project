import tkinter as tk
from peg_game import BaseSolitaireGame, ManualSolitaireGame, AutomatedSolitaireGame


class PegSolitaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire GUI")
        self.root.geometry("900x560")

        self.game = None
        self.selected = None

        self.board_size_var = tk.StringVar(value="7")
        self.board_type_var = tk.StringVar(value="English")
        self.game_mode_var = tk.StringVar(value="Manual")
        self.status_var = tk.StringVar(value="Select board size/type/mode, then click 'Start New Game'.")

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Solitaire Game", font=("Arial", 16)).place(x=10, y=10)

        tk.Label(self.root, text="Board size").place(x=600, y=15)
        tk.Spinbox(self.root, from_=5, to=15, increment=2,
                   textvariable=self.board_size_var, width=4).place(x=680, y=15)

        tk.Label(self.root, text="Board type").place(x=10, y=60)
        tk.Radiobutton(self.root, text="English",
                       variable=self.board_type_var, value="English").place(x=10, y=90)
        tk.Radiobutton(self.root, text="Hexagon",
                       variable=self.board_type_var, value="Hexagon").place(x=10, y=115)
        tk.Radiobutton(self.root, text="Diamond",
                       variable=self.board_type_var, value="Diamond").place(x=10, y=140)

        tk.Label(self.root, text="Game mode").place(x=120, y=60)
        tk.Radiobutton(self.root, text="Manual",
                       variable=self.game_mode_var, value="Manual").place(x=120, y=90)
        tk.Radiobutton(self.root, text="Automated",
                       variable=self.game_mode_var, value="Automated").place(x=120, y=115)

        tk.Button(self.root, text="Start New Game",
                  command=self.start_new_game).place(x=10, y=180)
        tk.Button(self.root, text="Randomize",
                  command=self.randomize_board).place(x=125, y=180)
        tk.Button(self.root, text="Autoplay Step",
                  command=self.autoplay_step).place(x=215, y=180)
        tk.Button(self.root, text="Autoplay To End",
                  command=self.autoplay_to_end).place(x=315, y=180)

        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w", justify="left")
        self.status_label.place(x=10, y=230)

        self.canvas = tk.Canvas(self.root, width=560, height=440, bg="white")
        self.canvas.place(x=280, y=70)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def start_new_game(self):
        size = int(self.board_size_var.get())
        btype = self.board_type_var.get()
        mode = self.game_mode_var.get()

        if mode == "Manual":
            self.game = ManualSolitaireGame(btype, size)
        else:
            self.game = AutomatedSolitaireGame(btype, size)

        self.selected = None
        self.render_board()
        self.status_var.set(f"New {mode.lower()} game started | Type: {btype} | Size: {self.game.size}")

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

                outline_width = 3 if self.selected == (r, c) else 1
                self.canvas.create_oval(x0 + 8, y0 + 8, x1 - 8, y1 - 8,
                                        outline="black", width=outline_width)

                if val == 1:
                    self.canvas.create_oval(x0 + 12, y0 + 12, x1 - 12, y1 - 12, fill="blue")
                elif val == 0:
                    self.canvas.create_oval(x0 + 16, y0 + 16, x1 - 16, y1 - 16, fill="lightgray")

    def on_canvas_click(self, event):
        if not self.game:
            return
        if not isinstance(self.game, ManualSolitaireGame):
            self.status_var.set("Canvas clicking is only used in Manual mode.")
            return

        cell = 40
        pad = 10
        r = (event.y - pad) // cell
        c = (event.x - pad) // cell

        if not self.game.in_bounds(r, c):
            return

        if self.game.board[r][c] == 1:
            self.selected = (r, c)
            self.render_board()
            self.status_var.set(f"Selected peg at {r},{c}")
            return

        if self.game.board[r][c] == 0 and self.selected:
            sr, sc = self.selected
            if self.game.make_manual_move(sr, sc, r, c):
                self.selected = None
                self.render_board()
                if self.game.is_game_over():
                    self.status_var.set("Manual game over")
                else:
                    self.status_var.set("Move successful")
            else:
                self.status_var.set("Invalid move")

    def randomize_board(self):
        if not self.game:
            return
        if not isinstance(self.game, ManualSolitaireGame):
            self.status_var.set("Randomize is only available during a manual game.")
            return

        changed = self.game.randomize_state(steps=5)
        self.selected = None
        self.render_board()

        if not changed:
            self.status_var.set("No legal moves available to randomize.")
        elif self.game.is_game_over():
            self.status_var.set("Board randomized. Manual game over.")
        else:
            self.status_var.set("Board randomized using legal moves.")

    def autoplay_step(self):
        if not self.game:
            return
        if not isinstance(self.game, AutomatedSolitaireGame):
            self.status_var.set("Autoplay is only available in automated mode.")
            return

        moved = self.game.make_automated_move()
        self.render_board()
        if moved:
            if self.game.is_game_over():
                self.status_var.set("Automated move made. Automated game over.")
            else:
                self.status_var.set("Automated move made.")
        else:
            self.status_var.set("No automated move available. Automated game over.")

    def autoplay_to_end(self):
        if not self.game:
            return
        if not isinstance(self.game, AutomatedSolitaireGame):
            self.status_var.set("Autoplay is only available in automated mode.")
            return

        steps = self.game.autoplay_to_end()
        self.render_board()
        self.status_var.set(f"Autoplay finished after {steps} automated move(s).")


if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireApp(root)
    root.mainloop()
