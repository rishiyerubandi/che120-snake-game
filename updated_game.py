# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech
# Modified by UW CHE 120 Students

import turtle
import time
import random

# ----------------------------
# Configuration / Globals
# ----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BUTTON_CORNER_RADIUS = 12
BUTTON_PADDING = 10

# gameplay timing
delay = 0.1

# scoring
score = 0
high_score = 0

# UI / state
game_state = "menu"   # "menu", "options", "playing"
selected_mode = "normal"  # "normal" or "modified"
running_game = False  # controls the main game loop

# Modified mode power-up state
double_active = False
double_remaining = 0
powerup_cooldown = 0  # frames until powerup may respawn

# ----------------------------
# Screen setup
# ----------------------------
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("green")
wn.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
wn.tracer(0)

# ----------------------------
# Utility: Rounded Rectangle Button Class
# ----------------------------
class RoundedButton:
    def __init__(self, x, y, w, h, fill_color, border_color, text, text_color="white", action=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill = fill_color
        self.border = border_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.drawer = turtle.Turtle(visible=False)
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.speed(0)
        self.visible = False

    def _draw_round_rect(self):
        r = BUTTON_CORNER_RADIUS
        w = self.w
        h = self.h
        x = self.x - w/2
        y = self.y - h/2
        d = self.drawer
        d.penup()
        d.goto(x + r, y)
        d.pendown()
        d.pensize(3)
        d.color(self.border, self.fill)
        d.begin_fill()
        d.forward(w - 2*r)
        d.circle(r, 90)
        d.forward(h - 2*r)
        d.circle(r, 90)
        d.forward(w - 2*r)
        d.circle(r, 90)
        d.forward(h - 2*r)
        d.circle(r, 90)
        d.end_fill()
        d.penup()

    def draw(self):
        # draw only if not visible (prevents overdraw flicker)
        self.drawer.clear()
        self._draw_round_rect()
        self.drawer.goto(self.x, self.y - 10)
        self.drawer.color(self.text_color)
        self.drawer.write(self.text, align="center", font=("Courier", 16, "bold"))
        self.visible = True

    def hide(self):
        self.drawer.clear()
        self.visible = False

    def contains(self, x, y):
        return (abs(x - self.x) <= self.w/2) and (abs(y - self.y) <= self.h/2)

    def click(self):
        if self.action:
            self.action()

# ----------------------------
# Define menu buttons (positions)
# ----------------------------
btn_w = 220
btn_h = 60
center_x = 0

# Main menu
play_btn = RoundedButton(center_x, 40, btn_w, btn_h, fill_color="blue", border_color="black",
                         text="PLAY", text_color="white")
options_btn = RoundedButton(center_x, -40, btn_w, btn_h, fill_color="red", border_color="black",
                            text="OPTIONS", text_color="white")

# Options menu
normal_btn = RoundedButton(center_x, 60, btn_w, btn_h, fill_color="purple", border_color="black",
                           text="NORMAL MODE", text_color="white")
modified_btn = RoundedButton(center_x, 0, btn_w, btn_h, fill_color="purple", border_color="black",
                             text="MODIFIED MODE", text_color="white")
back_btn = RoundedButton(center_x, -80, btn_w, btn_h, fill_color="orange", border_color="black",
                         text="BACK", text_color="white")

current_buttons = []

# ----------------------------
# Title / menu helper turtle
# ----------------------------
title_turtle = turtle.Turtle(visible=False)
title_turtle.hideturtle()
title_turtle.penup()
title_turtle.color("white")

# ----------------------------
# Game objects (created/stored, hidden until play)
# ----------------------------
# Snake head
head = turtle.Turtle()
head.hideturtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.hideturtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Powerup (double points)
powerup = turtle.Turtle()
powerup.hideturtle()
powerup.speed(0)
powerup.shape("circle")
powerup.color("yellow")
powerup.penup()
powerup.goto(1000, 1000)

# Body segments
segments = []

# Score pen
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)
pen.color("white")
pen.goto(0, 260)

# ----------------------------
# Menu display functions
# ----------------------------
def show_main_menu():
    global game_state, current_buttons
    game_state = "menu"
    hide_game_elements_for_menu()
    title_turtle.clear()
    title_turtle.goto(0, 140)
    title_turtle.write("SNAKE GAME", align="center", font=("Courier", 36, "bold"))
    play_btn.draw()
    options_btn.draw()
    normal_btn.hide()
    modified_btn.hide()
    back_btn.hide()
    current_buttons = [play_btn, options_btn]

def show_options_menu():
    global game_state, current_buttons
    game_state = "options"
    title_turtle.clear()
    title_turtle.goto(0, 140)
    title_turtle.write("OPTIONS", align="center", font=("Courier", 32, "bold"))
    play_btn.hide()
    options_btn.hide()
    normal_btn.draw()
    modified_btn.draw()
    back_btn.draw()
    current_buttons = [normal_btn, modified_btn, back_btn]

def hide_game_elements_for_menu():
    head.hideturtle()
    food.hideturtle()
    powerup.hideturtle()
    pen.clear()

# ----------------------------
# Game setup / reset helpers
# ----------------------------
def setup_game():
    global segments, score, delay, double_active, double_remaining, powerup_cooldown, running_game
    # show game items
    head.showturtle()
    head.goto(0, 0)
    head.direction = "stop"

    food.showturtle()
    food.goto(0, 100)

    powerup.hideturtle()
    powerup.goto(1000, 1000)

    # clear segments
    for s in segments:
        s.hideturtle()
        s.goto(1000, 1000)
    segments = []

    # reset game vars
    score = 0
    delay = 0.1
    double_active = False
    double_remaining = 0
    powerup_cooldown = 0

    update_score_display()
    running_game = True

def reset_game_and_return_to_menu():
    global segments, score, delay, double_active, double_remaining, powerup_cooldown, running_game
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    for s in segments:
        s.hideturtle()
        s.goto(1000, 1000)
    segments = []
    score = 0
    delay = 0.1
    double_active = False
    double_remaining = 0
    powerup_cooldown = 0
    running_game = False
    update_score_display()
    show_main_menu()

def update_score_display():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

# ----------------------------
# Movement functions & bindings
# ----------------------------
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move_head():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# ----------------------------
# Button actions
# ----------------------------
def play_action():
    # Start the game in the currently selected mode
    start_playing()

def options_action():
    show_options_menu()

play_btn.action = play_action
options_btn.action = options_action

def select_normal():
    global selected_mode
    selected_mode = "normal"
    normal_btn.text = "NORMAL MODE ✓"
    modified_btn.text = "MODIFIED MODE"
    normal_btn.draw()
    modified_btn.draw()

def select_modified():
    global selected_mode
    selected_mode = "modified"
    modified_btn.text = "MODIFIED MODE ✓"
    normal_btn.text = "NORMAL MODE"
    normal_btn.draw()
    modified_btn.draw()

def back_action():
    # clear selection ticks (keeps label simple)
    normal_btn.text = "NORMAL MODE"
    modified_btn.text = "MODIFIED MODE"
    show_main_menu()

normal_btn.action = select_normal
modified_btn.action = select_modified
back_btn.action = back_action

# ----------------------------
# Mouse click handler
# ----------------------------
def on_screen_click(x, y):
    # If in menu / options, check button clicks
    if game_state in ("menu", "options"):
        for b in current_buttons:
            if b.contains(x, y):
                b.click()
                return
    # If playing, ignore clicks (could be used for pause later)

wn.onscreenclick(on_screen_click)

# ----------------------------
# Game loop (classic loop) and start/stop
# ----------------------------
def start_playing():
    global game_state
    game_state = "playing"
    # hide menu UI
    for b in (play_btn, options_btn, normal_btn, modified_btn, back_btn):
        b.hide()
    title_turtle.clear()
    setup_game()
    run_game_loop()

def run_game_loop():
    global score, high_score, delay, double_active, double_remaining, powerup_cooldown, running_game

    # ensure controls are active
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")

    while running_game:
        wn.update()

        # Border collision -> end run and return to menu
        if head.xcor() > (WINDOW_WIDTH//2 - 10) or head.xcor() < -(WINDOW_WIDTH//2 - 10) or \
           head.ycor() > (WINDOW_HEIGHT//2 - 10) or head.ycor() < -(WINDOW_HEIGHT//2 - 10):
            reset_game_and_return_to_menu()
            break

        # Food collision
        if head.distance(food) < 20:
            # move food
            x = random.randint(-WINDOW_WIDTH//2 + 20, WINDOW_WIDTH//2 - 20)
            y = random.randint(-WINDOW_HEIGHT//2 + 20, WINDOW_HEIGHT//2 - 20)
            food.goto(x, y)

            # add a segment
            new_segment = turtle.Turtle()
            new_segment.hideturtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)
            new_segment.showturtle()

            # speed up slightly but keep reasonable floor
            delay = max(0.02, globals().get('delay', 0.1) - 0.001)
            globals()['delay'] = delay

            # scoring logic
            if selected_mode == "modified" and double_active:
                score += 20
                double_remaining -= 1
                if double_remaining <= 0:
                    double_active = False
            else:
                score += 10

            if score > high_score:
                high_score = score

            update_score_display()

        # Modified mode: powerup spawn logic
        if selected_mode == "modified":
            if powerup_cooldown > 0:
                powerup_cooldown -= 1
            else:
                # if powerup hidden, small chance to spawn
                if powerup.distance(1000, 1000) < 0.1:
                    if random.random() < 0.01:
                        px = random.randint(-WINDOW_WIDTH//2 + 40, WINDOW_WIDTH//2 - 40)
                        py = random.randint(-WINDOW_HEIGHT//2 + 40, WINDOW_HEIGHT//2 - 40)
                        powerup.goto(px, py)
                        powerup.showturtle()

        # Powerup pickup
        if selected_mode == "modified" and powerup.distance(head) < 20:
            powerup.hideturtle()
            powerup.goto(1000, 1000)
            double_active = True
            double_remaining = 5
            powerup_cooldown = 300

        # Move segments
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move_head()

        # Body collision detection
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game_and_return_to_menu()
                running_game = False
                break

        time.sleep(delay)

# ----------------------------
# Start the program by showing main menu
# ----------------------------
show_main_menu()
wn.mainloop()
