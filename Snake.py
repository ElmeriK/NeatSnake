import pygame
import neat
import os
from pygame.locals import *
from random import randint

import time
 

class Apple:
    x = 0
    y = 44
    step = 44
    points = 10
 
    def __init__(self,x,y):
        # give the apple a random position
        self.x = randint(2,9) * 44
        while self.y==44:
            self.y = randint(2,9) * 44
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
 
    updateCountMax = 0
    updateCount = 0
 
    def __init__(self, length):
        # initialize the lenght of the worm
        self.x = [0]
        self.y = [0]
        self.length = length
        for i in range(0,266):
           self.x.append(-100)
           self.y.append(-100)
 
        # initial positions, no collision.
        self.x[0] = 4*44
        self.x[1] = 3*44
        self.x[2] = 2*44
        self.y[0] = 1*44
        self.y[1] = 1*44
        self.y[2] = 1*44
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
        
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 == x2 and x1 == x2:
            if y1 == y2 and y1 == y2:
                return True
        return False
 
class App:
    config = 0
    genome = 0
    genome_id = 0
    windowWidth = 800
    windowHeight = 600
    player = 0
    apple = 0
 
    def __init__(self, genome_id, genome, config, displayMode):
        # displayMode determines if the game shows the game window or if it runs the game without the window
        self.displayMode = displayMode
        
        # stuff for the NEAT algorithm
        self.config = config
        self.genome_id = genome_id
        self.genome = genome
        self.genome.fitness = 0

        # variables for game logic
        self.noAppleCount = 0
        self.noCollision = True
        self._running = True
        
        # variables for the game window
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        
        # initial worm and apple variables
        self.player = Player(3) 
        self.apple = Apple(5,5)
 
    def on_init(self):
        self.noCollision = True
        self._running = True
        
        if self.displayMode:
            # initialize stuff for the game window
            pygame.init()
            self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
            self._image_surf = pygame.Surface((44,44))
            self._image_surf.fill((0,255,0))
            self._apple_surf = pygame.Surface((44,44))
            self._apple_surf.fill((255,0,0))
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_render(self):
        self._display_surf.fill((0,0,25))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        # printing information when the game ends and quitting the pygame module safely
        if self.displayMode:
            if self.noAppleCount > 1000:
                print(self.genome_id, round(self.genome.fitness), self.player.length, "apple")
            else:
                print(self.genome_id, round(self.genome.fitness), self.player.length)
            pygame.quit()

        
    def inputBoolean(self):
        input = [0,0,0,0,0,0]
        headx = self.player.x[0]
        heady = self.player.y[0]
        
        for i in range (1, self.player.length):
            #heading right
            if self.player.direction == 0:
                #danger left of snake
                if headx == self.player.x[i] and heady == self.player.y[i] + 44 or heady - 44 < 0:
                    input[0] = 1
                #danger ahead of snake
                if heady == self.player.y[i] and headx == self.player.x[i] - 44 or headx + 44 > 800:
                    input[1] = 1
                #danger right of snake
                if headx == self.player.x[i] and heady == self.player.y[i] - 44 or heady + 44 > 600:
                    input[2] = 1
                #apple on the left of snake
                if self.apple.y < heady:
                    input[3] = 1
                #apple ahead of snake
                if self.apple.x > headx:
                    input[4] = 1
                #apple right of snake
                if self.apple.y > heady:
                    input[5] = 1
            
            #heading right
            if self.player.direction == 1:
                #danger left of snake
                if headx == self.player.x[i] and heady == self.player.y[i] - 44 or heady + 44 > 600:
                    input[0] = 1
                #danger ahead of snake
                if heady == self.player.y[i] and headx == self.player.x[i] + 44 or headx - 44 < 0:
                    input[1] = 1
                #danger right of snake
                if headx == self.player.x[i] and heady == self.player.y[i] + 44 or heady - 44 < 0:
                    input[2] = 1
                #apple on the left of snake
                if self.apple.y > heady:
                    input[3] = 1
                #apple ahead of snake
                if self.apple.x < headx:
                    input[4] = 1
                #apple right of snake
                if self.apple.y < heady:
                    input[5] = 1
            #heading up
            if self.player.direction == 2:
                #danger left of snake
                if heady == self.player.y[i] and headx == self.player.x[i] + 44 or headx - 44 < 0:
                    input[0] = 1
                #danger ahead of snake
                if headx == self.player.x[i] and heady == self.player.y[i] + 44 or heady - 44 < 0:
                    input[1] = 1
                #danger right of snake
                if heady == self.player.y[i] and headx == self.player.x[i] - 44 or headx + 44 > 800:
                    input[2] = 1
                #apple on the left of snake
                if self.apple.x < headx:
                    input[3] = 1
                #apple ahead of snake
                if self.apple.y < heady:
                    input[4] = 1
                #apple right of snake
                if self.apple.x > headx:
                    input[5] = 1
            #heading down
            if self.player.direction == 3:
                #danger left of snake
                if heady == self.player.y[i] and headx == self.player.x[i] - 44 or headx + 44 > 800:
                    input[0] = 1
                #danger ahead of snake
                if headx == self.player.x[i] and heady == self.player.y[i] - 44 or heady + 44 > 600:
                    input[1] = 1
                #danger right of snake
                if heady == self.player.y[i] and headx == self.player.x[i] + 44 or headx - 44 < 0:
                    input[2] = 1
                #apple on the left of snake
                if self.apple.x > headx:
                    input[3] = 1
                #apple ahead of snake
                if self.apple.y > heady:
                    input[4] = 1
                #apple right of snake
                if self.apple.x < headx:
                    input[5] = 1
        return input
 
    def on_execute(self):
        #The main loop, important parts explained in the thesis

        if self.on_init() == False:
            self._running = False
        
        net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)
        
        while( self._running and self.noCollision ):
            if self.displayMode:
                pygame.event.pump()
                keys = pygame.key.get_pressed() 
    
                if (keys[K_ESCAPE]):
                    exit()
 
            self.player.update()
            self.genome.fitness += 0.1
 
            # does snake eat apple?
        
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[0], self.player.y[0],44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.player.length = self.player.length + 1   
                self.genome.fitness += self.apple.points
                self.noAppleCount = 0
            else:
                self.noAppleCount += 1
                
            
            for i in range(1,self.player.length):
                if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],20):
                    self.noCollision = False
                    break

            if self.player.x[0] > self.windowWidth or self.player.x[0] < 0 or self.player.y[0] > self.windowHeight or self.player.y[0] < 0:
                break

            output = net.activate(self.inputBoolean())

            #Turn left
            if output[0] >= output[1] and output[0] > output[2]:
                if self.player.direction == 0:
                    self.player.moveUp()
                elif self.player.direction == 1:
                    self.player.moveDown()
                elif self.player.direction == 2:
                    self.player.moveLeft()
                elif self.player.direction == 3:
                    self.player.moveRight()
            #Turn right
            
            if output[2] > output[0] and output[2] >= output[1]:
                if self.player.direction == 0:
                    self.player.moveDown()
                elif self.player.direction == 1:
                    self.player.moveUp()
                elif self.player.direction == 2:
                    self.player.moveRight()
                elif self.player.direction == 3:
                    self.player.moveLeft()
           
            if self.noAppleCount > 100:
                self.genome.fitness -= 100
                break
            
            if self.displayMode:
                self.on_render()
                time.sleep (10.0 / 1000.0)
        self.on_cleanup()

def evaluatePop(genomes, config):
    for genome_id, genome in genomes:
        app = App(genome_id, genome, config, False)
        app.on_execute()
        


def runNeat(config_file):
    # This method differs a bit from the version in the thesis. The changes run the algorithm multiple times to calculate the average generations needed for a succesful worm.

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_file)
    sumGen = 0
    i = 0
    while i <= 200:
        population = neat.Population(config)      
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        winner = population.run(evaluatePop, 200)
        app = App("winner", winner, config, True)         
        app.on_execute()  
        print(population.generation)      
        sumGen += population.generation
        i += 1
    print(sumGen/100) 
    
    app = App("winner", winner, config, True)         
    app.on_execute()  


if __name__ == "__main__" :
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    runNeat(config_path)