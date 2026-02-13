import tkinter as tk
import math

def show_selection():
    print("Checkbox:", check_var.get())
    print("Difficulty:", radio_var.get())

root = tk.Tk()
root.title("Solitaire GUI")
root.geometry("600x400")

#------------ Headings
title = tk.Label(root, text="Solitaire Game", font=("Arial", 16))
board_size = tk.Label(root, text="Board size", font=("Arial", 16))
game_mode = tk.Label(root, text="Game Mode", font=("Arial", 12))

title.place(x=5, y=5)
board_size.place(x=400, y=5)
game_mode.place(x=5, y=75)

#------------ Inputs
check_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Record Game",
                          variable=check_var)
checkbox.place(x=25, y=350)

num_input = tk.Spinbox(root, from_=1, to=10, width=4)
num_input.place(x=510, y=10)

#--------- Radio Buttons
radio_var = tk.StringVar(value="Easy")

radio1 = tk.Radiobutton(root, text="Easy", variable=radio_var, value="Easy")
radio2 = tk.Radiobutton(root, text="Medium", variable=radio_var, value="Medium")
radio3 = tk.Radiobutton(root, text="Hard", variable=radio_var, value="Hard")
radio1.place(x=25, y=100)
radio2.place(x=25, y=125)
radio3.place(x=25, y=150)

#--------- Buttons
new_game = tk.Button(root, text="Submit", command=show_selection)
replay = tk.Button(root, text="Replay", command=show_selection)
replay.place(x=100, y=180)
new_game.place(x=25, y=180)

#-------- lines
canvas = tk.Canvas(root, width=150, height=10)
canvas.place(x=0, y=35)

canvas.create_line(0, 5, 150, 5, width=2)
canvas.create_line(0, 10, 150, 10, width=2)

root.mainloop()
