from CODE.Process_Mesh.setup_processing_on_mesh import SetProcessingOnMesh
from CODE.For_Blender_Functions.setup_environment_blender import SetEnvironmentBlender as seb
from CODE.For_Blender_Functions.out_set_render import Process_Rendering_Frame
import os
import json


"""
Initialization of the class for Processing the Mesh

"""
def main_processed(dataname="", logfile_name="", valueeps=1.02, valuesample=5, valuedecimation=140000,
                   valuescalefactor=1.0, valuescalingtype=0, nomeofffile="processed", is_readyto_repair=False) -> None:

    my_setup = SetProcessingOnMesh(dataname=dataname, logfile_name=logfile_name)

    if my_setup.check_file_existence():
        my_setup.start_operation_processing(eps=valueeps,
                                            min_samples=valuesample,
                                            depth=9,
                                            decimation_value=valuedecimation,
                                            scale_factor=valuescalefactor,
                                            scaling_type=valuescalingtype,
                                            nome_off_file_output=nomeofffile,
                                            is_readyto_repair=is_readyto_repair)

def load_config(config_file='config.json') -> dict:
    """
    Import the parameters for the pipline, more details in ReadMe

    """
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


def write_config(data, config_file='config.json') -> bool:
    """
       Export the parameters for the pipline next PHASE

    """
    try:
        with open(config_file, 'w') as file:
            json.dump(data, file, indent=4)

        return True
    except Exception as e:
        print(f"Error occurred while modifying the JSON: {e}")
        return False

if __name__ == '__main__':

    """
    Function to load the configuration from a JSON file
    
    """
    param=load_config()
    dataname="000199_tumoredbrain"

    logfile_name_processing = r"logTprocessing"
    logfile_name_blender = r"logTBlender"


    """
    At the beginning of the phase 0 till the phase 1 the programm is processing the mesh
    
    """
    if param.get("processing_0"):

        print("MESH's PROCESSING")
        print(param.get("dataname"))

        main_processed(dataname=param.get("dataname"), logfile_name=logfile_name_processing,
                valueeps=param.get("value_eps"), valuesample=param.get("value_minsamples"),
                valuedecimation=param.get("value_decimation"), valuescalefactor=param.get("value_scalefactor"),
                valuescalingtype=param.get("value_scalingtype"), nomeofffile=param.get("name_off_file"),
                is_readyto_repair=param.get("processing_1"))

        param["dataname"] = param.get("name_off_file") + "_" + param.get("dataname")
        result = write_config(data=param)
        print(f"Succeed on Writing JSON's file: {result}")




    """
        On the phase 2 : the programm is preparing for a Blender Rendering
        The class abr. seb - create a blend file with the mesh and a set-up environment for a better rendering experience
        The user can change any value he wants from the code, just by looking the code below
        
    """

    if param.get("pipeline_operation") == 2:
        print("PREPARATION FOR BLENDER RENDERING")
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



        """ 
            Four Light-set mode:
            # 0 : Customize by the User
            # 1 : mode - 6 light
            # 2 : mode - 6 light
            # 3 : mode - only for Wireframe Material
            # 4 : mode - 1 light
            
        """
        my_setup.change_energy_light(light_front=0,
                                     light_back=3,
                                     light_right=0,
                                     light_left=2.5,
                                     light_top=1.5,
                                     light_bottom=0,
                                     light_set=1
                                     )




        """
            Tipo Material:
                0 : Dull Yellow
                1 : Transparent / Glass
                2 : Wireframe
                3 : Custom
                4 : Full-Transparency
    
            Tipo Material Plane:
                0 : White
                1 : White with Emission - better for Full-Transparency Material
    
            RBG VALUE TESTED: 0.586, 0.663, 0.612 ------- 0.713, 0.836, 1
            color_transp_bsdf=[], color_diff_bsdf=[] only for the FULL-TRANSPARENCY Material
        
        """

        my_setup.set_materials(material_value=3, material_plane_value=1,
                                 color_trasp_bsdf=[], color_diff_bsdf=[])

        """
        Type Engine:
            0 : Cycles
            1 : Eevee
        
        """
        my_setup.set_rendering_values(type_engine=0, type_device="GPU", n_samples=400,
                                        file_format="png", screen_percentage=1)

        my_setup.set_the_environment(nome_blend_file=param.get("blend_file_name"))




    """
        On the phase 3: final phase of the pipeline, the Output Blender Rendering
        Thought the subprocess lib the programm execute a prompt command on the computer and run blender on background
        OUTPUT: The blender rendering file, it can be a PNG or a JPEG based on the file_format above
        
    """
    if param.get("pipeline_operation") == 3:
        param["name_off_file"] = ""
        blender_path = r"C:\Program Files\Blender Foundation\Blender 4.2\blender-launcher.exe"
        print("OUTPUT BLENDER RENDERING")
        out_render = Process_Rendering_Frame(blender_path)
        out_render.get_parent_dirname()
        out_render.init_full_command_pipeline(nome_file_image=param.get("test_name"))
        out_render.start_execution()



