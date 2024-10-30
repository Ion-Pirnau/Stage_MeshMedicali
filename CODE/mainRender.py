from CODE.For_Blender_Functions.setup_environment_blender import SetEnvironmentBlender as seb
import os

dataname  = "cp2_fp_000201_tumoredbrain"
nome_log_file = "logInfo"

if __name__ == '__main__':

    my_setup = seb(dataname, nome_log_file, plane_on_base_size=1400)

    my_setup.change_location_scale_rotation_offset_energy(cubo_size=2,
                                                  rotation_cube=(0,0,0),
                                                  rotation_axes=(0,0,96),
                                                  location_axes=(0,0,0),
                                                  rotation_camera=(62, 0, 136),
                                                  offset_axes_camera=1,
                                                  offset_camera_light=0,
                                                  energy_light_at_camera=10,
                                                  location_plane_on_base=(0,0,-0.000925))

    my_setup.change_energy_light(light_front=0,
                                 light_back=2.5,
                                 light_right=0,
                                 light_left=1,
                                 light_top=1,
                                 light_bottom=0)

    # 0 : Cycles | 1: Eevee
    my_setup.setup_rendering_values(type_engine=0,type_device="GPU", n_samples=400,
                                    file_format="png",screen_percentage=1)

    my_setup.setup_the_environtment(nome_blend_file="unitsphere")



