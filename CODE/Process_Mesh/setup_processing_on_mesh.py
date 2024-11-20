from CODE.Process_Mesh.processing_functions import Processing_Mesh_PoC
from CODE.FunzioniUtili import utils as utl

# Class used to communicate with the processing_function file
# Basically in this file I just organize the pipeline for processing the mesh
# I do operations as:
# 1. Check if the file exists
# 2. Do the processing
# 3. Create the log File
class SetProcessingOnMesh:

    dataname = ""
    file_name = ""
    pm_poc = None
    vertices = 0.0
    normals = 0.0
    message_to_log = ""

    def __init__(self, dataname:str, logfile_name:str):
        self.dataname = dataname
        self.file_name = logfile_name


    def check_file_existence(self):

       self.pm_poc = Processing_Mesh_PoC(self.dataname)
       valore_veritas = self.pm_poc.check_mesh_file()

       if valore_veritas:
           print("File Esiste: " + str(valore_veritas))
           self.vertices, self.normals, self.faces = self.pm_poc.load_vert_normal_face()
           self.message_to_log += f"Working on: {self.dataname}\n"
           self.message_to_log += (f"vertices: {len(self.vertices)}\nnormals: "
                                   f"{len(self.normals)}\nfaces: {len(self.faces)}\n\n")
       else:
           print(f"File {self.dataname} non trovato")
           self.message_to_log = f"File {self.dataname} non trovato"
           utl.write_to_log(file_name=self.file_name, message=self.message_to_log, where_at=2)

           raise ValueError(f"File {self.dataname} non trovato")

       return valore_veritas

    def start_operation_processing(self, eps=1.02, min_samples=1, depth=9, decimation_value=190000, scale_factor=1,
                                   scaling_type=0, nome_off_file_output="", is_readyto_repair=False):

        self.pm_poc.create_point_cloud()
        self.pm_poc.initialize_mesh()

        """
        Step 1: Removing zero area faces and component not connected
        
        """
        if not is_readyto_repair:
            self.pm_poc.remove_zero_area_faces_call()
            self.pm_poc.controllo_not_connected_component()
            self.pm_poc.rimozione_not_connected_component(distance=eps, n_punti_vicini=min_samples)


        """
        Step 2: Removing holes in the mesh
        
        """
        if is_readyto_repair:
            self.pm_poc.repair_mesh(profondita=depth, n_decimation=decimation_value)

            if scaling_type == 0:
                self.pm_poc.scaling_mesh(scaling_factor=scale_factor)
            elif scaling_type == 1:
                self.pm_poc.scaling_mesh_unit_box()
            elif scaling_type == 2:
                self.pm_poc.scaling_mesh_unit_sphere()

        self.pm_poc.save_mesh(nome=nome_off_file_output, path="INPUT_SOURCE/")

        self.create_message_log()


    def create_message_log(self):
        self.message_to_log += self.pm_poc.get_message_log()
        utl.write_to_log(file_name=self.file_name, message=self.message_to_log, where_at=2)