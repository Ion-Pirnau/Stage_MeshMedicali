import bpy
from CODE.For_Blender_Functions.out_set_render import ScreenMonitorResolution as smr, OutputFileRender as oft


class RenderingSetup:
    """
        Class for setting the blend file for rendering.

        Set up the engine, device, sample, file format,
        percentage of the screen, resolution of the screen

        Every value are saved in the log file

        HOW IT WORKS: setup_environment_blender, create our environment and save the file
        the class open the file and apply the correct rendering values

        Because I find it difficult to re-save it the file again I just create a new one called outFinal,
        outFinal is the same file as the setup_enviroment_blender gives in output plus the values for rendering
    """

    output_blend_file = "BLEND_FILE_OUTPUT/"

    engines = {
        0: 'CYCLES',
        1: 'BLENDER_EEVEE_NEXT'
    }

    devices = ['CPU', 'GPU']

    images_type = ['JPEG', 'PNG']

    message_to_log = "RENDERING SETUP:\n"

    def __init__(self, type_engine: int, type_device: str, n_samples: int, file_format: str, screen_percentage: float,
                 film_transparency: bool):
        self.type_engine = type_engine
        self.type_device = type_device
        self.n_samples = n_samples
        self.file_format = file_format
        self.screen_percentage = screen_percentage
        self.film_transparency = film_transparency

    def set_engine_device(self):
        """
            Function: setting the engine and device for rendering
        """

        if self.type_engine in self.engines:
            single_engine = self.engines[self.type_engine]
            single_device = self.type_device.upper()

            if not(single_engine == 'BLENDER_EEVEE_NEXT'):
                if single_engine == 'CYCLES' and single_device in self.devices:
                    bpy.context.scene.cycles.device = self.type_device.upper()
                    bpy.context.scene.render.engine = single_engine
                    if self.film_transparency:
                        bpy.context.scene.render.film_transparent = True
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
            self.message_to_log += (f"RENDER SAMPLES: {self.n_samples}\n"
                                    f"Film-Transparency: {self.film_transparency}\n")
        else:
            raise ValueError("Invalid engine type. Use 'CYCLE' or 'EEVEE'.")


    def set_eevee_samples(self):

        """
            Function: set eevee samples for rendering
        """

        bpy.context.scene.eevee.taa_render_samples = self.n_samples
        print(f"RENDER SAMPLES: {self.n_samples}")


    def set_cycles_samples(self):

        """
            Function: setting the cycles samples
        """

        bpy.context.scene.cycles.samples = self.n_samples
        print(f"RENDER SAMPLES: {self.n_samples}")


    def set_file_format(self):

        """
            Function: setting the file format of the Image, the User want to render at the End of the Pipeline
            Phase 3, more info to README file
        """

        format_file = self.file_format.upper()
        if format_file in self.images_type:
            bpy.context.scene.render.image_settings.file_format = format_file
            print(f"File format set to: {format_file}")
            self.message_to_log += f"File format set to: {format_file}\n"
        else:
            raise ValueError("Invalid file format!")


    def set_resolution_screen(self, resolution_x, resolution_y):
        """
            Function: set resolution screen + screen resolution percentage

            Args:
                resolution_x: width value of the screen
                resolution_y: height value of the screen
        """

        screen_percentage = int(self.screen_percentage * 100)
        if screen_percentage <= 100 or screen_percentage >= 1:
            bpy.context.scene.render.resolution_percentage = screen_percentage
            bpy.context.scene.render.resolution_x = resolution_x
            bpy.context.scene.render.resolution_y = resolution_y

            print(f"Resolution set to: {resolution_x}x{resolution_y}")
            print(f"Resolution scale set to: {screen_percentage}%")

            self.message_to_log += f"Resolution set to: {resolution_x}x{resolution_y}\n"
            self.message_to_log += f"Resolution scale set to: {screen_percentage}%\n"
        else:
            raise ValueError("Invalid resolution screen!")


    def set_path_output_rendered(self, full_folder_path):
        """
            Function: set up the output path for rendering in the blend file

            Args:
                full_folder_path: destination path

            Note: This function is not used
        """

        # bpy.context.scene.render.filepath = full_folder_path
        print(f"Output path set to: {full_folder_path}")


    def open_file_blender(self, nome_file):
        """
            Function : open the blend file created during the setup_environment_blender

            Args:
                nome_file: define which blend file open
        """

        bpy.ops.wm.open_mainfile(filepath=self.output_blend_file+nome_file)
        print(f"Aperto il file: {nome_file}")

    def save_file_blender(self):
        """
            Function: saving the blend file

            Note: the new file is saved as outFinal
        """

        bpy.ops.wm.save_as_mainfile(filepath=self.output_blend_file+"outFinal.blend")

    def init_all_rendering_settings(self) -> None:

        """
            Function: initialize the device, engine, file format and the screen-resolution

        """

        my_screen =  smr()
        # my_outfolder = oft()
        self.set_engine_device()
        self.set_file_format()
        self.set_resolution_screen(my_screen.get_X(), my_screen.get_Y())
        # self.set_path_output_rendered(my_outfolder.get_path_output_rendering())


    def get_message(self) -> str:
        """
            Function: fetch the variable with all the strings to add to the log file

        """

        return self.message_to_log

