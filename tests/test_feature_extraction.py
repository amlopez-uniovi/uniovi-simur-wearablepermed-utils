import pytest
from uniovi_simur_wearablepermed_utils.preprocessing import *
from uniovi_simur_wearablepermed_utils.feature_extraction import *
import numpy as np

# GET_BASIC_STATS

def test_get_basic_stats_basic():
    
    epochdata = np.array([
            [1, 2, 3],
            [2, 3, 4],
            [3, 4, 5],
            [4, 5, 6],
            [5, 6, 7]
            ], dtype=np.float64)   
    
    filter_b = np.array([1, -1], dtype=np.float64)
    filter_a = np.array([1, -0.9], dtype=np.float64)
    
    
    expected_basic_statistics = [
        5.279741582765779, 5.279741582765779, 3.0, 4.0, 5.0, 4.0, 4.0, 4.0, 1.58113883, 1.58113883, 1.58113883, 2.5, 2.5, 2.5
    ]
    expected_enmo_trunc = np.array([2.74165739, 4.11099907, 5.38580217, 6.55111853, 7.60913077], dtype=np.float64)
    expected_enmo_filtered = np.array([2.74165739, 4.11099907, 5.38580217, 6.55111853, 7.60913077], dtype=np.float64)
    
    basic_statistics, enmo_trunc, enmo_filtered = get_basic_stats(epochdata, filter_b, filter_a)
    
    assert np.allclose(basic_statistics, expected_basic_statistics, atol=1e-2), f"Error: {basic_statistics}"
    assert np.allclose(enmo_trunc, expected_enmo_trunc, atol=1e-2), f"Error: {enmo_trunc}"
    assert np.allclose(enmo_filtered, expected_enmo_filtered, atol=1e-2), f"Error: {enmo_filtered}"
    
 
#getFFTpower

def test_get_FFT_power_basic():
    FFT = np.array([1, 2, 3, 4], dtype=np.complex128)
    expected = np.array([0.0625, 0.25, 0.5625, 1], dtype=np.float64)
    
    result = get_FFT_power(FFT)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_get_FFT_power_non_normalized():
    FFT = np.array([1, 2, 3, 4], dtype=np.complex128)
    expected = np.array([1, 4, 9, 16], dtype=np.float64)
    
    result = get_FFT_power(FFT, normalize=False)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"
    
#get_FF_magnitude

def test_get_FFT_magnitude_basic():
    FFT = np.array([1, 2, 3, 4], dtype=np.complex128)
    expected = np.array([0.25, 0.5, 0.75, 1], dtype=np.float64)
    
    result = get_FFT_magnitude(FFT)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_get_FFT_magnitude_non_normalized():
    FFT = np.array([1, 2, 3, 4], dtype=np.complex128)
    expected = np.array([1, 2, 3, 4], dtype=np.float64)
    
    result = get_FFT_magnitude(FFT, normalize=False)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"
