import numpy as np

class Stem(object):
    def __init__(self, obj,  x, y, z,  fill):
        self.obj = obj
        self.position = np.array([x, y, z])
        self.scale = 1
        self.fill = fill

    def updateStem(self, health):
        self.scale = health
        redRange = int((177-118) * health)
        greenRange = int((212-108) * health)
        blueRange = int((84 - 52) * health)

        self.fill = (118 + redRange, 108+ greenRange, 52 + blueRange)


class Petals(object):
    def __init__(self, obj, x, y, z, fill):
        self.obj = obj
        self.position = np.array([x, y, z])
        self.fill = fill
        self.scale = 1

    def updatePetals(self, health):
        self.scale = health

        redRange = int((255 - 176) * health)
        greenRange = int((236 - 160) * health)
        blueRange = int((118 - 108) * health)

        self.fill = (176 + redRange, 160 + greenRange, 108 + blueRange)


class ThreeDFlower(object):
    def __init__(self, stem, petals):
        self.stem = stem
        self.petals = petals

    def update(self, health):
        self.petals.updatePetals(health)
        self.stem.updateStem(health)





