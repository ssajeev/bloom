import numpy as np, pygame
import math, random, sys
import threading
from scipy.ndimage import convolve

#Threading function based on this: https://gist.github.com/awesomebytes/0483e65e0884f05fb95e314c4f2b3db8
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Cell(object):
    def __init__(self):
        self.a = 1
        self.b = 0

class Cells(object):
    def __init__(self, w , h, feed, kill, diffusion, time):
        self.feed = feed
        self.kill = kill
        self.diffusion = diffusion
        self.time = time
        self.health = 10

        self.weight = (
            [[0.05, .2, 0.05],
             [.2, -1, .2],
             [0.05, .2, 0.05]] )

        self.w = w
        self.h = h

        self.cellsA = np.ones((self.w, self.h), dtype="float64")
        self.cellsB = np.zeros((self.w, self.h), dtype="float64")

    #Updates each cell with the new concentrations of both A and B
    #based on equation from http://www.karlsims.com/rd.html
    @threaded
    def updateCells(self):
        curA = self.cellsA
        curB = self.cellsB
        self.cellsA += (convolve(self.cellsA, self.weight) * self.diffusion) - (curA * curB * curB) + (self.feed * (1 - curA))
        self.cellsB += (convolve(self.cellsB, self.weight) * 0.5) + (curA * curB * curB) - ((self.kill + self.feed) * curB)

        np.clip(self.cellsA, 0, 1, out=self.cellsA)
        np.clip(self.cellsB, 0, 1, out=self.cellsB)


    def constrain(self, val, minVal, maxVal):
        if( val < minVal):
            val = minVal
        if (val > maxVal):
            val = maxVal
        return val

    #Draws cells in green
    def draw(self, screen, x, y):
        for i in range(0, self.w):
            for j in range(0, self.h):
                cellA = self.cellsA[i][j]
                cellB = self.cellsB[i][j]
                color = math.floor((cellA-cellB) * 255)
                color = self.constrain(color, 0, 255)
                pygame.draw.rect(screen, (0, 255-color, 0), (x + i*5, y + j*5, 5, 5))

    def updateHealth(self, health):
        self.health = math.ceil(health * 10)
        self.feed = (health * (0.001)) + 0.0350
        self.kill = (health * (0.001)) + 0.0630

    def reset(self):
        self.cellsA = np.ones((self.w, self.h), dtype="float64")
        self.cellsB = np.zeros((self.w, self.h), dtype="float64")

        for i in range(45, 55):
            for j in range(45, 55):
                self.cellsB[i][j] = 1

def main():

    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size)

    a = Cells(100, 100, 0.0367, 0.0642, 1.0, 1.0)

    for i in range(45, 55):
        for j in range(45, 55):
            a.cellsB[i][j] = 1


    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        for i in range(a.health):
            handle = a.updateCells()
            handle.join()

        screen.fill((255, 255, 255))
        a.draw(screen, 100, 50)


        pygame.display.flip()
