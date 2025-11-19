# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech
# Modified with DOUBLE POINTS power-up

import turtle
import time
import random

delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game by @TokyoEdTech")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

# Double Points Power-Up
double_points = turtle.Turtle()
double_points.speed(0)
double_points.shape("circle")
double_points.color("yellow")
double_points.penup()
double_points.goto(-150, 150)
double_points.active = True
double_mode = False

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
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

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# End double mode
def end_double():
    global double_mode
    double_mode = False

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        segments.clear()
        score = 0
        delay = 0.1
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score),
                  align="center", font=("Courier", 24, "normal")) 

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001

        # --- Double Points scoring ---
        if double_mode:
            score += 20
        else:
            score += 10

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score),
                  align="center", font=("Courier", 24, "normal"))

        # --- Randomly respawn double points ---
        if not double_points.active and random.random() < 0.10:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            double_points.goto(x, y)
            double_points.active = True

    # --- Double Points Pickup ---
    if double_points.active and head.distance(double_points) < 20:
        double_points.goto(1000, 1000)
        double_points.active = False
        double_mode = True

        # Turn off after 10 seconds
        wn.ontimer(end_double, 10000)

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            for segment in segments:
                segment.goto(1000, 1000)
        
            segments.clear()
            score = 0
            delay = 0.1
        
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score),
                      align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()
