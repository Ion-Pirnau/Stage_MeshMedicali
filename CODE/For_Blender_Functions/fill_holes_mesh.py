import bpy

class FillHoles:

    """
        Class: For filling holes on mesh in Blender

    """

    def __init__(self, obj_name):
        self.obj_name = obj_name


    def fill_holes(self):
        """
            Function: fill the holes in mesh

        """

        obj = self.get_obj_from_context(self.obj_name)
        self.fill_mesh_obj(obj)
        self.actual_fill_holes(obj)



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


    def actual_fill_holes(self, obj):
        """
            Function: fill holes in mesh mode 2-triangulation

            Args:
                obj : obj that has to get holes filled
        """

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_non_manifold()

        if len([e for e in bpy.context.object.data.edges if e.select]) > 0:
            bpy.ops.mesh.fill(use_beauty=True)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()


    def fill_mesh_obj(self, obj):
        """
            Function: fill holes in mesh mode 1 - fill region

            Args:
                obj : obj that has to get holes filled
        """

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_non_manifold()

        if len([e for e in bpy.context.object.data.edges if e.select]) > 0:
            bpy.ops.mesh.fill_holes(sides=0)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.update()

    def get_message(self):
        return "\nIn Blender Function: All Holes Filled Applied\n\n"