import os
import open3d as o3d
import numpy as np
import datetime



#Python file with some functions that are used all over the project folder
#Main Operations like:
# Check the Existence of a File
# Read and Write on File
# Initialize a Mesh or Point Cloud
# and many more.
# The functions are self-explanatory

output_path="OUTPUT_SOURCE/"
output_log={
    1: "log_blender/",
    2: "log_processing/"
}
extension_log=".txt"

def check_file_exists(file_path):
    file_exists = os.path.exists(file_path)
    return file_exists

def load_off_with_loadtxt(file_path):
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

def array_colore_grigio(n_verts):
    # Valore RGB normalizzato per il grigio chiaro
    grigio_chiaro = [0.78, 0.78, 0.78]  # 200/255 ≈ 0.78
    # Crea un array NumPy con il colore grigio chiaro
    array_rgb = np.full((n_verts, 3), grigio_chiaro, dtype=np.float64)
    return grigio_chiaro

def check_array_format(array_to_check):
    # Array NumPy con la forma corretta
    if array_to_check.shape[1] != 3:
        raise ValueError("L'array vertices deve avere la forma (N, 3)")
    print("Forma dell'array:", array_to_check.shape)


def convert_array_tofloat64(array_to_convert):
    return array_to_convert.astype(np.float64)


def create_point_cloud(array_points, array_normal):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(array_points)
    pcd.normals = o3d.utility.Vector3dVector(array_normal)
    print("Point of Cloud Created")
    return pcd

def visualize_3d_screen(pcd, name_window=""):
    o3d.visualization.draw_geometries([pcd], window_name=name_window)

def visualize_3d_screen2(pcd, pcd2, name_window):
    o3d.visualization.draw_geometries([pcd, pcd2], window_name=name_window)

def save_ply_format(pcd, nomeFile):
    o3d.io.write_point_cloud(output_path+nomeFile+".ply", pcd)

def print_vertices(vertices_np):
    print("Vertices:\n", vertices_np)

def print_normals(normals_np):
    print("Normals:\n", normals_np)

def print_faces(faces_np):
    print("Faces:\n", faces_np)

def save_off_format(filename, vertices, normals, faces):
    with open(output_path+filename, 'w') as f:
        f.write("NOFF\n")
        f.write(f"{len(vertices)} {len(faces)} 0\n")

        for vertex, normal in zip(vertices, normals):
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {normal[0]} {normal[1]} {normal[2]}\n")

        for face in faces:
            f.write(f"3 {face[0]} {face[1]} {face[2]}\n")

        print("File creato!")

def extract_vertices_and_normals(pcd):
    vertices = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    return vertices, normals

def initialize_mesh(vet, nr, fac):
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vet)
    mesh.vertex_normals = o3d.utility.Vector3dVector(nr)
    # Convert the faces array to int32
    faces_int32 = fac.astype(np.int32)
    mesh.triangles = o3d.utility.Vector3iVector(faces_int32)
    return mesh

def write_to_log(file_name, message, where_at=1):
    with open(output_log[where_at]+file_name+extension_log, 'a') as log_file:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time}\n")
        log_file.write("--------------------------------------------\n")
        log_file.write("DETAILS:\n")
        log_file.write(f"{message}\n")
        log_file.write("--------------------------------------------\n")

    print("File log creato!")

def is_folder_empty():
    if not os.path.isdir(output_log[1]):
        raise FileNotFoundError(f"La cartella '{output_log[1]}' non esiste.")

    if len(os.listdir(output_log[1])) == 0:
        print("Empty")
    else:
        print("Not Empty")