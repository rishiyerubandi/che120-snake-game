# Simple Snake Game in Python 3 for Beginners
# By @TokyoEdTech


#Rishi Yerubandi (RY) 
#John Haddad (JH)
#Osagie Ebhonu (OE)



import turtle   # Import the turtle graphics module (RY)
import time     # Import the time module (RY)
import random   # Import the random module (RY)

delay = 0.1     # Controls the speed of the snake (RY)

# Score
score = 0       # Current score (RY)
high_score = 0  # Highest score reached (RY)

# ----------------------------
# Set up the game window
# ----------------------------
wn = turtle.Screen()                    # Creates the game window object (RY)
wn.title("Snake Game by @TokyoEdTech")  # Sets the title of the window (RY)
wn.bgcolor("green")                     # Sets the background color of the window (RY)
wn.setup(width=600, height=600)         # Sets the dimensions of the window (RY)
wn.tracer(0)                            # Turns off the screen updates


# ----------------------------
# Snake Head (the main player)
# ----------------------------
head = turtle.Turtle()                  # Creates a turtle object for the snake's head (RY)
head.speed(0)                           # Sets the speed of the animation to the maximum (RY)
head.shape("square")                    # Sets the shape of the snake's head (RY)
head.color("black")                     # Sets the color of the snake's head (RY)
head.penup()                            # Prevents the turtle from drawing lines (RY)
head.goto(0,0)                          # Places the snake's head at the center of the screen (RY)
head.direction = "stop"                 # Initial direction of the snake (RY)

# ----------------------------
# Snake Food
# ----------------------------
food = turtle.Turtle()                  # Creates a turtle object for the food (RY)
food.speed(0)                           # Sets the speed of the animation to the maximum (RY)
food.shape("circle")                    # Sets the shape of the food (RY)
food.color("red")                       # Sets the color of the food (RY)
food.penup()                            # Prevents the turtle from drawing lines (RY)
food.goto(0,100)                        # Places the food at a specific location (RY)

segments = []                           # List to keep track of snake segments (RY)

# ----------------------------
# Score Display (Pen)
# ----------------------------
pen = turtle.Turtle()               # Creates a turtle object for writing the score (JH)
pen.speed(0)                        # Sets the speed of the animation to the maximum (JH)
pen.shape("square")                 # Invisible square used as the text holder (JH)
pen.color("white")                  # Sets the color of the ptext (JH) 
pen.penup()                         # Prevents the turtle from drawing lines (JH) 
pen.hideturtle()                    # Hides the turtle icon (JH)
pen.goto(0, 260)                    # Positions the text at the top of the screen (JH)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))    # Initial score display (JH)

# ----------------------------
# Movement Functions
# These only change direction, not actual movement (JH)
# ----------------------------
def go_up():                               
    if head.direction != "down":  # Prevents the snake from reversing (JH)
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

# ----------------------------
# Function that physically moves the snake head each frame
# ----------------------------
def move():
    if head.direction == "up":
        y = head.ycor()         # Get the current y coordinate (JH)
        head.sety(y + 20)       # Move the head up by 20 units (JH)

    if head.direction == "down":
        y = head.ycor()        
        head.sety(y - 20)       # Move the head down by 20 units (JH)

    if head.direction == "left":
        x = head.xcor()         # Get the current x coordinate (JH)
        head.setx(x - 20)       # Move the head left by 20 units (JH)

    if head.direction == "right":                   
        x = head.xcor()
        head.setx(x + 20)       # Move the head right by 20 units (JH)

# ----------------------------
# Keyboard Bindings
#----------------------------
wn.listen()                       # Tell the window to expect keyboard input (JH)   
wn.onkeypress(go_up, "w")         # Bind the "w" key to go_up function (JH)
wn.onkeypress(go_down, "s")       # Bind the "s" key to go_down function (JH)
wn.onkeypress(go_left, "a")       # Bind the "a" key to go_left function (JH)
wn.onkeypress(go_right, "d")      # Bind the "d" key to go_right function (JH)

# ----------------------------
# Main Game Loop
# ----------------------------
while True:
    wn.update()       # Updates the screen for every loop (JH)

    # ------------------------
    # Border Collision Check
    # ------------------------
    # If the snake hits the border, restart the game (JH)
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:      
        time.sleep(1)               # Pause for a second before restarting (OE)   
        head.goto(0,0)              # Reset the head position to the center (OE)
        head.direction = "stop"     # Stop the snake's movement (OE)

        
        for segment in segments:    # Hide previous body segments after restarting (OE)
            segment.goto(1000, 1000)
        

        segments.clear()  # Clear the segments list (OE)

        
        score = 0         # Reset the score (OE)


        delay = 0.1       # Reset the delay (OE)

        pen.clear()       # Clear the previous score display (OE)
        
        # Returns initial score display when game restarts (OE)
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


    # ------------------------
    # Food Collision Check
    # ------------------------
    if head.distance(food) < 20:       # If the snake head is close enough to the food (OE)
        x = random.randint(-290, 290)  # Generate a random x coordinate (OE)
        y = random.randint(-290, 290)  # Generate a random y coordinate (OE)
        food.goto(x,y)                 # Move the food to the new random location (OE)    

        # Add a new body segment (JH)
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)    #Add the new segment to the body (OE)

        
        delay -= 0.001          # Slightly increase the speed of the snake (OE)


        score += 10             # Increase the score by 10 (OE)

        if score > high_score:  # Update high score if current score is greater (OE)
            high_score = score
        
        pen.clear()             # Clear the previous score display (OE)

        # Update the score display with new score as high score (OE)
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # ------------------------
    # Move body segments
    # ------------------------
    # Move each segment to the position of the one in front of it (OE)
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()      # Get the x coordinate of the segment in front (OE)
        y = segments[index-1].ycor()      # Get the y coordinate of the segment in front (OE)
        segments[index].goto(x, y)        # Move the current segment to that position (OE)

    # Move the first segment to where the head is (OE)
    if len(segments) > 0:
        x = head.xcor()                   # Get the x coordinate of the head (OE)
        y = head.ycor()                   # Get the y coordinate of the head (OE)
        segments[0].goto(x,y)             # Move the first segment to that position (OE)

    move()                                # Call the move function to move the snake head (OE)

    # ------------------------
    # Body Collision Check
    # ------------------------
    for segment in segments:
        if segment.distance(head) < 20:   # If the head collides with any body segment (OE)
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            
            for segment in segments:    # Hide previous body segments after collision (OE)
                segment.goto(1000, 1000)
        
            
            segments.clear()            # Clear the segments list (OE)

            
            score = 0                   # Reset the score (OE)

                                        
            delay = 0.1                 # Reset the delay (OE)  
         
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)           # Control the speed of the game by delay amount (OE)

wn.mainloop()            # Keeps the window open (OE)
