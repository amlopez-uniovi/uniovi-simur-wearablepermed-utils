"""
This example:
- Load two CSV files with MATRIX activity data (PMP1020_W1_PI.CSV, PMP1051_W1_PI.CSV) in an WereablePerMed standard experiment.
- Collects the timing for all the activities from the corresponding Excel log files
- Scales the time stamp to correct time drift
- Plot the accelerometer data for all the activities and save the figure as a .jpg file.
"""

import sys  # Import the sys module for system-specific parameters and functions
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for manipulating dates and times
import matplotlib.pyplot as plt  # Import pyplot from matplotlib for data visualization
import uniovi_simur_wearablepermed_utils as wpm 

if __name__ == "__main__":

# ************************** PATH TO DATA ****************************
    # MATRIX  (Thigh)
    # -------------------------------------

    # PMP1020 dataset
    csv_file_PMP1020_W1_PI =       './examples/data/PMP1020_W1_PI.CSV'                   # Ruta a nuestro archivo de datos .csv
    Registro_Actividades_PMP1020 = './examples/data/PMP1020_RegistroActividades.xlsx'    # Ruta a la hoja Excel del registro de actividades

    # PMP1051 dataset
    csv_file_PMP1051_W1_PI =       './examples/data/PMP1051_W1_PI.CSV'                   # Ruta a nuestro archivo de datos .csv
    Registro_Actividades_PMP1051 = './examples/data/PMP1051_RegistroActividades.xlsx'    # Ruta a la hoja Excel del registro de actividades

    # ********************  2.- SCALE TIMESTAMPS, PLOT SEGMENTED DATA **********************
    # MATRIX (Thigh)
    # -------------------------------------
    # PMP1020 dataset
    sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI = 13261119       # Init sample "CAMINAR - USUAL SPEED" dataset PMP1020 (PI)
    scaled_data_PMP1020_W1_PI, dictionary_timing_WPM_PMP1020_W1_PI = wpm.file_management.load_scale_WPM_data(csv_file_PMP1020_W1_PI, 
                                                                                    "Thigh", 
                                                                                    Registro_Actividades_PMP1020, 
                                                                                    sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI)
    #print(dictionary_timing_WPM_PMP1020_W1_PI)
    segmented_activity_data_PMP1020_W1_PI = wpm.segmentation.segment_WPM_activity_data(dictionary_timing_WPM_PMP1020_W1_PI, scaled_data_PMP1020_W1_PI)
    #print(type(segmented_activity_data_PMP1020_W1_PI))
    wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1020_W1_PI, './examples/data/datos_PMP1020_PI')

    # PMP1051 dataset
    scaled_data_PMP1051_W1_PI, dictionary_timing_WPM_PMP1051_W1_PI = wpm.file_management.load_scale_WPM_data(csv_file_PMP1051_W1_PI, 
                                                                                    "Thigh", 
                                                                                    Registro_Actividades_PMP1051, 
                                                                                    None)
    #print(dictionary_timing_WPM_PMP1051_W1_PI)
    segmented_activity_data_PMP1051_W1_PI = wpm.segmentation.segment_WPM_activity_data(dictionary_timing_WPM_PMP1051_W1_PI, scaled_data_PMP1051_W1_PI)
    #print(type(segmented_activity_data_PMP1051_W1_PI))
    wpm.segmentation.plot_segmented_WPM_data(segmented_activity_data_PMP1051_W1_PI, './examples/data/datos_PMP1051_PI')

    plt.show()
