# brick_breaker

import tkinter as tk

# --- Game Constants ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# --- Colors (Latest Polish) ---
PADDLE_COLOR = '#FF9933'    # Orange
BALL_COLOR = '#FFFF00'      # Yellow
BACKGROUND_COLOR = '#1A0033' # Dark Purple
BRICK_COLOR = '#33CCFF'     # Light Blue

# --- Ball & Movement Constants ---
BALL_RADIUS = 8
BALL_START_DX = 4           # Initial horizontal speed
BALL_START_DY = -4          # Initial vertical speed (upwards)
PADDLE_SPEED = 15           # Pixels to move per key press

# --- Game Objects Constants ---
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_START_X = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
PADDLE_START_Y = WINDOW_HEIGHT - 30

BALL_START_X = WINDOW_WIDTH // 2
BALL_START_Y = WINDOW_HEIGHT // 2

# --- Brick Constants ---
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 50
BRICK_HEIGHT = 15
BRICK_PADDING = 10
BRICK_OFFSET_TOP = 40
BRICK_OFFSET_LEFT = 35


# --- Game Class (The Main Controller) ---
class Game(tk.Frame):
    """Controls the main game window, canvas, and game loop."""
    def __init__(self, master):
        # Initialise the Tkinter frame
        super().__init__(master) 
        master.title("Tkinter Brick Breaker")

        # Setup the canvas where the game will be drawn
        self.canvas = tk.Canvas(self, 
                                bg=BACKGROUND_COLOR, 
                                width=WINDOW_WIDTH, 
                                height=WINDOW_HEIGHT)
        self.canvas.pack(pady=10, padx=10)
        self.pack()

        # --- 1. Create Game Objects and Assign IDs ---
        
        # Create Paddle
        self.paddle_id = self.canvas.create_rectangle(
            PADDLE_START_X, PADDLE_START_Y, 
            PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT, 
            fill=PADDLE_COLOR, tags='paddle_tag'
        )

        # Create Ball
        self.ball_id = self.canvas.create_oval(
            BALL_START_X - BALL_RADIUS, BALL_START_Y - BALL_RADIUS,
            BALL_START_X + BALL_RADIUS, BALL_START_Y + BALL_RADIUS,
            fill=BALL_COLOR, tags='ball_tag'
        )

        # Generate Bricks
        self.bricks = []
        self.setup_bricks() 

        # --- 2. Initialize Game State ---
        self.ball_dx = BALL_START_DX
        self.ball_dy = BALL_START_DY

        # --- 3. Bind Controls and Start Loop ---
        self.master.bind('<Left>', lambda event: self.move_paddle(-PADDLE_SPEED))
        self.master.bind('<Right>', lambda event: self.move_paddle(PADDLE_SPEED))

        # Start the game loop (MUST be called after all IDs are assigned)
        self.game_loop()


    def move_paddle(self, offset):
        """Moves the paddle object horizontally and checks boundaries."""
        # 1. Get current coordinates (x1, y1, x2, y2)
        coords = self.canvas.coords(self.paddle_id)
        current_x1 = coords[0]
        current_x2 = coords[2]

        # 2. Calculate new position
        new_x1 = current_x1 + offset
        new_x2 = current_x2 + offset

        # 3. Check boundaries (do not move off screen)
        if new_x1 >= 0 and new_x2 <= WINDOW_WIDTH:
            # Move the canvas item by (x, y) offset
            self.canvas.move(self.paddle_id, offset, 0)

    
    def check_paddle_collision(self, ball_coords):
        """Checks if the ball hits the paddle and reverses the Y velocity."""

        # Get ball boundaries: (left, top, right, bottom)
        ball_left, ball_top, ball_right, ball_bottom = ball_coords

        # Get paddle boundaries
        paddle_coords = self.canvas.coords(self.paddle_id)
        paddle_left, paddle_top, paddle_right, paddle_bottom = paddle_coords

        # Simple collision check:
        # 1. Ball must be moving downwards (self.ball_dy > 0)
        # 2. Ball's bottom edge must be below paddle's top edge
        # 3. Ball must overlap horizontally with the paddle
        if self.ball_dy > 0 and \
           ball_bottom >= paddle_top and ball_bottom <= paddle_bottom and \
           ball_right >= paddle_left and ball_left <= paddle_right:

            self.ball_dy *= -1 # Reverse vertical direction


    def setup_bricks(self):
        """Generates and draws the initial grid of bricks on the canvas."""
        # Loop through rows and columns to place bricks
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                # Calculate coordinates for the top-left and bottom-right corners
                brick_x1 = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                brick_y1 = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                brick_x2 = brick_x1 + BRICK_WIDTH
                brick_y2 = brick_y1 + BRICK_HEIGHT

                # Create the rectangle object on the canvas
                brick_id = self.canvas.create_rectangle(
                    brick_x1, brick_y1, brick_x2, brick_y2, 
                    fill=BRICK_COLOR, 
                    tags='brick'
                )
                # Store the canvas ID for future reference (e.g., deletion on hit)
                self.bricks.append(brick_id)


    def game_loop(self):
        """
        The main game loop function, called repeatedly to update physics and drawing.
        This function handles all movement and collision checks.
        """

        # 1. Update Ball Position (Animation)
        self.canvas.move(self.ball_id, self.ball_dx, self.ball_dy) 

        # 2. Get the new coordinates of the ball for boundary checking
        ball_coords = self.canvas.coords(self.ball_id)
        ball_left, ball_top, ball_right, ball_bottom = ball_coords

        # 3. Handle Wall Collisions (Simple reflection)

        # Check collision with Left or Right wall
        if ball_left <= 0 or ball_right >= WINDOW_WIDTH:
            self.ball_dx *= -1 # Reverse horizontal direction

        # Check collision with Top wall
        if ball_top <= 0:
            self.ball_dy *= -1 # Reverse vertical direction
        
        # 4. Handle collision with the paddle
        self.check_paddle_collision(ball_coords)

        # 5. Handle collision with bricks (Logic for next commit)

        # 6. Schedule the next update (e.g., every 30 milliseconds)
        self.master.after(30, self.game_loop)


# --- Application Entry Point ---
if __name__ == "__main__":
    # 1. Create the main Tkinter window instance
    root = tk.Tk()
    
    # 2. Instantiate the Game class
    game = Game(root)
    
    # 3. Start the Tkinter event loop (required for GUI)
    root.mainloop()