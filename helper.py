import numpy as np
import math

def get_projection_mat(aspect_ratio, camera):
    fov = camera.fov
    z_near = camera.z_near
    z_far = camera.z_far
    top = math.tan(fov * 0.5) * z_near
    bottom = -top
    right = top * aspect_ratio
    left = -right
    projection_mat = np.identity(4, dtype=float)
    projection_mat[0, 0] = 2 * z_near / (right - left)
    projection_mat[0, 2] = (right + left) / (right - left)
    projection_mat[1, 1] = 2 * z_near / (top - bottom)
    projection_mat[1, 2] = (top + bottom) / (top - bottom)
    projection_mat[2, 2] = -(z_far + z_near) / (z_far - z_near)
    projection_mat[2, 3] = -2 * z_far * z_near / (z_far - z_near)
    projection_mat[3, 2] = -1
    projection_mat[3, 3] = 0
    return projection_mat

def compute_normals(model):
        """
        Compute the cross product between the face's vectors
        The cross product results in a perpendicular vector to both,
        the normal vector.
        Then a dot product results in a rating of similaritie,
        between the normal vector and the facing direction along the Z axis.
        If more than 0, the face is "facing" the camera and need to be drawn,
        otherwise, it's descarted.
        """
        sorting = (model.transformed_faces[:, 0, 2] +
                   model.transformed_faces[:, 1, 2] +
                   model.transformed_faces[:, 2, 2]) / 3
        sorted_keys = np.argsort(sorting)
        model.transformed_faces = model.transformed_faces[sorted_keys]
        vector_a = (model.transformed_faces[:, 1, :3] -
                    model.transformed_faces[:, 0, :3])
        vector_b = (model.transformed_faces[:, 2, :3] -
                    model.transformed_faces[:, 0, :3])
        normal = np.cross(vector_a, vector_b)
        normal = normalized(normal)
        x = np.multiply(normal, model.transformed_faces[:, 0, :3]).sum(1)
        mask = x > 0
        model.transformed_faces = model.transformed_faces[mask]
        return normal[mask]

def projection(view_projection_model_mat, model):
    projected_faces = np.dot(model.faces, view_projection_model_mat)
    clipped_faces = clip(projected_faces)
    normalized_faces = (clipped_faces /
                      np.where(clipped_faces[:, :, 3, None] != 0,
                      clipped_faces[:, :, 3, None], 1))
    model.transformed_faces = normalized_faces

def view_port(model, width, height):
    model.transformed_faces[:, :, 0] += 1
    model.transformed_faces[:, :, 1] += 1
    model.transformed_faces[:, :, 0] *= (width - 1) * 0.5
    model.transformed_faces[:, :, 1] *= (height - 1) * 0.5

def base_transform():
    """
    Returns the base of a transform
    """
    return np.identity(4, dtype=float)

def translate_mat(amount_array):
    # Gets a base transform matrix
    translated_mat = base_transform()
    # Sets the last column, up to the 3º row, with the amount_array
    translated_mat[:3, 3] = amount_array[:]
    return translated_mat

def scale_mat(amount_array):
    # Gets a base transform matrix
    scaled_mat = base_transform()
    # Assembles the indices to a 3x3 matrix diagonals
    row, col = np.diag_indices(3)
    # Sets the scaled_mat diagonals, from the assembled indices,
    # with the values from amount_array
    scaled_mat[row, col] = amount_array[:]
    return scaled_mat

def rotate_matrix_x(angle, degrees):
    if (degrees is True):
        angle = math.radians(angle)
    rotation_matrix = np.identity(4, dtype=float)
    angle_cos = math.cos(angle)
    angle_sin = math.sin(angle)
    rotation_matrix[1][1] = angle_cos
    rotation_matrix[1][2] = -angle_sin
    rotation_matrix[2][1] = angle_sin
    rotation_matrix[2][2] = angle_cos
    return rotation_matrix

def rotate_matrix_y(angle, degrees):
    if (degrees is True):
        angle = math.radians(angle)
    rotation_matrix = np.identity(4, dtype=float)    
    angle_cos = math.cos(angle)
    angle_sin = math.sin(angle)
    rotation_matrix[0][0] = angle_cos
    rotation_matrix[0][2] = angle_sin
    rotation_matrix[2][0] = -angle_sin
    rotation_matrix[2][2] = angle_cos
    return rotation_matrix

def rotate_matrix_z(angle, degrees):
    if (degrees is True):
        angle = math.radians(angle)
    rotation_matrix = np.identity(4, dtype=float)
    angle_cos = math.cos(angle)
    angle_sin = math.sin(angle)
    rotation_matrix[0][0] = angle_cos
    rotation_matrix[0][1] = -angle_sin
    rotation_matrix[1][0] = angle_sin
    rotation_matrix[1][1] = angle_cos
    return rotation_matrix

def rotation_any_axis(axis, desired_angle, axis_point, degrees):
    """
    Return a matrix, capable of rotating any point by an arbitrary axis
    axis: The desired axis of rotation

    desired_angle: The angle to rotate by

    axis_point: a point where the axis of rotation passes by,
    if at origin ([0, 0, 0]), no translation is needed

    degrees: if True, the angle is in degrees, and will be converted to radians
    """
    if (degrees is True):
        desired_angle = math.radians(desired_angle)
    axis = np.array(normalized(axis), order="F")
    axis_point = np.array(normalized(axis_point), order="F")
    d = (axis[0] ** 2 + axis[1] ** 2) ** 0.5

    if (d != 0.0):
        txz = np.zeros((4, 4), dtype=float)
        txz[0][0] = axis[0] / d
        txz[0][1] = axis[1] / d
        txz[1][0] = -axis[1] / d
        txz[1][1] = axis[0] / d
        txz[2][2] = 1
        txz[3][3] = 1
        inverse_txz = np.linalg.inv(txz)
    else:
        txz = np.identity(4)
        inverse_txz = txz

    tz = np.zeros((4, 4), dtype=float)
    tz[0][0] = axis[2] / np.linalg.norm(axis)
    tz[0][2] = -d / np.linalg.norm(axis)
    tz[2][0] = d / np.linalg.norm(axis)
    tz[2][2] = axis[2] / np.linalg.norm(axis)
    tz[1][1] = 1
    tz[3][3] = 1
    inverse_tz = np.linalg.inv(tz)

    rotation_z = rotate_matrix_z(desired_angle)

    if (axis_point.any()):
        tp = translate_mat(axis_point * -1)
        inverse_tp = np.linalg.inv(tp)
        final_matrix = np.dot(inverse_tp, inverse_txz)
        final_matrix = np.dot(final_matrix, inverse_tz)
        final_matrix = np.dot(final_matrix, rotation_z)
        final_matrix = np.dot(final_matrix, tz)
        final_matrix = np.dot(final_matrix, txz)
        final_matrix = np.dot(final_matrix, tp)
    else:
        final_matrix = np.dot(inverse_txz, inverse_tz)
        final_matrix = np.dot(final_matrix, rotation_z)
        final_matrix = np.dot(final_matrix, tz)
        final_matrix = np.dot(final_matrix, txz)

    return final_matrix

def clip(projected_faces):
    x = projected_faces[:, :, 0]
    y = projected_faces[:, :, 1]
    z = projected_faces[:, :, 2]
    w = projected_faces[:, :, 3]
    x_inequality = (x >= -w) & (x <= w)
    y_inequality = (y >= -w) & (y <= w)
    z_inequality = (z >= -w) & (z <= w)
    inequality = (x_inequality & y_inequality & z_inequality)
    inside_faces = np.bitwise_and.reduce(~inequality, axis=1)
    return projected_faces

def normalized(a, axis=-1, order=2):
    # Check if column-major alters this
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    normalized = (a / np.expand_dims(l2, axis))
    return normalized[0] if len(normalized) == 1 else normalized