import bpy
from CODE.For_Blender_Functions.out_set_render import ScreenMonitorResolution as smr, OutputFileRender as oft


# Class for setting the blend file for rendering.
# Set up the engine, device, sample, file format,
# percentage of the screen, resolution of the screen (manually for now)
# Every value are saved in the log file
# How it works: setup_environment_blender, create our environment and save the file
# This class open the file and apply the correct rendering values
# Because I find it difficult to re-save it the file again I just create a new one called outFinal,
# outFinal is the same file as the setup_enviroment_blender gives in output plus the values for rendering
class RenderingSetup:
    output_blend_file = "BLEND_FILE_OUTPUT/"

    engines = {
        0: 'CYCLES',
        1: 'BLENDER_EEVEE_NEXT'
    }

    devices = ['CPU', 'GPU']

    images_type = ['JPEG', 'PNG']

    message_to_log = "RENDERING SETUP:\n"

    def __init__(self, type_engine: int, type_device: str, n_samples: int, file_format: str, percentage_screen):
        self.type_engine = type_engine
        self.type_device = type_device
        self.n_samples = n_samples
        self.file_format = file_format
        self.percentage_screen = percentage_screen

    def set_engine_device(self):
       if self.type_engine in self.engines:
            single_engine = self.engines[self.type_engine]
            single_device = self.type_device.upper()

            if not(single_engine == 'BLENDER_EEVEE_NEXT'):
                if single_engine == 'CYCLES' and single_device in self.devices:
                    bpy.context.scene.cycles.device = self.type_device.upper()
                    bpy.context.scene.render.engine = single_engine
                    self.set_cycles_samples()
                else:
                    raise ValueError("Invalid device type: Use 'CPU' or 'GPU'")
            else:
                bpy.context.scene.render.engine = single_engine
                self.set_eevee_samples()

            print(f"Render engine set to: {single_engine}")
            self.message_to_log += f"Render engine set to: {single_engine}\n"
            if not(single_engine == 'BLENDER_EEVEE_NEXT'):
                print(f"Render device set to: {single_device}")
                self.message_to_log += f"Render device set to: {single_device}\n"

            print(f"RENDER SAMPLES: {self.n_samples}")
            self.message_to_log += f"RENDER SAMPLES: {self.n_samples}\n"
       else:
            raise ValueError("Invalid engine type. Use 'CYCLE' or 'EEVEE'.")


    def set_eevee_samples(self):
        bpy.context.scene.eevee.taa_render_samples = self.n_samples
        print(f"RENDER SAMPLES: {self.n_samples}")


    def set_cycles_samples(self):
        bpy.context.scene.cycles.samples = self.n_samples
        print(f"RENDER SAMPLES: {self.n_samples}")

    def set_file_format(self):
        formato_file = self.file_format.upper()
        if formato_file in self.images_type:
            bpy.context.scene.render.image_settings.file_format = formato_file
            print(f"File format set to: {formato_file}")
            self.message_to_log += f"File format set to: {formato_file}\n"
        else:
            raise ValueError("Invalid file format!")

    def set_resolution_screen(self, resolution_x, resolution_y):
        percentage_screen = int(self.percentage_screen * 100)
        if percentage_screen <= 100 and percentage_screen >= 1:
            bpy.context.scene.render.resolution_percentage = percentage_screen
            bpy.context.scene.render.resolution_x = resolution_x
            bpy.context.scene.render.resolution_y = resolution_y

            print(f"Resolution set to: {resolution_x}x{resolution_y}")
            print(f"Resolution scale set to: {percentage_screen}%")

            self.message_to_log += f"Resolution set to: {resolution_x}x{resolution_y}\n"
            self.message_to_log += f"Resolution scale set to: {percentage_screen}%\n"
        else:
            raise ValueError("Invalid resolution screen!")

    def set_path_output_rendered(self, full_folder_path):
        # bpy.context.scene.render.filepath = full_folder_path
        print(f"Output path set to: {full_folder_path}")


    def open_file_blender(self, nome_file):
        bpy.ops.wm.open_mainfile(filepath=self.output_blend_file+nome_file)
        print(f"Aperto il file: {nome_file}")

    def save_file_blender(self):
        bpy.ops.wm.save_as_mainfile(filepath=self.output_blend_file+"outFinal.blend")

    def init_all_rendering_settings(self):
        my_screen =  smr()
        # my_outfolder = oft()
        self.set_engine_device()
        self.set_file_format()
        self.set_resolution_screen(my_screen.get_X(), my_screen.get_Y())
        # self.set_path_output_rendered(my_outfolder.get_path_output_rendering())

    def get_message(self):
        return self.message_to_log

