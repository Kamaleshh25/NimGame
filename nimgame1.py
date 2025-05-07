import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import messagebox

class NimGameUI:
    def __init__(self, master):
        self.master = master
        self.master.title("🔥 Nim Game - Human vs AI 🔥")
        self.master.geometry("550x450")
        self.master.configure(bg="#1e1e2f")

        self.total_stones = 21
        self.player_score = 0
        self.ai_score = 0

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Title using Canvas
        self.canvas = tk.Canvas(self.master, width=500, height=60, bg="#1e1e2f", bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.create_text(250, 30, text="🔥 NIM GAME 🔥", font=("Segoe UI", 28, "bold"), fill="#ffcb6b")

        # Game Info using Message widget
        self.info_message = tk.Message(self.master, text="🎮 Your Turn! Pick 1, 2, or 3 stones.",
                                       font=("Segoe UI", 16, "italic"), width=400, bg="#1e1e2f", fg="#f9f9f9")
        self.info_message.pack(pady=5)

        # Stone Display using Canvas
        self.stone_canvas = tk.Canvas(self.master, width=500, height=60, bg="#1e1e2f", bd=0, highlightthickness=0)
        self.stone_canvas.pack(pady=15)
        self.stone_canvas.create_text(250, 30, text=f"🪨 Stones left: {self.total_stones}", font=("Segoe UI", 22, "bold"), fill="#89ddff")

        # Buttons for taking stones replaced with Labels (now clickable)
        self.button_frame = tk.Frame(self.master, bg="#1e1e2f")
        self.button_frame.pack(pady=10)

        self.label1 = tk.Label(self.button_frame, text="Take 1", font=("Segoe UI", 14, "bold"),
                               bg="#42a5f5", fg="white", width=10, height=2, relief="solid", bd=1, cursor="hand2")
        self.label1.grid(row=0, column=0, padx=10)
        self.label1.bind("<Button-1>", lambda e: self.player_move(1))

        self.label2 = tk.Label(self.button_frame, text="Take 2", font=("Segoe UI", 14, "bold"),
                               bg="#ef5350", fg="white", width=10, height=2, relief="solid", bd=1, cursor="hand2")
        self.label2.grid(row=0, column=1, padx=10)
        self.label2.bind("<Button-1>", lambda e: self.player_move(2))

        self.label3 = tk.Label(self.button_frame, text="Take 3", font=("Segoe UI", 14, "bold"),
                               bg="#66bb6a", fg="white", width=10, height=2, relief="solid", bd=1, cursor="hand2")
        self.label3.grid(row=0, column=2, padx=10)
        self.label3.bind("<Button-1>", lambda e: self.player_move(3))

        # Scoreboard using Canvas
        self.score_canvas = tk.Canvas(self.master, width=500, height=60, bg="#1e1e2f", bd=0, highlightthickness=0)
        self.score_canvas.pack(pady=10)
        self.score_canvas.create_text(250, 30, text=f"👤 You: {self.player_score}   |   🤖 AI: {self.ai_score}",
                                      font=("Segoe UI Semibold", 14), fill="#ffb74d")

        # Restart Button (using Label for Restart instead of Button)
        self.restart_text = tk.Label(self.master, text="🔄 Restart Game", font=("Segoe UI", 12),
                                     bg="#7c4dff", fg="white", width=20, height=2, relief="solid", bd=1, cursor="hand2")
        self.restart_text.pack(pady=12)
        self.restart_text.bind("<Button-1>", self.restart_game)

    def update_display(self):
        self.stone_canvas.delete("all")  # Clear previous text
        self.stone_canvas.create_text(250, 30, text=f"🪨 Stones left: {self.total_stones}", font=("Segoe UI", 22, "bold"), fill="#89ddff")
        
        self.score_canvas.delete("all")  # Clear previous text
        self.score_canvas.create_text(250, 30, text=f"👤 You: {self.player_score}   |   🤖 AI: {self.ai_score}",
                                      font=("Segoe UI Semibold", 14), fill="#ffb74d")

    def player_move(self, move):
        if move > self.total_stones:
            messagebox.showwarning("Oops!", f"Only {self.total_stones} stone(s) left!")
            return
        self.total_stones -= move
        self.stone_canvas.delete("all")  # Clear previous text
        self.stone_canvas.create_text(250, 30, text=f"You took {move} stone(s) 🧍", font=("Segoe UI", 22, "bold"), fill="#89ddff")
        
        if self.total_stones == 0:
            self.end_game("You")
        else:
            self.disable_buttons()
            self.master.after(1000, self.ai_move)

    def ai_move(self):
        move = self.total_stones % 4
        if move == 0 or move > 3:
            move = 1
        self.total_stones -= move
        self.stone_canvas.delete("all")  # Clear previous text
        self.stone_canvas.create_text(250, 30, text=f"AI took {move} stone(s) 🤖", font=("Segoe UI", 22, "bold"), fill="#ffcb6b")
        
        # Update a new message to show how many stones AI took
        self.info_message.config(text=f"AI chose {move} stone(s) 🤖")

        if self.total_stones == 0:
            self.end_game("AI")
        else:
            self.enable_buttons()
            self.update_display()

    def end_game(self, winner):
        if winner == "You":
            self.player_score += 1
        else:
            self.ai_score += 1

        self.update_display()
        self.disable_buttons()
        messagebox.showinfo("🎉 Game Over", f"{winner} wins!")
        self.restart_text.config(state="normal")

    def disable_buttons(self):
        self.label1.config(state=tk.DISABLED)
        self.label2.config(state=tk.DISABLED)
        self.label3.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.label1.config(state=tk.NORMAL)
        self.label2.config(state=tk.NORMAL)
        self.label3.config(state=tk.NORMAL)

    def restart_game(self, event=None):
        self.total_stones = 21
        self.enable_buttons()
        self.update_display()
        self.stone_canvas.delete("all")  # Clear previous text
        self.restart_text.config(state=tk.DISABLED)  # Disable restart button

if __name__ == "__main__":
    root = tk.Tk()
    app = NimGameUI(root)
    root.mainloop()
