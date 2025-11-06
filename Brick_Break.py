# brick_breaker_tk.py

import tkinter as tk
import sys

# --- Game Constants ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
MAX_LIVES = 3 # New constant

# --- Colors ---
PADDLE_COLOR = "#B7CD28"
BALL_COLOR = "#E79625"
BACKGROUND_COLOR = "#597C9F"
BRICK_COLOR = "#203F8C"
FRONTPAGE_BG = "#97869D"
FRONTPAGE_PANEL = '#3D0070'
BUTTON_COLOR = '#FFD966'
BUTTON_HOVER = '#FFB347'

# --- Ball & Movement Constants ---
BASE_SPEED = 4
BALL_RADIUS = 8
BALL_START_DX = BASE_SPEED
BALL_START_DY = -BASE_SPEED
PADDLE_SPEED = 15

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

class Game(tk.Frame):
    """Controls the main game window, canvas, and game loop."""
    def __init__(self, master):
        super().__init__(master)
        master.title("Tkinter Brick Breaker")

        self.canvas = tk.Canvas(self,
                                 bg=BACKGROUND_COLOR,
                                 width=WINDOW_WIDTH,
                                 height=WINDOW_HEIGHT)
        self.canvas.pack(pady=10, padx=10)
        self.pack()

        # Pause and resume display - positioned top right
        self.canvas.create_text(
        WINDOW_WIDTH - 10, 10,
        text="P: Pause | R: Resume",
        anchor="ne",
        font=("Helvetica", 10, "italic"),
        fill="white")

        # --- SCORE ---
        self.score = 0
        self.score_text = self.canvas.create_text(
            10, 10,
            text="Score: 0",
            anchor="nw",
            font=("Helvetica", 14, "bold"),
            fill="white",
            tags="score"
        )
        
        # --- LIVES --- # NEW LIVES DISPLAY - positioned top center/left of controls
        self.lives = MAX_LIVES
        self.lives_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, 10,
            text=f"Lives: {self.lives}",
            anchor="n",
            font=("Helvetica", 14, "bold"),
            fill="#FF4C4C", # Red color for emphasis
            tags="lives"
        )

        # Create game objects
        self.paddle_id = self.canvas.create_rectangle(
            PADDLE_START_X, PADDLE_START_Y,
            PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT,
            fill=PADDLE_COLOR, tags='paddle_tag'
        )
        self.ball_id = self.canvas.create_oval(
            BALL_START_X - BALL_RADIUS, BALL_START_Y - BALL_RADIUS,
            BALL_START_X + BALL_RADIUS, BALL_START_Y + BALL_RADIUS,
            fill=BALL_COLOR, tags='ball_tag'
        )

        # Game state
        self.bricks = []
        self.setup_bricks()

        self.game_running = False

        # PAUSE VARIABLES
        self.paused = False
        self.stored_dx = BALL_START_DX
        self.stored_dy = BALL_START_DY

        self.ball_dx = BALL_START_DX
        self.ball_dy = BALL_START_DY

        # For frontpage widgets
        self.frontpage_items = []

        # Bindings
        self.master.bind('<Left>', lambda event: self.move_paddle(-PADDLE_SPEED))
        self.master.bind('<Right>', lambda event: self.move_paddle(PADDLE_SPEED))
        self.master.bind('<Return>', lambda event: self.start_game())
        
        # Bind Pause + Resume keys
        self.master.bind('p', self.pause_game)
        self.master.bind('r', self.resume_game)

        # Display front page
        self.show_frontpage()
        self.game_loop()

    # --- Pause & Resume with Countdown ---
    def pause_game(self, event=None):
        if self.game_running and not self.paused:
            self.paused = True
            self.stored_dx = self.ball_dx
            self.stored_dy = self.ball_dy
            self.ball_dx = 0
            self.ball_dy = 0

            # Show "Game Paused" text
            self.paused_text_id = self.canvas.create_text(
                WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                text="GAME PAUSED",
                font=("Helvetica", 36, "bold"),
                fill="yellow",
                tags="paused"
            )

    def resume_game(self, event=None):
        if self.game_running and self.paused:
            self.paused = False

            # Remove paused text
            self.canvas.delete("paused")

            # Start countdown before resuming
            self.start_countdown(3)

    def start_countdown(self, count):
        """Displays a countdown from count to 1, then resumes ball movement."""
        if count > 0:
            self.canvas.delete("countdown")
            self.countdown_text_id = self.canvas.create_text(
                WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                text=str(count),
                font=("Helvetica", 48, "bold"),
                fill="red",
                tags="countdown"
            )
            self.master.after(1000, lambda: self.start_countdown(count - 1))
        else:
            # Remove countdown and restore ball movement
            self.canvas.delete("countdown")
            self.ball_dx = self.stored_dx
            self.ball_dy = self.stored_dy


    # --- Front Page ---
    def show_frontpage(self):
        self.hide_frontpage()

        for i in range(20):
            # Create a gradient background
            r = 43 + i * 5
            b = 59 + i * 4
            color = f'#{r:02x}00{b:02x}'
            self.canvas.create_rectangle(0, i*20, WINDOW_WIDTH, (i+1)*20,
                                         fill=color, outline=color, tags='fp')

        panel = self.canvas.create_rectangle(50, 50, WINDOW_WIDTH-50, WINDOW_HEIGHT-50,
                                             fill=FRONTPAGE_PANEL, outline='#FFFFFF',
                                             width=2, tags='fp')
        self.frontpage_items.append(panel)

        title = self.canvas.create_text(WINDOW_WIDTH/2, 90, text='BRICK BREAKER',
                                         font=('Helvetica', 42, 'bold'),
                                         fill='#FFD966', tags='fp')
        self.frontpage_items.append(title)

        subtitle = self.canvas.create_text(WINDOW_WIDTH/2, 140, text='Classic Arcade Fun!',
                                            font=('Helvetica', 16), fill='#FFFFFF', tags='fp')
        self.frontpage_items.append(subtitle)

        # Logo updated to be smaller and more centered
        logo = self.canvas.create_oval(WINDOW_WIDTH/2 - 40, 170, WINDOW_WIDTH/2 + 40, 250,
                                        fill='#4B0082', outline='#FFD966', width=4, tags='fp')
        self.frontpage_items.append(logo)
        logo_text = self.canvas.create_text(WINDOW_WIDTH/2, 210, text='BB',
                                             font=('Helvetica', 32, 'bold'),
                                             fill='#FFD966', tags='fp')
        self.frontpage_items.append(logo_text)

        # Buttons - moved slightly down and adjusted x to make room for 3
        self.create_frontpage_button('Start Game', WINDOW_WIDTH/2 - 120, 280, self.start_game)
        self.create_frontpage_button('Settings', WINDOW_WIDTH/2, 280, self.show_settings)
        self.create_frontpage_button('Exit', WINDOW_WIDTH/2 + 120, 280, self.quit_game)

        note = self.canvas.create_text(WINDOW_WIDTH/2, 360,
                                         text='Use ← → to move — Press ENTER to start — P=Pause, R=Resume',
                                         font=('Helvetica', 10), fill='#CCCCCC', tags='fp')
        self.frontpage_items.append(note)

    def create_frontpage_button(self, text, x, y, command):
        btn = tk.Button(self.master, text=text, font=('Helvetica', 12, 'bold'),
                         bg=BUTTON_COLOR, activebackground=BUTTON_HOVER, command=command)
        btn_id = self.canvas.create_window(x, y, window=btn, tags='fp')
        self.frontpage_items.append(btn_id)

    def hide_frontpage(self):
        self.canvas.delete('fp')
        # Frontpage buttons are hidden by deleting the canvas window objects (btn_id)
        # but the actual tk.Button widgets still exist. We only keep track of canvas items.
        # Clean up widgets placed using create_window
        for item_id in self.frontpage_items:
            widget = self.canvas.itemcget(item_id, "window")
            if widget:
                widget_name = self.canvas.winfo_name(widget)
                if widget_name in self.master.children:
                    self.master.children[widget_name].destroy()
        self.frontpage_items = []

    def show_settings(self):
        # Remove frontpage or previous settings
        self.hide_frontpage()
        self.canvas.delete('settings')
        if hasattr(self, 'settings_widgets'):
            for w in self.settings_widgets:
                w.destroy()
        self.settings_widgets = []

        # Settings title
        self.canvas.create_text(WINDOW_WIDTH/2, 50,
                                 text='Settings',
                                 font=('Helvetica', 24, 'bold'),
                                 fill='white', tags='settings')

        # Default values for settings (use current values if already set)
        if not hasattr(self, 'temp_ball_speed'):
            self.temp_ball_speed = 'Normal'
        if not hasattr(self, 'temp_paddle_size'):
            self.temp_paddle_size = 'Normal'
        if not hasattr(self, 'temp_brick_color'):
            self.temp_brick_color = 'Blue'

        # --- Ball Speed ---
        # Positioning labels and menus relative to the canvas
        label_speed = tk.Label(self.master, text="Ball Speed:", bg=BACKGROUND_COLOR, fg='white')
        label_speed.place(x=150 + self.canvas.winfo_x(), y=100 + self.canvas.winfo_y())
        self.settings_widgets.append(label_speed)

        speed_var = tk.StringVar(value=self.temp_ball_speed)
        speed_menu = tk.OptionMenu(self.master, speed_var, 'Slow', 'Normal', 'Fast')
        speed_menu.place(x=250 + self.canvas.winfo_x(), y=95 + self.canvas.winfo_y())
        self.settings_widgets.append(speed_menu)

        # --- Paddle Size ---
        label_paddle = tk.Label(self.master, text="Paddle Size:", bg=BACKGROUND_COLOR, fg='white')
        label_paddle.place(x=150 + self.canvas.winfo_x(), y=150 + self.canvas.winfo_y())
        self.settings_widgets.append(label_paddle)

        paddle_var = tk.StringVar(value=self.temp_paddle_size)
        paddle_menu = tk.OptionMenu(self.master, paddle_var, 'Small', 'Normal', 'Large')
        paddle_menu.place(x=250 + self.canvas.winfo_x(), y=145 + self.canvas.winfo_y())
        self.settings_widgets.append(paddle_menu)

        # --- Brick Color ---
        label_brick = tk.Label(self.master, text="Brick Color:", bg=BACKGROUND_COLOR, fg='white')
        label_brick.place(x=150 + self.canvas.winfo_x(), y=200 + self.canvas.winfo_y())
        self.settings_widgets.append(label_brick)

        brick_var = tk.StringVar(value=self.temp_brick_color)
        brick_menu = tk.OptionMenu(self.master, brick_var, 'Blue', 'Red', 'Green')
        brick_menu.place(x=250 + self.canvas.winfo_x(), y=195 + self.canvas.winfo_y())
        self.settings_widgets.append(brick_menu)

        # --- Save button ---
        def save_settings():
            # Apply Ball Speed
            val = speed_var.get()
            speed_multiplier = {'Slow': 0.5, 'Normal': 1.0, 'Fast': 1.5}
            multiplier = speed_multiplier.get(val, 1.0)
            self.ball_dx = BASE_SPEED * multiplier
            self.ball_dy = -BASE_SPEED * multiplier
            self.stored_dx = self.ball_dx
            self.stored_dy = self.ball_dy
            self.temp_ball_speed = val

            # Apply Paddle Size
            val = paddle_var.get()
            size_map = {'Small': 60, 'Normal': 100, 'Large': 140}
            global PADDLE_WIDTH # Need global to modify constant
            PADDLE_WIDTH = size_map.get(val, 100)
            self.temp_paddle_size = val
            # Update paddle position (x1, y1, x2, y2)
            coords = self.canvas.coords(self.paddle_id)
            # Use the existing center (coords[0] + (coords[2]-coords[0])/2) and adjust width
            center_x = (coords[0] + coords[2]) / 2
            x1 = center_x - PADDLE_WIDTH / 2
            x2 = center_x + PADDLE_WIDTH / 2
            self.canvas.coords(self.paddle_id, x1, PADDLE_START_Y, x2, PADDLE_START_Y + PADDLE_HEIGHT)


            # Apply Brick Color
            val = brick_var.get()
            color_map = {'Blue':'#203F8C', 'Red':'#FF4C4C', 'Green':'#28B78F'}
            global BRICK_COLOR
            BRICK_COLOR = color_map.get(val, '#203F8C')
            self.setup_bricks()
            self.temp_brick_color = val

            # Close settings
            close_settings()

        # --- Reset button ---
        def reset_settings():
            speed_var.set('Normal')
            paddle_var.set('Normal')
            brick_var.set('Blue')

        # --- Close settings ---
        def close_settings():
            for w in self.settings_widgets:
                w.destroy()
            self.settings_widgets = []
            self.canvas.delete('settings')
            self.show_frontpage()

        # Place buttons relative to the canvas frame
        save_btn = tk.Button(self.master, text='Save', bg=BUTTON_COLOR, command=save_settings)
        save_btn.place(x=WINDOW_WIDTH/2 - 60 + self.canvas.winfo_x(), y=260 + self.canvas.winfo_y())
        self.settings_widgets.append(save_btn)

        reset_btn = tk.Button(self.master, text='Reset', bg=BUTTON_COLOR, command=reset_settings)
        reset_btn.place(x=WINDOW_WIDTH/2 + 20 + self.canvas.winfo_x(), y=260 + self.canvas.winfo_y())
        self.settings_widgets.append(reset_btn)

        back_btn = tk.Button(self.master, text='Back', bg=BUTTON_COLOR, command=close_settings)
        back_btn.place(x=WINDOW_WIDTH/2 - 20 + self.canvas.winfo_x(), y=310 + self.canvas.winfo_y())
        self.settings_widgets.append(back_btn)

    # --- Game Functions ---
    def start_game(self):
        if not self.game_running:
            self.hide_frontpage()
            self.game_running = True
            # Re-ensure lives display is up-to-date
            self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def lose_life(self):
        """Decrements a life and resets the ball/paddle if lives remain."""
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
        
        if self.lives <= 0:
            self.game_over()
        else:
            # Reset ball and paddle to starting positions
            self.canvas.coords(self.paddle_id, PADDLE_START_X, PADDLE_START_Y,
                               PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT)
            self.canvas.coords(self.ball_id, BALL_START_X - BALL_RADIUS, BALL_START_Y - BALL_RADIUS,
                               BALL_START_X + BALL_RADIUS, BALL_START_Y + BALL_RADIUS)
            
            # Reset ball movement direction/speed
            self.ball_dx = self.stored_dx # Use stored/configured speed
            self.ball_dy = self.stored_dy # Use stored/configured speed
            
            # Briefly pause and display a message before continuing
            self.paused = True
            self.canvas.delete("reset_msg")
            self.canvas.create_text(
                WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                text=f"Life Lost! {self.lives} Remaining.",
                font=("Helvetica", 24, "bold"),
                fill="red",
                tags="reset_msg"
            )
            # Resume after 2 seconds
            self.master.after(2000, self.clear_reset_msg_and_resume)
            
    def clear_reset_msg_and_resume(self):
        self.canvas.delete("reset_msg")
        self.paused = False

    def reset_game(self, event=None):
        self.canvas.delete("game_over_tag")
        self.score = 0
        self.lives = MAX_LIVES # Reset lives
        self.canvas.itemconfig(self.score_text, text="Score: 0")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

        self.master.unbind('<space>')
        self.master.unbind('<Escape>')
        self.canvas.coords(self.paddle_id, PADDLE_START_X, PADDLE_START_Y,
                           PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT)
        self.canvas.coords(self.ball_id, BALL_START_X - BALL_RADIUS, BALL_START_Y - BALL_RADIUS,
                           BALL_START_X + BALL_RADIUS, BALL_START_Y + BALL_RADIUS)

        # Reset ball direction based on stored/configured speed
        self.ball_dx = self.stored_dx
        self.ball_dy = self.stored_dy
        
        self.setup_bricks()
        self.game_running = False
        self.paused = False

        self.show_frontpage()

    def quit_game(self, event=None):
        self.master.destroy()
        sys.exit()

    def game_over(self):
        self.game_running = False
        self.paused = True # Stop movement immediately
        
        self.canvas.delete("reset_msg") # Clean up any life lost message

        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3,
                                 text='GAME OVER!', fill='Orange',
                                 font=('Arial', 30, 'bold'), tags='game_over_tag')
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                 text=f'Final Score: {self.score}', fill='yellow',
                                 font=('Arial', 24, 'bold'), tags='game_over_tag')
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50,
                                 text='Press SPACE to Home', fill='white',
                                 font=('Arial', 14), tags='game_over_tag')
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 75,
                                 text='Press ESC to Quit', fill='white',
                                 font=('Arial', 14), tags='game_over_tag')

        self.master.bind('<space>', self.reset_game)
        self.master.bind('<Escape>', self.quit_game)

    def move_paddle(self, offset):
        if not self.game_running or self.paused:
            return
        coords = self.canvas.coords(self.paddle_id)
        # Ensure paddle width uses the global constant for boundary check
        current_width = coords[2] - coords[0]
        new_x1 = coords[0] + offset
        new_x2 = coords[2] + offset
        if new_x1 >= 0 and new_x2 <= WINDOW_WIDTH:
            self.canvas.move(self.paddle_id, offset, 0)

    def check_paddle_collision(self, ball_coords):
        ball_left, ball_top, ball_right, ball_bottom = ball_coords
        paddle_coords = self.canvas.coords(self.paddle_id)
        paddle_left, paddle_top, paddle_right, paddle_bottom = paddle_coords
        
        # Check if the ball is moving down, hits the paddle's vertical region, 
        # and overlaps horizontally.
        if self.ball_dy > 0 and paddle_top <= ball_bottom <= paddle_bottom and \
           paddle_left <= ball_right and ball_left <= paddle_right:
            self.ball_dy *= -1
            
            # Optional: Add simple angle deflection based on where it hit the paddle
            paddle_center = (paddle_left + paddle_right) / 2
            ball_center_x = (ball_left + ball_right) / 2
            
            # Calculate hit distance from center (clamped between -1 and 1 for full width)
            hit_ratio = (ball_center_x - paddle_center) / (PADDLE_WIDTH / 2)
            
            # Small horizontal speed adjustment (max 1 unit)
            self.ball_dx += hit_ratio * 1 
            self.stored_dx += hit_ratio * 1 # Update stored speed
            
            # Ensure speed does not get excessive
            max_speed = BASE_SPEED * 2
            current_speed = (self.ball_dx**2 + self.ball_dy**2)**0.5
            if current_speed > max_speed:
                scale = max_speed / current_speed
                self.ball_dx *= scale
                self.ball_dy *= scale
                self.stored_dx = self.ball_dx
                self.stored_dy = self.ball_dy


    def check_brick_collision(self, ball_coords):
        overlapping = self.canvas.find_overlapping(*ball_coords)
        for obj_id in overlapping:
            if obj_id in self.bricks:
                self.canvas.delete(obj_id)
                self.bricks.remove(obj_id)

                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

                self.ball_dy *= -1
                return

    def setup_bricks(self):
        self.canvas.delete('brick')
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick_x1 = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                brick_y1 = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                brick_x2 = brick_x1 + BRICK_WIDTH
                brick_y2 = brick_y1 + BRICK_HEIGHT
                brick_id = self.canvas.create_rectangle(brick_x1, brick_y1,
                                                         brick_x2, brick_y2,
                                                         fill=BRICK_COLOR, tags='brick')
                self.bricks.append(brick_id)

    def game_loop(self):
        if self.game_running and not self.paused:
            self.canvas.move(self.ball_id, self.ball_dx, self.ball_dy)
            ball_coords = self.canvas.coords(self.ball_id)
            ball_left, ball_top, ball_right, ball_bottom = ball_coords

            if ball_bottom >= WINDOW_HEIGHT:
                self.lose_life() # Changed from game_over to lose_life
                
            if ball_left <= 0 or ball_right >= WINDOW_WIDTH:
                self.ball_dx *= -1

            if ball_top <= 0:
                self.ball_dy *= -1

            self.check_paddle_collision(ball_coords)
            self.check_brick_collision(ball_coords)
            
            if not self.bricks:
                self.game_over() # Win condition

        self.master.after(30, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()