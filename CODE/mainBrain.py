from CODE.Process_Mesh.processing_functions import Processing_Mesh_PoC

dataname="000059_tumoredbrain_zero_area_faces_ncc"

# INZIO MAIN
if __name__ == '__main__':
    my_pm = Processing_Mesh_PoC(dataname)
    if my_pm.check_mesh_file():
        print("File Esiste: " + str(my_pm.check_mesh_file()))
        vertex, normal, faces = my_pm.load_vert_normal_face()

        my_pm.create_point_cloud()
        my_pm.initialize_mesh()

        # my_pm.controllo_not_connected_component()
        # my_pm.visualize_mesh(nome="Mesh")

        # my_pm.scaling_mesh(0.5)
        my_pm.repair_mesh(profondita=9, n_decimation=160000)
        my_pm.controllo_not_connected_component()
        # my_pm.remove_zero_area_faces()
        # my_pm.initialize_mesh()
        # my_pm.visualize_mesh(nome="Mesh Riparata")

        # my_pm.rimozione_not_connected_component()
        # my_pm.visualize_mesh(nome="Mesh Filtrata")
        # my_pm.save_mesh(nome="_riparata")
    else:
        print(f"File {dataname} non trovato")