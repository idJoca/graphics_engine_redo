import numpy as np


class Model():

    def __init__(self, faces):
        """
        Model's class
        """
        self.faces = np.array(faces, dtype=float, order='F')
        self.transformed_faces = np.zeros_like(self.faces, order='F')
        self.transform_mat = np.identity(4, dtype=float)
        self.color = [255, 255, 255]
    
    def load_model_from_file(file_path):
        """
        Load a model's faces and vertices into memory
        Then, returns a Model object with the given faces
        """
        with open(file_path, "rb") as model_file:
            model_data_lines = model_file.readlines()
        if (model_data_lines == ""):
            raise ValueError("Invalid Model File!")
        model_data_lines = [line.decode("utf-8") for line in model_data_lines]
        def strip_line(line):
            line = [piece for piece in line.strip().split(" ")]
            return line
        faces_index = []
        vertices = []
        for line in model_data_lines:
            striped_line = strip_line(line)
            if (striped_line[0] == "v"):        
                vertex = striped_line[1:]
                vertex.append(1)
                vertices.append(vertex)
                continue
            elif (striped_line[0] == "f"):
                face = striped_line[1:]
                faces_index.append(striped_line[1:])
        faces = []
        vertices = np.array(vertices, dtype=float)
        for indexes in faces_index:
            points = []
            for index in indexes:
                point = (vertices[int(index) - 1])
                points.append(point)
            face = points
            faces.append(face)
        return Model(faces)