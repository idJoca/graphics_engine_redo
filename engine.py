from camera import Camera
from model import Model
from light import Light
from errors import *
import numpy as np
import math
import pygame.gfxdraw
from helper import *

class Engine():

    def __init__(self, canvas, camera=None):
        self.width = canvas.get_width()
        self.height = canvas.get_height()
        self.canvas = canvas
        self.aspect_ratio = self.height / self.width
        self.loaded_models = np.zeros(1, dtype=np.object, order='F')
        self.loaded_models_dict = {}
        self.loaded_lights = np.zeros(1, dtype=np.object, order='F')
        self.loaded_lights_dict = {}
        self.vectorized_draw = np.vectorize(self.draw)
        if (camera is None):
            self.camera = Camera()
        else:
            self.camera = camera
    
    def load_model(self, file_path, identifier):
        """
        Loads model into the loaded_models dict,
        for rendering in the pipeline.
        """
        if identifier in self.loaded_models_dict:
            raise NonUniqueIdentifierError
        model = Model.load_model_from_file(file_path)
        if not (self.loaded_models.any()):
            self.loaded_models[0] = model
        else:
            self.loaded_models = np.append(self.loaded_models, model)
        self.loaded_models_dict[identifier] = self.loaded_models.size - 1

    def load_light(self, light=None, identifier="main_light"):
        """
        loads a generic light into loaded_lights dict 
        """
        if identifier in self.loaded_lights:
            raise NonUniqueIdentifierError
        if (light is None):
            light = Light()
        else:
            light = light
        if (self.loaded_lights.size == 1):
            self.loaded_lights[0] = light
        else:
            self.loaded_lights = np.append(self.loaded_lights, light)
        self.loaded_lights_dict[identifier] = self.loaded_lights.size - 1

    def translate(self, identifier, translation_vector, model=True):
        """
        Translate the model, by the amount encoded at the translation_vector.
        The following matrix is used:
        1   0   0   trans.x
        0   1   0   trans.y
        0   0   1   trans.z
        0   0   0   1
        """
        if (model is True):
            translation_vector = np.array(translation_vector, dtype=float, order='F')
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            model.transform_mat = np.dot(model.transform_mat, translate_mat(translation_vector))
    
    def scale(self, identifier, scaling_vector, model=True):
        """
        Scale the model, by the amount encoded at the scaling_vector.
        The following matrix is used:
        scale.x   0   0   0
        0   scale.y   0   0
        0   0   scale.z   0
        0   0   0   1
        """
        if (model is True):
            scaling_vector = np.array(scaling_vector, dtype=float, order='F')
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            if not(scaling_vector.any()):
                raise InvalidVectorError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            model.transform_mat = np.dot(model.transform_mat, scale_mat(scaling_vector))

    def rotate_any(self, identifier, axis, angle, axis_point=[0, 0, 0], degrees=True, model=True):
        """
        Rotate the model, at axis by the angle.
        If degrees is true, the angle is assumed to be in degrees and
        will be converted to radians
        """
        if (model is True):
            axis = np.array(axis, dtype=float, order='F')
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            if not(axis.any()):
                raise InvalidVectorError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            model.transform_mat = np.dot(model.transform_mat, rotation_any_axis(axis, angle, axis_point, degrees))
    
    def rotate_x(self, identifier, angle, degrees=True, row_order=False, model=True):
        """
        Rotate the model, at the x axis by the angle.
        If degrees is true, the angle is assumed to be in degrees and
        will be converted to radians
        """
        if (model is True):
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            if (row_order is True):
                model.transform_mat = np.dot(model.transform_mat, np.linalg.inv(rotate_matrix_x(angle, degrees)))
            else:
                model.transform_mat = np.dot(model.transform_mat, rotate_matrix_x(angle, degrees))


    def rotate_y(self, identifier, angle, degrees=True, row_order=False, model=True):
        """
        Rotate the model, at the y axis by the angle.
        If degrees is true, the angle is assumed to be in degrees and
        will be converted to radians
        """
        if (model is True):
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            if (row_order is True):
                model.transform_mat = np.dot(model.transform_mat, np.linalg.inv(rotate_matrix_y(angle, degrees)))
            else:
                model.transform_mat = np.dot(model.transform_mat, rotate_matrix_y(angle, degrees))
    
    def rotate_z(self, identifier, angle, degrees=True, row_order=False, model=True):
        """
        Rotate the model, at the z axis by the angle.
        If degrees is true, the angle is assumed to be in degrees and
        will be converted to radians
        """
        if (model is True):
            if not(identifier in self.loaded_models_dict):
                raise InexistentIdentifierError
            index = self.loaded_models_dict[identifier]
            model = self.loaded_models[index]
            if (row_order is True):
                model.transform_mat = np.dot(model.transform_mat, np.linalg.inv(rotate_matrix_z(angle, degrees)))
            else:
                model.transform_mat = np.dot(model.transform_mat, rotate_matrix_z(angle, degrees))

    def draw_triangles(self, faces, intensity):
        for vertices in faces:
            shadow = (255 * -intensity[self.index])
            shadow = shadow if shadow > 0 else 0
            shadow = shadow if shadow < 255 else 255
            pygame.gfxdraw.aapolygon(self.canvas,
                                     vertices,
                                     (shadow,
                                      shadow,
                                      shadow))
            pygame.gfxdraw.filled_polygon(self.canvas,
                                     vertices,
                                     (shadow,
                                      shadow,
                                      shadow))
            self.index += 1

    def draw(self, model):
        """
        Projects the model into raster space,
        calculates the lights intensity on the model,
        draw the mesh and resets the transform_mat of the model
        """
        view_projection_model_mat = np.dot(model.transform_mat.T, self.view_projection_mat)
        projection(view_projection_model_mat, model)
        normals = compute_normals(model)
        view_port(model, self.width, self.height)
        points = model.transformed_faces[:, :, 0:2]
        points = points.reshape(-1, 3, 2)
        if (self.loaded_lights.size == 0):
            raise NoLightsLoadedError
        lights = self.loaded_lights
        dist = np.linalg.norm([light.pos for light in lights] - normals, axis=1)
        intensity = np.dot([light.direction for light in lights], normals.T).reshape(-1)
        intensity *= [light.light_intensity for light in lights]
        intensity /= (dist) ** 0.5 + 0.1
        self.index = 0
        self.draw_triangles(points, intensity)
        model.transform_mat = np.identity(4, dtype=float)

    def render(self):
        """ 
        Renders the whole scene. The view_projection_mat is the same
        to all models. Therefore, it's computed only once, per loop.
        """
        projection_mat = get_projection_mat(self.aspect_ratio, self.camera)
        view_mat = self.camera.camera_matrix()
        view_mat = np.linalg.inv(view_mat)
        self.view_projection_mat = np.dot(projection_mat, view_mat)
        [self.draw(model) for model in self.loaded_models]
