import numpy as np
import helper

class Light():

    def __init__(self, direction=[-1, -1, -1], pos=[0, 0, 1], color=(255, 255, 255), light_intensity=0.9):
        """
        Light's class
        """
        self.direction = helper.normalized(direction)
        self.pos = np.array(pos)
        self.light_intensity = light_intensity
        self.color = color