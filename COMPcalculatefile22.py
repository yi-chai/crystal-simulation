import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
import seaborn as sns

def read_gro_file_with_masses(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]

    molecules = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            molecule_number = int(line[0:5])
            atom_type = line[10:15].strip()
            x, y, z = map(float, [line[20:28].strip(), line[28:36].strip(), line[36:44].strip()])
            if molecule_number in molecules:
                molecules[molecule_number].append((x, y, z, atom_type))
            else:
                molecules[molecule_number] = [(x, y, z, atom_type)]
        except ValueError:
            continue
    return molecules

def extract_specific_carbon_atoms(atoms, carbon_labels):
    return [atom for atom in atoms if any(c_label in atom[3] for c_label in carbon_labels)]

def calculate_kd_tree_nearest_specific_carbon_distances(molecules, carbon_labels):
    carbon_atoms = {mol_id: extract_specific_carbon_atoms(atoms, carbon_labels) for mol_id, atoms in molecules.items()}

    flat_list = [(mol_id, atom) for mol_id, atoms in carbon_atoms.items() for atom in atoms]
    points = np.array([atom[1][:3] for atom in flat_list])
    mol_ids = np.array([atom[0] for atom in flat_list])

    tree = cKDTree(points)
    distances, indexes = tree.query(points, k=2)

    nearest_distances = []
    for dist, idx, mol_id in zip(distances[:, 1], indexes[:, 1], mol_ids):
        if mol_id != mol_ids[idx]:
            nearest_distances.append(dist*10)

    return nearest_distances

def plot_probability_density(distances, title):
    plt.figure(figsize=(7, 4))
    sns.kdeplot(distances)
    plt.title(title)
    plt.xlabel('Distance (A)', weight='bold', size='large')
    plt.ylabel('Probability Density', weight='bold', size='large')
    plt.show()

file_path = 'grofiles/run3.gro'
specific_carbon_labels = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                          'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                          'C20', 'C21', 'C22']

molecules = read_gro_file_with_masses(file_path)
kd_tree_distances = calculate_kd_tree_nearest_specific_carbon_distances(molecules, specific_carbon_labels)
plot_probability_density(kd_tree_distances, ' ')