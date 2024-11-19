from CODE.Process_Mesh.setup_processing_on_mesh import SetProcessingOnMesh
from CODE.For_Blender_Functions.setup_environment_blender import SetEnvironmentBlender as seb
from CODE.For_Blender_Functions.out_set_render import Process_Rendering_Frame
import os
import json


# Get the input from the user, this is a default function for getting the user input
def get_user_input(testo, valore_originale):
    user_input = input(f"{testo} (valore predefinito: {valore_originale}): ")
    return user_input if user_input else valore_originale


# Initialization of the class for Processing the Mesh
def main_processed(dataname="", logfile_name="", valueeps=1.02, valuesample=5, valuedecimation=140000,
                   valuescalefactor=1.0, valuescalingtype=0, nomeofffile="processed") -> None:

    my_setup = SetProcessingOnMesh(dataname=dataname, logfile_name=logfile_name)

    # print(dataname)
    if my_setup.check_file_existence():
        # Valori di Default : 1.02 5
        # Mesh Molto Aperte : eps alto ex: 1.5 e min_samples=1

        my_setup.start_operation_processing(eps=valueeps,
                                            min_samples=valuesample,
                                            depth=9,
                                            decimation_value=valuedecimation,
                                            scale_factor=valuescalefactor,
                                            scaling_type=valuescalingtype,
                                            nome_off_file_output=nomeofffile)

def load_config(config_file='config.json') ->dict:
    """
    Import the parameters for the pipline, more details in ReadMe
    """
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

if __name__ == '__main__':

    # Function to load the configuration from a JSON file
    param=load_config()
    dataname="000199_tumoredbrain"

    logfile_name_processing = r"logTprocessing"
    logfile_name_blender = r"logTBlender"
    file_path_choosen = r"\sceltaUserRiunione.txt"
    dir_name_scelta = r"\log_sceltaUtente"

    # Scaling Type:
    # 0 : scaling su X Y e Z
    # 1 : scaling UNIT BOX
    # 2 : scaling UNIT SPHERE

    input_user = "" #@ION questa variabile che senso ha?

    # if os.path.exists(os.getcwd()+"\log_processing"):
    #     print("Esiste")
    # else:
    #     print("Non Esiste")


    #choosen_path_name = os.getcwd()+dir_name_scelta+file_path_choosen
    #param["dataname"] = str(other_file_name) + param["dataname"] if other_file_name else param["dataname"] 

    # So at the beggining of the pipeline till the phase 1 the programm is processing the mesh
    if param.get("processing"):

        print("MESH's PROCESSING")
        print(param.get("dataname"))

        main_processed(dataname=param.get("dataname"), logfile_name=logfile_name_processing, valueeps=param.get("value_eps"), valuesample=param.get("value_minsamples"),
                   valuedecimation=param.get("value_decimation"), valuescalefactor=param.get("value_scalefactor"),
                   valuescalingtype=param.get("value_scalingtype"), nomeofffile=param.get("name_off_file"))


    # On the phase 2 : the programm is preparing for a Blender Rendering
    param["name_off_file"] = param.get("name_off_file") + "_"
    if param.get("blender_ex"):
        param["name_off_file"] = ""
        print("PREPARATION FOR BLENDER RENDERING")
    # The class abr. seb - create a blend file with the mesh and a set-up environment for a better rendering experience
    # The user can change any value he wants from the code, just by looking the code below
        my_setup = seb(param["dataname"], logfile_name_blender, plane_on_base_size=1400)
        my_setup.change_environment_settings(cube_size=1.5,
                                            cube_rotation=(0, 0, 0),
                                            axes_rotation=(0, 0, -180.22),
                                            axes_location=(-0.83, -1.0589, 0),
                                            camera_rotation=(74.04, 0.65194, 137.58),
                                            camera_axes_offset=1,
                                            camera_light_offset=0,
                                            light_energy=1.5,
                                            base_plane_location=(0, 0, -0.000925)
                                            )


        # Four Light-set mode:
        # 0 : Choose by User
        # 1 : mode - 6 light
        # 2 : mode - 6 light
        # 3 : mode - only for Wireframe Material
        # 4 : mode - 1 light
        my_setup.change_energy_light(light_front=0,
                                     light_back=3,
                                     light_right=0,
                                     light_left=2.5,
                                     light_top=1.5,
                                     light_bottom=0,
                                     light_set=1
                                     )


        # Tipo Material:
        # 0 : Giallo-Opaco
        # 1 : Trasparente / Glass
        # 2 : Wireframe
        # 3 : Custom
        # 4 : Full-Transparency

        # Tipo Material Plane:
        # 0 : Bianco
        # 1 : Bianco con Emission - better for Full-Transparency Material

        # RBG VALUE TESTED: 0.586, 0.663, 0.612 ------- 0.713, 0.836, 1
        # color_trasp_bsdf=[], color_diff_bsdf=[] only for the FULL-TRANSPARENCY Material
        my_setup.set_materials(material_value=3, material_plane_value=1,
                                 color_trasp_bsdf=[], color_diff_bsdf=[])


        # Choose which Wall should appear in the world (Default all True)
        my_setup.setup_walls(wall_front=False, wall_right=False)

        # 0 : Cycles | 1: Eevee
        my_setup.set_rendering_values(type_engine=0, type_device="GPU", n_samples=400,
                                        file_format="png", screen_percentage=1)

        my_setup.set_the_environment(nome_blend_file="test_comment")

    # On the phase 3: final phase of the pipeline, the Output Blender Rendering
    # Thought the subprocess lib the programm execute a prompt command on the computer and run blender on background
    # The output? The blender rendering file, it can be a png or a jpeg based on the file_format above
    if param.get("rendering"):
        param["name_off_file"] = ""
        blender_path = r"C:\Program Files\Blender Foundation\Blender 4.2\blender-launcher.exe"
        print("OUTPUT BLENDER RENDERING")
        out_render = Process_Rendering_Frame(blender_path)
        out_render.get_parent_dirname()
        out_render.init_full_command_pipeline(nome_file_image=param.get("test_name"))
        out_render.start_execution()

