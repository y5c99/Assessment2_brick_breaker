# brick_breaker_tk.py

import tkinter as tk
import sys

# --- Game Constants ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

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


            #pause and resume display
        self.controls_text = self.canvas.create_text(
        WINDOW_WIDTH - 10, 10,  # 10 pixels from right edge
        text="P: Pause | R: Resume",
        anchor="ne",  # Top-right corner alignment
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

        #  NEW — PAUSE VARIABLES
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

        #  NEW — Bind Pause + Resume keys
        self.master.bind('p', self.pause_game)
        self.master.bind('r', self.resume_game)

        # Display front page
        self.show_frontpage()
        self.game_loop()

        #  NEW — Pause Function
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
            color = f'#{hex(43 + i*5)[2:]}00{hex(59 + i*4)[2:]}'
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

        logo = self.canvas.create_oval(WINDOW_WIDTH/2 - 60, 160, WINDOW_WIDTH/2 + 60, 280,
                                       fill='#4B0082', outline='#FFD966', width=4, tags='fp')
        self.frontpage_items.append(logo)
        logo_text = self.canvas.create_text(WINDOW_WIDTH/2, 220, text='BB',
                                            font=('Helvetica', 32, 'bold'),
                                            fill='#FFD966', tags='fp')
        self.frontpage_items.append(logo_text)

        self.create_frontpage_button('Start Game', WINDOW_WIDTH/2 - 100, 320, self.start_game)
        self.create_frontpage_button('Settings', WINDOW_WIDTH/2, 320, self.show_settings)
        self.create_frontpage_button('Exit', WINDOW_WIDTH/2 + 100, 320, self.quit_game)

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
        title = self.canvas.create_text(WINDOW_WIDTH/2, 50,
                                        text='Settings',
                                        font=('Helvetica', 24, 'bold'),
                                        fill='white', tags='settings')

        # --- Use last saved settings or defaults ---
        ball_speed_default = getattr(self, 'temp_ball_speed', 'Normal')
        paddle_size_default = getattr(self, 'temp_paddle_size', 'Normal')
        brick_color_default = getattr(self, 'temp_brick_color', 'Blue')

        # --- Ball Speed Options ---
        tk.Label(self.master, text="Ball Speed:", bg=BACKGROUND_COLOR, fg='white').place(x=150, y=100)
        speed_var = tk.StringVar(value=ball_speed_default)
        speed_menu = tk.OptionMenu(self.master, speed_var, 'Slow', 'Normal', 'Fast')
        speed_menu.place(x=250, y=95)
        self.settings_widgets.append(speed_menu)

        # --- Paddle Size Options ---
        tk.Label(self.master, text="Paddle Size:", bg=BACKGROUND_COLOR, fg='white').place(x=150, y=150)
        paddle_var = tk.StringVar(value=paddle_size_default)
        paddle_menu = tk.OptionMenu(self.master, paddle_var, 'Small', 'Normal', 'Large')
        paddle_menu.place(x=250, y=145)
        self.settings_widgets.append(paddle_menu)

        # --- Brick Color Options ---
        tk.Label(self.master, text="Brick Color:", bg=BACKGROUND_COLOR, fg='white').place(x=150, y=200)
        brick_var = tk.StringVar(value=brick_color_default)
        brick_menu = tk.OptionMenu(self.master, brick_var, 'Blue', 'Red', 'Green')
        brick_menu.place(x=250, y=195)
        self.settings_widgets.append(brick_menu)

        # --- Save button ---
        def save_settings():
            # Save Ball Speed
            val = speed_var.get()
            if val == 'Slow':
                self.ball_dx = BASE_SPEED / 2
                self.ball_dy = -BASE_SPEED / 2
            elif val == 'Normal':
                self.ball_dx = BASE_SPEED
                self.ball_dy = -BASE_SPEED
            elif val == 'Fast':
                self.ball_dx = BASE_SPEED * 1.5
                self.ball_dy = -BASE_SPEED * 1.5
            self.temp_ball_speed = val

            # Save Paddle Size
            val = paddle_var.get()
            global PADDLE_WIDTH
            if val == 'Small':
                PADDLE_WIDTH = 60
            elif val == 'Normal':
                PADDLE_WIDTH = 100
            elif val == 'Large':
                PADDLE_WIDTH = 140
            self.temp_paddle_size = val
            self.canvas.coords(self.paddle_id, PADDLE_START_X, PADDLE_START_Y,
                            PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT)

            # Save Brick Color
            val = brick_var.get()
            color_map = {'Blue':'#203F8C', 'Red':'#FF4C4C', 'Green':'#28B78F'}
            global BRICK_COLOR
            BRICK_COLOR = color_map.get(val, '#203F8C')
            self.setup_bricks()
            self.temp_brick_color = val

            # Close settings after saving
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

        # Buttons
        save_btn = tk.Button(self.master, text='Save', bg=BUTTON_COLOR, command=save_settings)
        save_btn.place(x=WINDOW_WIDTH/2 - 60, y=260)
        self.settings_widgets.append(save_btn)

        reset_btn = tk.Button(self.master, text='Reset', bg=BUTTON_COLOR, command=reset_settings)
        reset_btn.place(x=WINDOW_WIDTH/2 + 20, y=260)
        self.settings_widgets.append(reset_btn)

        back_btn = tk.Button(self.master, text='Back', bg=BUTTON_COLOR, command=close_settings)
        back_btn.place(x=WINDOW_WIDTH/2 - 20, y=310)
        self.settings_widgets.append(back_btn)







    # --- Game Functions ---
    def start_game(self):
        if not self.game_running:
            self.hide_frontpage()
            self.game_running = True

    def reset_game(self, event=None):
        self.canvas.delete("game_over_tag")
        self.score = 0
        self.canvas.itemconfig(self.score_text, text="Score: 0")

        self.master.unbind('<space>')
        self.master.unbind('<Escape>')
        self.canvas.coords(self.paddle_id, PADDLE_START_X, PADDLE_START_Y,
                           PADDLE_START_X + PADDLE_WIDTH, PADDLE_START_Y + PADDLE_HEIGHT)
        self.canvas.coords(self.ball_id, BALL_START_X - BALL_RADIUS, BALL_START_Y - BALL_RADIUS,
                           BALL_START_X + BALL_RADIUS, BALL_START_Y + BALL_RADIUS)

        self.ball_dx = BALL_START_DX
        self.ball_dy = -BALL_START_DY
        self.setup_bricks()
        self.game_running = False
        self.paused = False

        self.show_frontpage()

    def quit_game(self, event=None):
        self.master.destroy()
        sys.exit()

    def game_over(self):
        self.game_running = False

        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3,
                                text='GAME OVER!', fill='red',
                                font=('Arial', 30, 'bold'), tags='game_over_tag')
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                text='Press SPACE to Play Again', fill='white',
                                font=('Arial', 18), tags='game_over_tag')
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40,
                                text='Press ESC to Quit', fill='white',
                                font=('Arial', 18), tags='game_over_tag')

        self.master.bind('<space>', self.reset_game)
        self.master.bind('<Escape>', self.quit_game)

    def move_paddle(self, offset):
        if not self.game_running or self.paused:
            return
        coords = self.canvas.coords(self.paddle_id)
        new_x1 = coords[0] + offset
        new_x2 = coords[2] + offset
        if new_x1 >= 0 and new_x2 <= WINDOW_WIDTH:
            self.canvas.move(self.paddle_id, offset, 0)

    def check_paddle_collision(self, ball_coords):
        ball_left, ball_top, ball_right, ball_bottom = ball_coords
        paddle_coords = self.canvas.coords(self.paddle_id)
        paddle_left, paddle_top, paddle_right, paddle_bottom = paddle_coords
        if self.ball_dy > 0 and paddle_top <= ball_bottom <= paddle_bottom and \
           paddle_left <= ball_right and ball_left <= paddle_right:
            self.ball_dy *= -1

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
                self.game_over()

            if ball_left <= 0 or ball_right >= WINDOW_WIDTH:
                self.ball_dx *= -1

            if ball_top <= 0:
                self.ball_dy *= -1

            self.check_paddle_collision(ball_coords)
            self.check_brick_collision(ball_coords)
            if not self.bricks:
                self.game_over()

        self.master.after(30, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
