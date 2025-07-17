"""
Ejemplo de pipeline: carga de un CSV, enventanado y extracción de features
"""

import numpy as np
import uniovi_simur_wearablepermed_utils as wpm
import os

# Ruta al archivo CSV de ejemplo (ajusta la ruta según tu estructura)
csv_file = './examples/data/PMP1051_W1_PI.CSV'  # Cambia por el archivo que quieras usar
registro_actividades = './examples/data/PMP1051_RegistroActividades.xlsx'

# 1. Cargar y escalar los datos desde el CSV
scaled_data, timing_dict = wpm.file_management.load_scale_WPM_data(
    csv_file, 'Thigh', registro_actividades, None
)

# 2. Segmentar los datos por actividad
segmented_data = wpm.segmentation.segment_WPM_activity_data(timing_dict, scaled_data)

# 3. Seleccionar una actividad para el ejemplo (por ejemplo, la primera disponible)
actividad = list(segmented_data.keys())[0]
data_actividad = segmented_data[actividad]

# 4. Enventanar los datos (por ejemplo, ventanas de 250 muestras)
window_size = 250
# data_actividad tiene forma (N, columnas), queremos (num_ventanas, columnas, window_size)
windowed = wpm.segmentation.apply_windowing_WPM_segmented_data({actividad: data_actividad}, window_size)[actividad]
# Seleccionamos solo las columnas de interés (por ejemplo, 1:7 para Acc y Gyr)
windowed = windowed[:, 1:7, :]  # (num_ventanas, 6, window_size)

# 5. Extraer features para cada ventana
features = wpm.feature_extraction.extract_features(windowed, n_imus=1)

print(f"Actividad: {actividad}")
print(f"Shape de datos enventanados: {windowed.shape}")
print(f"Shape de features extraídos: {features.shape}")
print("Primeras features de la primera ventana:")
print(features[0])
