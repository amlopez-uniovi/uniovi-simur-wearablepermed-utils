
# Ejemplo de preprocesamiento de datos WPM: carga, segmentación, autocalibración, enventanado y guardado de stacks
# Este script procesa únicamente los datasets PMP1020 y PMP1051, tanto para muslo como para muñeca.


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import uniovi_simur_wearablepermed_utils as wpm

# ************************** 1.- RUTAS A NUESTROS ARCHIVOS DE DATOS Y REGISTROS DE ACTIVIDADES ****************************

data_directory = './examples/data/'

Registro_Actividades_PMP1020 = os.path.join(data_directory, 'PMP1020_RegistroActividades.xlsx')
Registro_Actividades_PMP1051 = os.path.join(data_directory, 'PMP1051_RegistroActividades.xlsx')

# MATRIX colocado en el muslo (Thigh)
csv_file_PMP1020_W1_PI = os.path.join(data_directory, 'PMP1020_W1_PI.CSV')
csv_file_PMP1051_W1_PI = os.path.join(data_directory, 'PMP1051_W1_PI.CSV')

# MATRIX colocado en la muñeca (Wrist)
csv_file_PMP1020_W1_M = os.path.join(data_directory, 'PMP1020_W1_M.CSV')
csv_file_PMP1051_W1_M = os.path.join(data_directory, 'PMP1051_W1_M.CSV')

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
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1020_W1_PI, os.path.join(plots_dir, 'datos_PMP1020_PI'))

scaled_data_PMP1051_W1_PI, dictionary_timing_WPM_PMP1051_W1_PI = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1051_W1_PI, "Thigh", Registro_Actividades_PMP1051, None)
segmented_activity_data_PMP1051_W1_PI = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1051_W1_PI, scaled_data_PMP1051_W1_PI)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1051_W1_PI, os.path.join(plots_dir, 'datos_PMP1051_PI'))


# ********************  2b.- ESCALADO DE TIMESTAMPS Y REPRESENTACIÓN GRÁFICA DE LOS DATOS SEGMENTADOS (MUÑECA) **********************
sample_init_CAMINAR_USUAL_SPEED_PMP1020_M = 13266119
scaled_data_PMP1020_W1_M, dictionary_timing_WPM_PMP1020_W1_M = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1020_W1_M, "Thigh", Registro_Actividades_PMP1020, sample_init_CAMINAR_USUAL_SPEED_PMP1020_M)
segmented_activity_data_PMP1020_W1_M = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1020_W1_M, scaled_data_PMP1020_W1_M)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1020_W1_M, os.path.join(plots_dir, 'datos_PMP1020_M'))

scaled_data_PMP1051_W1_M, dictionary_timing_WPM_PMP1051_W1_M = wpm.file_management.load_scale_WPM_data(
    csv_file_PMP1051_W1_M, "Thigh", Registro_Actividades_PMP1051, None)
segmented_activity_data_PMP1051_W1_M = wpm.segmentation.segment_WPM_activity_data(
    dictionary_timing_WPM_PMP1051_W1_M, scaled_data_PMP1051_W1_M)
wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1051_W1_M, os.path.join(plots_dir, 'datos_PMP1051_M'))

# %%

segmented_data_directory = './examples/data/segmented_WPM_data/'

# ************************************** 3.- SALVADO DE DATOS SEGMENTADOS EN FICHERO ".npz" **********************************
# MATRIX colocado en el muslo
wpm.file_management.save_segmented_data_to_compressed_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1020_W1_PI"), segmented_activity_data_PMP1020_W1_PI)
wpm.file_management.save_segmented_data_to_compressed_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1051_W1_PI"), segmented_activity_data_PMP1051_W1_PI)
# MATRIX colocado en la muñeca
wpm.file_management.save_segmented_data_to_compressed_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1020_W1_M"), segmented_activity_data_PMP1020_W1_M)
wpm.file_management.save_segmented_data_to_compressed_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1051_W1_M"), segmented_activity_data_PMP1051_W1_M)


# **************** 4.- Enventanado de los datasets ****************


window_size_samples = 250  # 10 segundos a 25 Hz

data_loaded_1020_thigh = wpm.segmentation.load_dicts_from_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1020_W1_PI.npz"))
data_loaded_1020_wrist = wpm.segmentation.load_dicts_from_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1020_W1_M.npz"))
data_concatenated_1020 = wpm.segmentation.concatenate_arrays_by_key([data_loaded_1020_thigh, data_loaded_1020_wrist], crop_columns=slice(1, 7))
windowed_data_1020 = wpm.segmentation.apply_windowing_WPM_segmented_data(data_concatenated_1020, window_size_samples)
stacked_data_1020, stacked_data_1020_labels = wpm.segmentation.create_stack_from_windowed_dict(windowed_data_1020)

data_loaded_1051_thigh = wpm.segmentation.load_dicts_from_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1051_W1_PI.npz"))
data_loaded_1051_wrist = wpm.segmentation.load_dicts_from_npz(os.path.join(segmented_data_directory, "datos_segmentados_PMP1051_W1_M.npz"))
data_concatenated_1051 = wpm.segmentation.concatenate_arrays_by_key([data_loaded_1051_thigh, data_loaded_1051_wrist], crop_columns=slice(1, 7))
windowed_data_1051 = wpm.segmentation.apply_windowing_WPM_segmented_data(data_concatenated_1051, window_size_samples)
stacked_data_1051, stacked_data_1051_labels = wpm.segmentation.create_stack_from_windowed_dict(windowed_data_1051)

concatenated_stack, concatenated_stack_labels = wpm.segmentation.concatenate_stacks([
    (stacked_data_1020, stacked_data_1020_labels),
    (stacked_data_1051, stacked_data_1051_labels)
])


print("Datos concatenados:")
print(stacked_data_1051)
print(stacked_data_1051.shape)

# ***************************************** 6.- Guardamos nuestro stack de datos etiquetados ******************************************
stacks_directory = './examples/data/stacks/'

if not os.path.exists(stacks_directory):
    os.makedirs(stacks_directory)
    
file_name = "data_tot_PMP1020.npz"
np.savez(os.path.join(stacks_directory, file_name), concatenated_data=stacked_data_1020, labels=stacked_data_1020_labels)

file_name = "data_tot_PMP1051.npz"
np.savez(os.path.join(stacks_directory, file_name), concatenated_data=stacked_data_1051, labels=stacked_data_1051_labels)

file_name = "data_tot_PMP1020_1051.npz"
np.savez(os.path.join(stacks_directory, file_name), concatenated_data=concatenated_stack, labels=concatenated_stack_labels)

print(f"Stacks y etiquetas guardados en: {stacks_directory}")
