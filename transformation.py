import numpy as np
import math

 
class Transformation():

    def __init__(self):
        pass
    
    def base_transform():
        """
        Returns the base of a transform
        """
        return np.identity(4, dtype=float)

    def translate(self, engine, amount_array):
        """
        Creates a translation matrix and sends it to the engine queue.
        The amount_array follows the (dx, dy, dz) order.
        """
        # Gets a base transform matrix
        translated_mat = Transformation.base_transform()
        # Sets the last column, up to the 3º row, with the amount_array
        translated_mat[:3, 3] = amount_array[:]
        # Queues the transformation TODO
        # engine.queue_transformation(translated_mat)

    def scale(self, engine, amount_array):
        """
        Creates a scaling matrix and sends it to the engine queue.
        The amount_array follows the (dx, dy, dz) order.
        """
        # Gets a base transform matrix
        scaled_mat = Transformation.base_transform()
        # Assembles the indices to a 3x3 matrix diagonals
        row, col = np.diag_indices(3)
        # Sets the scaled_mat diagonals, from the assembled indices,
        # with the values from amount_array
        scaled_mat[row, col] = amount_array[:]
        # Queues the transformation TODO
        # engine.queue_transformation(translated_mat)

    def rotate_x(self, engine, angle, degrees=True):
        """
        Creates a rotation around the X axis matrix
        and sends it to the engine queue.
        By default, 'angle' is in degrees and will be converted
        to radians. If you desire to send your angle in radians,
        set 'degrees' to False
        """
        # Converts angle to radians
        if (degrees is True):
            angle = math.radians(angle)
        # Gets a base transform matrix
        x_rotated_mat = Transformation.base_transform()

        angle_cos = math.cos(angle)
        angle_sin = math.sin(angle)
        # X rotation template:
        # 1     0       0       1
        #      nv   
        x_rotated_mat[1, 1:3] = angle_cos
        x_rotated_mat[1, 2] = -angle_sin
        x_rotated_mat[2, 1] = angle_sin
        # Queues the transformation TODO
        # engine.queue_transformation(translated_mat)