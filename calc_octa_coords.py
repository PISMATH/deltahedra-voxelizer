import trimesh
import numpy as np

# Ask the user for the STL file path and the output file name
stl_mesh_path = input("Enter the path to your STL file (e.g., 'input.stl'): ")
output_file = input("Enter the output filename (e.g., 'output.scad'): ")

# Load the mesh from the STL file
mesh = trimesh.load_mesh(stl_mesh_path)

# Find the farthest distance from the center of the mesh to any vertex
center = np.mean(mesh.vertices, axis=0)  # Center of the mesh
farthest_distance = max(np.linalg.norm(vertex - center) for vertex in mesh.vertices)

# Define the range for a, b, and c as -2x to 2x, where x is the farthest distance
x = farthest_distance
range_min = int(np.floor(-x))
range_max = int(np.ceil(x))

print(f"Estimated {range_max**3*8} point in mesh checks")
# Generate all oct_points for a, b, c in the range [-2x, 2x]
oct_points = []
tetra_points_b = []
tetra_points_c = []
for a in range(range_min, range_max + 1):
    for b in range(range_min, range_max + 1):
        for c in range(range_min, range_max + 1):
            # Calculate point A as specified
            A = [a + b, a - b + c, c]
            B = [a + b + 0.5, a - b + c + 0.5, c + 0.5]
            C = [a + b - 0.5, a - b + c + 0.5, c + 0.5]
            oct_points.append(A)
            tetra_points_b.append(B)
            tetra_points_c.append(C)

# Check which oct_points are inside the mesh
inside_oct_points = [point for point in oct_points if mesh.contains([point])[0]]
inside_tetra_points_b = [point for point in tetra_points_b if mesh.contains([point])[0]]
inside_tetra_points_c = [point for point in tetra_points_c if mesh.contains([point])[0]]

# Prepare SCAD script content
octa_coords_text = ',\n'.join([f'{point}' for point in inside_oct_points])
tetra_norm_coords_text = ',\n'.join([f'{point}' for point in inside_tetra_points_b])
tetra_rot_coords_text = ',\n'.join([f'{point}' for point in inside_tetra_points_c])

scad_content = f"""
// Function to create an octahedron using hull of small spheres
module octahedron(center = [0, 0, 0], size = 1.01) {{
    vertices = [
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ];
    scaled_vertices = [for (v = vertices) v * size + center];
    faces = [
        [0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4],
        [0, 3, 5], [3, 1, 5], [1, 2, 5], [2, 0, 5]
    ];
    polyhedron(points = scaled_vertices, faces = faces);
}}

module tetrahedron(center = [0, 0, 0], size = 0.501) {{
    vertices = [
        [1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]
    ];
    scaled_vertices = [for (v = vertices) v * size + center];
    faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]];
    polyhedron(points = scaled_vertices, faces = faces);
}}

module rot_tetrahedron(center = [0, 0, 0], size = 0.501) {{
    vertices = [
        [-1, 1, 1], [1, -1, 1], [-1, -1, -1], [1, 1, -1]
    ];
    scaled_vertices = [for (v = vertices) v * size + center];
    faces = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]];
    polyhedron(points = scaled_vertices, faces = faces);
}}

oct_positions = [
{octa_coords_text}
];

tetra_pos_norm = [
{tetra_norm_coords_text}
];

tetra_pos_rot = [
{tetra_rot_coords_text}
];

for (pos = oct_positions) {{
    octahedron(center=pos);
}}

for (pos = tetra_pos_norm) {{
    tetrahedron(center=pos);
}}

for (pos = tetra_pos_rot) {{
    rot_tetrahedron(center=pos);
}}
"""

# Write the SCAD content to the output file
with open(output_file, 'w') as file:
    file.write(scad_content)

print(f"SCAD file successfully saved as {output_file}.")
