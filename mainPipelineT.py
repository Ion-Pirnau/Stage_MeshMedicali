from CODE.Process_Mesh.setup_processing_on_mesh import SetProcessingOnMesh
from CODE.For_Blender_Functions.setup_environment_blender import SetEnvironmentBlender as seb
from CODE.For_Blender_Functions.out_set_render import Process_Rendering_Frame

import json


"""
Initialization of the class for Processing the Mesh

"""
def main_processed(type_off_file:str="", dataname:str="", logfile_name:str="", valueeps:float=1.02,
                   valuesample:float=5, valuedecimation:int=140000,
                   valuescalefactor:float=1.0, valuescalingtype:int=0, nomeofffile:str="processed",
                   is_readyto_repair=[False, False]) -> None:

    """
        Function: set up values for processing the mesh

        Args:
            type_off_file : string value, define the off file type: OFF or NOFF
            dataname : string value, define the name of the file the program is going to work on
            logfile_name : string value, define the name of the txt file to save operations that has been done
            valueeps : float value, define the distance between points to form a cluster
            valuesample : integer value, define the min points to form a cluster
            valuedecimation : integer value to decimate the mesh
            valuescalefactor : float value, define the value to scale the mesh
            valuescalingtype : integer value, define the type of scaling to apply on the mesh
            nomeofffile : string value, define the name of the output file generated at the end of the processing
            is_readyto_repair : [bool, bool] value, define the type of operation to apply to the mesh

        Returns:
            bool

    """

    my_setup = SetProcessingOnMesh(dataname=dataname, logfile_name=logfile_name)

    if my_setup.check_file_existence():
        my_setup.start_operation_processing(off_type=type_off_file, eps=valueeps,
                                            min_samples=valuesample,
                                            depth=9,
                                            decimation_value=valuedecimation,
                                            scale_factor=valuescalefactor,
                                            scaling_type=valuescalingtype,
                                            nome_off_file_output=nomeofffile,
                                            is_readyto_repair=is_readyto_repair)

def load_config(config_file='config.json') -> dict:
    """
        Function: Import the parameters for the pipline, more details in ReadMe

        Args:
            config_file : string value, define the name of config file

        Returns:
            dict

    """
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


def write_config(data, config_file='config.json') -> bool:
    """
       Function: Export the parameters for the pipline next PHASE

       Args:
           data : data to write on the JSON file
           config_file : string value, name of the config file where to write the data

       Returns:
           bool

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

    logfile_name_processing = param.get("logfile_name_processing")
    logfile_name_blender = param.get("logfile_name_blender")


    """
    At the beginning of the phase 0 till the phase 1 the programm is processing the mesh
    
    """
    if param.get("processing_0"):

        print("MESH's PROCESSING")
        print(param.get("dataname"))

        main_processed(type_off_file=param.get("type_off_file"),dataname=param.get("dataname"),
                logfile_name=logfile_name_processing,
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
    if param.get("blend_file_ex"):
        print("PREPARATION FOR BLENDER RENDERING")
        my_setup = seb(param["dataname"], logfile_name_blender, plane_on_base_size=param.get("plane_on_base_size"))
        my_setup.change_environment_settings(cube_size=param.get("cube_size"),
                                            cube_rotation=param.get("cube_rotation"),
                                            axes_rotation=param.get("axes_rotation"),
                                            axes_location=param.get("axes_location"),
                                            camera_rotation=param.get("camera_rotation"),
                                            camera_axes_offset=param.get("camera_axes_offset"),
                                            camera_light_offset=param.get("camera_light_offset"),
                                            light_energy=param.get("light_energy_at_camera"),
                                            base_plane_location=param.get("base_plane_location")
                                            )



        """ 
            Four Light-set mode:
            # 0 : Customize by the User
            # 1 : mode - 6 light
            # 2 : mode - 6 light
            # 3 : mode - for Wireframe Material or Sun-Light
            
        """
        my_setup.change_energy_light(light_front=param.get("light_front"),
                                     light_back=param.get("light_back"),
                                     light_right=param.get("light_right"),
                                     light_left=param.get("light_left"),
                                     light_top=param.get("light_top"),
                                     light_bottom=param.get("light_bottom"),
                                     light_set=param.get("light_set")
                                     )

        my_setup.setup_sun_light(sun_strength=param.get("sun_strength"), sun_angle=param.get("sun_angle"))


        """
            Tipo Material:
                0 : Dull Yellow
                1 : Transparent / Glass
                2 : Wireframe
                3 : Custom
                4 : Full-Transparency
                5 : ColorMap's Values:
                    - 0 : Propagation from Origin
                    - 1 : Curvature Analysis
                    - 2 : Heat-Map on Axis
                    - 3 : Deformation on Surface
                6 : ColorMaps - Scalar Value
    
            Tipo Material Plane:
                0 : White
                1 : White with Emission - better for Full-Transparency Material
    
            RBG VALUE TESTED: 0.586, 0.663, 0.612 ------- 0.713, 0.836, 1
        
        """

        my_setup.set_materials(material_value=param.get("material_value"),
                               material_plane_value=param.get("material_plane_value"),
                               color_map_value=param.get("color_map_value"), hex_color=param.get("hex_color"),
                               color_transp_bsdf=param.get("color_transp_bsdf"),
                               color_diff_bsdf=param.get("color_diff_bsdf"))


        my_setup.setup_walls(wall_front=param.get("wall_front"), wall_back=param.get("wall_back"),
                             wall_right=param.get("wall_right"), wall_left=param.get("wall_left"))


        my_setup.setup_scalarfield(param.get("name_scalar_field_txt"),
                                   param.get("name_scalar_labels_txt"), param.get("scalar_field"))


        my_setup.set_rendering_values(type_engine=param.get("type_engine"), type_device=param.get("type_device"),
                                      n_samples=param.get("n_samples"), file_format=param.get("file_format"),
                                      screen_percentage=param.get("screen_percentage"))

        my_setup.set_the_environment(nome_blend_file=param.get("blend_file_name"))




    """
        On the phase 3: final phase of the pipeline, the Output Blender Rendering
        Thought the subprocess lib the programm execute a prompt command on the computer and run blender on background
        OUTPUT: The blender rendering file, it can be a PNG or a JPEG based on the file_format above
        
    """
    if param.get("render_file_ex"):
        print("OUTPUT BLENDER RENDERING")
        out_render = Process_Rendering_Frame(path_blender_exe=param.get("blender_path_execute"))
        out_render.get_parent_dirname()
        out_render.init_full_command_pipeline(nome_file_image=param.get("render_file_name"))
        out_render.start_execution()
