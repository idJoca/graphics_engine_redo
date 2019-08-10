import numpy as np
import helper

class Light():

    def __init__(self, **kwargs):
        """
        Light's class
        """
        
        self.type = kwargs['type']
        self.color = kwargs['color']
        self.intensity = kwargs['intensity']
        if (self.type == 'ambient'):
            pass
        elif (self.type == 'directional'):
            self.direction = helper.normalized(kwargs['direction'])
        elif (self.type == 'point'):
            self.position = np.array(kwargs['position'])
            self.attenuation = kwargs['attenuation']
        elif (self.type == 'specular'):
            self.direction = helper.normalized(kwargs['direction'])
            self.strength = kwargs['strength']

    def apply_lightning(self, engine, model, normals):
        if (self.type == 'ambient'):
            ambient_light = np.multiply(self.color, self.intensity)
            return np.resize(ambient_light, (normals.shape[0], 3))
        elif (self.type == 'directional'):
            diffuse_light = self.intensity * (np.dot(-normals, self.direction))
            diffuse_light = diffuse_light[:, None] * self.color
            return np.clip(diffuse_light, 0, 255)
        elif (self.type == 'point'):
            pass
        elif (self.type == 'specular'):
            spec = np.dot(normals, engine.camera.forward)
            scattering = np.dot(normals, self.direction)
            specular_intensity = 2 * scattering * ((spec + 1) ** self.strength) * -self.intensity
            specular_light = specular_intensity[:, None] * self.color
            return specular_light