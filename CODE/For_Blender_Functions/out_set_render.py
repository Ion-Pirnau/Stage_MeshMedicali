import os
import subprocess
import pyautogui

# This file has few classes in it
# 1. Screen Size : Monitor Resolution
# 2. Output Render : the output where the rendering image should go
# 3. Process Rendering : through the subprocess lib, the class run the command to run blender in background
# and rendering the image


# PROBLEMS: there are no good libs, for now, that work better for Win or MAC
# the res_x and res_y. should be changed manually
# THINKING on new IDEAS
class ScreenMonitorResolution:

    def __init__(self,):
        self.screenWidth, self.screenHeight  = self.get_screen_dimension()


    def get_screen_dimension(self) -> tuple[int, int]:
        """
        Gets the user screen dimensions (width and height).

        Returns:
            tuple[int, int]: A tuple containing the screen width and height in pixels.
        """
        screenWidth, screenHeight = pyautogui.size()
        print("the value for width is:", screenWidth, "the value for Height is:", screenHeight)
        return (screenWidth,screenHeight)
    
    def get_X(self) -> int:
        return self.screenWidth
    
    def get_Y(self) -> int:
        return self.screenHeight




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

    def init_full_command_pipeline(self, nome_file_image) -> None:
        blend_file_path_name = self.get_current_workfolder() + self.blend_file_path + "\\outFinal.blend"
        image_output_path_name = self.get_current_workfolder() + self.render_path_folder + f"\\{nome_file_image}"

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


    # The function that run the actual command, the result is used just to be sure if everything is done correctly
    # The RETURN_CODE:
    # 0: good
    # otherwise: bad
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
