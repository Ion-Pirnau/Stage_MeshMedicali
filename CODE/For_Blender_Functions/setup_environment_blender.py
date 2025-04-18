from CODE.For_Blender_Functions.deformation_on_mesh import DeformMesh
from CODE.For_Blender_Functions.fill_holes_mesh import FillHoles
from CODE.Process_Mesh.processing_functions import Processing_Mesh_PoC
from CODE.FunzioniUtili import utils as utl
from CODE.For_Blender_Functions.set_rendering import RenderingSetup
from CODE.For_Blender_Functions.materials_blender import CreationMaterial
from CODE.For_Blender_Functions.fetch_scalarmap_value import ScalarFieldValue as sfv
import bpy
import numpy as np

"""
    Class used to set the blend file for future rendering
    Create an environment with: The main Mesh, Lights, Plane, Camera
"""
class SetEnvironmentBlender:

    output_blend_file = "BLEND_FILE_OUTPUT/"
    output_fileOff_folder = "INPUT_SOURCE/"
    extension = ".blend"
    message_to_log = ""
    render_setup = None
    vertices = None
    normals = None
    faces = None

    energy_settings = {
        'light_front': 100000,
        'light_back': 100000,
        'light_right': 100000,
        'light_left': 100000,
        'light_top': 100000,
        'light_bottom': 100000
    }

    lights_radius_value = {
        'light_front': 0.0,
        'light_back': 0.0,
        'light_right': 0.0,
        'light_left': 0.0,
        'light_top': 0.0,
        'light_bottom': 0.0
    }

    light_names = [
        'light_front',
        'light_back',
        'light_right',
        'light_left',
        'light_top',
        'light_bottom'
    ]


    nome_cubo = 'Cube_Reference'
    nome_axes = 'Axes_to_Camera'
    nome_camera = 'Camera_Main'
    nome_camera_light = 'Light_to_Camera'

    wall_names = ["FrontPlane", "BackPlane", "RightPlane", "LeftPlane"]
    wall_on_off = [
        True,
        True,
        True,
        True
    ]


    # Initialize the Class
    def __init__(self, nome_mesh: str, nome_log_file: str, plane_on_base_size: int,
                 fill_holes: bool) -> None:
        self.nome_mesh = nome_mesh
        self.nome_log_file = nome_log_file
        self.plane_on_base = plane_on_base_size
        self.is_fill_holes = fill_holes

        self.energy_light_at_camera = 100000
        self.size_cube = 187.0
        self.location_cube = (0.0, 0.0, 0.0)
        self.rotation_camera = (0.0, 0.0, 0.0)
        self.rotation_empty_axes = (0.0, 0.0, 0.0)
        self.location_axes = (0.0, 0.0, 0.0)
        self.rotation_empty_cube = (0.0, 0.0, 0.0)
        self.camera_offset_value_from_empty_axes = 72
        self.light_offset_value_from_camera = 0
        self.base_plane_location = None
        self.type_engine = None
        self.type_device = None
        self.n_samples = None
        self.file_format = None
        self.screen_percentage = None
        self.my_setup_render = None
        self.nome_file_blend = None
        self.mat_chosen = None

        self.sun_strength = None
        self.sun_angle = None
        self.sun_light_name = None
        self.sun_color = None
        self.sun_location = None
        self.sun_rotation = None
        self.scalar_field = None

        self.is_scalar_active = False
        self.is_deformation_active = False
        self.deformation_on_mesh = None
        self.median_coordinate = None
        self.number_deformation = 1
        self.min_value_d = None
        self.max_value_d = None
        self.uv_scale_factor = None
        self.deform_message = None
        self.fillholes = None

        self.light_energy_radius_at_camera = 0.0
        self.lights_radius = []

        self.floor_transparency = False
        self.film_transparency = False
        self.camera_type = ""
        self.lens_camera = 0.0
        self.ortho_scale = 0.0
        self.set_light_mode = 0
        self.mesh_location = (0.0, 0.0, 0.0)
        self.mesh_rotation = (0.0, 0.0, 0.0)



    def change_energy_light(self, 
                            light_front=100000, light_back=100000, 
                            light_right=100000, light_left=100000, 
                            light_top=100000, light_bottom=100000,
                            lights_radius=[],
                            light_set=0) -> None:
        """
        Update energy light settings either with custom values or selecting a predefined set.

        Parameters:
            light_front (float): Custom value for the front-light.
            light_back (float): Custom value for the back-light.
            light_right (float): Custom value for the right-light.
            light_left (float): Custom value for the left-light.
            light_top (float): Custom value for the top-light.
            light_bottom (float): Custom value for the bottom-light.
            lights_radius (List of float): value for lights radius, define the edge's smoothness of the light
            light_set (int): Predefined light set mode (0 for custom).


        Predefined_sets:
                    0 - Customized by the User
                    1 - Film Lighting Scenario
                    2 - ShowRoom Lighting Scenario
                    3 - Black Lighting Scenario, useful for Surface with Emission Lighting

        """

        predefined_sets = {
            0: {  # 
                "light_front": light_front, "light_back": light_back,
                "light_right": light_right, "light_left": light_left,
                "light_top": light_top, "light_bottom": light_bottom
            },
            1: {  # 
                "light_front": 3.5, "light_back": 3.5,
                "light_right": 4.5, "light_left": 4.5,
                "light_top": 15, "light_bottom": 0
            },
            2: {  # 
                "light_front": 2.5, "light_back": 2.5,
                "light_right": 2.5, "light_left": 2.5,
                "light_top": 10, "light_bottom": 0
            },
            3: {  # 
                "light_front": 0, "light_back": 0,
                "light_right": 0, "light_left": 0,
                "light_top": 0, "light_bottom": 0
            }
        }

        self.set_light_mode = light_set
        if light_set not in predefined_sets:
            raise ValueError(f"Light set mode {light_set} does not exist!")

        self.energy_settings.update(predefined_sets[light_set])

        keys = list(self.lights_radius_value.keys())
        for i, key in enumerate(keys):
            self.lights_radius_value[key] = lights_radius[i]



    def setup_sun_light(self, sun_strength:float=1.0, sun_angle:float=0.526,
                      sun_location:[float,float,float]=[0.0, 0.0, 3.0],
                      sun_rotation:[float,float,float]=[0.0, 0.0, 0.0],
                      sun_color:[float,float,float]=[1.0, 1.0, 1.0]) -> None:

        """
            Function: add light type Sun to the Environment

            Args:
                sun_strength : define the strength of the light
                sun_angle : define the angle of the light
                sun_color : define the color of the light, RGB values from 0 to 1
                sun_rotation : define the rotation of the light
                sun_location : define the location of the light

            Returns:
                None

        """
        if self.set_light_mode in [1, 2]:
            sun_strength = 0.0
        self.sun_strength = sun_strength
        self.sun_angle = sun_angle
        self.sun_light_name = "LightSun"
        self.sun_location = sun_location
        self.sun_rotation = sun_rotation
        self.sun_color = sun_color


    def change_environment_settings(self,
                                    cube_size=187,
                                    cube_rotation=[0.0, 0.0, 0.0],
                                    cube_location=[0.0, 0.0, None],
                                    axes_rotation=[0.0, 0.0, 96.0],
                                    axes_location=[0.0, 0.0, 0.0],
                                    camera_rotation=[62.0, 0.0, 136.0],
                                    camera_axes_offset=72.0,
                                    camera_light_offset=0.0,
                                    camera_type="",
                                    lens_camera=0.0,
                                    ortho_scale=0.0,
                                    light_energy_radius=0.0,
                                    light_energy=10.0,
                                    base_plane_location=(0.0, 0.0, 0.0),
                                    mesh_location=[0.0, 0.0, 0.0],
                                    mesh_rotation=[0.0, 0.0, 0.0]) -> None:
        """
        Update various settings in the blender environment.

        Parameters:
            cube_size (float): Size of the cube.
            cube_rotation (list): Rotation of the cube (x, y, z).
            cube_location (list): Location of the cube (x, y, z). If z is None, it defaults to cube_size/2.
            axes_rotation (list): Rotation of the axes (x, y, z).
            axes_location (list): Location of the axes (x, y, z).
            camera_rotation (list): Rotation of the camera (x, y, z).
            camera_axes_offset (float): Offset distance between the camera and axes.
            camera_light_offset (float): Offset distance between the camera and the light.
            camera_type (str) : type camera view
            lens_camera (float) : lens camera value
            ortho_scale (float) : ortho scale value
            light_energy_radius (float): Value for light radius
            light_energy (float): Energy of the light at the camera.
            base_plane_location (list): Location of the base plane (x, y, z).
            mesh_location (list): Location of the mesh (x, y, z)
            mesh_rotation (list): Rotation of the mesh (x, y, z)
        """
        self.size_cube = cube_size

        self.rotation_empty_cube = cube_rotation
        x, y, z = cube_location
        if z is None:
            z = cube_size / 2
        self.location_cube = (x, y, z)

        self.rotation_empty_axes = axes_rotation
        self.location_axes = axes_location

        self.rotation_camera = camera_rotation
        self.camera_offset_value_from_empty_axes = camera_axes_offset

        self.light_offset_value_from_camera = camera_light_offset
        self.camera_type = camera_type
        self.lens_camera = lens_camera
        self.ortho_scale = ortho_scale
        self.light_energy_radius_at_camera = light_energy_radius
        self.energy_light_at_camera = light_energy

        self.base_plane_location = base_plane_location
        self.mesh_location = mesh_location
        self.mesh_rotation = mesh_rotation



    def set_rendering_values(self,
                            type_engine: int = 1,
                            type_device: str = "GPU",
                            n_samples: int = 300,
                            file_format: str = "JPEG",
                            screen_percentage: float = 1.0,
                            floor_transparency:bool=False,
                            film_transparency:bool=False
                               ) -> None:
        """
        Updates the rendering settings with the provided values. 

        Args:
            type_engine (int): The rendering Engine, e.g., "Cycles" : 0, "EEVEE" : 1.
            type_device (str): The rendering device, e.g., "GPU" or "CPU" (default: GPU).
            n_samples (int): number of sample for rendering the image.
            file_format (str): Output file format, e.g., "JPEG" or "PNG" (default: JPEG).
            screen_percentage (float): Screen percentage for render resolution (default: 1.0).
            floor_transparency : bool value to activate transparency on floor
            film_transparency : bool value to active transparency on world

        Returns:
            None
        """

        self.type_engine = type_engine
        self.type_device = type_device
        self.n_samples = n_samples
        self.file_format = file_format
        self.film_transparency = film_transparency

        if self.type_engine == 0:
            self.floor_transparency = floor_transparency


        try:
            assert screen_percentage<=1 or screen_percentage>=0
            self.screen_percentage = screen_percentage
        except AssertionError:
            print("Expected values of screen percentage between 0 and 1.")



    def set_materials(self, material_value: int =0, material_plane_value: int =0,
                      color_map_value: int =0, hex_color: list=[],
                      color_transp_bsdf: list=[], color_diff_bsdf: list=[], mix_shader_fac: float=0.5) -> None:
        """
        Sets the material for the blender scene + color for ONLY the Transparency Material

        Args:
            material_value (int): The value corrisponding to a material in the CreationMaterial Class (default: 0).
            material_plane_value (int): The value corrisponding to a material plane in the CreationMaterial Class (default: 0).
            color_map_value (int): The value corrisponding to a material ColorMap in the CreationMaterial Class (default: 0)
            hex_color (List[]) : list of hex_value to apply to the color-ramp. This is only for the ColorMap
            color_transp_bsdf (List[]): list of float values, 0 to 1. Only for the FULL-TRANSPARENCY Material
            color_diff_bsdf (List[]): list of float values, 0 to 1. Only for the FULL-TRANSPARENCY Material
            mix_shader_fac (float): value to define which Principled Shader Apply. Only for the SCALAR-MAP material

        Returns:
            None
        """
        if material_value == 6:
            self.is_scalar_active = True
        else:
            self.is_scalar_active = False
        self.mat_chosen = CreationMaterial(material_value, material_plane_value, color_map_value,
                                           hex_color, color_transp_bsdf, color_diff_bsdf, mix_shader_fac)
        self.mat_chosen.check_parameter()


    def setup_walls(self, wall_front:bool=True, wall_back:bool=True, wall_right:bool=True, wall_left:bool=True) -> None:
        """
            Function: set up the wall round the plane at the base

            Args:
                wall_front : bool value to set the Front Wall
                wall_back : bool value to set the Back Wall
                wall_right : bool value to set the Right Wall
                wall_left : bool value to set the Left Wall

            Returns:
                None

        """

        self.wall_on_off[0] = wall_front
        self.wall_on_off[1] = wall_back
        self.wall_on_off[2] = wall_right
        self.wall_on_off[3] = wall_left


    def setup_scalarfield(self, scalar_field_file:str, scalar_template_labels:str):
        """
            Function: load scalar data

            Args:
                scalar_field_file : path of the scalar field file
                scalar_template_labels : path of the scalar template labels
                is_scalar_active : define if apply the scalar to the mesh

            Returns:
                None
        """
        self.scalar_field = sfv(scalar_field_file, scalar_template_labels)



    def setup_deformation(self, median_coordinate=[], min_value:float=-1.0, max_value:float=1.0, uv_scale_factor:float=0.1,
                          is_deformation_active:bool=False, number_deformation:int=1):
        """
            Function: setup for deformation on mesh

            Args:
                median_coordinate : array's of 3D coordinate
                min_value : min value to deform the mesh
                max_value : max value to deform the mesh
                uv_scale_factor : scale value for uv_sphere
                is_deformation_active : bool value for applying the deformation
                number_deformation : number of deformation to apply on mesh

        """
        self.is_deformation_active = is_deformation_active
        self.median_coordinate = median_coordinate
        self.min_value_d = min_value
        self.max_value_d = max_value
        self.uv_scale_factor = uv_scale_factor
        self.number_deformation = number_deformation


    def set_the_environment(self, nome_blend_file: str = "output1") -> None:
        """
        Sets up the environment, creates the blend file, and prepares the log file.

        Args:
            nome_blend_file (str): Name of the blend file to save (default: "output1").

        Returns:
            None
        """
        # Initialize the render setup
        self.my_setup_render = RenderingSetup(
            type_engine=self.type_engine,
            type_device=self.type_device,
            n_samples=self.n_samples,
            file_format=self.file_format,
            screen_percentage=self.screen_percentage,
            film_transparency=self.film_transparency
        )

        # Perform initial setup tasks
 
        self.check_mesh_existence()
        self.start_creation_scene()
        self.save_blend_file(nome_blend_file)

        # Open Blender file with setup render
        self.my_setup_render.open_file_blender(self.nome_file_blend)
        self.my_setup_render.init_all_rendering_settings()
        self.my_setup_render.save_file_blender()

        # Create a log file
        self.create_file_log()


    def check_mesh_existence(self) -> None:
            """
            Checks if the mesh file exists. If it exists, loads the mesh data (vertices, normals, faces).
            If the file doesn't exist, raises an error and logs the issue.

            Raises:
                ValueError: If the mesh file does not exist.
            """
            my_mesh = Processing_Mesh_PoC(self.nome_mesh)
            mesh_exists = my_mesh.check_mesh_file()
        
            if mesh_exists:

                print(f"File exists: {mesh_exists}")
                self.vertices, self.normals, self.faces = my_mesh.load_vert_normal_face()

                self.message_to_log += f"Working on: {self.nome_mesh}\n"
                self.message_to_log += (f"vertices: {len(self.vertices)}\n"
                                        f"normals: {len(self.normals)}\n"
                                        f"faces: {len(self.faces)}\n\n")
            else:

                error_message = f"File {self.nome_mesh} not found."
                print(error_message)
                self.message_to_log = error_message
                try:
                    utl.write_to_log(file_name=self.nome_log_file, message=self.message_to_log, where_at=1)
                except Exception as e:
                    print(f"Error writing to log: {e}")
                    raise 

                raise ValueError(error_message)


    def start_creation_scene(self) -> None:
        """
        Creates a 3D scene in Blender by setting up the following elements:
        
        1. Insert the mesh in the WORLD
        2. Insert an empty Cube
        3. Adds light sources to the scene, parents them to the Cube Empty, 
        and adjusts their energy settings.
        4. Creates a camera and an empty object to serve as its parent, then positions 
        and rotates the camera.
        5. Creates an empty object representing axes, parented to the camera.
        6. Adds a plane object at the base of the scene for visual context.
        
        This function updates viewport settings, sets the origin to the geometry 
        of the mesh, and applies transformations such as location and rotation to various objects.

        Args:
        
        Returns:
            None: This function doesn't return any values, but modifies the scene in Blender.
        """


        """
            Step 1: Create a new scene with an obj in it
        """
        bpy.ops.scene.new(type='NEW')
        scene = bpy.context.scene

        mesh = bpy.data.meshes.new(name=self.nome_mesh)
        obj = bpy.data.objects.new(self.nome_mesh + "_Object", mesh)
        mesh_name = self.nome_mesh+"_Object"

        # Link the object to the current collection
        bpy.context.collection.objects.link(obj)

        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.update()
        # Set custom vertex normals
        if not utl.is_array_empty(self.normals) and len(self.normals) > 0:
            mesh.normals_split_custom_set_from_vertices(self.normals)


        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].shading.type = 'SOLID'

        obj = self.select_object(obj)

        self.set_geometry_origin()

        obj = self.move_mesh_up_z(obj)
        self.apply_transformation(obj,[True, False, False])

        if any(value != 0.0 for value in self.mesh_rotation):
            self.rotate_empty_object(obj, rotation=self.mesh_rotation)
        if any(value != 0.0 for value in self.mesh_location):
            self.move_empty_object(obj, location=self.mesh_location)

        material = self.mat_chosen.fetch_material()

        if self.is_fill_holes:
            self.fillholes = FillHoles(mesh_name)
            self.fillholes.fill_holes()


        if self.is_scalar_active:
            obj = self.scalar_field.add_value_to_mesh_vertex(obj, self.scalar_field.fetch_data_scalar(),
                                                             self.scalar_field.fetch_data_labels())

        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)


        """
            Step 2/3: Create Cube Empty and parent lights
        """
        cubo_vuoto = self.create_cube_empty(cube_size=self.size_cube)

        lights_spot = self.parent_to_cube_add_light(cubo_vuoto)

        self.move_empty_object(cubo_vuoto, location=self.location_cube)

        self.rotate_empty_object(obj=cubo_vuoto, rotation=self.rotation_empty_cube)


        """
            Step 4/5: Create and position camera and empty axes
        """
        empty_axes, camera = self.create_camera_with_empty_axes(
            location=(self.size_cube + self.camera_offset_value_from_empty_axes,
                      self.size_cube + self.camera_offset_value_from_empty_axes,
                      self.size_cube + self.camera_offset_value_from_empty_axes),
            rotation=self.rotation_camera)

        self.move_empty_object(empty_axes, location=self.location_axes)
        self.rotate_empty_object(empty_axes, rotation=self.rotation_empty_axes)


        self.add_spot_light_at_camera(camera, empty_axes, spot_size=127, spot_blend=0.15,
                                                        energy=self.energy_light_at_camera,
                                                        offset_value_camera=self.light_offset_value_from_camera)


        """
            Modify light energy for all lights
        """
        self.modify_light_energy(lights_spot, self.energy_settings, self.lights_radius_value)


        """
            Step 6: Add plane on base
        """
        self.add_plane_on_base(self.plane_on_base)

        """
            Step 7: Add a Light Type Sun, for Enlightenment of the 3D World
        """

        self.add_sun_light_world()

        """
            Step 8: If True apply deformation
        """
        if self.is_deformation_active:
            self.deformation_on_mesh = DeformMesh(mesh_name, self.median_coordinate, self.uv_scale_factor,
                                                  self.min_value_d, self.max_value_d, self.number_deformation)
            self.deformation_on_mesh.apply_deformation()
            self.deform_message = self.deformation_on_mesh.get_message_deform()

        """
            Step 9: Save the Mesh on OFF file after Deformation Applied
        """
        if self.is_deformation_active:
            obj = bpy.data.objects.get(mesh_name)
            obj_to_save = self.select_object(obj)
            self.fetch_data_after_deformation(obj_to_save)




    def select_object(self, obj):
        """
        Selects a specific object in the Blender scene.

        In Blender, when a new object is created, it becomes the active and selected object. 

        The function performs the following actions:
        1. Deselects all objects in the scene.
        2. Selects the provided object.
        3. Sets the provided object as the active object for further operations.

        Args:
            obj (bpy.types.Object): The object to be selected in the scene.

        Returns:
            bpy.types.Object: The selected object, now set as the active object.
        """
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        return obj



    def set_geometry_origin(self) -> None:
        """
        Sets the object's origin point to the center of its geometry.
        The object's position in the scene remains unchanged, but the origin point is updated to match 
        the geometry's center.

        Returns:
            None
        """
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')



    def move_mesh_up_z(self, obj):
        """
        Moves the mesh object along the Z-axis to ensure all vertices are above or on the Z=0 plane.

        This function works by first checking the minimum Z-coordinate of the vertices in the mesh. 
        If any part of the mesh is below the Z=0 plane (i.e., has a negative Z-coordinate), 
        the entire object is moved upwards along the Z-axis to make sure the lowest vertex is positioned at Z=0.

        Args:
            obj (bpy.types.Object): The object (mesh) to be moved.

        Returns:
            bpy.types.Object: The object with its location adjusted along the Z-axis.
        """
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = obj.data

        # Find the minimum Z-coordinate among the vertices
        min_z = min((vertex.co.z for vertex in mesh.vertices))

        # If the minimum Z is negative, move the object up to make the lowest vertex at Z=0
        if min_z < 0:
            obj.location.z -= min_z

        return obj



    def apply_transformation(self, obj, values:[bool, bool, bool]=[False, False, True]) -> None:
        """
        Applies the scale transformation to the specified object.

        Args:
            obj (bpy.types.Object): The object whose scale transformation is to be applied.
            values : bool values

        Returns:
            None
        """
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=values[0], rotation=values[1], scale=values[2])
    


    def create_cube_empty(self, cube_size=1):
        """
        Creates an empty object of type 'CUBE' in the Blender scene.

        This function adds an empty object with the shape of a cube to the scene. 
        The function also sets the name of the empty object and applies the specified scale.

        Args:
            cube_size (float, optional): The size of the cube. Defaults to 1.0. 
                The value is used to uniformly scale the cube along the X, Y, and Z axes.

        Returns:
            bpy.types.Object: The newly created cube empty object with the specified size.
        """
        bpy.ops.object.empty_add(type='CUBE', location=(0, 0, 0))
        cube_empty = bpy.context.object
        cube_empty.name = self.nome_cubo
        cube_empty.scale = (cube_size, cube_size, cube_size)

        # apply_transformation(cube_empty)  # Uncomment if transformation needs to be applied

        return cube_empty


    def parent_to_cube_add_light(self, cube_empty):
        """
        Parents spotlights to an empty cube and positions them based on the cube's scale.

        This function generates six spotlights corresponding to the sides of the cube 
        (right, left, back, front, top, bottom). Each spotlight is positioned and rotated 
        relative to the cube's dimensions and then parented to the cube. The spotlights' 
        names are defined in `self.light_names`.

        Args:
            cube_empty (bpy.types.Object): The empty cube object to which the lights will be parented.

        Returns:
            dict: A dictionary mapping light names to their respective spotlight objects.
        """

        scale_x, scale_y, scale_z = cube_empty.scale

        positions = np.array([
            [scale_x, 0, 0],   # Right
            [-scale_x, 0, 0],  # Left
            [0, scale_y, 0],   # Back
            [0, -scale_y, 0],  # Front
            [0, 0, scale_z],   # Top
            [0, 0, -scale_z]   # Bottom
        ])

        rotations_degrees = np.array([
            [0, 90, 0],    # Right
            [0, -90, 0],   # Left
            [0, 90, 90],   # Back
            [0, -90, 90],  # Front
            [0, 0, 0],     # Top
            [-180, 0, 0]   # Bottom
        ])
        rotations_radians = np.deg2rad(rotations_degrees)

        # Create and parent the lights
        lights_spot_dict = {
            name: self.add_spot_light(name, cube_empty, positions[i], rotations_radians[i])
            for i, name in enumerate(self.light_names)
        }

        return lights_spot_dict

    def add_spot_light(self, name:str, parent, location:[], rotation:[], spot_size: int =127, spot_blend:
                        float =0.15, energy: float=10.0):
        """
        Adds a spotlight to the Blender scene with specified properties and parents it to a given object.

        Args:
            name (str): The name of the spotlight object.
            parent (bpy.types.Object): The parent object to which the spotlight will be attached.
            location (tuple[float, float, float]): The position of the spotlight relative to the parent object.
            rotation (tuple[float, float, float]): The rotation of the spotlight in radians.
            spot_size (float, optional): The cone angle of the spotlight in degrees. Defaults to 127.
            spot_blend (float, optional): The softness of the spotlight's edge. Defaults to 0.15.
            energy (float, optional): The intensity of the spotlight. Defaults to 10.0.

        Returns:
            bpy.types.Object: The created spotlight object.
        """

        bpy.ops.object.light_add(type='SPOT', location=(0, 0, 0), rotation=(0, 0, 0))
        light = bpy.context.object
        light.name = name

        light.data.spot_size = np.deg2rad(spot_size)
        light.data.spot_blend = spot_blend
        light.data.energy = energy

        light.parent = parent
        light.matrix_parent_inverse = parent.matrix_world.inverted()

        light.location = location
        light.rotation_euler = rotation

        return light

    def rotate_empty_object(self, obj, rotation:tuple) -> None:
        """
        Rotates an object to a specified rotation in degrees.

        Args:
            obj (bpy.types.Object): The object to rotate.
            rotation (tuple[float, float, float]): The rotation angles in degrees (x, y, z).

        Raises:
            ValueError: If the specified object is not found in `bpy.data.objects`.
        """
        target_object = bpy.data.objects.get(obj.name)
        if not target_object:
            raise ValueError(f"Object '{obj.name}' not found!")

        rad_rotation = np.deg2rad(rotation)
        target_object.rotation_euler = rad_rotation



    def move_empty_object(self, obj, location:tuple) -> None:
        """
        Moves an object to a specified location.

        Args:
            obj (bpy.types.Object): The object to move.
            location (tuple[float, float, float]): The target location as (x, y, z) coordinates.

        Raises:
            ValueError: If the specified object is not found in `bpy.data.objects`.
        """

        target_object = bpy.data.objects.get(obj.name)
        if not target_object:
            raise ValueError(f"Object '{obj.name}' not found!")

        target_object.location = location



    def create_camera_with_empty_axes(self, location:tuple, rotation:tuple):
        """
        Creates an empty axes and a camera in the scene,
        then parents the camera to the empty object.

        Args:
            location (tuple[float, float, float]): The camera's location as (x, y, z) coordinates.
            rotation (tuple[float, float, float]): The camera's rotation in degrees (x, y, z).

        Returns:
            tuple[bpy.types.Object, bpy.types.Object]: The created empty object and camera.

        Raises:
            RuntimeError: If Blender's operators for creating objects fail.
        """
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        empty_axes = bpy.context.object
        empty_axes.name = self.nome_axes

        rotation_radians = np.deg2rad(rotation)

        type_camera = ["ORTHO", "PERSP"]
        bpy.ops.object.camera_add(location=location, rotation=rotation_radians)
        camera = bpy.context.object
        camera.name = self.nome_camera

        camera_type_upper = self.camera_type.upper()
        if camera_type_upper in type_camera:
            if camera_type_upper == type_camera[0]:
                camera.data.type = type_camera[0]
                if self.ortho_scale is not None:
                    camera.data.ortho_scale = self.ortho_scale
            elif camera_type_upper == type_camera[1]:
                camera.data.type = type_camera[1]
                if self.lens_camera is not None:
                    camera.data.lens = self.lens_camera

        # Parent the camera to the empty object
        camera.parent = empty_axes
        bpy.context.scene.camera = camera

        return empty_axes, camera


    def add_spot_light_at_camera(
        self,
        camera,
        empty_axes,
        spot_size=127,
        spot_blend=0.15,
        energy=100000,
        offset_value_camera=0
    ) -> None:
        """
        Adds a spot-light positioned relative to the camera and parents it to an empty object.

        Args:
            camera (bpy.types.Object): The camera object to base the light's position and rotation on.
            empty_axes (bpy.types.Object): The empty object to parent the light to.
            spot_size (float, optional): The angle of the light cone in degrees. Defaults to 127.
            spot_blend (float, optional): The blend factor for the light cone. Defaults to 0.15.
            energy (float, optional): The intensity of the light. Defaults to 100000.
            offset_value_camera (float, optional): The offset value to adjust the light's location relative to the camera. Defaults to 0.

        Returns:
            bpy.types.Object: The created spot-light object.

        Raises:
            ValueError: If the camera or empty_axes object is not valid.
        """
        if not camera or not empty_axes:
            raise ValueError("Invalid camera or empty_axes object provided.")

        # Calculate the light's position relative to the camera
        light_location = (
            camera.location.x + offset_value_camera,
            camera.location.y + offset_value_camera,
            camera.location.z + offset_value_camera
        )

        bpy.ops.object.light_add(type='SPOT', location=light_location, rotation=camera.rotation_euler)
        light = bpy.context.object
        light.name = self.nome_camera_light

        light.data.spot_size = np.deg2rad(spot_size)
        light.data.spot_blend = spot_blend
        light.data.energy = energy
        light.data.shadow_soft_size = self.light_energy_radius_at_camera

        light.parent = empty_axes



    def modify_light_energy(self, all_lights, lights_energy, lights_radius):
        """
        Modifies the energy settings of a collection of lights.

        Args:
            all_lights (dict): A dictionary where keys are light names and values are Blender light objects.
            lights_energy (dict): A dictionary where keys are light names and values are desired energy values.
            lights_radius (dict): A dictionary where keys are light names and values are desired radius values.

        Returns:
            None
        """
        for name, energy in lights_energy.items():
            light = all_lights.get(name)
            if light:
                radius = lights_radius.get(name)
                if light.data.energy != energy:
                    light.data.energy = energy
                    print(f"Energy of {name} set to {energy}")
                if light.data.shadow_soft_size != radius:
                    light.data.shadow_soft_size = radius
                    print(f"Radius of {name} set to {radius}")

            else:
                print(f"Warning: Light '{name}' not found in the provided lights dictionary.")



    def add_plane_on_base(self, size_plane=100) -> None:
        """
        Adds a horizontal plane at the origin of the world with a specified size and applies a material.
        + add a wall round the plane at the base

        Args:
            size_plane (float): The size of the plane to be added. Default is 100.

        Returns:
            bpy.types.Object: The created plane object.
        """

        new_collection = bpy.data.collections.new(name="SetPlanes")
        bpy.context.scene.collection.children.link(new_collection)

        bpy.ops.mesh.primitive_plane_add(size=size_plane, location=self.base_plane_location)
        obj_plane = bpy.context.active_object

        material = self.mat_chosen.fetch_material_plane()

        if obj_plane.data.materials:
            obj_plane.data.materials[0] = material
        else:
            obj_plane.data.materials.append(material)

        if self.floor_transparency:
            bpy.context.object.is_shadow_catcher = True

        new_collection.objects.link(obj_plane)
        bpy.context.scene.collection.objects.unlink(obj_plane)

        locations = [
            (0, -size_plane / 2, size_plane / 2),  # Fronte
            (0, size_plane / 2, size_plane / 2),
            (size_plane / 2, 0, size_plane / 2),  # Right
            (-size_plane / 2, 0, size_plane / 2)
        ]

        rotations = [
            (-(np.pi / 2), 0, 0),
            ((np.pi / 2), 0, 0),
            ((np.pi / 2), 0, -(np.pi / 2)),
            ((np.pi / 2), 0, (np.pi / 2))
        ]


        for wall_on_off, name, location, rotation in zip(self.wall_on_off, self.wall_names, locations, rotations):
            if wall_on_off:
                self.add_wall(name, location, rotation, material, size_plane, new_collection)

        print(f"Plane added at {self.base_plane_location} with size {size_plane}")



    def add_wall(self, name, location, rotation, material, size_plane, new_collection):
        """
            Function: add planes round the plane at the base

            Args:
                name : name of the planes
                location : location of the plane
                rotation : rotation of the plane
                material : material-type is going be applied to the plane
                size_plane : size of the plane
                new_collection : plane linked to the collection

            Returns:
                None
        """

        bpy.ops.mesh.primitive_plane_add(size=size_plane, location=location, rotation=rotation)
        obj_plane = bpy.context.active_object
        obj_plane.name = name

        if obj_plane.data.materials:
            obj_plane.data.materials[0] = material
        else:
            obj_plane.data.materials.append(material)

        if self.floor_transparency:
            bpy.context.object.is_shadow_catcher = True

        new_collection.objects.link(obj_plane)
        bpy.context.scene.collection.objects.unlink(obj_plane)


    def add_sun_light_world(self):
        """
            Function: create a Sun-light

        """
        bpy.ops.object.light_add(type='SUN',
                                 location=(self.sun_location[0], self.sun_location[1], self.sun_location[2]),
                                 rotation=(self.sun_rotation[0], self.sun_rotation[1], self.sun_rotation[2]))

        sun_light_obj = bpy.context.object
        sun_light_obj.name = self.sun_light_name
        sun_light_obj.data.color = (self.sun_color[0], self.sun_color[1], self.sun_color[2])
        sun_light_obj.data.angle = np.deg2rad(self.sun_angle)
        sun_light_obj.data.energy = self.sun_strength


    def sun_write_message(self):
        """
            Function: write a str value to message to add to the Log File

        """
        msg = (f"Created Sun Light: {self.sun_light_name}\n"
               f"Sun Location: {self.sun_location}\n"
               f"Sun Rotation: {self.sun_rotation}\n"
               f"Sun color: {self.sun_color}\n"
               f"Sun strength: {self.sun_strength}\n"
               f"Sun angle: {self.sun_angle} deg\n")
        return msg



    def save_blend_file(self, final_name: str) -> None:
        """
        Saves the current Blender file with a specified name.

        Args:
            final_name (str): The base name to use for saving the `.blend` file.

        Returns:
            None
        """
        self.nome_file_blend = f"{final_name}_{self.nome_mesh}{self.extension}"
        file_path = f"{self.output_blend_file}{self.nome_file_blend}"

        try:
            bpy.ops.wm.save_as_mainfile(filepath=file_path)
            print(f"Blend file saved successfully at: {file_path}")
        except Exception as e:
            print(f"Error saving blend file: {e}")
            raise IOError(f"Failed to save blend file at {file_path}") from e


    def fetch_data_after_deformation(self, obj_to_save):
        """
            Fetch data from the obj_to_save after deformation is applied and save to the file

            Args:
                obj_to_save : bpy obj
            Result:
                None
        """
        vertices = np.array([[v.co.x, v.co.y, v.co.z] for v in obj_to_save.data.vertices])
        normals =  np.array([[n.normal.x, n.normal.y, n.normal.z] for n in obj_to_save.data.vertices])
        faces = np.array([p.vertices[:] for p in obj_to_save.data.polygons])

        vertices = utl.convert_array_tofloat64(vertices)
        normals = utl.convert_array_tofloat64(normals)
        utl.save_off_format(self.nome_mesh+"_Deformed"+".off", vertices, normals, faces, self.output_fileOff_folder)
        print(f"File: {self.nome_mesh}_Deformed - Salvato")
        #print(vertices)
        #print(faces)

    def create_file_log(self) -> None:
        """
            Function : Creates and writes a log file with detailed information about the scene setup.
                
            Returns:
                None
        """

        log_messages = []

        if not utl.is_array_empty(self.normals):
            lenght_norm = len(self.normals)
        else:
            lenght_norm = 0

        log_messages.append(f"Created Mesh: {self.nome_mesh}\n"
                            f"Vertex: {len(self.vertices)}\n"
                            f"Normals: {lenght_norm}\n"
                            f"Faces: {len(self.faces)}\n")

        log_messages.append(f"Created plane on base:\nSize: {self.plane_on_base}\n"
                            f"Location: {self.base_plane_location}\n"
                            f"Transparency: {self.floor_transparency}\n")

        log_messages.append("Created Wall round the Base")
        for wall_on_off, wall_name in zip(self.wall_on_off, self.wall_names):
            if wall_on_off:
                log_messages.append(f"{wall_name}")


        log_messages.append(f"\nCreated empty cube: {self.nome_cubo}\n"
                            f"Dimension: {self.size_cube}\nLocation: {self.location_cube}\n"
                            f"Rotation: {self.rotation_empty_cube}\n")

        log_messages.append(f"Created {len(self.light_names)} lights:")
        for light in self.light_names:
            log_messages.append(f"{light}: Energy={self.energy_settings.get(light)} "
                                f"Radius={self.lights_radius_value.get(light)}")


        log_messages.append(f"\nCreated empty axes: {self.nome_axes}\n"
                            f"Location: {self.location_axes}\nRotation: {self.rotation_empty_axes}\n")

        type_camera = ["ORTHO", "PERSP"]
        type_value = ""
        value_numeric = ""
        camera_type_upper = self.camera_type.upper()
        if camera_type_upper == type_camera[0]:
            type_value = type_camera[0]
            value_numeric = f"Orthographic scale: {self.ortho_scale}"
        elif camera_type_upper == type_camera[1]:
            type_value = type_camera[1]
            value_numeric = f"Focal Length: {self.lens_camera}"

        log_messages.append(f"Created camera: {self.nome_camera}\n"
                            f"Type: {type_value}\n"
                            f"{value_numeric}\n"
                            f"Offset from {self.nome_axes}: {self.camera_offset_value_from_empty_axes}\n"
                            f"Rotation: {self.rotation_camera}\n")

        log_messages.append(f"Created light at camera: {self.nome_camera_light}\n"
                            f"Offset from camera: {self.light_offset_value_from_camera}\n"
                            f"Energy: {self.energy_light_at_camera}\n"
                            f"Radius: {self.light_energy_radius_at_camera}\n")


        log_messages.append(self.sun_write_message())

        log_messages.append(self.mat_chosen.get_message())

        if self.is_deformation_active:
            log_messages.append(self.deform_message)

        if self.is_fill_holes:
            log_messages.append(self.fillholes.get_message())

        log_messages.append(self.my_setup_render.get_message())

        # Join all log messages into a single string
        self.message_to_log = "\n".join(log_messages)
        utl.write_to_log(file_name=self.nome_log_file, message=self.message_to_log, where_at=1)
