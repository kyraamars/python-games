# Snake Game in Python
# By Kyra Mars

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object): 
    rows = 20 
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        #Set to 1 initially, want to make sure we start moving in a direction
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny): 
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False): 
        #Figure out distance between each x value and each y value for each cube
        dis = self.w // self.rows
        #Row
        i = self.pos[0]
        #Column
        j = self.pos[1]
        #
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2)) #Math is so you can see the grid lines when filled

        #Draw eyes
        if eyes: 
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

#Snake Object Will Contain Cube Objects
class snake(object): 
    #Create Snake Body
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        #Add the head to the body
        self.body.append(self.head)
        #Direction for x - to move snake
        self.dirnx = 0
        #Direction for y - to move snake
        self.dirny = 1

    def move(self): 
        for event in pygame.event.get(): 
            #Enable
            if event.type == pygame.QUIT: 
                pygame.quit()
            #Get dictionary of key values and if they were pressed or not
            keys = pygame.key.get_pressed()

            for key in keys: 
                if keys[pygame.K_LEFT]: 
                    self.dirnx = -1
                    self.dirny = 0
                    #Need to remember where the head of the snake turned (will add a key to a dictionary to let us know)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]: 
                    self.dirnx = 1
                    self.dirny = 0
                    #Need to remember where the head of the snake turned (will add a key to a dictionary to let us know)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]: 
                    self.dirnx = 0
                    self.dirny = -1
                    #Need to remember where the head of the snake turned (will add a key to a dictionary to let us know)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]: 
                    self.dirnx = 0
                    self.dirny = 1
                    #Need to remember where the head of the snake turned (will add a key to a dictionary to let us know)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
            #Get index(i) and cube(c) object in our self.body(body of snake is made of cube objects) 
            for i, c in enumerate(self.body): 
                #All cube objects have a position, grab it
                p = c.pos[:]
                #See If the position is in the turns, and add to the turn list
                if p in self.turns: 
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])
                    #If we are on the last cube, we will remove the turn from the list
                    if i == len(self.body) - 1: 
                        self.turns.pop(p)
                #If position is not in the turn list, we still need to move the snake and check border limits
                else: 
                    #If we are moving left and the x position of our cube is less than or equal to zero, then we're going to change the position so it gpes to the right side of the screen.
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    #If we are moving right and the x position is at the end of the screen
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                    #If we are moving down
                    elif c.dirnx == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    #If we are moving up
                    elif c.dirnx == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                    #If we are not at the edge at the screen, then we are just going to move our cube in direction x and y
                    else: c.move(c.dirnx, c.dirny)


    def reset(self, pos): 
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 0

    def addCube(self): 
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        #Check what direction the tail is currently moving in, so we know where to add the cube
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface): 
        for i, c in enumerate(self.body):
            #Check to see if it's the first cube object, if it is, draw eyes for the snake
            if i == 0: 
                c.draw(surface, True)
            else: 
                c.draw(surface)

def drawGrid(w, rows, surface): 
    sizeBtwn = w // rows

    x=0
    y=0 

    for l in range(rows): 
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0), (x, w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w, y))

def redrawWindow(surface): 
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
    while True: 
        x = random.randrange(rows)
        y = random.randrange(rows)
        #Get a list of a filtered list and see if any positions are the same as the current positions of the snake (no snacks on top of snake)
        if len(list(filter(lambda z:z.pos == (x,y), positions)))> 0: 
            continue
        else: 
            break

    return (x,y)

def message_box(subject, content): 
    #Uses tkinter module, which creates a window
    root = tk.Tk()
    #Makes sure the window is the top "layer"
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try: 
        root.destroy()
    except: 
        pass

#Main Game Loop
def main(): 
    #Create Game Window
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))

    #Set Up Snake Object
    s = snake((255,0,0), (10,10))
    #Create snack
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

    #-----Start Main Loop-----#
    
    #Create Time Object
    clock = pygame.time.Clock()

    flag = True
    while flag: 
        pygame.time.delay(50) #the lower this number goes, the faster it will be 
        clock.tick(10) #Makes sure the game doesn't run faster than 10 frames per second (the lowere this number the slower it will be)
        #Will check everytime we run the loop if a key has been pressed, if it has, we're going to move accordingly
        s.move()
        if s.body[0].pos == snack.pos: 
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
        
        for x in range(len(s.body)): 
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print("Score: ", len(s.body))
                message_box("You Lost!", "Play Again...")
                s.reset((10,10))
                break

        redrawWindow(win)

    pass

main()