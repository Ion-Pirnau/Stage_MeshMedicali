import os
import subprocess

class ScreenMonitorResolution:

    def __init__(self, res_x=1920, res_y=1080):
        self.res_x = res_x
        self.res_y = res_y


    def get_X(self):
        return self.res_x

    def get_Y(self):
        return self.res_y







class OutputFileRender:
    render_path_folder = '\IMAGE_RENDERED'

    def __init__(self):
        pass

    def get_current_workfolder(self):
        return os.getcwd()

    def get_path_output_rendering(self):
        return self.get_current_workfolder()+self.render_path_folder+'\\'



class Process_Rendering_Frame:
    render_path_folder = '\IMAGE_RENDERED'
    blend_file_path = '\BLEND_FILE_OUTPUT'
    log_file_render = '\log_blender'

    command = []


    def __init__(self, path_blender_exe):
        self.path_blender_exe = path_blender_exe

    def init_simple_command(self):
        self.command = [
            self.path_blender_exe
        ]

    def init_full_command(self, nome_file_image):

        blend_file_path_name = self.get_parent_dirname()+self.blend_file_path+"\\outFinal.blend"
        image_output_path_name = self.get_parent_dirname()+self.render_path_folder+f"\\{nome_file_image}"

        self.command = [
            self.path_blender_exe,
            "-b",
            blend_file_path_name,
            "-o",
            image_output_path_name,
            "-f", "1"
        ]

        # print(self.command)

    def get_current_workfolder(self):
        return os.getcwd()

    def get_parent_dirname(self):
        parent_directory = os.path.dirname(self.get_current_workfolder())
        # print(f"Cartella superiore: {parent_directory}")
        return parent_directory

    def start_execution(self):
        result = subprocess.run(self.command, capture_output=True, text=True, check=True)

        if not result.stdout == '':
            print("Output:")
            print(result.stdout)
        if not result.stderr == '':
            print("Errori:")
            print(result.stderr)

        print("Codice di ritorno:")
        print(result.returncode)
        print("Rendering Completato!")
