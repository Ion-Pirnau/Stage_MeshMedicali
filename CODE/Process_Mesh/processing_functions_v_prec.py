from CODE.FunzioniUtili import utils as utl
import numpy as np
import open3d as o3d
from CODE.Function_for_Process import area_faccia_nulla as afn, detect_repair_mesh as drm, scaling_mesh as s_mesh, \
    rimozione_ncc as r_ncc

class Processing_Mesh_PoC:

    extension_file = ".off"
    input_path = "INPUT_SOURCE/"
    vertex = 0.0
    normal = 0.0
    face = 0
    nvert = 0
    pcd = o3d.geometry.PointCloud()
    mesh = o3d.geometry.TriangleMesh()

    def __init__(self, dataname: str):
        self.dataname = dataname

    def check_mesh_file(self):
        result =  utl.check_file_exists(self.input_path + self.dataname + self.extension_file)
        print("Controllo esistenza file: "+ self.dataname + self.extension_file)
        return result

    def load_vert_normal_face(self):
        vertices, normals, faces, n_verts = utl.load_off_with_loadtxt(self.input_path + self.dataname + self.extension_file)

        vertices = utl.convert_array_tofloat64(vertices)
        normals = utl.convert_array_tofloat64(normals)
        self.vertex = vertices
        self.normal = normals
        self.face = faces
        self.nvert = n_verts
        return vertices, normals, faces

    def create_point_cloud(self):
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)
        utl.visualize_3d_screen(self.pcd, self.dataname)

    def remove_zero_area_faces(self):
        # Rimuovi le facce con area nulla
        self.face, n_facesremoved = afn.remove_zero_area_faces(self.vertex, self.face)
        print("Numero facce rimosse: " + str(n_facesremoved))

    def scaling_mesh(self, scaling_factor=1.0):
        self.vertex, self.normal = s_mesh.scale_mesh(self.vertex, self.normal, scaling_factor)
        self.vertex = utl.convert_array_tofloat64(self.vertex)
        self.normal = utl.convert_array_tofloat64(self.normal)
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)
        utl.visualize_3d_screen(self.pcd, "Scaled Point Cloud")

    def save_mesh(self, nome=""):
        utl.save_off_format(self.dataname + nome + self.extension_file, self.vertex, self.normal, self.face)

    def initialize_mesh(self):
        self.mesh = utl.initialize_mesh(self.vertex, self.normal, self.face)

    def visualize_mesh(self, nome=""):
        utl.visualize_3d_screen(self.mesh, name_window=nome)

    def repair_mesh(self, profondita=9, n_decimation=190000):
        #Modo più semplice libreria Pymesh

        holes = drm.find_holes_in_mesh(self.mesh)

        print("Ci sono: " + str(len(holes)) + " buchi nella mesh")
        # Converti np.int32 a int
        # holes_int contiene gli spigoli/edges (coppia di indici che fanno riferimento ai vertici)
        # holes_int = [[(int(edge[0]), int(edge[1])) for edge in hole] for hole in holes]

        mesh_poisson, density_mesh = drm.ricostruzione_mesh_poisson(self.pcd, profondita)

        # Estrai i punti (vertici) dalla mesh
        punti_estratti = np.asarray(mesh_poisson.vertices)

        # Estrai le normali dei vertici dalla mesh
        normali_estratte = np.asarray(mesh_poisson.vertex_normals)

        print("Punti Poisson: " + str(len(punti_estratti)))
        pcd_da_poisson = utl.create_point_cloud(punti_estratti, normali_estratte)

        utl.visualize_3d_screen(pcd_da_poisson, "PCD DA POISSON")

        mesh_decimated = drm.decimate_mesh_and_process(mesh_poisson, n_decimation)
        holes = drm.find_holes_in_mesh(mesh_decimated)
        print("Ci sono: " + str(len(holes)) + " buchi nella mesh")
        print("Punti Poisson DECIMATED: " + str(len(np.asarray(mesh_decimated.vertices))))

        self.vertex = np.asarray(mesh_decimated.vertices)
        self.normal = np.asarray(mesh_decimated.vertex_normals)
        self.face = np.asarray(mesh_decimated.triangles)

        pcd_da_poisson_decimated = utl.create_point_cloud(self.vertex, self.normal)
        utl.visualize_3d_screen(pcd_da_poisson_decimated, "PCD DA POISSON DECIMATED")

    def rimozione_not_connected_component(self, densita=1.02, n_punti_vicini=1):
        filtered_points, face_list = r_ncc.find_cluster_connected(self.pcd, self.face, densita, n_punti_vicini)
        self.vertex, self.normal = utl.extract_vertices_and_normals(filtered_points)
        self.face = np.array(face_list)
        utl.visualize_3d_screen(filtered_points, "Filtered Points " + self.dataname)
        self.controllo_not_connected_component()

    def controllo_not_connected_component(self):
        self.initialize_mesh()
        island_on_mesh = r_ncc.find_islands_in_mesh(self.mesh)

        # Stampa l'array delle isole
        # for i, island in enumerate(island_on_mesh):
        #     island = [int(vertex) for vertex in island]
        #     print(f"Isola {i+1}: {island}")
        main_island = max(island_on_mesh, key=len)  # La mesh principale è l'isola più grande
        other_islands = [island for island in island_on_mesh if island != main_island]
        print("Ci sono: " + str(len(other_islands)) + " isole nella mesh")
        # # for i, island in enumerate(other_islands):
        # #     island = [int(vertex) for vertex in island]
        # #     print(f"Isola {i + 1}: {island}")
        # #
        other_islands = [[int(elemento) for elemento in riga] for riga in other_islands]
        print(other_islands)
