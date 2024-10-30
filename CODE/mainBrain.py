from CODE.Process_Mesh.setup_processing_on_mesh import SetProcessingOnMesh

dataname="000058_tumoredbrain"
logfile_name="loginfo"

# Quando si esegue il mainBrain la prima esecuzione effettuo le seguenti operazioni:
#   Rimozione Facce ad Area Nulla
#   Rimozione Componenti Connesse
# Il file di Ouput deve essere spostato in input e su questo effettuare le ultime operazioni:
#  Ricostruzione
#  Scaling

# Scaling Type:
    # 0 : scaling su X Y e Z
    # 1 : scaling UNIT BOX
    # 2 : scaling UNIT SPHERE

if __name__ == '__main__':
    my_setup = SetProcessingOnMesh(dataname=dataname, logfile_name=logfile_name)

    if my_setup.check_file_existence():
        # Default: 1.02 5
        # Per Mesh Molto Aperte : eps alto ex: 1.5 e min_samples=1
        my_setup.start_operation_processing(eps=1.02, min_samples=5, depth=9,
                                            decimation_value=140000, scale_factor=1, scaling_type=0,
                                            nome_off_file_output="cp",
                                            is_ready_repair=True)