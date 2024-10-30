from CODE.Process_Mesh.processing_functions import Processing_Mesh_PoC
from CODE.FunzioniUtili import utils as utl
from CODE.For_Blender_Functions.set_rendering import RenderingSetup
import bpy
import numpy as np


class SetEnvironmentBlender:
    output_blend_file = "BLEND_FILE_OUTPUT/"
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

    light_names = [
        'light_front',
        'light_back',
        'light_right',
        'light_left',
        'light_top',
        'light_bottom'
    ]

    energy_light_at_camera = 100000
    size_cubo = 187
    rotazione_camera = (62, 0, 136)

    rotazione_empty_axes = (0, 0, 96)
    location_axes = (0,0,0)

    rotazione_empty_cube = (0, 0, 0)
    location_cube = (0, 0, 0)

    camera_offset_value_from_empty_axes = 72
    light_offset_value_from_camera = 0

    location_plane_on_base = None

    nome_cubo = 'Cube_Reference'
    nome_axes = 'Empty_Axes_to_Camera'
    nome_camera = 'Camera_Main'
    nome_camera_light = 'Light_to_Camera'

    type_engine = None
    type_device = None
    n_samples = None
    file_format = None
    screen_percentage = None
    my_setup_render = None
    nome_file_blend = None


    def __init__(self, nome_mesh: str, nome_log_file: str, plane_on_base_size: int):
        self.nome_mesh = nome_mesh
        self.nome_log_file = nome_log_file
        self.plane_on_base = plane_on_base_size


    def change_energy_light(self, light_front=100000, light_back=100000,
                            light_right=100000, light_left=100000,
                            light_top=100000, light_bottom=100000):
        self.energy_settings['light_front'] = light_front
        self.energy_settings['light_back'] = light_back
        self.energy_settings['light_right'] = light_right
        self.energy_settings['light_left'] = light_left
        self.energy_settings['light_top'] = light_top
        self.energy_settings['light_bottom'] = light_bottom

    def change_location_scale_rotation_offset_energy(self, cubo_size=187, rotation_cube=(0, 0, 0),
                                             location_cube=(0,0,size_cubo/2), rotation_axes=(0, 0, 96), location_axes=(0,0,0),
                                             rotation_camera=(62, 0, 136), offset_axes_camera=72,
                                             offset_camera_light=0, energy_light_at_camera=100000, location_plane_on_base=(0,0,0)):
        self.size_cubo = cubo_size
        self.rotazione_empty_cube = rotation_cube
        x, y, _ = location_cube
        z = self.size_cubo / 2
        location_cube = (x, y, z)
        self.location_cube = location_cube

        self.rotazione_empty_axes = rotation_axes
        self.location_axes = location_axes

        self.rotazione_camera = rotation_camera
        self.camera_offset_value_from_empty_axes = offset_axes_camera

        self.light_offset_value_from_camera = offset_camera_light
        self.energy_light_at_camera = energy_light_at_camera

        self.location_plane_on_base = location_plane_on_base

    def setup_rendering_values(self, type_engine=1, type_device="GPU", n_samples=300, file_format="JPEG", screen_percentage=1.0):
        self.type_engine = type_engine
        self.type_device = type_device
        self.n_samples = n_samples
        self.file_format = file_format
        self.screen_percentage = screen_percentage

    def setup_the_environtment(self, nome_blend_file="output1"):
        self.my_setup_render = RenderingSetup(self.type_engine, self.type_device, self.n_samples, self.file_format,
                                              self.screen_percentage)
        self.check_mesh_existence()
        self.start_creation_scene()
        self.save_blend_file(nome_blend_file)

        self.my_setup_render.open_file_blender(self.nome_file_blend)
        self.my_setup_render.init_all_rendering_settings()
        self.my_setup_render.save_file_blender()

        self.create_file_log()

    def check_mesh_existence(self):
        my_mesh =  Processing_Mesh_PoC(self.nome_mesh)
        valore_veritas = my_mesh.check_mesh_file()

        if valore_veritas:
            print("File Esiste: " + str(valore_veritas))
            self.vertices, self.normals, self.faces = my_mesh.load_vert_normal_face()
            self.message_to_log+=f"Working on: {self.nome_mesh}\n"
            self.message_to_log+=(f"vertices: {len(self.vertices)}\nnormals: "
                                  f"{len(self.normals)}\nfaces: {len(self.faces)}\n\n")
        else:
            print(f"File {self.nome_mesh} non trovato")
            self.message_to_log=f"File {self.nome_mesh} non trovato"
            utl.write_to_log(file_name=self.nome_log_file, message=self.message_to_log, where_at=1)
            raise ValueError(f"File {self.nome_mesh} non trovato")


    def start_creation_scene(self):
        # Creo una nuova scena
        bpy.ops.scene.new(type='NEW')
        scene = bpy.context.scene

        # Creo una nuova mesh e un nuovo oggetto
        mesh = bpy.data.meshes.new(name=self.nome_mesh)
        obj = bpy.data.objects.new(self.nome_mesh + "_Object", mesh)

        # Collego l'oggetto alla scena
        bpy.context.collection.objects.link(obj)

        # Creo la mesh dai dati prelevati
        mesh.from_pydata(self.vertices, [], self.faces)

        # Aggiorna la mesh con i dati
        mesh.update()

        # Assegno le normali ai vertici
        mesh.normals_split_custom_set_from_vertices(self.normals)

        # Imposta la vista su 'Solid' per visualizzare la mesh
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].shading.type = 'SOLID'


        oggetto = bpy.context.object
        obj = self.seleziona_oggetto(obj)

        self.imposta_origine_geometria()

        obj = self.move_mesh_up_zpositive(obj)

        cubo_vuoto = self.create_cube_empty(cube_size=self.size_cubo)

        lights_spot = self.parent_to_cube_add_light(cubo_vuoto)

        self.move_empty_object(cubo_vuoto, location=self.location_cube)

        self.rotate_empty_object(cubo_vuoto, rotazione=self.rotazione_empty_cube)

        empty_axes, camera = self.create_camera_with_empty_axes(
            location=(self.size_cubo + self.camera_offset_value_from_empty_axes,
                      self.size_cubo + self.camera_offset_value_from_empty_axes,
                      self.size_cubo + self.camera_offset_value_from_empty_axes),
            rotation=self.rotazione_camera)

        self.move_empty_object(empty_axes, location=self.location_axes)
        self.rotate_empty_object(empty_axes, rotazione=self.rotazione_empty_axes)

        light_at_camera = self.add_spot_light_at_camera(camera, empty_axes, spot_size=127, spot_blend=0.15,
                                                        energy=self.energy_light_at_camera,
                                                        offset_value_camera=self.light_offset_value_from_camera)

        self.modify_light_energy(lights_spot, self.energy_settings)
        self.add_plane_on_base(self.plane_on_base)

    def seleziona_oggetto(self, oggetto):
        bpy.ops.object.select_all(action='DESELECT')
        oggetto.select_set(True)
        bpy.context.view_layer.objects.active = oggetto
        return oggetto

    def imposta_origine_geometria(self):
        # Imposta geometria all'origine
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

    def move_mesh_up_zpositive(self, oggetto):
        bpy.ops.object.mode_set(mode='OBJECT')
        # Accesso ai vertici
        mesh = oggetto.data

        min_z = min((vertex.co.z for vertex in mesh.vertices))

        if min_z < 0:
            oggetto.location.z -= min_z

        return oggetto

    def apply_transformation(self, obj):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    def create_cube_empty(self, cube_size=1):
        bpy.ops.object.empty_add(type='CUBE', location=(0, 0, 0))
        cube_empty = bpy.context.object
        cube_empty.name = self.nome_cubo
        cube_empty.scale = (cube_size, cube_size, cube_size)

        # apply_transformation(cube_empty)
        return cube_empty

    def parent_to_cube_add_light(self, cube_empty):
        scale_x, scale_y, scale_z = cube_empty.scale
        posizione_o = np.array([
            # DX
            [scale_x, 0, 0],
            # SX
            [-scale_x, 0, 0],

            # RETRO
            [0, scale_y, 0],
            # FRONTE
            [0, -scale_y, 0],

            # TOP
            [0, 0, scale_z],
            # BOTTOM
            [0, 0, -scale_z]
        ])

        rotazione_o = np.array([
            # DX
            [0, 90, 0],
            # SX
            [0, -90, 0],

            # RETRO
            [0, 90, 90],
            # FRONTE
            [0, -90, 90],

            # TOP
            [0, 0, 0],
            # BOTTOM
            [-180, 0, 0]
        ])

        rotazione_o = np.deg2rad(rotazione_o)


        lights_spot_dic = {name: self.add_spot_light(name, cube_empty, posizione_o[i], rotazione_o[i]) for i, name in
                           enumerate(self.light_names)}
        return lights_spot_dic

    def add_spot_light(self, name, parent, location, rotation, spot_size=127, spot_blend=0.15, energy=100000):
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

    def rotate_empty_object(self, obj, rotazione):
        oggetto = bpy.data.objects.get(obj.name)
        if not oggetto:
            raise ValueError(f"Empty {obj.name} non trovato!")

        rad_rotation = np.deg2rad(rotazione)
        oggetto.rotation_euler = rad_rotation

    def move_empty_object(self, obj, location):
        oggetto = bpy.data.objects.get(obj.name)
        if not oggetto:
            raise ValueError(f"Empty {obj.name} non trovato!")

        oggetto.location = location

    def create_camera_with_empty_axes(self, location, rotation):
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        empty_axes = bpy.context.object
        empty_axes.name = self.nome_axes
        rotazione_grad = np.deg2rad(rotation)
        bpy.ops.object.camera_add(location=location, rotation=rotazione_grad)
        camera = bpy.context.object
        camera.name = self.nome_camera

        camera.parent = empty_axes

        bpy.context.scene.camera = camera

        return empty_axes, camera

    def add_spot_light_at_camera(self, camera, empty_axes, spot_size, spot_blend, energy, offset_value_camera):
        light_location = (camera.location.x + offset_value_camera, camera.location.y + offset_value_camera,
                          camera.location.z + offset_value_camera)

        bpy.ops.object.light_add(type='SPOT', location=light_location, rotation=camera.rotation_euler)
        light = bpy.context.object
        light.name = self.nome_camera_light
        light.data.spot_size = np.deg2rad(spot_size)
        light.data.spot_blend = spot_blend
        light.data.energy = energy

        light.parent = empty_axes
        return light

    def modify_light_energy(self ,all_lights, lights_energy):
        for name, energy in lights_energy.items():
            if name in all_lights:
                if not all_lights[name].data.energy == energy:
                    all_lights[name].data.energy = energy
                    print(f"Energy of {name} set to {energy}")
            else:
                print(f"Light {name} not found in lights")

    def add_plane_on_base(self, size_plane=100):
        bpy.ops.mesh.primitive_plane_add(size=size_plane, location=self.location_plane_on_base)

    def save_blend_file(self, final_name):
        # Salvo il file .blend con la nuova mesh aggiunta
        self.nome_file_blend = f"{final_name}_" + self.nome_mesh + self.extension
        bpy.ops.wm.save_as_mainfile(
            filepath=self.output_blend_file + f"{final_name}_" + self.nome_mesh + self.extension)

    def create_file_log(self):

        self.message_to_log += (f"Created plane on base:\nSize: {self.plane_on_base}\n"
                                f"Location: {self.location_plane_on_base}\n\n")

        self.message_to_log += (f"Created empty cube: {self.nome_cubo}\n"
                                f"Dimension: {self.size_cubo}\n"
                                f"Location: {self.location_cube}\n"
                                f"Rotation: {self.rotazione_empty_cube}\n\n")

        self.message_to_log += f"Created {len(self.light_names)} lights:\n"

        for light in self.light_names:
            self.message_to_log +=f"{light}: {self.energy_settings[light]}\n"

        self.message_to_log +="\n"
        self.message_to_log += (f"Created empty axes: {self.nome_axes}\n"
                                f"Location: {self.location_axes}\n"
                                f"Rotation: {self.rotazione_empty_axes}\n\n")

        self.message_to_log += (f"Created camera: {self.nome_camera}\n"
                                f"Offset from {self.nome_axes}: {self.camera_offset_value_from_empty_axes}\n"
                                f"Rotation: {self.rotazione_camera}\n\n")
        self.message_to_log += (f"Create light at camera: {self.nome_camera_light}\n"
                                f"Offset from camera: {self.light_offset_value_from_camera}\n"
                                f"Energy: {self.energy_light_at_camera}\n\n")

        self.message_to_log += self.my_setup_render.get_message()
        utl.write_to_log(file_name=self.nome_log_file, message=self.message_to_log, where_at=1)
