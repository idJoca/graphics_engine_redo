import numpy as np
import helper
import math

class Camera():

    def __init__(self, fov=90, z_near=0.1, z_far=1000,
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
        self.transformations = np.identity(4, dtype=float)

    def camera_matrix(self):
        camera_matrix = np.identity(4, dtype=float)
        camera_matrix[:3, 0] = self.left[:]
        camera_matrix[:3, 1] = self.up[:]
        camera_matrix[:3, 2] = self.forward[:]
        camera_matrix[:3, 3] = self.pos[:]
        camera_matrix = np.dot(camera_matrix, self.transformations)
        return camera_matrix
    
    def translate(self, amount_array):
        """
        Translate the camera in world space
        """
        x = amount_array[0] * self.left[0] + amount_array[1] * self.up[0] + amount_array[2] * self.forward[0]
        y = amount_array[0] * self.left[1] + amount_array[1] * self.up[1] + amount_array[2] * self.forward[1]
        z = amount_array[0] * self.left[2] + amount_array[1] * self.up[2] + amount_array[2] * self.forward[2]
        self.pos += [x, y, z]
    
    def rotate_x(self, angle, degrees=True):
        """
        Rotate around the X axis in the camera
        coordinate system
        """
        if (degrees is True):
            angle = math.radians(angle)
        self.forward = -math.sin(angle) * self.up + math.cos(angle) * self.forward
        self.forward = helper.normalized(self.forward)
        self.up = np.cross(self.forward, self.left)
        self.up = helper.normalized(self.up)
    
    def rotate_y(self, angle, degrees=True):
        """
        Rotate around the Y axis in the camera
        coordinate system
        """
        if (degrees is True):
            angle = math.radians(angle)
        self.forward = math.sin(angle) * self.left + math.cos(angle) * self.forward
        self.forward = helper.normalized(self.forward)
        self.left = np.cross(self.up, self.forward)
        self.left = helper.normalized(self.left)

    def rotate_z(self):
        """
        Rotate around the Z axis in the camera
        coordinate system
        """
        pass

    def rotate(self, yaw, pitch, degrees=True):
        rotation_mat_y = helper.rotate_matrix_y(yaw, degrees)
        rotation_mat_x = helper.rotate_matrix_y(pitch, degrees)
        rotation_mat = np.dot(rotation_mat_x, rotation_mat_y)
        self.transformations = rotation_mat

    def rotate_around_mouse(self, pitch, yaw, degrees=True):
        if (degrees is True):
            angle = math.radians(angle)
        x = math.sin(pitch) * math.cos(yaw)
        y = math.cos(pitch)
        z = -math.cos(pitch) * math.cos(yaw)
        self.forward = helper.normalized([x, y, z])