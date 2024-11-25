import numpy as np
import bpy
import os

class ScalarFieldValue:
    """
        Class: Fetch the scalar value from file
    """

    def __init__(self, filename_scalar:str, filename_labels:str):
        self.filename_scalar = filename_scalar
        self.filename_labels = filename_labels


    def fetch_data_scalar(self):
        """
            Function: fetch data (scalar field) from the file txt

            Returns:
                None
        """

        if self.check_file_scalar():
            with open(self.get_current_workfolder()+self.filename_scalar, 'r') as f:
                fmap_values = np.array([float(line.strip()) for line in f])

            return fmap_values


    def fetch_data_labels(self):
        """
            Function: fetch data (labels) from the file txt

            Returns:
                None
        """

        if self.check_file_labels():
            with open(self.get_current_workfolder()+self.filename_labels, 'r') as f:
                fmap_values = np.array([int(line.strip()) for line in f])

            return fmap_values


    def get_current_workfolder(self) -> str:

        """
            Function : get current work-folder

            Returns:
                str

        """

        return os.getcwd()+'\\'


    def check_file_scalar(self):
        """
            Function: check if file exists

            Returns:
                bool
        """

        if os.path.exists(self.get_current_workfolder()+self.filename_scalar):
            return True
        else:
            raise ValueError(f"File at chosen path: "
                             f"{self.get_current_workfolder()+self.filename_scalar}, does not exists")


    def check_file_labels(self):
        """
            Function: check if file exists

            Returns:
                bool
        """

        if os.path.exists(self.get_current_workfolder()+self.filename_labels):
            return True
        else:
            raise ValueError(f"File at chosen path: "
                             f"{self.get_current_workfolder()+self.filename_labels}, does not exists")


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


    def add_value_to_mesh_vertex(self, obj, fmap_values, labels_values):

        """
            Function: add scalar value to mesh vertex

            Args:
                obj : obj to which add the values
                fmap_values : array with values to add to the mesh's vertex
                labels_values : array with values to add to the mesh's vertex
        """

        mesh = obj.data

        if 'fmap_values' not in mesh.attributes:
            mesh.attributes.new(name='fmap_values', type='FLOAT', domain='POINT')

        if 'labels_values' not in mesh.attributes:
            mesh.attributes.new(name='labels_values', type='FLOAT', domain='POINT')

        if 'col' not in mesh.vertex_colors:
            mesh.vertex_colors.new(name='col')

        normalized_values_scalar = self.normalize(fmap_values, new_min=0.0, new_max=1.0)
        #normalized_values_scalar = (fmap_values - np.min(fmap_values)) / (np.max(fmap_values) - np.min(fmap_values))
        normalized_values_labels = self.normalize(labels_values, new_min=0.0, new_max=1.0)

        color_layer = mesh.vertex_colors['col'].data

        vertex_colors = {}

        for i, vertex in enumerate(mesh.vertices):
            mesh.attributes['fmap_values'].data[i].value = normalized_values_scalar[i]
            mesh.attributes['labels_values'].data[i].value = normalized_values_labels[i]

            color_value = normalized_values_scalar[i]
            color = (color_value, color_value, color_value, 1.0)

            vertex_colors[vertex.index] = color

        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                loop_vertex_index = mesh.loops[loop_index].vertex_index
                color_layer[loop_index].color = vertex_colors[loop_vertex_index]



        return obj

