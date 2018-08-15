import sys, pygame, math
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ThreeDflower import *
from TwoDFlower import *
from objectloader import *
import plantHealth
import numpy as np

#Class that handles and stores properties of the two representations
class Environment(object):
    def __init__(self, threeD, twoD, curMode):
        self.threeD = threeD
        self.twoD = twoD
        self.curMode = curMode
        self.water = 0.5
        self.temp = 18
        self.UV = 1
        self.health = 10

    def switchMode(self, environment, curMode):
        if(curMode == 2):
            TwoDAnimation(environment)
        else:
            ThreeDAmination(environment)

    def healthUpdate(self, x, y):
        change = False
        if(610 <= y <= 640):
            if(130<=x<160 and 0<=self.water):
                self.water = self.water + 0.1
                change = True
            elif(220 <= x <= 250):
                self.water = self.water - 0.1
                change = True

            elif (270 <= x <= 300 and self.UV <= 12):
                self.UV += 1
                change = True

            elif (380 <= x <= 410 and 1 <= self.UV):
                self.UV -= 1
                change = True

            elif (430 <= x <= 460):
                self.temp += 1
                change = True

            elif (510 <= x <= 540):
                self.temp -= 1
                change = True

        if(change):
            health = plantHealth.mlModel()
            predict = health.predict(np.array([[self.temp, self.UV, self.water]]))
            self.twoD.updateHealth(predict)
            self.threeD.update(predict)
            self.health = math.ceil(predict*10)

    def drawThreeD(self, rx, ry, tx, ty, obj):
        zpos = 10
        flower = self.threeD
        glPushMatrix()
        glTranslate(tx / 20., ty / 20., -zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)

        glScale(1.5*flower.petals.scale, 1.5*flower.petals.scale, 1)
        glColor3f(flower.petals.fill[0] / 255, flower.petals.fill[1] / 255, flower.petals.fill[2] / 255)
        glCallList(flower.petals.obj.gl_list)
        glColor3f(220 / 255, 0 / 255, 220 / 255)
        glCallList(obj.gl_list)
        glPopMatrix()

        glPushMatrix()
        glTranslate(tx / 20., ty / 20., -zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)

        glScale(1, 1, flower.stem.scale)
        glColor3f(flower.stem.fill[0] / 255, flower.stem.fill[1] / 255, flower.stem.fill[2] / 255)
        glCallList(flower.stem.obj.gl_list)

        glPopMatrix()
        drawText([-2, -1.75, 0], "Cell Mode")
        drawText([-2, -2, 0], "Plant Health: " + str(self.health))

    def drawTwoBackground(self, screen, viewport):

        img = pygame.image.load("control-panel.jpg")
        screen.blit(img, (125, viewport[1] - img.get_height()))

        font = pygame.font.SysFont("Moon Flower Bold", 27)
        textSurface = font.render("Water: " + str(round(self.water, 3)), True, (255, 255, 255, 50))
        screen.blit(textSurface, (125, viewport[1] - img.get_height() - 25))

        textSurface = font.render("UV: " + str(self.UV), True, (255, 255, 255, 0))
        screen.blit(textSurface, (275, viewport[1] - img.get_height() - 25))

        textSurface = font.render("Temperature: " + str(self.temp) + " C", True, (255, 255, 255, 50))
        screen.blit(textSurface, (410, viewport[1] - img.get_height() - 25))

        font = pygame.font.SysFont("Moon Flower Bold", 50)
        textSurface = font.render("Plant Health: " + str(self.twoD.health), True, (255, 255, 255, 50))
        screen.blit(textSurface, (235, 10))

        font = pygame.font.SysFont("Moon Flower Bold", 30)
        textSurface = font.render("Plant Mode", True, (0, 0, 0, 50), (255, 255, 255, 50))
        screen.blit(textSurface, (10, 10))

# Function that draws the environment for the Two D Animation
def TwoDAnimation(environment):

    viewport = (700, 700)
    screen = pygame.display.set_mode(viewport)
    screen.fill((0, 0, 0))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    environment.twoD.reset()

                if e.key == K_3:
                    environment.switchMode(environment, 3)
            if e.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if(10 <= x <= 90 and 10 <= y <= 40):
                    environment.switchMode(environment, 3)

                environment.healthUpdate(x, y)

        screen.fill((0, 0, 0))

        for i in range(environment.twoD.health):
            handle = environment.twoD.updateCells()
            handle.join()

        environment.twoD.draw(screen, 100, 25)
        environment.drawTwoBackground(screen, viewport)

        pygame.display.flip()

#Draws the text in 3D mode
def drawText(position, textString):
    font = pygame.font.SysFont("Moon Flower Bold", 30)
    textSurface = font.render(textString, True, (255,255,255,50), (0,0,0,50))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(position[0], position[1], position[2])
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

#Loads background for 3D Mode
def drawBackground(sun,hill):
    glPushMatrix()
    glColor3f(250 / 255, 250 / 255, 0)
    glTranslate(-2, 2, 0)
    glCallList(sun.gl_list)
    glPopMatrix()

    glPushMatrix()
    glColor3f(74/255, 151/255, 0)
    glScale(0.5, 0.3, 0.3)
    glTranslate(0, -4.5, 0)
    glRotate(-90, 1, 0, 0)
    glCallList(hill.gl_list)
    glPopMatrix()

#Draws the flying clouds for the 3D Mode
def drawFlyingClouds(cloud, x, y):
    glPushMatrix()
    glScale(0.4, 0.4, 0.4)
    glColor4f(240 / 255, 245 / 255, 216 / 255, .5)
    glTranslate(x%7 - 3, 3.75, 0)
    glRotate(90, 0, 0, 1)
    glRotate(45, 0, 1, 0)
    glCallList(cloud.gl_list)
    glPopMatrix()

#Intializes lights for OpenGL
def setLights():
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

# Function that draws the environment for of the 3D Animation
def ThreeDAmination(environment):
    viewport = (700,700)

    pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    setLights()

    sun = OBJ("sun.obj", swapyz=True)
    cloud = OBJ("cloud.obj", swapyz=True)
    hillObj = OBJ("hill.obj", swapyz=True)
    middleObj = OBJ("middle.obj", swapyz=True)
    petalObj = OBJ("petals.obj", swapyz=True)
    stemObj = OBJ("stem.obj", swapyz=True)


    glMatrixMode(GL_PROJECTION)
    width, height = viewport
    gluPerspective(45, width/float(height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    cloudX = 0
    cloudY = 2

    rx, ry = (0,-80)
    tx, ty = (0,0)
    rotate = move = False

    while 1:

        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    sys.exit()
                if e.key == K_2:
                    environment.switchMode(environment, 2)

            elif e.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if(15 <= x <= 75 and 615 <= y <= 645):
                    environment.switchMode(environment, 2)
                if e.button == 1: rotate = True
                elif e.button == 3: move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1: rotate = False
                elif e.button == 3: move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(135/255, 206/255, 250/255, 0)
        glLoadIdentity()


        glTranslatef(0, 0, -5)
        glDeleteTextures(3)
        glDisable(GL_TEXTURE_2D)
        drawBackground(sun, hillObj)

        cloudX = cloudX + 0.001
        glDisable(GL_TEXTURE_2D)
        drawFlyingClouds(cloud, cloudX, cloudY)

        glDisable(GL_TEXTURE_2D)
        environment.drawThreeD(rx, ry, tx, ty, middleObj)

        pygame.display.flip()


def main():
    pygame.init()

    viewport = (700, 700)

    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    setLights()

    sun = OBJ("sun.obj", swapyz=True)
    cloud = OBJ("cloud.obj", swapyz=True)
    hillObj = OBJ("hill.obj", swapyz=True)
    middleObj = OBJ("middle.obj", swapyz=True)
    petalObj = OBJ("petals.obj", swapyz=True)
    stemObj = OBJ("stem.obj", swapyz=True)



    petals = Petals(petalObj, 0, 0, 0, (245, 222, 77))
    stem = Stem(stemObj, 0, 0, 0, (177, 212, 84))
    flower = ThreeDFlower(stem, petals)

    cellsManager = Cells(100, 100, 0.0367, 0.0642, 1.0, 1.0)
    for i in range(45, 55):
        for j in range(45, 55):
            cellsManager.cellsB[i][j] = 1

    environment = Environment(flower, cellsManager, 3)

    ThreeDAmination(environment)

main()