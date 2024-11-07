from CODE.Process_Mesh.setup_processing_on_mesh import SetProcessingOnMesh
from CODE.For_Blender_Functions.setup_environment_blender import SetEnvironmentBlender as seb
from CODE.For_Blender_Functions.out_set_render import Process_Rendering_Frame
import os

# N.B. : prima di Eseguire il codice, modificare il valore della dimensione schermo in
# CODE/For_Blender_Functions/out_set_render.py
# nella classe ScreenMonitorResolution modificare i valori di: res_x=1920, res_y=1080



def get_user_input(testo, valore_originale):
    user_input = input(f"{testo} (valore predefinito: {valore_originale}): ")
    return user_input if user_input else valore_originale

def main_processed(dataname="", logfile_name="", valueeps=1.02, valuesample=5, valuedecimation=140000,
                   valuescalefactor=1.0, valuescalingtype=0, nomeofffile="fp", valueisready=False):

    my_setup = SetProcessingOnMesh(dataname=dataname, logfile_name=logfile_name)

    # print(dataname)
    if my_setup.check_file_existence():
        # Valori di Default : 1.02 5
        # Mesh Molto Aperte : eps alto ex: 1.5 e min_samples=1

        my_setup.start_operation_processing(eps=valueeps, min_samples=valuesample, depth=9,
                                            decimation_value=valuedecimation, scale_factor=valuescalefactor,
                                            scaling_type=valuescalingtype,
                                            nome_off_file_output=nomeofffile,
                                            is_ready_repair=valueisready)


def ask_and_write(file_path, nome_file, valid_choices):

    while True:
        try:
            risposta = int(input(f"Continua con la pipeline n° operazione ({'/'.join(map(str, valid_choices))}): "))
            if risposta in valid_choices:
                break
            else:
                print(f"Value not valid. Please, choose between {valid_choices}")

        except ValueError:
            print("Please, insert a correct value")

    with open(file_path, 'w') as file:
        file.write(str(risposta) + "\n")
        if risposta == 1 or risposta == 2 or risposta == 3:
            file.write(nome_file + "\n")

def read_and_fetch(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            if not lines:
                return None, None, None

            risposta = int(lines[0].strip())
            nome_prefix = lines[1].strip() if len(lines) > 1 else None


            if risposta == 0:
                valid_choices = [0, 1]
            elif risposta == 1:
                valid_choices = [1, 2]
            elif risposta == 2 or risposta == 3:
                valid_choices = [2, 3]
            else:
                valid_choices = []

            return risposta, nome_prefix, valid_choices

    except FileNotFoundError:
        print("Il file non esiste.")
        return None, None, [0, 1]


if __name__ == '__main__':

    dataname="000058_tumoredbrain"

    logfile_name_processing = "logTprocessing"
    logfile_name_blender = "logTBlender"
    file_path_choosen = "sceltaUserRiunione.txt"
    dir_name_scelta = "\log_sceltaUtente\\"

    # Scaling Type:
    # 0 : scaling su X Y e Z
    # 1 : scaling UNIT BOX
    # 2 : scaling UNIT SPHERE

    value_eps = 1.02
    value_minsamples = 5
    value_decimation = 140000
    value_scalefactor = 1
    value_scalingtype = 0
    value_isreadyrepair = False
    name_off_file = "fp"
    input_user = ""

    # if os.path.exists(os.getcwd()+"\log_processing"):
    #     print("Esiste")
    # else:
    #     print("Non Esiste")


    choosen_path_name = os.getcwd()+dir_name_scelta+file_path_choosen
    continue_pipeline, other_file_name, valid_choice = read_and_fetch(choosen_path_name)
    dataname = str(other_file_name) + dataname if other_file_name else dataname

    print(f"Working on: {dataname}")

    if continue_pipeline is None or continue_pipeline == 0 or continue_pipeline == 1:
        print("MESH's PROCESSING")

    if continue_pipeline is None or continue_pipeline == 0:
        value_eps = float(get_user_input("Inserisci il valore eps", 1.02))
        value_minsamples = int(get_user_input("Inserisci il valore min_samples", 5))
        value_decimation = int(get_user_input("Inserisci il valore decimation", 140000))
        # value_isreadyrepair = get_user_input("Vuoi eseguire la riparazione (True/False)?",
        #                                      "False").lower() == 'true'
        name_off_file = get_user_input("Inserisci il nome del file off", "fp")
    elif continue_pipeline == 1:
        name_off_file = get_user_input("Inserisci il nome del file off", "fp")
        value_scalefactor = float(get_user_input("Inserisci il valore scale_factor", 1))
        value_scalingtype = int(get_user_input("Inserisci il tipo di scaling", 0))
        value_isreadyrepair = True

    if continue_pipeline is None or continue_pipeline == 0 or continue_pipeline == 1:
        print(dataname)
        print(value_isreadyrepair)
        main_processed(dataname=dataname, logfile_name=logfile_name_processing, valueeps=value_eps, valuesample=value_minsamples,
                   valuedecimation=value_decimation, valuescalefactor=value_scalefactor,
                   valuescalingtype=value_scalingtype, nomeofffile=name_off_file, valueisready=value_isreadyrepair)



    name_off_file = name_off_file + "_"
    if continue_pipeline == 2:
        name_off_file = ""
        print("PREPARATION FOR BLENDER RENDERING")

        my_setup = seb(dataname, logfile_name_blender, plane_on_base_size=1400)
        my_setup.change_location_scale_rotation_offset_energy(cubo_size=1,
                                                              rotation_cube=(0, 0, 0),
                                                              rotation_axes=(0, 0, 96),
                                                              location_axes=(0, 0, 0),
                                                              rotation_camera=(58.56, 0, 136),
                                                              offset_axes_camera=1,
                                                              offset_camera_light=0,
                                                              energy_light_at_camera=1.5,
                                                              location_plane_on_base=(0, 0, -0.000925))

        # Ci sono 4 ligh-set mode:
        # 0 : scelta Utente
        # 1 : predefinita
        # 2 : predefinita
        # 3 : predefinita - usarla solo per il wireframe
        my_setup.change_energy_light(light_front=0,
                                     light_back=3,
                                     light_right=0,
                                     light_left=2.5,
                                     light_top=1.5,
                                     light_bottom=0,
                                     light_set=1)

        # Tipo Material:
        # 0 : Giallo-Opaco
        # 1 : Trasparente / Glass
        # 2 : Wireframe
        # 3 : Custom
        my_setup.setup_materials(material_value=0)

        # 0 : Cycles | 1: Eevee
        my_setup.setup_rendering_values(type_engine=0, type_device="GPU", n_samples=400,
                                        file_format="png", screen_percentage=1)

        my_setup.setup_the_environtment(nome_blend_file="unitbox")

    if continue_pipeline == 3:
        name_off_file = ""
        blender_path = r"C:\Program Files\Blender Foundation\Blender 4.2\blender-launcher.exe"
        print("OUTPUT BLENDER RENDERING")
        out_render = Process_Rendering_Frame(blender_path)
        out_render.get_parent_dirname()
        out_render.init_full_command_pipeline(nome_file_image="prova")
        out_render.start_execution()


    if other_file_name is None:
        other_file_name = ""
    ask_and_write(choosen_path_name, name_off_file+other_file_name, valid_choice)
