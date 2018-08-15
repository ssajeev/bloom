
import pygame, random
import numpy as np
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Firefly class that includes position and velocity of the firefly
class Firefly():
    def __init__(self):
        self.position = np.array([random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5)])
        self.radius = random.uniform(0.1, 0.25)
        self.velocity = np.array([0, 0, 0])
        self.color = (0.27, 0.27, 0.63, 0.5)
        self.timer = 10

    def __eq__(self, other):
        return (self.position[0] == other.position[0]
                and self.position[1] == other.position[1]
                and self.position[2] == other.position[2]
                and self.radius == other.radius
                and self.velocity[0] == other.velocity[0]
                and self.velocity[1] == other.velocity[1]
                and self.velocity[2] == other.velocity[2])

# Class that organizes all fireflies and applies the boid algorithm for flocking
class Fireflies():
    # Empty list of fireflies initially
    def __init__(self):
        self.fireflies = []
        self.fireflyNum = 0
        self.lightUp = []

    # Adds a new firefly to the system
    def addFirefly(self):
        self.fireflies.append(Firefly())
        self.fireflyNum += 1

    def removeFirefly(self):
        self.fireflies.pop()

###### ADDED CODE FOR FIREFLY ASYNCHRONOUS#########
    #Lights up a firefly randomly
    def lightFirefly(self):
        if(len(self.lightUp) > 0.75*len(self.fireflies)):
            return

        lightUpNum = random.randint(0, len(self.fireflies) -1)

        lightUpBug = self.fireflies[lightUpNum]

        lightUpBug.color = (0.90, 0.90, 0.0, 0.06)

        self.lightUp.append(lightUpBug)

    #Unlights up a firefly randomly
    def unlightFirefly(self):
        lightUpNum = 0
        if(len(self.lightUp) == 0):
            return False

        lightUpBug = self.lightUp[0]

        lightUpBug.color = (0.27, 0.27, 0.63, 0.5)

        self.lightUp.pop(lightUpNum)

    # Adds weightage so fireflies are attracted to ones that have light ons
    def followLightUp(self, firefly):
        vec1 = np.array([0.0, 0.0, 0.0])
        for i in range(0, len(self.lightUp)):
            curFirefly = self.lightUp[i]
            if (firefly != curFirefly):
                vec1 = vec1 + curFirefly.position

        vec1 = vec1 / (len(self.lightUp) + 1)
        return (vec1 - firefly.position) / 300


    # Boid rules based on psuedocode from http://www.kfish.org/boids/pseudocode.html

    # Fly to center of mass
    def rule1(self, firefly):

        vec1 = np.array([0.0, 0.0, 0.0])
        for i in range(0, self.fireflyNum):
            curFirefly = self.fireflies[i]
            if(firefly != curFirefly):
                vec1 = vec1 + curFirefly.position

        vec1 = vec1 / (self.fireflyNum-1)
        return (vec1 - firefly.position) / 10000

    # Prevent Collisions, have small distance
    def rule2(self, firefly):

        c = np.array([0,0,0])
        for i in range(0, self.fireflyNum):
            curFirefly = self.fireflies[i]
            if( np.linalg.norm(curFirefly.position - firefly.position) < 1):
                c = c - (curFirefly.position - firefly.position)

        return c

    # Match surrounding boid velocity
    def rule3(self, firefly):

        c = np.array([0,0,0])
        for i in range(0, self.fireflyNum):
            curFirefly = self.fireflies[i]
            if(firefly != curFirefly):
                c = c + curFirefly.velocity

        c = c / (self.fireflyNum - 1)

        return (c- firefly.velocity) / 8

    # Bound boid within window
    def boundPosition(self, firefly):
        xmin, xmax, ymin, ymax, zmin, zmax = -10, 10, -10, 10, -10, 10
        v = np.array([0,0,0])
        if(firefly.position[0] < xmin):
            v[0] = 4
        elif(firefly.position[0] > xmax):
            v[0] = xmin-1
        if(firefly.position[1] < ymin):
            v[1] = ymax-1
        elif(firefly.position[1] > ymax):
            v[1] = ymin-1
        if (firefly.position[2] < zmin):
            v[2] = zmax-1
        elif (firefly.position[2] > zmax):
            v[2] = zmin-1

        return v

    # Attract boid to center
    def gotToCenter(self, firefly):
        center = np.array([0, 0, 0])
        return (center - firefly.position) / 100

    # Apply boid rules to move fireflies
    def moveFireflies(self):

        for i in range(0, self.fireflyNum):
            firefly = self.fireflies[i]
            v1 = self.rule1(firefly)
            v2 = self.rule2(firefly)
            v3 = self.rule3(firefly)
            v4 = self.gotToCenter(firefly)
            v5 = self.followLightUp(firefly)


            firefly.velocity = firefly.velocity + v1 + v2 + v3 + v4 + v5

            firefly.position = firefly.position + firefly.velocity
            v4 = self.boundPosition(firefly)
            firefly.position = firefly.position + v4

    # Draws the fireflies as ellipses
    def drawFireflies(self, color):

        for i in range(0, self.fireflyNum):
            firefly = self.fireflies[i]

            glPushMatrix()

            glTranslatef(firefly.position[0], firefly.position[1], firefly.position[2])
            radius = firefly.radius
            numSlices = 32
            numStacks = 8
            pQuadric = gluNewQuadric(GL_SMOOTH)
            glDisable(GL_BLEND)
            glColor4f(firefly.color[0], firefly.color[1], firefly.color[2], firefly.color[3])
            glScalef(0.9, 0.25, 0.7)
            gluSphere(pQuadric, radius, numSlices, numStacks)
            glPopMatrix()

def main():
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.time.set_timer(USEREVENT + 1, 500)
    pygame.time.set_timer(USEREVENT + 3, 1000)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)


    glTranslatef(0, 0, -17)

    count = 0
    offColor = (0.27, 0.27, 0.63, 0.5)
    onColor = (0.90, 0.90, 0.0, 0.06)
    color = onColor

    fireflyCollector = Fireflies()

    for i in range(0, 2):
        fireflyCollector.addFirefly()

    fireflyCollector.lightFirefly()

    while True:
        for event in pygame.event.get():
            if event.type == USEREVENT + 1:
                fireflyCollector.lightFirefly()
            if event.type == USEREVENT + 3:
                fireflyCollector.unlightFirefly()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fireflyCollector.addFirefly()
                if event.key == pygame.K_RIGHT:
                    fireflyCollector.lightFirefly()
                if event.key == pygame.K_LEFT:
                    fireflyCollector.unlightFirefly()



        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(0.098, 0.098, 0.439, 0)

        fireflyCollector.drawFireflies(color)
        fireflyCollector.moveFireflies()


        pygame.display.flip()
        pygame.time.wait(100)

main()