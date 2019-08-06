import numpy as np
import helper

class Light():

    def __init__(self, direction=[0, -1, 0], pos=[1, 0, 0], color=(255, 255, 255), light_intensity=1):
        """
        Light's class
        """
        self.direction = np.array(direction, dtype=float, order='F')
        self.pos = np.array(pos, dtype=float, order='F')
        self.light_intensity = light_intensity
        self.color = color