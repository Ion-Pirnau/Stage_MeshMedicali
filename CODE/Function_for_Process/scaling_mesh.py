import numpy as np

def scale_mesh(vertices, normals, scale_factor):
    # Effettua lo scaling dei vertici
    scaled_vertices = vertices * scale_factor
    # Normalizza le normali dopo lo scaling
    scaled_normals = normals / np.linalg.norm(normals, axis=1)[:, np.newaxis]

    return scaled_vertices, scaled_normals