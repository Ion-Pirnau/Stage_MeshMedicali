from CODE.FunzioniUtili import utils as utl
import numpy as np
import open3d as o3d


"""
Class: Does the actual processing operation on the mesh

"""
class Processing_Mesh_PoC:

    extension_file = ".off"
    input_path = "INPUT_SOURCE/"
    vertex = 0.0
    normal = 0.0
    face = 0
    nvert = 0
    pcd = o3d.geometry.PointCloud()
    mesh = o3d.geometry.TriangleMesh()
    message_to_log = ""
    islands_on_mesh = None

    def __init__(self, dataname: str) -> None:
        self.dataname = dataname


    def check_mesh_file(self) -> bool:
        """
            Check if the file exists

        """
        result =  utl.check_file_exists(self.input_path + self.dataname + self.extension_file)
        print("Controllo esistenza file: "+ self.dataname + self.extension_file)
        return result



    def load_vert_normal_face(self):
        """
            Read from the file the values:
            1. vertices
            2. normals
            3. faces

        """
        vertices, normals, faces, n_verts = utl.load_off_with_loadtxt(self.input_path + self.dataname + self.extension_file)

        vertices = utl.convert_array_tofloat64(vertices)
        normals = utl.convert_array_tofloat64(normals)
        self.vertex = vertices
        self.normal = normals
        self.face = faces
        self.nvert = n_verts
        return vertices, normals, faces



    def create_point_cloud(self) -> None:
        """
            Create a point cloud

        """
        self.message_to_log += "\nPoint Of Cloud Created\n"
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)





    """
    MOST OF THE FUNCTION BELOW are used to call the actual function for processing the mesh
    It was organized differently before
    I prefer to leave like this and don't let the User call the actual Function
    
    """

    def remove_zero_area_faces_call(self) -> None:
        """
            Remove Null Area Faces

        """
        self.face, n_facesremoved = self.remove_zero_area_faces()

        self.message_to_log += "\nApplied: Remove Zero Area Faces Algorithm\n"
        self.message_to_log += f"Zero Area Faces removed: {n_facesremoved}\n\n"


    def scaling_mesh(self, scaling_factor=1.0) -> None:
        """
            Function: Scaling the mesh on X, Y and Z axis

            args:
                scaling_factor = scaling the mesh by its value

        """
        self.vertex, self.normal = self.scale_mesh(scaling_factor)
        self.vertex = utl.convert_array_tofloat64(self.vertex)
        self.normal = utl.convert_array_tofloat64(self.normal)
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)

        self.message_to_log += "\nApplied: Scaling Algorithm\n"
        self.message_to_log += f"Mesh scaled by: x{scaling_factor} factor\n\n"


    def scaling_mesh_unit_box(self) -> None:
        """
            Function: Scaling the mesh to a Unit Box

        """

        self.vertex, self.normal, scale_factor = self.scale_mesh_to_unit_box()
        self.vertex = utl.convert_array_tofloat64(self.vertex)
        self.normal = utl.convert_array_tofloat64(self.normal)
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)

        self.message_to_log += "\nApplied: Scaling Algorithm UNIT BOX\n"
        self.message_to_log += f"Mesh scaled by: x{scale_factor} factor\n\n"


    def scaling_mesh_unit_sphere(self) -> None:
        """
            Function: Scaling the mesh to a Unit Sphere

        """

        self.vertex, self.normal, scale_factor = self.scale_mesh_to_unit_sphere()
        self.vertex = utl.convert_array_tofloat64(self.vertex)
        self.normal = utl.convert_array_tofloat64(self.normal)
        self.pcd = utl.create_point_cloud(self.vertex, self.normal)

        self.message_to_log += "\nApplied: Scaling Algorithm UNIT SPHERE\n"
        self.message_to_log += f"Mesh scaled by: x{scale_factor} factor\n\n"



    def save_mesh(self, nome="", path=None) -> None:
        """
            Save the mesh in the off file

        """


        file_name = nome + "_" +self.dataname + self.extension_file
        self.message_to_log += f"File saved as: {file_name}"
        
        if path==None:
            utl.save_off_format(file_name, self.vertex, self.normal, self.face)
        else:
            utl.save_off_format(file_name, self.vertex, self.normal, self.face, path)



    def initialize_mesh(self) -> None:
        """
            Function for initializing the mesh, NOT the point cloud but the actual mesh.

        """
        self.message_to_log += "\nMesh Initialized\n"
        self.mesh = utl.initialize_mesh(self.vertex, self.normal, self.face)



    def visualize_mesh(self, nome="") -> None:
        """
            Function for visualizing the mesh

        """
        utl.visualize_3d_screen(self.mesh, name_window=nome)




    def repair_mesh(self, profondita=9, n_decimation=190000):
        """
            Function for repairing the mesh.
            HARD to find an actual method to repair a mesh or a python lib that works fine.
            IDEA: use the open3D reconstruction method, POISSON.
            By choosing the level of detail, the mesh is also decimated for reduce the number of data but maintaining
            the same level of details

            There are some lib, but I wanted to have my own repair method

            Args:
                profondita: depth, the amout of detail we want to see to a mesh.
                n_decimation: decimate the mesh by its values. Reduce the number of vertices but the details remains

        """

        #Modo più semplice libreria Pymesh
        self.message_to_log += "\nApplied: Repair Mesh Algorithm\n"

        holes = self.find_holes_in_mesh(self.mesh)

        print("Ci sono: " + str(len(holes)) + " buchi nella mesh")
        self.message_to_log += f"There are: " + str(len(holes)) + " holes in the mesh\n"
        # Converti np.int32 a int
        # holes_int contiene gli spigoli/edges (coppia di indici che fanno riferimento ai vertici)
        # holes_int = [[(int(edge[0]), int(edge[1])) for edge in hole] for hole in holes]

        mesh_poisson, density_mesh = self.reconstruction_mesh_poisson(profondita)

        # Estrai i punti (vertici) dalla mesh
        punti_estratti = np.asarray(mesh_poisson.vertices)

        # Estrai le normali dei vertici dalla mesh
        normali_estratte = np.asarray(mesh_poisson.vertex_normals)

        print("Punti Poisson: " + str(len(punti_estratti)))

        self.message_to_log += f"\nAFTER RECOSTRUCTION:\nNumber of Points on Mesh: {str(len(punti_estratti))}"

        pcd_da_poisson = utl.create_point_cloud(punti_estratti, normali_estratte)

        mesh_decimated = self.decimate_mesh_and_process(mesh_poisson, n_decimation)

        holes = self.find_holes_in_mesh(mesh_decimated)
        print("Ci sono: " + str(len(holes)) + " buchi nella mesh")

        self.message_to_log += f"\nThere are: " + str(len(holes)) + " holes in the mesh\n"

        print("Punti Poisson DECIMATED: " + str(len(np.asarray(mesh_decimated.vertices))))

        self.message_to_log += (f"AFTER DECIMATION:\nNumber of Points on Mesh: "
                                f"{str(len(np.asarray(mesh_decimated.vertices)))}\n")

        self.vertex = np.asarray(mesh_decimated.vertices)
        self.normal = np.asarray(mesh_decimated.vertex_normals)
        self.face = np.asarray(mesh_decimated.triangles)

        pcd_da_poisson_decimated = utl.create_point_cloud(self.vertex, self.normal)



    # Function for removing the not connected components.
    # Thanks to the Open-3d methods
    # I work on the point cloud and by implementing a built-in function by Open3d and choosing the correct values
    # The function is working fine by removing additional noise on the mesh
    def remove_not_connected_component(self, distance=1.02, n_punti_vicini=1):
        self.message_to_log += "\nApplied: Remove Not Connected Component Algorithm\n"

        filtered_points, face_list = self.find_cluster_connected(distance, n_punti_vicini)
        self.vertex, self.normal = utl.extract_vertices_and_normals(filtered_points)
        self.face = np.array(face_list)
        self.controll_not_connected_component()



    def controll_not_connected_component(self):
        """
            Function: controls the existence of not connected components

        """

        self.initialize_mesh()
        island_on_mesh = self.find_islands_in_mesh()

        # Stampa l'array delle isole
        main_island = max(island_on_mesh, key=len)  # La mesh principale è l'isola più grande
        other_islands = [island for island in island_on_mesh if island != main_island]
        print("Ci sono: " + str(len(other_islands)) + " isole nella mesh")
        self.message_to_log += f"\nCi sono: " + str(len(other_islands)) + " isole nella mesh\n\n"
        other_islands = [[int(elemento) for elemento in riga] for riga in other_islands]
        self.islands_on_mesh = other_islands
        print(other_islands)


    def get_message_log(self):
        """
            Get the message log

        """
        return self.message_to_log





    """
        FUNCTION FOR ACTUAL PROCESSING
    
    """

    def remove_zero_area_faces(self):
        """
            Function for checking the faces. Removing the Null Area Faces
            If some faces don't pass the min values they are not valid faces
        """

        areas = np.zeros(len(self.face))
        for i, face in enumerate(self.face):
            v0, v1, v2 = self.vertex[face]
            areas[i] = 0.5 * np.linalg.norm(np.cross(v1 - v0, v2 - v0))

        valid_faces = self.face[areas > 1e-12]

        return valid_faces, len(self.face) - len(valid_faces)



    def find_edges_repair(self, triangles) -> list:
        """
            Function: checking the external edge of a mesh

            Args:
                triangles: arrays containing the edges

        """

        edges = set()
        for triangle in triangles:
            for i in range(3):
                edge = tuple(sorted((triangle[i], triangle[(i + 1) % 3])))
                if edge in edges:
                    edges.remove(edge)  # Rimuovi il bordo se è già presente (bordo interno)
                else:
                    edges.add(edge)  # Aggiungi il bordo se non è presente
        return list(edges)



    def find_holes_in_mesh(self, mesh) -> list:
        """
            Function: finding the hole in the mesh
            DFS method. Analyze each edge and for each edge the vertices

            Args:
                mesh: detect the holes on the mesh

        """

        triangles = np.asarray(mesh.triangles)
        edges = self.find_edges_repair(triangles)

        """
            Create a dictionary to memorize vertices and their connections
        """
        edge_dict = {}
        for edge in edges:
            for vertex in edge:
                if vertex not in edge_dict:
                    edge_dict[vertex] = []
                edge_dict[vertex].append(edge)

        holes = []
        visited_edges = set()

        for edge in edges:
            if edge not in visited_edges:
                hole = []
                stack = [edge]
                while stack:
                    current_edge = stack.pop()
                    if current_edge not in visited_edges:
                        visited_edges.add(current_edge)
                        hole.append(current_edge)
                        for vertex in current_edge:
                            for next_edge in edge_dict[vertex]:
                                if next_edge not in visited_edges:
                                    stack.append(next_edge)
                holes.append(hole)

        return holes



    def reconstruction_mesh_poisson(self, profondita=9):
        """
            Function for reconstruction the mesh

            Args:
                profondita: depth value. Detail of the mesh

        """
        mesh_ricostruita, densitiy = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.pcd, depth=profondita,
                                                                                               width=0, scale=1.1,
                                                                                               linear_fit=False)
        return mesh_ricostruita, densitiy


    def decimate_mesh_and_process(self, mesh_final, n_decimation=10000):
        """
            Function for decimating the mesh after Repair

            Args:
                mesh_final : var used to execute operation on
                n_decimation : reducing the number of vertices, maintaining the level of details

        """


        mesh_final = mesh_final.simplify_quadric_decimation(n_decimation)
        mesh_final.remove_degenerate_triangles()
        mesh_final.remove_duplicated_triangles()
        mesh_final.remove_duplicated_vertices()
        mesh_final.remove_non_manifold_edges()
        return mesh_final



    def find_cluster_connected(self, density=1.1, points_min=1):
        """
            Implementing the Open-3d to remove the not connected components
            and fix the old index to the new ones

            Args:
                density: distance between points in order to form a cluster
                points_min: min number of point to form a cluster

        """

        labels = np.array(self.pcd.cluster_dbscan(eps=density, min_points=points_min))
        largest_cluster_idx = np.argmax(np.bincount(labels[labels >= 0]))
        filtered_points = self.pcd.select_by_index(np.where(labels == largest_cluster_idx)[0])

        old_to_new_index = {old_idx: new_idx for new_idx, old_idx in
                            enumerate(np.where(labels == largest_cluster_idx)[0])}
        new_faces = []
        for face in self.face:
            try:
                new_face = [old_to_new_index[vertex] for vertex in face]
                new_faces.append(new_face)
            except KeyError:
                continue

        return filtered_points, new_faces



    def find_islands_in_mesh(self):
        """
            Function for searching if there are some islands on the mesh
            Usig the DFS methods for searching connected components
        """

        triangles = np.asarray(self.mesh.triangles)
        edges = self.find_edges(triangles)

        edge_dict = {}
        for edge in edges:
            for vertex in edge:
                if vertex not in edge_dict:
                    edge_dict[vertex] = []
                edge_dict[vertex].append(edge)

        islands = []
        visited_vertices = set()

        for vertex in edge_dict:
            if vertex not in visited_vertices:
                island = []
                stack = [vertex]
                while stack:
                    current_vertex = stack.pop()
                    if current_vertex not in visited_vertices:
                        visited_vertices.add(current_vertex)
                        island.append(current_vertex)
                        for edge in edge_dict[current_vertex]:
                            for next_vertex in edge:
                                if next_vertex not in visited_vertices:
                                    stack.append(next_vertex)
                islands.append(island)

        return islands



    def find_edges(self, triangles):
        """
            Function for defining the edges of the triangles

            Args:
                triangles: var containing the edges

        """

        edges = set()
        for triangle in triangles:
            for i in range(3):
                edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
                edges.add(edge)
        return list(edges)



    """
        These last function are used for scaling the mesh:
            1. Normal Scaling
            2. Unit Box Scaling
            3. Unit Sphere Scaling
    
    """
    def scale_mesh(self, scale_factor):
        # Effettua lo scaling dei vertici
        scaled_vertices = self.vertex * scale_factor
        # Normalizza le normali dopo lo scaling
        scaled_normals = self.normal / np.linalg.norm(self.normal, axis=1)[:, np.newaxis]

        return scaled_vertices, scaled_normals

    def scale_mesh_to_unit_box(self):
        min_coord = np.min(self.vertex, axis=0)
        max_coord = np.max(self.vertex, axis=0)

        center_box = (min_coord+max_coord) / 2

        dimension_box = max_coord - min_coord

        scale_factor = 1.0 / np.max(dimension_box)

        scaled_vertices = (self.vertex - center_box) * scale_factor

        scaled_normals = self.normal / np.linalg.norm(self.normal, axis=1)[:, np.newaxis]

        return scaled_vertices, scaled_normals, scale_factor

    def scale_mesh_to_unit_sphere(self):
        center = np.mean(self.vertex, axis=0)

        max_distance = np.max(np.linalg.norm(self.vertex-center, axis=1))

        scale_factor = 1.0 / max_distance

        scaled_vertices = (self.vertex - center) * scale_factor

        scaled_normals = self.normal / np.linalg.norm(self.normal, axis=1)[:, np.newaxis]

        return scaled_vertices, scaled_normals, scale_factor
