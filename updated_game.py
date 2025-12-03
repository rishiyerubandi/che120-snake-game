# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech
# Modified by UW CHE 120 Students

import turtle
import time
import random


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BUTTON_CORNER_RADIUS = 12
BUTTON_PADDING = 10

delay = 0.1

double_cooldown = 0
reverse_cooldown = 0
phantom_cooldown = 0
shield_cooldown = 0
pointloss_cooldown = 0

score = 0
high_score = 0

shield_respawning = False

game_state = "menu"
selected_mode = "normal"
running_game = False

double_active = False
double_remaining = 0
powerup_cooldown = 0

double_mode = False
reverse_mode = False
phantom_mode = False
shield_mode = False


def random_grid_pos():
    x = random.randrange(-14, 15) * 20
    y = random.randrange(-14, 15) * 20
    return x, y


def safe_spawn(occupied_positions):
    for _ in range(500):
        pos = random_grid_pos()
        if pos not in occupied_positions:
            return pos
    return random_grid_pos()


shield_shape = (
    (0,25),
    (12,18),
    (18,4),
    (14,-18),
    (0,-25),
    (-14,-18),
    (-18,4),
    (-12,18)
)

wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech (Merged)")
wn.bgcolor("green")
wn.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
wn.tracer(0)

turtle.register_shape("shield_icon", shield_shape)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

double_points = turtle.Turtle()
double_points.speed(0)
double_points.shape("circle")
double_points.color("yellow")
double_points.penup()
double_points.goto(1000, 1000)
double_points.active = False
double_points.hideturtle()

reverse_token = turtle.Turtle()
reverse_token.speed(0)
reverse_token.shape("circle")
reverse_token.color("blue")
reverse_token.penup()
reverse_token.goto(1000, 1000)
reverse_token.active = False
reverse_token.hideturtle()

phantom_token = turtle.Turtle()
phantom_token.speed(0)
phantom_token.shape("circle")
phantom_token.color("blue")
phantom_token.penup()
phantom_token.goto(1000, 1000)
phantom_token.active = False
phantom_token.hideturtle()

shield_token = turtle.Turtle()
shield_token.speed(0)
shield_token.shape("shield_icon")
shield_token.color("white")
shield_token.penup()
shield_token.goto(1000, 1000)
shield_token.active = False
shield_token.hideturtle()

point_loss_token = turtle.Turtle()
point_loss_token.speed(0)
point_loss_token.shape("circle")
point_loss_token.color("yellow")
point_loss_token.penup()
point_loss_token.goto(1000, 1000)
point_loss_token.active = False
point_loss_token.hideturtle()

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))


def go_up():
    global reverse_mode
    if not reverse_mode:
        if head.direction != "down":
            head.direction = "up"
    else:
        if head.direction != "up":
            head.direction = "down"


def go_down():
    global reverse_mode
    if not reverse_mode:
        if head.direction != "up":
            head.direction = "down"
    else:
        if head.direction != "down":
            head.direction = "up"


def go_left():
    global reverse_mode
    if not reverse_mode:
        if head.direction != "right":
            head.direction = "left"
    else:
        if head.direction != "left":
            head.direction = "right"


def go_right():
    global reverse_mode
    if not reverse_mode:
        if head.direction != "left":
            head.direction = "right"
    else:
        if head.direction != "right":
            head.direction = "left"


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

    x, y = head.xcor(), head.ycor()
    if phantom_mode:
        if x > 290:
            head.setx(-280)
        if x < -290:
            head.setx(280)
        if y > 290:
            head.sety(-280)
        if y < -290:
            head.sety(280)


def end_double():
    global double_mode
    double_mode = False


def end_reverse():
    global reverse_mode
    reverse_mode = False


def end_phantom():
    global phantom_mode
    phantom_mode = False


def end_shield():
    global shield_mode
    shield_mode = False


wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


def hide_all_powerups():
    double_points.goto(1000,1000); double_points.hideturtle(); double_points.active = False
    reverse_token.goto(1000,1000); reverse_token.hideturtle(); reverse_token.active = False
    phantom_token.goto(1000,1000); phantom_token.hideturtle(); phantom_token.active = False
    shield_token.goto(1000,1000); shield_token.hideturtle(); shield_token.active = False
    point_loss_token.goto(1000,1000); point_loss_token.hideturtle(); point_loss_token.active = False


hide_all_powerups()


def run_game_loop(mode="normal"):
    global delay, double_cooldown, reverse_cooldown, phantom_cooldown, shield_cooldown, pointloss_cooldown
    global score, high_score, segments, double_mode, reverse_mode, phantom_mode, shield_mode, shield_respawning
    global running_game, double_active, double_remaining, powerup_cooldown

    running_game = True

    while running_game:
        wn.update()

        if shield_respawning:
            shield_respawning = False

        if double_cooldown > 0:
            double_cooldown -= 1
        if reverse_cooldown > 0:
            reverse_cooldown -= 1
        if phantom_cooldown > 0:
            phantom_cooldown -= 1
        if shield_cooldown > 0:
            shield_cooldown -= 1
        if pointloss_cooldown > 0:
            pointloss_cooldown -= 1

        simul = (score >= 200)

        occupied = set()
        occupied.add((round(head.xcor()), round(head.ycor())))
        for s in segments:
            occupied.add((round(s.xcor()), round(s.ycor())))
        occupied.add((round(food.xcor()), round(food.ycor())))
        if double_points.active:
            occupied.add((round(double_points.xcor()), round(double_points.ycor())))
        if reverse_token.active:
            occupied.add((round(reverse_token.xcor()), round(reverse_token.ycor())))
        if phantom_token.active:
            occupied.add((round(phantom_token.xcor()), round(phantom_token.ycor())))
        if shield_token.active:
            occupied.add((round(shield_token.xcor()), round(shield_token.ycor())))
        if point_loss_token.active:
            occupied.add((round(point_loss_token.xcor()), round(point_loss_token.ycor())))
        if selected_mode == "modified":
            if (simul or (not double_points.active)) and double_cooldown <= 0 and random.random() < 0.01:
                x,y = safe_spawn(occupied)
                double_points.goto(x,y)
                double_points.showturtle()
                double_points.active = True
                occupied.add((x,y))
    
            if (simul or (not reverse_token.active)) and reverse_cooldown <= 0 and random.random() < 0.01:
                x,y = safe_spawn(occupied)
                reverse_token.goto(x,y)
                reverse_token.showturtle()
                reverse_token.active = True
                occupied.add((x,y))
    
            if (simul or (not phantom_token.active)) and phantom_cooldown <= 0 and random.random() < 0.01:
                x,y = safe_spawn(occupied)
                phantom_token.goto(x,y)
                phantom_token.showturtle()
                phantom_token.active = True
                occupied.add((x,y))
    
            if (simul or (not shield_token.active)) and shield_cooldown <= 0 and random.random() < 0.005:
                x,y = safe_spawn(occupied)
                shield_token.goto(x,y)
                shield_token.showturtle()
                shield_token.active = True
                occupied.add((x,y))
    
            if (simul or (not point_loss_token.active)) and pointloss_cooldown <= 0 and random.random() < 0.01:
                x,y = safe_spawn(occupied)
                point_loss_token.goto(x,y)
                point_loss_token.showturtle()
                point_loss_token.active = True
                occupied.add((x,y))

        if not phantom_mode and (head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290):
            if shield_mode:
                shield_mode = False
                shield_respawning = True

                head.goto(0, 0)
                head.direction = "stop"

                for i, seg in enumerate(segments):
                    seg.goto(head.xcor(), head.ycor() - 20 * (i + 1))

                hide_all_powerups()
                time.sleep(0.1)
                continue
            else:
                time.sleep(1)
                head.goto(0,0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000,1000)
                segments.clear()
                score = 0
                delay = 0.1
                double_mode = False
                reverse_mode = False
                phantom_mode = False
                shield_mode = False
                hide_all_powerups()
                double_cooldown = reverse_cooldown = phantom_cooldown = shield_cooldown = pointloss_cooldown = 0
                running_game = False
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score),
                          align="center", font=("Courier", 24, "normal"))
                break

        if head.distance(food) < 20:
            occ2 = set()
            occ2.add((round(head.xcor()), round(head.ycor())))
            for s in segments:
                occ2.add((round(s.xcor()), round(s.ycor())))
            if double_points.active:
                occ2.add((round(double_points.xcor()), round(double_points.ycor())))
            if reverse_token.active:
                occ2.add((round(reverse_token.xcor()), round(reverse_token.ycor())))
            if phantom_token.active:
                occ2.add((round(phantom_token.xcor()), round(phantom_token.ycor())))
            if shield_token.active:
                occ2.add((round(shield_token.xcor()), round(shield_token.ycor())))
            if point_loss_token.active:
                occ2.add((round(point_loss_token.xcor()), round(point_loss_token.ycor())))

            fx, fy = safe_spawn(occ2)
            food.goto(fx, fy)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            new_segment.goto(1000, 1000)
            segments.append(new_segment)

            delay -= 0.001

            if double_mode:
                score += 20
            else:
                score += 10

            if score > high_score:
                high_score = score

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score),
                      align="center", font=("Courier", 24, "normal"))

        if double_points.active and head.distance(double_points) < 20:
            double_points.goto(1000,1000)
            double_points.hideturtle()
            double_points.active = False
            double_mode = True
            double_cooldown = 300
            wn.ontimer(end_double, 10000)

        if reverse_token.active and head.distance(reverse_token) < 20:
            reverse_token.goto(1000,1000)
            reverse_token.hideturtle()
            reverse_token.active = False
            reverse_mode = True
            reverse_cooldown = 300
            wn.ontimer(end_reverse, 8000)

        if phantom_token.active and head.distance(phantom_token) < 20:
            phantom_token.goto(1000,1000)
            phantom_token.hideturtle()
            phantom_token.active = False
            phantom_mode = True
            phantom_cooldown = 300
            wn.ontimer(end_phantom, 8000)

        if shield_token.active and head.distance(shield_token) < 20:
            shield_token.goto(1000,1000)
            shield_token.hideturtle()
            shield_token.active = False
            shield_mode = True
            shield_cooldown = 300
            wn.ontimer(end_shield, 12000)

        if point_loss_token.active and head.distance(point_loss_token) < 20:
            point_loss_token.goto(1000,1000)
            point_loss_token.hideturtle()
            point_loss_token.active = False
            score = max(0, score - 30)
            pointloss_cooldown = 300
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score),
                      align="center", font=("Courier", 24, "normal"))

        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        collided = False
        for segment in segments:
            if segment.distance(head) < 20:
                collided = True
                if phantom_mode:
                    collided = False
                    break
                if shield_mode:
                    shield_mode = False
                    shield_respawning = True

                    head.goto(0, 0)
                    head.direction = "stop"

                    for i, seg in enumerate(segments):
                        seg.goto(head.xcor(), head.ycor() - 20 * (i + 1))

                    hide_all_powerups()
                    time.sleep(0.1)
                    collided = False
                    break
                time.sleep(1)
                head.goto(0,0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000,1000)
                segments.clear()
                score = 0
                delay = 0.1
                double_mode = False
                reverse_mode = False
                phantom_mode = False
                shield_mode = False
                hide_all_powerups()
                double_cooldown = reverse_cooldown = phantom_cooldown = shield_cooldown = pointloss_cooldown = 0
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score),
                          align="center", font=("Courier", 24, "normal"))
                running_game = False
                break

        time.sleep(delay)

    running_game = False
    return


# Main Menu

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


btn_w = 220
btn_h = 60
center_x = 0

play_btn = RoundedButton(center_x, 40, btn_w, btn_h, fill_color="blue", border_color="black", text="PLAY", text_color="white")
options_btn = RoundedButton(center_x, -40, btn_w, btn_h, fill_color="red", border_color="black", text="OPTIONS", text_color="white")

normal_btn = RoundedButton(center_x, 60, btn_w, btn_h, fill_color="purple", border_color="black", text="NORMAL MODE", text_color="white")
modified_btn = RoundedButton(center_x, 0, btn_w, btn_h, fill_color="purple", border_color="black", text="MODIFIED MODE", text_color="white")
back_btn = RoundedButton(center_x, -80, btn_w, btn_h, fill_color="orange", border_color="black", text="BACK", text_color="white")

current_buttons = []

title_turtle = turtle.Turtle(visible=False)
title_turtle.hideturtle()
title_turtle.penup()
title_turtle.color("white")

head.hideturtle()
food.hideturtle()
double_points.hideturtle()
double_points.goto(1000,1000)
reverse_token.hideturtle()
reverse_token.goto(1000,1000)
phantom_token.hideturtle()
phantom_token.goto(1000,1000)
shield_token.hideturtle()
shield_token.goto(1000,1000)
point_loss_token.hideturtle()
point_loss_token.goto(1000,1000)
pen.hideturtle()


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
    double_points.hideturtle()
    reverse_token.hideturtle()
    phantom_token.hideturtle()
    shield_token.hideturtle()
    point_loss_token.hideturtle()
    pen.clear()
    pen.hideturtle()


def setup_game():
    global segments, score, delay, double_active, double_remaining, powerup_cooldown, running_game, double_mode
    head.showturtle()
    head.goto(0, 0)
    head.direction = "stop"

    food.showturtle()
    food.goto(0, 100)

    double_points.hideturtle(); double_points.goto(1000,1000); double_points.active=False
    reverse_token.hideturtle(); reverse_token.goto(1000,1000); reverse_token.active=False
    phantom_token.hideturtle(); phantom_token.goto(1000,1000); phantom_token.active=False
    shield_token.hideturtle(); shield_token.goto(1000,1000); shield_token.active=False
    point_loss_token.hideturtle(); point_loss_token.goto(1000,1000); point_loss_token.active=False

    for s in segments:
        s.hideturtle()
        s.goto(1000, 1000)
    segments = []

    score = 0
    delay = 0.1
    double_active = False
    double_mode = False
    double_remaining = 0
    powerup_cooldown = 0

    pen.showturtle()
    update_score_display()
    running_game = True


def reset_game_and_return_to_menu():
    global segments, score, delay, double_active, double_remaining, powerup_cooldown, running_game, double_mode
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
    double_mode = False
    double_remaining = 0
    powerup_cooldown = 0
    running_game = False
    update_score_display()
    show_main_menu()


def update_score_display():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))


wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


def play_action():
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
    normal_btn.text = "NORMAL MODE"
    modified_btn.text = "MODIFIED MODE"
    show_main_menu()


normal_btn.action = select_normal
modified_btn.action = select_modified
back_btn.action = back_action


def on_screen_click(x, y):
    if game_state in ("menu", "options"):
        for b in current_buttons:
            if b.contains(x, y):
                b.click()
                return


wn.onscreenclick(on_screen_click)


def start_playing():
    global game_state
    game_state = "playing"
    for b in (play_btn, options_btn, normal_btn, modified_btn, back_btn):
        b.hide()
    title_turtle.clear()
    setup_game()
    run_game_loop(mode=selected_mode)
    show_main_menu()


show_main_menu()
wn.mainloop()
