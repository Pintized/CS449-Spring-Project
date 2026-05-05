import json
import tkinter as tk
from tkinter import filedialog, messagebox

from peg_game import ManualSolitaireGame, AutomatedSolitaireGame


class PegSolitaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solitaire GUI")
        self.root.geometry("900x560")

        self.game = None
        self.selected = None

        self.replay_moves = []
        self.replay_index = 0
        self.replay_file_loaded = None

        self.board_size_var = tk.StringVar(value="7")
        self.board_type_var = tk.StringVar(value="English")
        self.game_mode_var = tk.StringVar(value="Manual")
        self.record_game_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Select board size/type/mode, then click 'New Game'.")

        self.recording_file = "recorded_game.txt"

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Sample GUI of Solitaire", font=("Arial", 16)).place(x=10, y=10)

        tk.Label(self.root, text="Board size").place(x=600, y=15)
        tk.Spinbox(self.root, from_=5, to=15, increment=2,
                   textvariable=self.board_size_var, width=4).place(x=680, y=15)

        tk.Label(self.root, text="Board Type").place(x=10, y=60)
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

        tk.Button(self.root, text="Replay", width=14,
                  command=self.replay_button_clicked).place(x=840, y=105)
        tk.Button(self.root, text="New Game", width=14,
                  command=self.start_new_game).place(x=840, y=145)
        tk.Button(self.root, text="Save Recording", width=14,
                  command=self.save_recording_as).place(x=840, y=185)

        tk.Button(self.root, text="Autoplay", width=14,
                  command=self.autoplay_step, bg="#90d84f").place(x=840, y=330)
        tk.Button(self.root, text="Randomize", width=14,
                  command=self.randomize_board, bg="#90d84f").place(x=840, y=370)

        tk.Checkbutton(self.root, text="Record game",
                       variable=self.record_game_var).place(x=10, y=345)

        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w", justify="left")
        self.status_label.place(x=10, y=500)

        self.canvas = tk.Canvas(self.root, width=560, height=420, bg="white")
        self.canvas.place(x=220, y=70)
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
        self.replay_moves = []
        self.replay_index = 0
        self.replay_file_loaded = None

        self.render_board()
        self.status_var.set(f"New {mode.lower()} game started | Type: {btype} | Size: {self.game.size}")
        self._auto_save_recording()

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
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=outline_width)

                if val == 1:
                    self.canvas.create_oval(x0 + 12, y0 + 12, x1 - 12, y1 - 12, fill="black")
                elif val == 0:
                    self.canvas.create_oval(x0 + 16, y0 + 16, x1 - 16, y1 - 16, fill="white", outline="white")

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
                self._auto_save_recording()
                if self.game.is_game_over():
                    self.status_var.set("Move successful. Manual game over.")
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
        self._auto_save_recording()

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
        self._auto_save_recording()
        if moved:
            if self.game.is_game_over():
                self.status_var.set("Automated move made. Automated game over.")
            else:
                self.status_var.set("Automated move made.")
        else:
            self.status_var.set("No automated move available. Automated game over.")

    # ---------------- Recording / Replay ----------------

    def build_recording_data(self):
        if not self.game:
            return None
        return {
            "board_type": self.game.board_type,
            "board_size": self.game.size,
            "game_mode": self.game_mode_var.get(),
            "moves": self.game.move_history
        }

    def _auto_save_recording(self):
        if not self.record_game_var.get() or not self.game:
            return

        data = self.build_recording_data()
        with open(self.recording_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def save_recording_as(self):
        if not self.game:
            self.status_var.set("Start a game before saving a recording.")
            return

        path = filedialog.asksaveasfilename(
            title="Save game recording",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return

        data = self.build_recording_data()
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        self.status_var.set(f"Recording saved to {path}")

    def replay_button_clicked(self):
        # First click loads a file. Later clicks replay one move at a time.
        if not self.replay_moves:
            self.load_replay_file()
        else:
            self.replay_next_move()

    def load_replay_file(self):
        path = filedialog.askopenfilename(
            title="Open recorded game",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as error:
            messagebox.showerror("Replay Error", f"Could not read replay file.\n\n{error}")
            return

        btype = data["board_type"]
        size = int(data["board_size"])
        moves = data.get("moves", [])

        self.board_type_var.set(btype)
        self.board_size_var.set(str(size))
        self.game_mode_var.set("Manual")
        self.game = ManualSolitaireGame(btype, size)
        self.game.move_history = []
        self.selected = None

        self.replay_moves = moves
        self.replay_index = 0
        self.replay_file_loaded = path

        self.render_board()
        self.status_var.set(f"Replay loaded: {len(moves)} move(s). Click Replay again to step through.")

    def replay_next_move(self):
        if not self.game or self.replay_index >= len(self.replay_moves):
            self.status_var.set("Replay finished.")
            self.replay_moves = []
            self.replay_index = 0
            return

        move = self.replay_moves[self.replay_index]
        sr, sc = move["from"]
        dr, dc = move["to"]

        success = self.game.try_move(sr, sc, dr, dc, save_to_history=False)
        if not success:
            messagebox.showerror("Replay Error", f"Invalid recorded move at step {self.replay_index + 1}.")
            self.replay_moves = []
            self.replay_index = 0
            return

        self.replay_index += 1
        self.render_board()

        if self.replay_index >= len(self.replay_moves):
            self.status_var.set("Replay finished.")
            self.replay_moves = []
            self.replay_index = 0
        else:
            self.status_var.set(f"Replayed move {self.replay_index}/{len(self.replay_moves)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireApp(root)
    root.mainloop()
