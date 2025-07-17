
# Ejemplo de preprocesamiento de datos WPM: carga, segmentación, autocalibración, enventanado y guardado de stacks
# Este script procesa únicamente los datasets PMP1020 y PMP1051, tanto para muslo como para muñeca.


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import uniovi_simur_wearablepermed_utils as wpm



# ************************** 1.- RUTAS A NUESTROS ARCHIVOS DE DATOS Y REGISTROS DE ACTIVIDADES ****************************
# MATRIX colocado en el muslo (Thigh)
csv_file_PMP1020_W1_PI = './examples/data/PMP1020_W1_PI.CSV'
Registro_Actividades_PMP1020 = './examples/data/PMP1020_RegistroActividades.xlsx'
csv_file_PMP1051_W1_PI = './examples/data/PMP1051_W1_PI.CSV'
Registro_Actividades_PMP1051 = './examples/data/PMP1051_RegistroActividades.xlsx'


# MATRIX colocado en la muñeca (Wrist)
csv_file_PMP1020_W1_M = './examples/data/PMP1020_W1_M.CSV'
csv_file_PMP1051_W1_M = './examples/data/PMP1051_W1_M.CSV'

# Crear el directorio para guardar los plots si no existe
plots_dir = './examples/data/plots/'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

# %%

# ********************  2.- ESCALADO DE TIMESTAMPS Y REPRESENTACIÓN GRÁFICA DE LOS DATOS SEGMENTADOS **********************
# MATRIX colocado en el muslo (Thigh)
sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI = 13261119
scaled_data_PMP1020_W1_PI, dictionary_timing_WPM_PMP1020_W1_PI = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1020_W1_PI, "Thigh", Registro_Actividades_PMP1020, sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI)
segmented_activity_data_PMP1020_W1_PI = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1020_W1_PI, scaled_data_PMP1020_W1_PI)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1020_W1_PI, './examples/data/plots/datos_PMP1020_PI')

scaled_data_PMP1051_W1_PI, dictionary_timing_WPM_PMP1051_W1_PI = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1051_W1_PI, "Thigh", Registro_Actividades_PMP1051, None)
segmented_activity_data_PMP1051_W1_PI = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1051_W1_PI, scaled_data_PMP1051_W1_PI)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1051_W1_PI, './examples/data/plots/datos_PMP1051_PI')


# ********************  2b.- ESCALADO DE TIMESTAMPS Y REPRESENTACIÓN GRÁFICA DE LOS DATOS SEGMENTADOS (MUÑECA) **********************
sample_init_CAMINAR_USUAL_SPEED_PMP1020_M = 13266119
scaled_data_PMP1020_W1_M, dictionary_timing_WPM_PMP1020_W1_M = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1020_W1_M, "Thigh", Registro_Actividades_PMP1020, sample_init_CAMINAR_USUAL_SPEED_PMP1020_M)
segmented_activity_data_PMP1020_W1_M = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1020_W1_M, scaled_data_PMP1020_W1_M)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1020_W1_M, './examples/data/plots/datos_PMP1020_M')

scaled_data_PMP1051_W1_M, dictionary_timing_WPM_PMP1051_W1_M = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1051_W1_M, "Thigh", Registro_Actividades_PMP1051, None)
segmented_activity_data_PMP1051_W1_M = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1051_W1_M, scaled_data_PMP1051_W1_M)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1051_W1_M, './examples/data/plots/datos_PMP1051_M')

# %%
# ************************************** 3.- SALVADO DE DATOS SEGMENTADOS EN FICHERO ".npz" **********************************
# MATRIX colocado en el muslo
wpm.file_management.save_segmented_data_to_compressed_npz("./examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_PI", segmented_activity_data_PMP1020_W1_PI)
wpm.file_management.save_segmented_data_to_compressed_npz("./examples/data/Segmented_WPM_Data/datos_segmentados_PMP1051_W1_PI", segmented_activity_data_PMP1051_W1_PI)
# MATRIX colocado en la muñeca
wpm.file_management.save_segmented_data_to_compressed_npz("./examples/data/Segmented_WPM_Data/datos_segmentados_PMP1020_W1_M", segmented_activity_data_PMP1020_W1_M)
wpm.file_management.save_segmented_data_to_compressed_npz("./examples/data/Segmented_WPM_Data/datos_segmentados_PMP1051_W1_M", segmented_activity_data_PMP1051_W1_M)


# **************** 4.- Enventanado de los datasets ****************
window_size_samples = 250  # 10 segundos a 25 Hz
folder_path = "./examples/data/Segmented_WPM_Data/"
file_names_thigh = ["datos_segmentados_PMP1020_W1_PI.npz", "datos_segmentados_PMP1051_W1_PI.npz"]
file_names_wrist = ["datos_segmentados_PMP1020_W1_M.npz", "datos_segmentados_PMP1051_W1_M.npz"]

windowed_data_dict_thigh = {}
windowed_data_dict_wrist = {}
labels_thigh = []
labels_wrist = []

for file_name in file_names_thigh:
    file_path = os.path.join(folder_path, file_name)
    data_loaded = wpm.segmentation.load_dicts_from_npz(file_path)
    windowed_data_thigh = wpm.segmentation.apply_windowing_WPM_segmented_data(data_loaded, window_size_samples)
    windowed_data_dict_thigh.update(windowed_data_thigh)
    labels_thigh.extend(windowed_data_thigh.keys())

for file_name in file_names_wrist:
    file_path = os.path.join(folder_path, file_name)
    data_loaded = wpm.segmentation.load_dicts_from_npz(file_path)
    windowed_data_wrist = wpm.segmentation.apply_windowing_WPM_segmented_data(data_loaded, window_size_samples)
    windowed_data_dict_wrist.update(windowed_data_wrist)
    labels_wrist.extend(windowed_data_wrist.keys())


# %%
# ************** 5.- Creación del stack de datos para clasificación **************
concatenated_data = []
all_labels = []

if windowed_data_dict_thigh and windowed_data_dict_wrist:
    # Unir por actividad, asegurando que ambas partes tengan la misma cantidad de ventanas
    for activity in windowed_data_dict_thigh:
        if activity in windowed_data_dict_wrist:
            data_thigh = windowed_data_dict_thigh[activity][:, 1:7, :]
            data_wrist = windowed_data_dict_wrist[activity][:, 1:7, :]
            min_dim = min(data_thigh.shape[0], data_wrist.shape[0])
            data_thigh = data_thigh[:min_dim]
            data_wrist = data_wrist[:min_dim]
            concatenated = np.hstack((data_thigh, data_wrist))
            concatenated_data.append(concatenated)
            all_labels.extend([activity] * concatenated.shape[0])
elif windowed_data_dict_thigh:
    for activity, data_thigh in windowed_data_dict_thigh.items():
        data_thigh_selected = data_thigh[:, 1:7, :]
        concatenated_data.append(data_thigh_selected)
        all_labels.extend([activity] * data_thigh_selected.shape[0])
elif windowed_data_dict_wrist:
    for activity, data_wrist in windowed_data_dict_wrist.items():
        data_wrist_selected = data_wrist[:, 1:7, :]
        concatenated_data.append(data_wrist_selected)
        all_labels.extend([activity] * data_wrist_selected.shape[0])

if concatenated_data:
    concatenated_data = np.vstack(concatenated_data)
else:
    concatenated_data = np.array([])

print("Datos concatenados:")
print(concatenated_data)
print(concatenated_data.shape)

# ***************************************** 6.- Guardamos nuestro stack de datos etiquetados ******************************************
folder_path = './examples/data/stacks/'
file_name_WPM = "data_tot_PMP1020_1051.npz"
output_file_path = os.path.join(folder_path, file_name_WPM)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
np.savez(output_file_path, concatenated_data=concatenated_data, labels=all_labels)
print(f"Datos y etiquetas guardados en: {output_file_path}")