import numpy as np
import bpy
import os

class ScalarFieldValue:
    """
        Class: Fetch the scalar value from file
    """

    def __init__(self, filename:str):
        self.filename = filename


    def fetch_data(self):
        """
            Function: fetch data (scalar field) from the file txt

            Returns:
                None
        """

        if self.check_file():
            with open(self.get_current_workfolder()+self.filename, 'r') as f:
                fmap_values = np.array([float(line.strip()) for line in f])

            return fmap_values


    def get_current_workfolder(self) -> str:

        """
            Function : get current work-folder

            Returns:
                str

        """

        return os.getcwd()+'\\'

    def check_file(self):
        """
            Function: check if file exists

            Returns:
                bool
        """

        if os.path.exists(self.get_current_workfolder()+self.filename):
            return True
        else:
            raise ValueError(f"File at chosen path: {self.get_current_workfolder()+self.filename}, does not exists")



    def normalize(self, values, new_min=0.0, new_max=1.0):

        """
            Function: normalize the scalar values in a range

            Args:
                values : values to normalize
                new_min : min value to start normalize
                new_max : max value to start normalize

        """

        old_min = np.min(values)

        old_max = np.max(values)
        normalized = new_min + (values - old_min) * (new_max - new_min) / (old_max - old_min)
        return normalized


    def add_value_to_mesh_vertex(self, obj, fmap_values):

        """
            Function: add scalar value to mesh vertex

            Args:
                obj : obj to which add the values
                fmap_values : array with values to add to the mesh's vertex
        """

        mesh = obj.data

        if 'fmap_values' not in mesh.attributes:
            mesh.attributes.new(name='fmap_values', type='FLOAT', domain='POINT')

        normalized_values = self.normalize(fmap_values, new_min=0.0, new_max=1.0)

        for i, vertex in enumerate(mesh.vertices):
            mesh.attributes['fmap_values'].data[i].value = normalized_values[i]

        return obj

