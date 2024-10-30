from CODE.For_Blender_Functions.out_set_render import Process_Rendering_Frame

blender_path = r"C:\Program Files\Blender Foundation\Blender 4.2\blender-launcher.exe"

if __name__ == '__main__':

    out_render = Process_Rendering_Frame(blender_path)
    out_render.init_full_command(nome_file_image="out000201_")
    out_render.start_execution()