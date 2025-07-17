import pytest
from uniovi_simur_wearablepermed_utils.segmentation import *

import numpy as np
from datetime import datetime, time
import os

def test_find_closest_timestamp_exact():
    """Test finding the exact timestamp."""
    timestamps = np.array([1000, 2000, 3000, 4000, 5000])
    target = 3000
    assert find_closest_timestamp(timestamps, target) == 2

def test_find_closest_timestamp_lower():
    """Test finding the closest timestamp when the target is slightly lower than a value."""
    timestamps = np.array([1000, 2000, 3000, 4000, 5000])
    target = 2500
    assert find_closest_timestamp(timestamps, target) == 1  # Should return the closest index (2000)

def test_find_closest_timestamp_higher():
    """Test finding the closest timestamp when the target is slightly higher than a value."""
    timestamps = np.array([1000, 2000, 3000, 4000, 5000])
    target = 4500
    assert find_closest_timestamp(timestamps, target) == 3  # Should return the closest index (4000)

def test_find_closest_timestamp_out_of_bounds_low():
    """Test finding the closest timestamp when the target is lower than all values."""
    timestamps = np.array([1000, 2000, 3000, 4000, 5000])
    target = 500
    assert find_closest_timestamp(timestamps, target) == 0  # Should return the first index (1000)

def test_find_closest_timestamp_out_of_bounds_high():
    """Test finding the closest timestamp when the target is higher than all values."""
    timestamps = np.array([1000, 2000, 3000, 4000, 5000])
    target = 6000
    assert find_closest_timestamp(timestamps, target) == 4  # Should return the last index (5000)

def test_segment_MATRIX_data_by_dates():
    """Test segmentation of data between two dates."""
    # Define start and end dates for segmentation
    
    start_date = datetime(2021, 1, 1, 0, 1, 0)
    ts_start_date = start_date.timestamp()*1000
    
    end_date = datetime(2021, 1, 1, 0, 2, 0)
    ts_end_date = end_date.timestamp()*1000

    # Mock data with timestamps (in milliseconds) and some arbitrary values
    imu_data = np.array([[ts_start_date-1, 1, 2, 3],  # Jan 1, 2021, 00:00:00
                         [ts_start_date, 4, 5, 6],  # Jan 1, 2021, 00:01:00
                         [ts_end_date, 7, 8, 9],  # Jan 1, 2021, 00:02:00
                         [ts_end_date+1, 10, 11, 12]]) # Jan 1, 2021, 00:03:00


    # Call the function
    segmented_data = segment_MATRIX_data_by_dates(imu_data, start_date, end_date)

    # Expected data between the start and end date
    expected_segment = np.array([[ts_start_date, 4, 5, 6],  
                                 [ts_end_date, 7, 8, 9]]) 

    assert np.allclose(segmented_data, expected_segment)

def test_segment_WPM_activity_data():
    # Diccionario simulado con horas y fechas de actividades basado en los datos proporcionados
    dictionary_hours_wpm = {
        "Hora de inicio de acelerómetro muslo (hh:mm:ss) - Hora de ordenador": time(9, 41, 6),
        "Hora de inicio de acelerómetro cadera (hh:mm:ss) - Hora de ordenador": time(9, 35, 51),
        "Hora de inicio de acelerómetro muñeca (hh:mm:ss) - Hora de ordenador": time(9, 35, 21),
        "Fecha día 1": datetime(2024, 7, 8,0, 0),
        "FASE REPOSO CON K5 - Hora de inicio": time(9, 47, 45),
        "FASE REPOSO CON K5 - Hora de fin": time(10, 22, 45),
        "TAPIZ RODANTE - Hora de inicio": time(10, 45, 5),
        "TAPIZ RODANTE - Hora de fin": time(11, 13, 5),
        "SIT TO STAND 30 s - Hora de inicio": time(11, 31, 19),
        "SIT TO STAND 30 s - Hora de fin": time(11, 31, 49),
        "INCREMENTAL CICLOERGOMETRO - Hora de inicio REPOSO": time(11, 51, 35),
        "INCREMENTAL CICLOERGOMETRO - Hora de inicio CALENTAMIENTO": time(11, 54, 35),
        "INCREMENTAL CICLOERGOMETRO - Hora de inicio INCREMENTAL": time(11, 57, 35),
        "INCREMENTAL CICLOERGOMETRO - Hora de fin": time(12, 7, 18),
        
        "ACTIVIDAD NO ESTRUCTURADA - Hora de inicio": time(13, 11, 22),  # Replace with correct time
        "ACTIVIDAD NO ESTRUCTURADA - Hora de fin": time(10, 11, 22),  # Replace with correct time

        "Fecha día 7": datetime(2024, 7, 15,0,0),
        "YOGA - Hora de inicio": time(12, 36, 32),
        "YOGA - Hora de fin": time(12, 38, 32),
        "SENTADO VIENDO LA TV - Hora de inicio": time(12, 39, 0),
        "SENTADO VIENDO LA TV - Hora de fin": time(12, 41, 0),
        "SENTADO LEYENDO - Hora de inicio": time(12, 41, 16),
        "SENTADO LEYENDO - Hora de fin": time(12, 43, 16),
        "SENTADO USANDO PC - Hora de inicio": time(12, 44, 46),
        "SENTADO USANDO PC - Hora de fin": time(12, 46, 46),
        "DE PIE USANDO PC - Hora de inicio": time(12, 47, 13),
        "DE PIE USANDO PC - Hora de fin": time(12, 49, 13),
        "DE PIE DOBLANDO TOALLAS - Hora de inicio": time(12, 51, 57),
        "DE PIE DOBLANDO TOALLAS - Hora de fin": time(12, 53, 57),
        "DE PIE MOVIENDO LIBROS - Hora de inicio": time(12, 54, 46),
        "DE PIE MOVIENDO LIBROS - Hora de fin": time(12, 56, 46),
        "DE PIE BARRIENDO - Hora de inicio": time(12, 57, 14),
        "DE PIE BARRIENDO - Hora de fin": time(12, 59, 14),
        "CAMINAR USUAL SPEED - Hora de inicio": time(13, 1, 30),
        "CAMINAR USUAL SPEED - Hora de fin": time(13, 3, 30),
        "CAMINAR CON MÓVIL O LIBRO - Hora de inicio": time(13, 3, 48),
        "CAMINAR CON MÓVIL O LIBRO - Hora de fin": time(13, 5, 48),
        "CAMINAR CON LA COMPRA - Hora de inicio": time(13, 6, 14),
        "CAMINAR CON LA COMPRA - Hora de fin": time(13, 8, 14),
        "CAMINAR ZIGZAG - Hora de inicio": time(13, 8, 55),
        "CAMINAR ZIGZAG - Hora de fin": time(13, 10, 55),
        "TROTAR - Hora de inicio": time(13, 11, 16),
        "TROTAR - Hora de fin": time(13, 13, 16),
        "SUBIR Y BAJAR ESCALERAS - Hora de inicio": time(13, 15, 16),
        "SUBIR Y BAJAR ESCALERAS - Hora de fin": time(13, 17, 16),
        }

    # Datos simulados de IMU (ejemplo de matriz 2D con timestamps y valores de aceleración)
    imu_data = np.array([
    # Día 1 (8 de Julio, 2024)
    [datetime(2024, 7, 8, 9, 47, 45).timestamp(), 0.1, 0.2, 0.3],  # Inicio FASE REPOSO CON K5
    [datetime(2024, 7, 8, 10, 22, 45).timestamp(), 0.4, 0.5, 0.6],  # Fin FASE REPOSO CON K5
    [datetime(2024, 7, 8, 10, 45, 5).timestamp(), 0.7, 0.8, 0.9],   # Inicio TAPIZ RODANTE
    [datetime(2024, 7, 8, 11, 13, 5).timestamp(), 1.0, 1.1, 1.2],   # Fin TAPIZ RODANTE
    [datetime(2024, 7, 8, 11, 31, 19).timestamp(), 1.3, 1.4, 1.5],  # Inicio SIT TO STAND 30s
    [datetime(2024, 7, 8, 11, 31, 49).timestamp(), 1.6, 1.7, 1.8],  # Fin SIT TO STAND 30s
    [datetime(2024, 7, 8, 11, 51, 35).timestamp(), 1.9, 2.0, 2.1],  # Inicio INCREMENTAL CICLOERGÓMETRO (Reposo)
    [datetime(2024, 7, 8, 12, 7, 18).timestamp(), 2.2, 2.3, 2.4],   # Fin INCREMENTAL CICLOERGÓMETRO

    #actividad no estructurada
    [datetime(2024, 7, 8, 13, 11, 30).timestamp(), 2.2, 2.3, 2.4],   # Fin INCREMENTAL CICLOERGÓMETRO
    [datetime(2024, 7, 15, 9, 10, 11).timestamp(), 2.2, 2.3, 2.4],   # Fin INCREMENTAL CICLOERGÓMETRO
     
    # Día 7 (15 de Julio, 2024)
    [datetime(2024, 7, 15, 12, 36, 32).timestamp(), 2.5, 2.6, 2.7],  # Inicio YOGA
    [datetime(2024, 7, 15, 12, 38, 32).timestamp(), 2.8, 2.9, 3.0],  # Fin YOGA
    [datetime(2024, 7, 15, 12, 39, 0).timestamp(), 3.1, 3.2, 3.3],   # Inicio SENTADO VIENDO TV
    [datetime(2024, 7, 15, 12, 41, 0).timestamp(), 3.4, 3.5, 3.6],   # Fin SENTADO VIENDO TV
    [datetime(2024, 7, 15, 12, 41, 16).timestamp(), 3.7, 3.8, 3.9],  # Inicio SENTADO LEYENDO
    [datetime(2024, 7, 15, 12, 43, 16).timestamp(), 4.0, 4.1, 4.2],  # Fin SENTADO LEYENDO
    [datetime(2024, 7, 15, 12, 44, 46).timestamp(), 4.3, 4.4, 4.5],  # Inicio SENTADO USANDO PC
    [datetime(2024, 7, 15, 12, 46, 46).timestamp(), 4.6, 4.7, 4.8],  # Fin SENTADO USANDO PC
    [datetime(2024, 7, 15, 12, 47, 13).timestamp(), 4.9, 5.0, 5.1],  # Inicio DE PIE USANDO PC
    [datetime(2024, 7, 15, 12, 49, 13).timestamp(), 5.2, 5.3, 5.4],  # Fin DE PIE USANDO PC
    [datetime(2024, 7, 15, 12, 51, 57).timestamp(), 5.5, 5.6, 5.7],  # Inicio DE PIE DOBLANDO TOALLAS
    [datetime(2024, 7, 15, 12, 53, 57).timestamp(), 5.8, 5.9, 6.0],  # Fin DE PIE DOBLANDO TOALLAS
    [datetime(2024, 7, 15, 12, 54, 46).timestamp(), 6.1, 6.2, 6.3],  # Inicio DE PIE MOVIENDO LIBROS
    [datetime(2024, 7, 15, 12, 56, 46).timestamp(), 6.4, 6.5, 6.6],  # Fin DE PIE MOVIENDO LIBROS
    [datetime(2024, 7, 15, 12, 57, 14).timestamp(), 6.7, 6.8, 6.9],  # Inicio DE PIE BARRIENDO
    [datetime(2024, 7, 15, 12, 59, 14).timestamp(), 7.0, 7.1, 7.2],  # Fin DE PIE BARRIENDO
    [datetime(2024, 7, 15, 13, 1, 30).timestamp(), 7.3, 7.4, 7.5],   # Inicio CAMINAR USUAL SPEED
    [datetime(2024, 7, 15, 13, 3, 30).timestamp(), 7.6, 7.7, 7.8],   # Fin CAMINAR USUAL SPEED
    [datetime(2024, 7, 15, 13, 3, 48).timestamp(), 7.9, 8.0, 8.1],   # Inicio CAMINAR CON MÓVIL O LIBRO
    [datetime(2024, 7, 15, 13, 5, 48).timestamp(), 8.2, 8.3, 8.4],   # Fin CAMINAR CON MÓVIL O LIBRO
    [datetime(2024, 7, 15, 13, 6, 14).timestamp(), 8.5, 8.6, 8.7],   # Inicio CAMINAR CON LA COMPRA
    [datetime(2024, 7, 15, 13, 8, 14).timestamp(), 8.8, 8.9, 9.0],   # Fin CAMINAR CON LA COMPRA
    [datetime(2024, 7, 15, 13, 8, 55).timestamp(), 9.1, 9.2, 9.3],   # Inicio CAMINAR ZIGZAG
    [datetime(2024, 7, 15, 13, 10, 55).timestamp(), 9.4, 9.5, 9.6],  # Fin CAMINAR ZIGZAG
    [datetime(2024, 7, 15, 13, 11, 16).timestamp(), 9.7, 9.8, 9.9],  # Inicio TROTAR
    [datetime(2024, 7, 15, 13, 13, 16).timestamp(), 10.0, 10.1, 10.2],  # Fin TROTAR
    [datetime(2024, 7, 15, 13, 15, 16).timestamp(), 10.3, 10.4, 10.5],  # Inicio SUBIR Y BAJAR ESCALERAS
    [datetime(2024, 7, 15, 13, 17, 16).timestamp(), 10.6, 10.7, 10.8],  # Fin SUBIR Y BAJAR ESCALERAS
    ])

    # Función que se llama para hacer la segmentación
    result = segment_WPM_activity_data(dictionary_hours_wpm, imu_data)

    # Verifica la segmentación de datos
    
    assert 'ACTIVIDAD NO ESTRUCTURADA' in result, "No se segmentó correctamente la fase de actividad no estructurada"
    assert len(result['ACTIVIDAD NO ESTRUCTURADA']) > 0, "Datos segmentados incorrectamente para fase de actividad no estructurada"

    assert 'FASE REPOSO CON K5' in result, "No se segmentó correctamente la fase de reposo"
    assert len(result['FASE REPOSO CON K5']) > 0, "Datos segmentados incorrectamente para fase de reposo"

    assert 'TAPIZ RODANTE' in result, "No se segmentó correctamente la actividad TAPIZ RODANTE"
    assert len(result['TAPIZ RODANTE']) > 0, "Datos segmentados incorrectamente para TAPIZ RODANTE"

    assert 'SIT TO STAND 30 s' in result, "No se segmentó correctamente la actividad SIT TO STAND 30 s"
    assert len(result['SIT TO STAND 30 s']) > 0, "Datos segmentados incorrectamente para SIT TO STAND 30 s"

    assert 'INCREMENTAL CICLOERGOMETRO' in result, "No se segmentó correctamente la actividad INCREMENTAL CYCLE ERGOMETER"
    assert len(result['INCREMENTAL CICLOERGOMETRO']) > 0, "Datos segmentados incorrectamente para INCREMENTAL CYCLE ERGOMETER"

    assert 'FASE REPOSO CON K5' in result, "No se segmentó correctamente la fase de reposo"
    assert len(result['FASE REPOSO CON K5']) > 0, "Datos segmentados incorrectamente para fase de reposo"

    assert 'YOGA' in result, "No se segmentó correctamente la actividad YOGA"
    assert len(result['YOGA']) > 0, "Datos segmentados incorrectamente para YOGA"

    assert 'SENTADO VIENDO LA TV' in result, "No se segmentó correctamente la actividad SENTADO VIENDO LA TV"
    assert len(result['SENTADO VIENDO LA TV']) > 0, "Datos segmentados incorrectamente para SENTADO VIENDO LA TV"

    assert 'SENTADO LEYENDO' in result, "No se segmentó correctamente la actividad SENTADO LEYENDO"
    assert len(result['SENTADO LEYENDO']) > 0, "Datos segmentados incorrectamente para SENTADO LEYENDO"

    assert 'SENTADO USANDO PC' in result, "No se segmentó correctamente la actividad SENTADO USANDO PC"
    assert len(result['SENTADO USANDO PC']) > 0, "Datos segmentados incorrectamente para SENTADO USANDO PC"

    assert 'DE PIE USANDO PC' in result, "No se segmentó correctamente la actividad DE PIE USANDO PC"
    assert len(result['DE PIE USANDO PC']) > 0, "Datos segmentados incorrectamente para DE PIE USANDO PC"

    assert 'DE PIE DOBLANDO TOALLAS' in result, "No se segmentó correctamente la actividad DE PIE DOBLANDO TOALLAS"
    assert len(result['DE PIE DOBLANDO TOALLAS']) > 0, "Datos segmentados incorrectamente para DE PIE DOBLANDO TOALLAS"

    assert 'DE PIE MOVIENDO LIBROS' in result, "No se segmentó correctamente la actividad DE PIE MOVIENDO LIBROS"
    assert len(result['DE PIE MOVIENDO LIBROS']) > 0, "Datos segmentados incorrectamente para DE PIE MOVIENDO LIBROS"

    assert 'DE PIE BARRIENDO' in result, "No se segmentó correctamente la actividad DE PIE BARRIENDO"
    assert len(result['DE PIE BARRIENDO']) > 0, "Datos segmentados incorrectamente para DE PIE BARRIENDO"

    assert 'CAMINAR USUAL SPEED' in result, "No se segmentó correctamente la actividad CAMINAR USUAL SPEED"
    assert len(result['CAMINAR USUAL SPEED']) > 0, "Datos segmentados incorrectamente para CAMINAR USUAL SPEED"

    assert 'CAMINAR CON MÓVIL O LIBRO' in result, "No se segmentó correctamente la actividad CAMINAR CON MÓVIL O LIBRO"
    assert len(result['CAMINAR CON MÓVIL O LIBRO']) > 0, "Datos segmentados incorrectamente para CAMINAR CON MÓVIL O LIBRO"

    assert 'CAMINAR CON LA COMPRA' in result, "No se segmentó correctamente la actividad CAMINAR CON LA COMPRA"
    assert len(result['CAMINAR CON LA COMPRA']) > 0, "Datos segmentados incorrectamente para CAMINAR CON LA COMPRA"

    assert 'CAMINAR ZIGZAG' in result, "No se segmentó correctamente la actividad CAMINAR ZIGZAG"
    assert len(result['CAMINAR ZIGZAG']) > 0, "Datos segmentados incorrectamente para CAMINAR ZIGZAG"

    assert 'TROTAR' in result, "No se segmentó correctamente la actividad TROTAR"
    assert len(result['TROTAR']) > 0, "Datos segmentados incorrectamente para TROTAR"

    assert 'SUBIR Y BAJAR ESCALERAS' in result, "No se segmentó correctamente la actividad SUBIR Y BAJAR ESCALERAS"
    assert len(result['SUBIR Y BAJAR ESCALERAS']) > 0, "Datos segmentados incorrectamente para SUBIR Y BAJAR ESCALERAS"

#save_segmented_data_to_compressed_npz tests

def test_save_segmented_data_to_compressed_npz(tmp_path):
    """Test saving segmented activity data to a compressed .npz file."""
    # Create a temporary directory
    temp_dir = tmp_path / "Segmented_WPM_Data"
    temp_dir.mkdir()

    # Mock data to save
    file_name = "test_segmented_data"
    segmented_activity_data_wpm = {
        "activity_1": np.array([[1, 2, 3], [4, 5, 6]]),
        "activity_2": np.array([[7, 8, 9], [10, 11, 12]])
    }

    # Call the function
    save_segmented_data_to_compressed_npz(file_name, segmented_activity_data_wpm)

    # Check if the file was created
    saved_file_path = os.path.join("Segmented_WPM_Data", file_name + ".npz")
    assert os.path.exists(saved_file_path), "The .npz file was not created."

    # Load the saved file and verify its contents
    loaded_data = np.load(saved_file_path, allow_pickle=True)
    for key in segmented_activity_data_wpm:
        assert key in loaded_data, f"Key '{key}' is missing in the saved file."
        assert np.array_equal(loaded_data[key], segmented_activity_data_wpm[key]), f"Data for key '{key}' does not match."

    # Clean up the created file
    os.remove(saved_file_path)
    os.rmdir("Segmented_WPM_Data")
    
#test load_dicts_from_npz

def test_load_dicts_from_npz(tmp_path):
    """Test loading dictionaries from a .npz file."""
    # Create a temporary directory
    temp_dir = tmp_path / "test_npz"
    temp_dir.mkdir()

    # Mock data to save in the .npz file
    file_name = temp_dir / "test_data.npz"
    mock_data = {
        "array_1": np.array([1, 2, 3]),
        "array_2": np.array([[4, 5, 6], [7, 8, 9]]),
        "array_3": np.array([10.5, 11.5, 12.5])
    }

    # Save the mock data to a .npz file
    np.savez(file_name, **mock_data)

    # Call the function to load the data
    loaded_data = load_dicts_from_npz(file_name)

    # Verify the loaded data matches the original mock data
    for key in mock_data:
        assert key in loaded_data, f"Key '{key}' is missing in the loaded data."
        assert np.array_equal(loaded_data[key], mock_data[key]), f"Data for key '{key}' does not match."

def test_load_dicts_from_npz_file_not_found():
    """Test loading from a non-existent .npz file."""
    non_existent_file = "non_existent_file.npz"
    try:
        load_dicts_from_npz(non_existent_file)
        assert False, "Expected FileNotFoundError was not raised."
    except FileNotFoundError:
        pass  # Expected behavior

def test_load_dicts_from_npz_invalid_file(tmp_path):
    """Test loading from an invalid .npz file."""
    # Create a temporary invalid file
    invalid_file = tmp_path / "invalid_file.npz"
    with open(invalid_file, "w") as f:
        f.write("This is not a valid .npz file.")

    try:
        load_dicts_from_npz(invalid_file)
        assert False, "Expected Exception was not raised for invalid file."
    except Exception:
        pass  # Expected behavior

## Apply windowing tests

def test_apply_windowing_2d_array():
    """Test apply_windowing with a 2D array."""
    data_dict = {
        "signal_2d": np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15],
            [16, 17, 18],
            [19, 20, 21],
            [22, 23, 24],
            [25, 26, 27],
            [28, 29, 30]
        ])
    }
    window_size = 3
    step_size = 2

    result = apply_windowing_WPM_segmented_data(data_dict, window_size, step_size)

    expected_result = {
        "signal_2d": np.array([
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ],
            [
                [7, 8, 9],
                [10, 11, 12],
                [13, 14, 15]
            ],
            [
                [13, 14, 15],
                [16, 17, 18],
                [19, 20, 21]
            ],
            [
                [19, 20, 21],
                [22, 23, 24],
                [25, 26, 27]
            ]
        ]).transpose(0, 2, 1)
    }

    assert "signal_2d" in result, "Key 'signal_2d' is missing in the result."
    assert np.array_equal(result["signal_2d"], expected_result["signal_2d"]), "Windowed data does not match expected result."

def test_apply_windowing_no_overlap():
    """Test apply_windowing with no overlap (step size equals window size)."""
    data_dict = {
        "signal_2d": np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
            [13, 14, 15],
            [16, 17, 18]
        ])
    }
    window_size = 3
    step_size = 3

    result = apply_windowing_WPM_segmented_data(data_dict, window_size, step_size)

    expected_result = {
        "signal_2d": np.array([
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ],
            [
                [10, 11, 12],
                [13, 14, 15],
                [16, 17, 18]
            ]
        ]).transpose(0, 2, 1)
    }

    assert "signal_2d" in result, "Key 'signal_2d' is missing in the result."
    assert np.array_equal(result["signal_2d"], expected_result["signal_2d"]), "Windowed data does not match expected result."


def test_apply_windowing_short_signal():
    """Test apply_windowing with a signal shorter than the window size."""
    data_dict = {
        "signal_2d": np.array([
            [1, 2, 3],
            [4, 5, 6]
        ])
    }
    window_size = 3

    result = apply_windowing_WPM_segmented_data(data_dict, window_size)

    # The signal should be resampled to match the window size
    expected_result = {
          "signal_2d": np.array([
            [1, 2, 3],
            [4, 5, 6]
        ])
    }

    assert "signal_2d" in result, "Key 'signal_2d' is missing in the result."
    assert np.allclose(result["signal_2d"], expected_result["signal_2d"]), "Resampled data does not match expected result."


def test_apply_windowing_empty_dict():
    """Test apply_windowing with an empty dictionary."""
    data_dict = {}
    window_size = 3

    result = apply_windowing_WPM_segmented_data(data_dict, window_size)

    assert result == {}, "Result should be an empty dictionary."


def test_apply_windowing_unsupported_dimensions():
    """Test apply_windowing with unsupported array dimensions."""
    data_dict = {
        "signal_1d": np.array([1, 2, 3, 4, 5]),
        "signal_3d": np.random.rand(5, 3, 2)
    }
    window_size = 3

    result = apply_windowing_WPM_segmented_data(data_dict, window_size)

    assert "signal_1d" not in result, "1D signals should not be processed."
    assert "signal_3d" not in result, "3D signals should not be processed."

#test create_labeled_stack_wpm

def test_create_labeled_stack_wpm_valid_input():
    """Test create_labeled_stack_wpm with valid input."""
    list_of_windowed_dicts = [
        {
            "activity_1": np.array([[1, 2, 3], [4, 5, 6]]),
            "activity_2": np.array([[7, 8, 9]])
        },
        {
            "activity_3": np.array([[10, 11, 12], [13, 14, 15]])
        }
    ]

    stacked_data, labels = create_labeled_stack_wpm(list_of_windowed_dicts)

    expected_stacked_data = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
        [13, 14, 15]
    ])
    expected_labels = np.array([
        "activity_1",
        "activity_1",
        "activity_2",
        "activity_3",
        "activity_3"
    ])

    assert np.array_equal(stacked_data, expected_stacked_data), "Stacked data does not match expected result."
    assert np.array_equal(labels, expected_labels), "Labels do not match expected result."



def test_create_labeled_stack_wpm_mismatched_shapes():
    """Test create_labeled_stack_wpm with arrays of mismatched shapes."""
    list_of_windowed_dicts = [
        {
            "activity_1": np.array([[1, 2, 3], [4, 5, 6]]),
            "activity_2": np.array([[7, 8]])
        }
    ]

    try:
        create_labeled_stack_wpm(list_of_windowed_dicts)
        assert False, "Expected ValueError for mismatched shapes was not raised."
    except ValueError:
        pass  # Expected behavior

# save stacked data and labels to compressed npz tests


def test_save_stacked_data_and_labels(tmp_path):
    """Test saving stacked data and labels into a .npz file."""
    # Create a temporary directory
    folder_path = tmp_path / "test_save_stacked_data"
    folder_path.mkdir()

    # Mock data to save
    stacked_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    labels = np.array(["label_1", "label_2", "label_3"])
    file_name = "test_data"

    # Call the function
    save_stacked_data_and_labels(stacked_data, labels, str(folder_path), file_name)

    # Check if the file was created
    saved_file_path = folder_path / (file_name + ".npz")
    assert saved_file_path.exists(), "The .npz file was not created."

    # Load the saved file and verify its contents
    loaded_data = np.load(saved_file_path, allow_pickle=True)
    assert "data" in loaded_data, "Key 'data' is missing in the saved file."
    assert "labels" in loaded_data, "Key 'labels' is missing in the saved file."
    assert np.array_equal(loaded_data["data"], stacked_data), "Saved stacked data does not match the original data."
    assert np.array_equal(loaded_data["labels"], labels), "Saved labels do not match the original labels."

def test_save_stacked_data_and_labels_invalid_path():
    """Test saving stacked data and labels with an invalid folder path."""
    # Mock data to save
    stacked_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    labels = np.array(["label_1", "label_2", "label_3"])
    invalid_folder_path = "/invalid/path"
    file_name = "test_data"

    try:
        save_stacked_data_and_labels(stacked_data, labels, invalid_folder_path, file_name)
        assert False, "Expected an exception for invalid folder path, but none was raised."
    except Exception:
        pass  # Expected behavior





if __name__ == "__main__":
    pytest.main()
