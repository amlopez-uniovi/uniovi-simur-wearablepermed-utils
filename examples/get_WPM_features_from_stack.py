"""
Ejemplo de pipeline: carga de un archivo NPZ con un stack de datos enventanados y extracción de features
"""

import numpy as np
import uniovi_simur_wearablepermed_utils as wpm
import os

# Ruta al archivo NPZ de stack (ajusta la ruta según tu estructura). Se trata de un stack de dos imus, muslo y muñeca
stack_file = './examples/data/stacks/data_tot_PMP1020_1051.npz'  # Cambia por el archivo que quieras usar

# 1. Cargar el stack y las etiquetas
with np.load(stack_file, allow_pickle=True) as data:
    concatenated_data = data['concatenated_data']  # (num_ventanas, canales, window_size)
    labels = data['labels']

print(f"Shape del stack: {concatenated_data.shape}")
print(f"Número de etiquetas: {len(labels)}")

# 2. Extraer features para cada ventana del stack
features = wpm.feature_extraction.extract_features(concatenated_data, n_imus=2)

print(f"Shape de features extraídos: {features.shape}")
print("Primeras features de la primera ventana:")
print(features[0])
print(f"Primera etiqueta: {labels[0]}")
