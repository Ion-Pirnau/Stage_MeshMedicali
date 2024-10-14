import numpy as np


# eps (float) – Density parameter that is used to find neighbouring points.
# min_points (int) – Minimum number of points to form a cluster.
def find_cluster_connected(pcd, faces, density=1.1, points_min=1):
    # Trova i cluster connessi
    # eps=1.1, 1.6
    labels = np.array(pcd.cluster_dbscan(eps=density, min_points=points_min))
    # print(labels)
    largest_cluster_idx = np.argmax(np.bincount(labels[labels >= 0]))
    filtered_points = pcd.select_by_index(np.where(labels == largest_cluster_idx)[0])

    # Crea una mappa dai vecchi indici ai nuovi indici
    old_to_new_index = {old_idx: new_idx for new_idx, old_idx in enumerate(np.where(labels == largest_cluster_idx)[0])}
    # Aggiorna le facce
    new_faces = []
    for face in faces:
        try:
            new_face = [old_to_new_index[vertex] for vertex in face]
            new_faces.append(new_face)
        except KeyError:
            # Se un vertice della faccia è stato rimosso, ignoriamo la faccia
            continue

    return filtered_points, new_faces



def find_islands_in_mesh(mesh):
    triangles = np.asarray(mesh.triangles)
    edges = find_edges(triangles)

    # Crea un dizionario per memorizzare i vertici e i loro bordi connessi
    edge_dict = {}
    for edge in edges:
        for vertex in edge:
            if vertex not in edge_dict:
                edge_dict[vertex] = []
            edge_dict[vertex].append(edge)

    # Trova le isole
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

def find_edges(triangles):
    edges = set()
    for triangle in triangles:
        for i in range(3):
            edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
            edges.add(edge)
    return list(edges)


# Funzione per dividere i sotto-array in gruppi di tre elementi
def divide_in_gruppi_di_tre(array):
    risultato = []
    for sotto_array in array:
        gruppi = [sotto_array[i:i+3] for i in range(0, len(sotto_array), 3)]
        risultato.extend(gruppi)
    return risultato