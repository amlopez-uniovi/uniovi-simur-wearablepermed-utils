import sys  # Import the sys module for system-specific parameters and functions
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for manipulating dates and times
import matplotlib.pyplot as plt  # Import pyplot from matplotlib for data visualization
import uniovi_simur_wearablepermed_utils as wpm  # Import the simur_wpm_utils module for wearable permed utilities


if __name__ == "__main__":
    

    # PMP1020 dataset PI
    csv_file_PMP1020_W1_PI =       './examples/data/PMP1020_W1_PI.CSV'                   # Ruta a nuestro archivo de datos .csv
    Registro_Actividades_PMP1020 = './examples/data/PMP1020_RegistroActividades.xlsx'    # Ruta a la hoja Excel del registro de actividades

    sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI = 13261119       # Init sample "CAMINAR - USUAL SPEED" dataset PMP1020 (PI)
    scaled_data_PMP1020_W1_PI, dictionary_timing_WPM_PMP1020_W1_PI = wpm.file_management.load_scale_WPM_data(csv_file_PMP1020_W1_PI, 
                                                                                    "Thigh", 
                                                                                    Registro_Actividades_PMP1020, 
                                                                                    sample_init_CAMINAR_USUAL_SPEED_PMP1020_PI)
    #print(dictionary_timing_WPM_PMP1020_W1_PI)
    segmented_activity_data_PMP1020_W1_PI = wpm.segmentation.segment_WPM_activity_data(dictionary_timing_WPM_PMP1020_W1_PI, scaled_data_PMP1020_W1_PI)
    print(type(segmented_activity_data_PMP1020_W1_PI))

    datos_acc_actividad_no_estructurada = segmented_activity_data_PMP1020_W1_PI['ACTIVIDAD NO ESTRUCTURADA'][:,0:4]  # timestamps y datos de aceleración
    print(datos_acc_actividad_no_estructurada)

    datos_acc_actividad_no_estructurada_autocalibrados, slope, offset = wpm.autocalibration.auto_calibrate(datos_acc_actividad_no_estructurada, fm = 25)

    # Representación gráfica de los datos de aceleración calibrados
    plt.figure(figsize=(10, 5))
    plt.plot(datos_acc_actividad_no_estructurada_autocalibrados)
    plt.xlabel('Número de Muestras')
    plt.ylabel('Aceleración [g]')
    plt.title('Datos CALIBRADOS de Aceleración - Actividad no estructurada (PMP1020)')
    plt.grid(True)
    plt.show()
