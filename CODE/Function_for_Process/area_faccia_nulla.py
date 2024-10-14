import numpy as np

def remove_zero_area_faces(vertices, faces):
    # Calcola le aree delle facce
    areas = np.zeros(len(faces))
    for i, face in enumerate(faces):
        v0, v1, v2 = vertices[face]
        areas[i] = 0.5 * np.linalg.norm(np.cross(v1 - v0, v2 - v0))

    # Trova gli indici delle facce con area non nulla
    valid_faces = faces[areas > 1e-12]

    return valid_faces, len(faces) - len(valid_faces)