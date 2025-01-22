import numpy as np
import bpy
from CODE.FunzioniUtili import utils as utl
from CODE.FunzioniUtili.utils import is_array_empty


class DeformMesh:
    """
        Class: contains the methods for deform the mesh
    """

    def __init__(self, obj_name:str="", median_coordinate=[], scale_uv_sphere:float=0.1,
                 min_value:float=-1.0, max_value:float=1.0, number_deformation:int=1):
        self.obj_name = obj_name
        self.median_coordinate = median_coordinate
        self.scale_uv_sphere = scale_uv_sphere
        self.min_value = min_value
        self.max_value = max_value
        self.log_message = ""
        self.number_deformation = number_deformation


    def apply_deformation(self):
        """
            Function: use to apply deformation on mesh

            Args:
                mesh_name : name of the mesh
                median_coordinate : coordinates to which apply the deformation
        """

        uv_sphere_name = 'My_UV'

        obj = self.get_obj_from_context(self.obj_name)

        self.remove_uv_sphere(uv_sphere_name)

        target_sphere = self.create_uv_sphere(uv_sphere_name, self.scale_uv_sphere)

        face_index = []
        if not utl.is_array_empty(self.median_coordinate) and self.number_deformation == 0:
            for coordinate in self.median_coordinate:
                face_index.append(self.select_face_by_medians(obj, coordinate))
                bpy.ops.object.mode_set(mode='OBJECT')
        elif self.number_deformation > 0:
            for i in range(self.number_deformation):
                index = self.select_face_on_mesh(obj)
                face_index.append(index)
                bpy.ops.object.mode_set(mode='OBJECT')

        if face_index:
            for index in face_index:
                self.translate_face_within_sphere(obj, target_sphere, index, self.min_value, self.max_value)

        self.remove_uv_sphere(uv_sphere_name)
        self.write_to_log_deformation()



    def get_obj_from_context(self, obj_name:str):
        """
            Function: get the obj, to apply the deformation on

            Args:
                obj_name : obj's name
        """

        obj = bpy.data.objects.get(obj_name)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.select_all(action='DESELECT')
        return obj


    def change_mode(self, obj):
        """
            Function: not used, useful to change the mode in blender Environment
        """

        if obj is not None:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')
            bpy.ops.mesh.select_all(action='DESELECT')


    def select_face_on_mesh(self, obj) -> int:
        """
            Function: used to select random face in a obj

            Args:
                obj : obj to fetch the index face

            Returns:
                int
        """

        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')

        num_faces = len(obj.data.polygons)

        face_index = np.random.choice(num_faces)

        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.polygons[face_index].select = True

        bpy.ops.object.mode_set(mode='EDIT')

        return face_index


    def remove_uv_sphere(self, uv_sphere_name):
        """
            Function: remove an uv-sphere if already exists in the world

            Args:
                uv_sphere_name : name of the uv_sphere
        """
        bpy.ops.object.select_all(action='DESELECT')
        if uv_sphere_name in bpy.data.objects:
            uv_sphere = bpy.data.objects.get(uv_sphere_name)
            bpy.context.view_layer.objects.active = uv_sphere
            uv_sphere.select_set(True)
            bpy.ops.object.delete()


    def create_uv_sphere(self, uv_sphere_name:str, scale_factor:float):
        """
            Function: create an uv-sphere

            Args:
                uv_sphere_name: name of the uv_sphere
                scale_factor : scale value to apply to the uv-sphere

        """

        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))

        uv_sphere = bpy.context.object
        uv_sphere.name = uv_sphere_name

        uv_sphere.scale = (scale_factor, scale_factor, scale_factor)

        bpy.ops.object.transform_apply(scale=True)

        return uv_sphere


    def translate_face_within_sphere(self, obj, target_sphere, face_index:int, min_limit:float, max_limit:float):
        """
            Function: move the face chosen in a limited space

            Args:
                obj: obj to which apply the deformation
                target_sphere: uv-sphere for deform
                face_index: index of face where apply the deformation
                min_limit: limit min for deformation. Default: 0.0
                max_limit: limit max for deformation Default: 0.0

        """

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = obj

        face = obj.data.polygons[face_index]
        vert_coords = [np.array(obj.matrix_world @ obj.data.vertices[vert_index].co) for vert_index in face.vertices]
        face_center = np.mean(vert_coords, axis=0)

        face_normal = np.array(obj.matrix_world.to_3x3() @ face.normal)
        face_normal = face_normal / np.linalg.norm(face_normal)

        min_limit = min_limit
        max_limit = max_limit

        translation_factor = np.random.uniform(min_limit, max_limit)

        target_sphere.location = face_center
        sphere_radius = max(vert.co.length for vert in target_sphere.data.vertices)

        translation = face_normal * translation_factor * sphere_radius

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.polygons[face_index].select = True
        bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.transform.translate(value=translation, proportional_edit_falloff='SMOOTH',
                                    use_proportional_edit=True, use_proportional_connected=True,
                                    proportional_size=sphere_radius)

        bpy.context.tool_settings.use_proportional_edit = False
        bpy.ops.object.mode_set(mode='OBJECT')


    def select_face_by_medians(self, obj, medians) -> int:
        """
            Function: select face-index by medians coordinates

            Args:
                obj: fetch the face's index
                medians: array's coordinates

            Returns:
                int
        """

        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='OBJECT')

        chosen_mean_values = np.array(medians)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')

        num_faces = len(obj.data.polygons)
        face_index = 0
        for f_index in range(num_faces):
            face = obj.data.polygons[f_index]
            #vert_coords = [np.array(obj.matrix_world @ obj.data.vertices[vert_index].co) for vert_index in
            #              face.vertices]
            vert_coords = [obj.data.vertices[vert_index].co for vert_index in face.vertices]
            face_center = np.mean(vert_coords, axis=0)

            if np.allclose(face_center, chosen_mean_values):
                face_index = f_index
                break

        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.polygons[face_index].select = True

        bpy.ops.object.mode_set(mode='EDIT')

        return face_index


    def write_to_log_deformation(self) -> None:
        """
            Function: write on log message deformation info

            Returns:
                None
        """

        deformation_random = 0 if self.number_deformation == 0 else self.number_deformation
        median_coord = [] if self.number_deformation > 0 else self.median_coordinate
        self.log_message = (f"Applied Deformation on mesh: {self.obj_name}")
        self.log_message += (f"Details:\n"
                            f"UV-SPHERE scale: {self.scale_uv_sphere}\n"
                            f"Range value (Min-Max): From {self.min_value} to {self.max_value}\n"
                            f"Random Deformation: {deformation_random}\n"
                            f"Coordinates Deform applied: {median_coord}\n\n")


    def get_message_deform(self) -> str:
        """
            Function: return the message

            Returns:
                str
        """

        return self.log_message