from CODE.Process_Mesh.processing_functions import Processing_Mesh_PoC
from CODE.FunzioniUtili import utils as utl


class SetProcessingOnMesh:

    """
        Class used to communicate with the processing_function file
        Basically in this file it's just for organize the pipeline for processing the mesh
        The operations are:
        1. Check if the file exists
        2. Do the processing
        3. Create the log File
    """

    dataname = ""
    file_name = ""
    pm_poc = None
    vertices = 0.0
    normals = 0.0
    message_to_log = ""

    def __init__(self, dataname:str, logfile_name:str):
        self.dataname = dataname
        self.file_name = logfile_name


    def check_file_existence(self) -> bool:
        """
            Function: check if file exists

            Returns:
                bool
        """

        self.pm_poc = Processing_Mesh_PoC(self.dataname)
        valore_veritas = self.pm_poc.check_mesh_file()

        if valore_veritas:
           print("File Esiste: " + str(valore_veritas))
           self.vertices, self.normals, self.faces = self.pm_poc.load_vert_normal_face()
           self.message_to_log += f"Working on: {self.dataname}\n"
           if not utl.is_array_empty(self.normals):
               lenght_norm = len(self.normals)
           else:
               lenght_norm = 0


           self.message_to_log += (f"vertices: {len(self.vertices)}\nnormals: "
                                   f"{lenght_norm}\nfaces: {len(self.faces)}\n\n")
        else:
           print(f"File {self.dataname} non trovato")
           self.message_to_log = f"File {self.dataname} non trovato"
           utl.write_to_log(file_name=self.file_name, message=self.message_to_log, where_at=2)

           raise ValueError(f"File {self.dataname} non trovato")

        return valore_veritas



    def start_operation_processing(self, off_type="", eps=1.02, min_samples=1, depth=9, decimation_value=190000, scale_factor=1,
                                   scaling_type=0, nome_off_file_output="", is_readyto_repair=[False, False]) -> None:

        """
            Function: Do processing-operation on the mesh based on the arguments

            Args:
                eps - float value to define the distance between points to form a cluster
                min_samples - integer value to define min points to form a cluster
                depth - integer value to define the level of reconstruction of the mesh
                decimation_value - integer value used for decimate the mesh
                scale_factor - float value used to scale the mesh
                scaling_type - integer value to choose the type of scaling to apply to the mesh
                nome_off_file_output - string value to define the name of the output off file
                is_readyto_repair - [bool, bool] values to define when to do the repair or scaling operation

        """

        self.pm_poc.create_point_cloud()
        self.pm_poc.initialize_mesh()

        """
        Step 1: Removing zero area faces and component not connected
        
        """
        if not any(is_readyto_repair):
            print("Entrato PHASE 0")
            self.pm_poc.remove_zero_area_faces_call()
            self.pm_poc.controll_not_connected_component()
            self.pm_poc.remove_not_connected_component(distance=eps, n_punti_vicini=min_samples)


        """
        Step 2: Removing holes in the mesh
        
        """
        if is_readyto_repair[0]:
            print("Entrato PHASE 1 REPAIR")
            if off_type.lower() == 'off':
                self.pm_poc.reconstruction_no_normals(poisson_density=12300)
            self.pm_poc.repair_mesh(profondita=depth, n_decimation=decimation_value)

        if is_readyto_repair[1]:
            print("Entrato PHASE 1 SCALE")
            if scaling_type == 0:
                self.pm_poc.scaling_mesh(scaling_factor=scale_factor)
            elif scaling_type == 1:
                self.pm_poc.scaling_mesh_unit_box()
            elif scaling_type == 2:
                self.pm_poc.scaling_mesh_unit_sphere()

        self.pm_poc.save_mesh(nome=nome_off_file_output, path="INPUT_SOURCE/")

        self.create_message_log()


    def create_message_log(self) -> None:
        """
            Function: calling the Utils' method to write the logFile

        """
        self.message_to_log += self.pm_poc.get_message_log()
        utl.write_to_log(file_name=self.file_name, message=self.message_to_log, where_at=2)