import pygame
from pygame import Rect
import time

BLACK = (0,0,0)
WHITE = (220,220,220)
GREEN = (50,205,50)
RED = (255,0,0)
YELLOW = (255,255,0)
GREY = (128,128,128)
DARK_GREEN = (0,100,0)

class World():
    def __init__(self):
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = 400
        self.BLOCK_SIZE = 20
        self.agent = (120,280)
        self.goal = (80,80)
        self.fakeGoal = (320,80)
        self.walls = [(140,160),(160,160),(180,160),(200,160),
                      (140,180),(160,180),(180,180),(200,180),
                      (140,200),(160,200),(180,200),(200,200),
                      (160,220),(180,220),]

        pygame.init()
        pygame.display.set_caption('Deceptive agent')
        
        #Creates a 400 x 400 screen
        self.screen = pygame.display.set_mode((self.WINDOW_HEIGHT,self.WINDOW_WIDTH))
        self.drawGrid()
        return


    def drawGrid(self):

        block = self.BLOCK_SIZE
        for y in range(0, self.WINDOW_HEIGHT, block):
            for x in range(0, self.WINDOW_WIDTH, block):

                rect = pygame.Rect(x,y,block,block) #Shape location and size

                #Colour selection for different objects
                if self.agent == (x,y):
                    colour = YELLOW
                elif self.goal == (x,y):
                    colour = GREEN
                elif self.fakeGoal == (x,y):
                    colour = DARK_GREEN
                elif (x,y) in self.walls:
                    colour = BLACK
                else:
                    colour = GREY

                pygame.draw.rect(self.screen,colour,rect)
                pygame.draw.rect(self.screen,WHITE,rect,1) #White border

        pygame.display.update()
        return

    def agent_step(self, action):
        x, y = self.agent
        block = self.BLOCK_SIZE
        if action == 'LEFT':
            self.agent = (x - block, y)
        elif action == 'UP':
            self.agent = (x, y - block)
        elif action == 'RIGHT':
            self.agent = (x + block, y)
        else:
            self.agent = (x, y + block)

        self.drawGrid()

        time.sleep(0.2)

        return
    
    def valid(self, location):
        x, y = location
        if y > self.WINDOW_HEIGHT-self.BLOCK_SIZE or y < 0 or x > self.WINDOW_WIDTH-self.BLOCK_SIZE \
        or x < 0 or (x, y) in self.walls:
            return False
        else:
            return True

    def getSuccessors(self, state):
        successors = []
        x, y = state
        block = self.BLOCK_SIZE
        #Each successor node contains the location, the action taken to get there, and the cost
        successors.append(((x - block, y), 'LEFT', 1))
        successors.append(((x + block, y), 'RIGHT', 1))
        successors.append(((x, y + block), 'DOWN', 1))
        successors.append(((x, y - block), 'UP', 1))

        return [node for node in successors if self.valid(node[0])]

