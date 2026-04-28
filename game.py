import tkinter as tk

class PongGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pong - Tkinter Edition")
        self.root.resizable(False, False)

        # Game constants
        self.canvas_width = 800
        self.canvas_height = 600
        self.paddle_width = 15
        self.paddle_height = 100
        self.ball_size = 15
        
        # Setup Canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#222", highlightthickness=0)
        self.canvas.pack()

        # Dashed line
        self.canvas.create_line(400, 0, 400, 600, fill="white", dash=(10, 10))

        # Paddles and Ball
        self.left_paddle = self.canvas.create_rectangle(20, 250, 20 + self.paddle_width, 350, fill="cyan")
        self.right_paddle = self.canvas.create_rectangle(765, 250, 765 + self.paddle_width, 350, fill="magenta")
        self.ball = self.canvas.create_oval(392, 292, 392 + self.ball_size, 292 + self.ball_size, fill="white")

        # Scores
        self.score_a = 0
        self.score_b = 0
        self.score_display = self.canvas.create_text(400, 50, text="0   0", fill="white", font=("Courier", 40, "bold"))

        # Movement variables
        self.ball_dx = 4
        self.ball_dy = 4
        self.pressed_keys = set()

        # Key bindings
        self.root.bind("<KeyPress>", lambda e: self.pressed_keys.add(e.keysym))
        self.root.bind("<KeyRelease>", lambda e: self.pressed_keys.discard(e.keysym))

        self.update()
        self.root.mainloop()

    def move_paddles(self):
        # Player A (W/S)
        if "w" in self.pressed_keys and self.canvas.coords(self.left_paddle)[1] > 0:
            self.canvas.move(self.left_paddle, 0, -6)
        if "s" in self.pressed_keys and self.canvas.coords(self.left_paddle)[3] < self.canvas_height:
            self.canvas.move(self.left_paddle, 0, 6)
        
        # Player B (Arrows)
        if "Up" in self.pressed_keys and self.canvas.coords(self.right_paddle)[1] > 0:
            self.canvas.move(self.right_paddle, 0, -6)
        if "Down" in self.pressed_keys and self.canvas.coords(self.right_paddle)[3] < self.canvas_height:
            self.canvas.move(self.right_paddle, 0, 6)

    def update(self):
        self.move_paddles()
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        
        ball_pos = self.canvas.coords(self.ball)

        # Wall collisions (Top/Bottom)
        if ball_pos[1] <= 0 or ball_pos[3] >= self.canvas_height:
            self.ball_dy *= -1

        # Paddle collisions
        if self.ball_dx < 0: # Moving Left
            if self.is_collision(self.ball, self.left_paddle):
                self.ball_dx *= -1.05 # Speed up
        else: # Moving Right
            if self.is_collision(self.ball, self.right_paddle):
                self.ball_dx *= -1.05

        # Scoring
        if ball_pos[0] <= 0:
            self.reset_ball("B")
        elif ball_pos[2] >= self.canvas_width:
            self.reset_ball("A")

        self.root.after(10, self.update)

    def is_collision(self, ball, paddle):
        b = self.canvas.coords(ball)
        p = self.canvas.coords(paddle)
        return b[2] >= p[0] and b[0] <= p[2] and b[3] >= p[1] and b[1] <= p[3]

    def reset_ball(self, winner):
        if winner == "A": self.score_a += 1
        else: self.score_b += 1
        
        self.canvas.itemconfig(self.score_display, text=f"{self.score_a}   {self.score_b}")
        self.canvas.coords(self.ball, 392, 292, 392 + self.ball_size, 292 + self.ball_size)
        self.ball_dx = 4 if winner == "B" else -4 # Serve to winner

if __name__ == "__main__":
    PongGame()
