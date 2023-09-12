# Simple Pongo in Python for Beginnners
# By Kyra Mars
# Part 1: Getting Started

#turtle is a pre-installed Python library that enables users to create pictures and shapes by providing them with a virtual canvas.
#https://realpython.com/beginners-guide-python-turtle/ 
import turtle
import winsound


#Window Settings
wn = turtle.Screen()
wn.title("Pong by @kyra_mars")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

#Score
score_a = 0
score_b = 0

#Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0) #this the speed of animation, something we need to do for the turtle module to set things to the maximum possible speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

#Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0) #this the speed of animation, something we need to do for the turtle module to set things to the maximum possible speed
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

#Ball
ball = turtle.Turtle()
ball.speed(0) #this the speed of animation, something we need to do for the turtle module to set things to the maximum possible speed
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
#Every time the ball moves, it moves by x pixels. d means change
ball.dx = 0.25
ball.dy = -0.25

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

#Functions
def paddle_a_up(): 
    y = paddle_a.ycor()
    y += 30
    paddle_a.sety(y)

def paddle_a_down(): 
    y = paddle_a.ycor()
    y -= 30
    paddle_a.sety(y)

def paddle_b_up(): 
    y = paddle_b.ycor()
    y += 30
    paddle_b.sety(y)

def paddle_b_down(): 
    y = paddle_b.ycor()
    y -= 30
    paddle_b.sety(y)

#Keyboard Binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

#Main Game Loop
while True: 
    wn.update()

    #Move the Ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Border Checking - Compare Coordinates
    if ball.ycor() > 290: #top
        ball.sety(290)
        #Reverses the direction
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if ball.ycor() < -290: #bottom
        ball.sety(-290)
        #Reverses the direction
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
    
    if ball.xcor() > 390: #right
        ball.goto(0,0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
    
    if ball.xcor() < -390: #left
        ball.goto(0,0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    #Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40): 
        ball.setx(340)
        ball.dx *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40): 
        ball.setx(-340)
        ball.dx *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
