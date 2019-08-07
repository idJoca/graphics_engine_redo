import numpy as np
import math

class Camera():

    def __init__(self, fov=90, z_near=0.1, z_far=100,
                 pos=[0, 0, -1], left=[1, 0, 0], up=[0, 1, 0], forward=[0, 0, -1]):
        """
        Camera's class
        """
        self.fov = math.radians(fov)
        self.z_near = z_near
        self.z_far = z_far
        self.pos = np.array(pos, dtype=float, order='F')
        self.left = np.array(left, dtype=float, order='F')
        self.up = np.array(up, dtype=float, order='F')
        self.forward = np.array(forward, dtype=float, order='F')

    def camera_matrix(self):
        camera_matrix = np.identity(4, dtype=float)
        camera_matrix[:3, 0] = self.left[:]
        camera_matrix[:3, 1] = self.up[:]
        camera_matrix[:3, 2] = self.forward[:]
        camera_matrix[:3, 3] = self.pos[:]
        return camera_matrix
    
    def translate(self):
        pass
    
    def rotate_x(self):
        """
        Rotate around the X axis in the camera
        coordinate system
        """
        pass
    
    def rotate_y(self):
        """
        Rotate around the Y axis in the camera
        coordinate system
        """
        pass
    
    def rotate_z(self):
        """
        Rotate around the Z axis in the camera
        coordinate system
        """
        pass