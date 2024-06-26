import random 
import pygame
import math
import random as rand
import os
import time
import sys




class Env():

    global WIDTH, HEIGHT, PUCK_SIZE,PADDLE_SIZE, SPEED_CLOCK, WHITE, RED, BROWN, BLACK,BACKGROUND_color
    global GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1

    # metric and time 
    WIDTH = 500
    HEIGHT = 650
    PUCK_SIZE = 20 
    PADDLE_SIZE = 100
    SPEED_CLOCK = 15
    GOAL_x0, GOAL_x1, GOAL_y0, GOAL_y1 = 0*int(1*WIDTH/15), int(15*WIDTH/15) , 0, HEIGHT/40

    # rgb colors
    WHITE = (255, 255, 255)
    RED = (200,55,55)
    BROWN = (122, 115, 81)
    BLACK = (0,0,0)
    BACKGROUND_color = (252, 235, 151)

    def __init__(self):

        self.done1,self.done2 = False,False
        self.reward1,self.reward2 = 0,0
        self.hit1,self.hit2 = 0,0
        self.total_hit1, self.miss1,self.total_hit2, self.miss2 = 0,0,0,0


        pygame.init()
        gamelogo = pygame.image.load(os.path.join('cynaptics.png'))
        pygame.display.set_icon(gamelogo)

        pygame.display.set_caption('Cynaptics NeuralNexus RL')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.smallfont = pygame.font.SysFont("comicsans", 25)
        self.roundfont = pygame.font.SysFont("comicsans", 45)  
        

        self.clock = pygame.time.Clock()


        self.paddle1x = WIDTH/2
        self.paddle1y = 1*HEIGHT/10
        self.paddle1dx = 33

        self.paddle2x = WIDTH/2
        self.paddle2y = 9*HEIGHT/10
        self.paddle2dx = 33

        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = int(HEIGHT/2)
        n = random.randint(0,9)
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = ((-1)**n)*25


    def paddle1_right(self):
        if self.paddle1x < WIDTH-PADDLE_SIZE/2:
            self.paddle1x +=  self.paddle1dx

    def paddle1_left(self):
        if self.paddle1x > PADDLE_SIZE/2 :
            self.paddle1x -=  self.paddle1dx

    def paddle2_right(self):
        if self.paddle2x < WIDTH-PADDLE_SIZE/2:
            self.paddle2x +=  self.paddle2dx

    def paddle2_left(self):
        if self.paddle2x > PADDLE_SIZE/2 :
            self.paddle2x -=  self.paddle2dx

    def run_frame(self):

        self.puckx +=  int(math.cos(self.puckangle)*self.puckdx)
        self.pucky += int(math.sin(self.puckangle)*self.puckdy)


        # Collision Mechanism
        if self.puckx > WIDTH - PUCK_SIZE:
            self.puckx = WIDTH - PUCK_SIZE
            self.puckdx *= -1

        if self.puckx < PUCK_SIZE :
            self.puckx = 0 + PUCK_SIZE
            self.puckdx *= -1
                


        # Goal Mechanism
        if self.pucky < self.paddle1y:
            self.miss1 += 1
            self.reward1 -= 1
            self.done1 = True
            self.hit1 = 0
            text = pygame.font.Font('arial.ttf', 40).render("GOAL !", True, BLACK)
            self.screen.blit(text, [WIDTH/2-65, HEIGHT/2-15])
            pygame.display.flip()
            time.sleep(0.3)
            self.reset()

        if self.pucky > self.paddle2y + PADDLE_SIZE/5:
            self.miss2 += 1
            self.reward2 -= 1
            self.done2 = True
            self.hit2 = 0
            text = pygame.font.Font('arial.ttf', 40).render("GOAL !", True, BLACK)
            self.screen.blit(text, [WIDTH/2-65, HEIGHT/2-15])
            pygame.display.flip()
            time.sleep(0.3)
            self.reset()

        # Ball Player collision mechanism
        if  abs((self.paddle1y - self.pucky + abs(self.puckdy/2))) <= PUCK_SIZE/2 + PADDLE_SIZE/10 and abs(self.paddle1x - self.puckx - abs(self.puckdx/2)) <= PADDLE_SIZE/2:
            self.pucky += PUCK_SIZE
            self.puckdy *= -1
            self.hit1 += 1
            self.total_hit1 += 1
            self.reward1 += 1
                 
        if  abs((self.paddle2y - self.pucky - abs(self.puckdy/2))) <= PUCK_SIZE/2 + PADDLE_SIZE/10 and abs(self.paddle2x - self.puckx - abs(self.puckdx/2)) <= PADDLE_SIZE/2:
            self.pucky -= PUCK_SIZE
            self.puckdy *= -1
            self.hit2 += 1
            self.total_hit2 += 1
            self.reward2 += 1
            
        

    #Print screen
    def update_screen(self):
        self.screen.fill(BACKGROUND_color)
        pygame.draw.circle(self.screen,WHITE, (WIDTH / 2, HEIGHT / 2), 70, 5)
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 6) #borders
        pygame.draw.rect(self.screen, WHITE, (0,HEIGHT / 2, WIDTH, 6))
        pygame.draw.circle(self.screen, RED, (self.puckx, self.pucky), PUCK_SIZE/2, 0,True,True,True,True) #ball
        # Paddle 1
        pygame.draw.rect(self.screen, (50,200,50), pygame.Rect(self.paddle1x-int(PADDLE_SIZE/2), self.paddle1y , PADDLE_SIZE, int(PADDLE_SIZE/5)))
        pygame.draw.ellipse(self.screen, (50,200,50), pygame.Rect(self.paddle1x-int(PADDLE_SIZE/2), self.paddle1y- int(PADDLE_SIZE/10)  , PADDLE_SIZE, int(PADDLE_SIZE/2)))
        text = pygame.font.Font('arial.ttf', 20).render(" AI ", True, BLACK)
        self.screen.blit(text, [self.paddle1x-18, self.paddle1y]) 
        # Paddle 2
        pygame.draw.rect(self.screen, (50,50,200), pygame.Rect(self.paddle2x-int(PADDLE_SIZE/2), self.paddle2y , PADDLE_SIZE, int(PADDLE_SIZE/5)))
        pygame.draw.ellipse(self.screen, (50,50,200), pygame.Rect(self.paddle2x-int(PADDLE_SIZE/2), self.paddle2y - int(PADDLE_SIZE/5)  , PADDLE_SIZE, int(PADDLE_SIZE/2)))
        text = pygame.font.Font('arial.ttf', 20).render(" ME ", True, BLACK)
        self.screen.blit(text, [self.paddle2x-18, self.paddle2y-15])

        # Updating score text
        text = pygame.font.Font('arial.ttf', 40).render(str(self.miss2), True, (50,200,50))
        self.screen.blit(text, [WIDTH/10, HEIGHT/2-90])
        text = pygame.font.Font('arial.ttf', 40).render(str(self.miss1), True, (50,50,200))
        self.screen.blit(text, [WIDTH/10, HEIGHT/2+50])
        
        
        pygame.display.flip()

    def terminate(self):
        if(self.miss1==5 or self.miss2==5):
            if(self.miss1>self.miss2):
                text = pygame.font.Font('arial.ttf', 40).render("YOU WON !", True, BLACK)
                self.screen.blit(text, [WIDTH/2-65, HEIGHT/2+30])
                pygame.display.flip()
                time.sleep(2)
                sys.exit()
            if(self.miss2>self.miss1):
                text = pygame.font.Font('arial.ttf', 40).render("AI WON!", True, BLACK)
                self.screen.blit(text, [WIDTH/2-65, HEIGHT/2+30])
                pygame.display.flip()
                time.sleep(2)
                sys.exit()

    # 0 move left
    # 1 do nothing
    # 2 move right

    def reset(self):
        self.puckx = random.randint(int(WIDTH/3),int(2*WIDTH/3))
        self.pucky = int(HEIGHT/2)
        n = random.randint(0,9)
        self.puckangle = rand.uniform(math.pi/3, 2*math.pi/3)
        self.puckdx = 25
        self.puckdy = ((-1)**n)*25

        self.paddle1x = int(WIDTH/2)
        self.paddle1y = int(1*HEIGHT/10)

        self.paddle2x = int(WIDTH/2)
        self.paddle2y = int(9*HEIGHT/10)

        return [self.paddle1x/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5],[self.paddle2x/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5]

    def step(self, action1,action2):

        self.reward1 = 0
        self.reward2 = 0
        self.done1 = 0
        self.done2 = 0

        if action1 == 0:
            self.paddle1_left()
            self.reward1 -= 0 

        if action1 == 2:
            self.paddle1_right()
            self.reward1 -= 0 

        if action2 == 0:
            self.paddle2_left()
            self.reward2 -= 0 

        if action2 == 2:
            self.paddle2_right()
            self.reward2 -= 0

        self.run_frame()  

        
        state1 =  [self.paddle1x/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5]
        state2 =  [self.paddle2x/WIDTH, self.puckx/WIDTH, self.pucky/HEIGHT, 0.5*(math.cos(self.puckangle)*self.puckdx)/self.puckdx+0.5, 0.5*(math.sin(self.puckangle)*self.puckdy)/self.puckdy+0.5]

        self.update_screen()
        self.clock.tick(SPEED_CLOCK)

        return self.reward1,self.reward2, state1, state2, self.done1,self.done2,self.hit1,self.hit2,self.total_hit1,self.total_hit2