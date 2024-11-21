import os
import open3d as o3d
import numpy as np
import datetime



"""
    Python file with some functions that are used all over the project folder
    Main Operations like:
    Check the Existence of a File
    Read and Write on File
    Initialize a Mesh or Point Cloud
    and many more.
    The functions are self-explanatory

"""


output_path="OUTPUT_SOURCE/"
output_log={
    1: "logsFile/",
    2: "logsFile/"
}
extension_log=".txt"

def check_file_exists(file_path) -> bool:

    """
        Function: check the existence of file

        Args:
            file_path : path of the file to check the existence
    """

    file_exists = os.path.exists(file_path)
    return file_exists

def load_off_with_loadtxt(file_path):

    """
        Function: read the off file and fetch the information from it

        Args:
            file_path : path of the off file to fetch the information

    """

    with open(file_path, 'r') as file:
        if 'NOFF' != file.readline().strip():
            raise ValueError('Not a valid OFF header')

        n_verts, n_faces, _ = map(int, file.readline().strip().split())
        print("Sono stati trovati:\nNumero Vertici="+str(n_verts)+"\nNumero Facce="+str(n_faces))

        # Load vertices and normals
        vertices_and_normals = np.loadtxt(file, max_rows=n_verts)

        vertices = vertices_and_normals[:,:3]  # First three columns are x, y, z
        normals = vertices_and_normals[:,3:6]  # Remaining columns are normals

        # Load faces
        faces = np.loadtxt(file, dtype=int)
        faces = faces[:,1:]  # Skip the first number in each row (the number of vertices in the face)

    return vertices, normals, faces, n_verts

def array_colore_grigio(n_verts) -> list[float]:
    """
        Function : not used function. Get the grey rgb values in floating values, aLso having an array with grey vales
        for each vertex

        Args:
            n_verts : number of vertices to define the dimension of the array to fill it with grey rgb values
    """

    grigio_chiaro = [0.78, 0.78, 0.78]  # 200/255 ≈ 0.78

    array_rgb = np.full((n_verts, 3), grigio_chiaro, dtype=np.float64)
    return grigio_chiaro

def check_array_format(array_to_check):
    """
        Function: not used function. Display the array form

        Args:
            array_to_check : array to check the form
    """

    if array_to_check.shape[1] != 3:
        raise ValueError("The array must have this Form: (N, 3)")
    print("Array's Form:", array_to_check.shape)


def convert_array_tofloat64(array_to_convert):
    """
        Function: convert an array to float-64 type

        Args:
            array_to_convert : array to convert its values to float-64 type
    """

    return array_to_convert.astype(np.float64)


def create_point_cloud(array_points, array_normal):

    """
        Function: create a point cloud from points and normals

        Args:
            array_points : array with vertices for point cloud creation
            array_normal : array with normals for each vertex for point cloud creation

        Returns:
            o3d.geometry.PointCloud()
    """

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(array_points)
    pcd.normals = o3d.utility.Vector3dVector(array_normal)
    #print("Point of Cloud Created")
    return pcd

def visualize_3d_screen(pcd, name_window=""):
    """
        Function: visualize a single point cloud

        Args:
            pcd : point cloud object to visualize
            name_window : name of the window to display the point cloud

    """
    o3d.visualization.draw_geometries([pcd], window_name=name_window)

def visualize_3d_screen2(pcd, pcd2, name_window):
    """
        Function: visualize multiple point cloud

        Args:
            pcd : point cloud object to visualize
            pcd2 : point cloud object to visualize
            name_window : name of the window to display the point clouds
    """

    o3d.visualization.draw_geometries([pcd, pcd2], window_name=name_window)

def save_ply_format(pcd, nomeFile):

    """
        Function: not used function. Save the point cloud into a ply file format

        Args:
            pcd : point cloud to save to a ply file format
            nomeFile : file name of ply file format

    """

    o3d.io.write_point_cloud(output_path+nomeFile+".ply", pcd)

def print_vertices(vertices_np):
    """
        Function: print vertices

        Args:
            vertices_np : print vertex obj

    """

    print("Vertices:\n", vertices_np)

def print_normals(normals_np):
    """
        Function: print normals

        Args:
            normals_np : print normal obj

    """
    print("Normals:\n", normals_np)

def print_faces(faces_np):
    """
        Function: print faces

         Args:
            faces_np : print face obj

    """

    print("Faces:\n", faces_np)

def save_off_format(filename, vertices, normals, faces, path=output_path):

    """
        Function: save information to off file format

        Args:
            filename : name of the file where to save the information
            vertices : information to save into the file. Vertex
            normals : information to save into the file. Normals
            faces : information to save into the file. Face
            path : path where to save the file

    """

    with open(path+filename, 'w') as f:
        f.write("NOFF\n")
        f.write(f"{len(vertices)} {len(faces)} 0\n")

        for vertex, normal in zip(vertices, normals):
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {normal[0]} {normal[1]} {normal[2]}\n")

        for face in faces:
            f.write(f"3 {face[0]} {face[1]} {face[2]}\n")

        print("File creato!")

def extract_vertices_and_normals(pcd):
    """
        Function: extract the vertices and normal from a point cloud object

        Args:
            pcd : point cloud object from where to extract the information

    """

    vertices = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    return vertices, normals

def initialize_mesh(vet, nr, fac):

    """
        Function: initializing the mesh with information

        Args:
            vet: initializing the mesh with vertex information
            nr : initializing the mesh with normals information
            fac : initializing the mesh with faces information

        Returns:
            o3d.geometry.TriangleMesh()

    """

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vet)
    mesh.vertex_normals = o3d.utility.Vector3dVector(nr)
    # Convert the faces array to int32
    faces_int32 = fac.astype(np.int32)
    mesh.triangles = o3d.utility.Vector3iVector(faces_int32)
    return mesh

def write_to_log(file_name, message, where_at=1):

    """
        Function: create a log file

        Args:
            file_name : name of the log file
            message : message to save into a log file
            where_at : folder destination where to save the log file
    """

    with open(output_log[where_at]+file_name+extension_log, 'a') as log_file:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time}\n")
        log_file.write("--------------------------------------------\n")
        log_file.write("DETAILS:\n")
        log_file.write(f"{message}\n")
        log_file.write("--------------------------------------------\n")

    print("File log creato!")

def is_folder_empty():

    """
        Function: not used function. Function to check if a folder is empty

    """

    if not os.path.isdir(output_log[1]):
        raise FileNotFoundError(f"La cartella '{output_log[1]}' non esiste.")

    if len(os.listdir(output_log[1])) == 0:
        print("Empty")
    else:
        print("Not Empty")