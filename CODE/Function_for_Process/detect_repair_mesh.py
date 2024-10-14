import numpy as np
import open3d as o3d

def find_edges(triangles):
    edges = set()
    for triangle in triangles:
        for i in range(3):
            edge = tuple(sorted((triangle[i], triangle[(i + 1) % 3])))
            if edge in edges:
                edges.remove(edge)  # Rimuovi il bordo se è già presente (bordo interno)
            else:
                edges.add(edge)  # Aggiungi il bordo se non è presente
    return list(edges)

def create_mesh(vertices, normali, faces):
    # Create a TriangleMesh object
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.vertex_normals = o3d.utility.Vector3dVector(normali)
    # Convert the faces array to int32
    faces_int32 = faces.astype(np.int32)
    mesh.triangles = o3d.utility.Vector3iVector(faces_int32)
    # print('Vertices:')
    # print(np.asarray(mesh.vertices))
    # print('Triangles:')
    # print(np.asarray(mesh.triangles))
    # o3d.visualization.draw_geometries([mesh])
    return mesh

def find_holes_in_mesh(mesh):
    triangles = np.asarray(mesh.triangles)
    edges = find_edges(triangles)

    # Crea un dizionario per memorizzare i vertici e i loro bordi connessi
    edge_dict = {}
    for edge in edges:
        for vertex in edge:
            if vertex not in edge_dict:
                edge_dict[vertex] = []
            edge_dict[vertex].append(edge)

    # Trova i buchi
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


def extract_hole_vertices(vertices, normale, holes):
    # Crea un set per memorizzare i vertici unici dei buchi
    hole_vertices_set = set()

    # Itera attraverso i buchi e aggiungi i vertici al set
    for hole in holes:
        for edge in hole:
            hole_vertices_set.add(edge[0])
            hole_vertices_set.add(edge[1])
        break


    # Crea un array di vertici per i buchi
    hole_vertices = np.array([vertices[v] for v in hole_vertices_set])
    hole_normals = np.array([normale[la_normale] for la_normale in hole_vertices_set])

    return hole_vertices, hole_normals


def calculate_perimeter(vertices):
    perimeter = 0.0
    num_vertices = len(vertices)

    for i in range(num_vertices):
        # Trova i due vertici consecutivi
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]

        # Calcola la distanza tra i due vertici
        distance = np.linalg.norm(v1 - v2)

        # Aggiungi la distanza al perimetro
        perimeter += distance

    return perimeter


def ricostruzione_mesh_poisson(pcd, profondita=9):
    # Esegui la ricostruzione di Poisson
    mesh_ricostruita, densitiy = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=profondita, width=0, scale=1.1, linear_fit=False)
    return mesh_ricostruita, densitiy

def decimate_mesh_and_process(mesh_final, n_decimation=10000):
    mesh_final = mesh_final.simplify_quadric_decimation(n_decimation)
    mesh_final.remove_degenerate_triangles()
    mesh_final.remove_duplicated_triangles()
    mesh_final.remove_duplicated_vertices()
    mesh_final.remove_non_manifold_edges()
    return mesh_final

def remove_by_density(mesh, densities):
    # Rimozione dei vertici con bassa densità
    vertices_to_remove = densities < np.quantile(densities, 0.01)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    return mesh
