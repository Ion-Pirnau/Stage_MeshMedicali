import os
import subprocess
import pyautogui


"""
This file has few classes in it
    1. Screen Size : Monitor Resolution
    2. Output Render : the output where the rendering image should go
    3. Process Rendering : through the subprocess lib, the class run the command to run blender in background
        and rendering the image

"""


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
    """
    Class: getting the current work-folder path and the save + the directory for the Image Rendering

    """

    def __init__(self) -> None:
        self.render_path_folder = '\IMAGE_RENDERED'
        pass

    def get_current_workfolder(self) -> str:
        """
            Function: get current work-folder

            Returns:
                str

        """
        return os.getcwd()

    def get_path_output_rendering(self) -> str:
        """
            Function: get current work-folder

            Returns:
                 str

               """
        return self.get_current_workfolder()+self.render_path_folder+'\\'



class Process_Rendering_Frame:

    command = []


    def __init__(self, path_blender_exe) -> None:
        self.path_blender_exe = path_blender_exe
        self.render_path_folder = '\IMAGE_RENDERED'
        self.blend_file_path = '\BLEND_FILE_OUTPUT'


    def init_simple_command(self):
        """
            Function: init a simple command

        """

        self.command = [
            self.path_blender_exe
        ]

    def init_full_command(self, nome_file_image):

        """
            Function: init a test command

            Args:
                nome_file_image : name of the images that is going to be rendered

        """

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

        """
            Function: init full command to use

            Args:
                nome_file_image : name of the images that is going to be rendered

        """

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

    def get_current_workfolder(self) -> str:

        """
            Function : get current work-folder

            Returns:
                str

        """

        return os.getcwd()

    def get_parent_dirname(self) -> str:

        """
            Function: get current directory name

            Returns:
                str

        """
        parent_directory = os.path.dirname(self.get_current_workfolder())
        return parent_directory



    def start_execution(self):

        """
            Function: run the actual command, the result is used just to be
            sure if everything is done correctly

            The RETURN_CODE:
                0 = good
                otherwise = bad

        """

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
