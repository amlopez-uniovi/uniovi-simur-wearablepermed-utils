import pytest
from uniovi_simur_wearablepermed_utils.preprocessing import *
from uniovi_simur_wearablepermed_utils.feature_extraction import *
import numpy as np

def test_norm_basic():
    data = np.array([
        [3, 4, 0],  
        [1, 2, 2],  
        [6, 8, 0],  
        [8, 6, 0]   
    ], dtype=np.float64)
    
    expected = np.array([5, 3, 10, 10], dtype=np.float64)
    
    result = NORM(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_norm_single_vector():
    data = np.array([3, 4], dtype=np.float64)
    
    expected = np.array([5], dtype=np.float64)
    
    result = NORM(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_norm_empty():
    data = np.array([], dtype=np.float64).reshape(0, 0)
    
    expected = np.array([], dtype=np.float64)
    
    result = NORM(data)
    assert np.array_equal(result, expected), f"Error: {result}"

def test_norm_zeros():
    data = np.array([
        [0, 0, 0],  
        [0, 0, 0],  
        [0, 0, 0],  
        [0, 0, 0],  
        [0, 0, 0]   
    ], dtype=np.float64)
    
    expected = np.array([0, 0, 0, 0, 0], dtype=np.float64)
    
    result = NORM(data)
    assert np.array_equal(result, expected), f"Error: {result}"

def test_norm_large_values():
    data = np.array([
        [3000, 4000, 0],  
        [1000, 2000, 2000],  
        [6000, 8000, 0],  
        [2000, 1000, 2000]  
    ], dtype=np.float64)
    
    expected = np.array([5000, 3000, 10000, 3000], dtype=np.float64)
    
    result = NORM(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"
    
#ENMO

def test_enmo_basic():
    data = np.array([
        [6, 8, 0],
        [3, 4, 0],  
        [1, 2, 2],  
        [6, 8, 0]   
    ], dtype=np.float64)
    
    expected = np.array([9, 4, 2, 9], dtype=np.float64)
    
    result = ENMO(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_enmo_basic_G9_8():
    data = np.array([
        [6, 8, 0],
        [3, 4, 0],  
        [1, 2, 2],  
        [6, 8, 0]   
    ], dtype=np.float64)
    
    expected = np.array([10, 5, 3, 10], dtype=np.float64)-9.8
    
    result = ENMO(data, G=9.8)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_enmo_single_vector():
    data = np.array([3, 4], dtype=np.float64)
    
    expected = np.array([4], dtype=np.float64)
    
    result = ENMO(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"

def test_enmo_empty():
    data = np.array([], dtype=np.float64).reshape(0, 0)
    
    expected = np.array([], dtype=np.float64)
    
    result = ENMO(data)
    assert np.array_equal(result, expected), f"Error: {result}"

def test_enmo_zeros():
    data = np.array([
        [0, 0, 0],  
        [0, 0, 0],  
        [0, 0, 0],  
        [0, 0, 0]   
    ], dtype=np.float64)
    
    expected = np.array([-1, -1, -1, -1], dtype=np.float64)
    
    result = ENMO(data)
    assert np.array_equal(result, expected), f"Error: {result}"

def test_enmo_large_values():
    data = np.array([
        [3000, 4000, 0],  
        [1000, 2000, 2000],  
        [6000, 8000, 0] ,  
        [1000, 2000, 2000]  
    ], dtype=np.float64)
    
    expected = np.array([4999, 2999, 9999, 2999], dtype=np.float64)
    
    result = ENMO(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"
  
#MAD

def test_mad_basic():
    data = np.array([
        [1, 2, 3],  
        [4, 5, 6],  
        [7, 8, 9],
        [10, 11, 12]  
    ], dtype=np.float64)
    
    expected = 5.129184919390214
    
    result = MAD(data)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"


#CLIP_DATA

def test_clip_data_basic():
    data = np.array([
        [5, 10, -12],  
        [6, 15, -20],  
        [4, 8, -9],
        [7, 9, -8]
    ], dtype=np.float64)
    
    expected = np.array([
        [5, 8, -8],  
        [6, 8, -8],  
        [4, 8, -8],
        [7, 8, -8]  
    ], dtype=np.float64)
    
    clip_data(data)  
    assert np.array_equal(data, expected), f"Error: {data}"

def test_clip_data_custom_clip_value():
    data = np.array([
        [5, 10, -12],  
        [6, 15, -20],  
        [4, 8, -9],
        [7, 9, -8]
    ], dtype=np.float64)
    
    expected = np.array([
        [5, 6, -6],  
        [6, 6, -6],  
        [4, 6, -6],
        [6, 6, -6]  
    ], dtype=np.float64)
    
    clip_data(data, clip_value=6)  
    assert np.array_equal(data, expected), f"Error: {data}"

def test_clip_data_partial_index():
    data = np.array([
        [5, 10, -12],  
        [6, 15, -20],  
        [4, 8, -9],
        [7, 9, -8]
    ], dtype=np.float64)
    
    expected = np.array([
        [5, 10, -8],  
        [6, 15, -8],  
        [4, 8, -8],
        [7, 9, -8]  
    ], dtype=np.float64)
    
    clip_data(data, index=[0, 2])  
    assert np.array_equal(data, expected), f"Error: {data}"
    
def test_time_interp_basic():
    data = np.array([
        [0, 10, 5],
        [1, 20, 15],
        [2, 30, 25],
        [3, 40, 35],
        [4, 50, 45]
     ], dtype=np.float64)
    
    expected = np.array([
        [0, 10, 5],
        [0.5, 15, 10],
        [1, 20, 15],
        [1.5, 25, 20],
        [2, 30, 25],
        [2.5, 35, 30],
        [3, 40, 35],
        [3.5, 45, 40],
        [4, 50, 45]
        ], dtype=np.float64)
    
    result = time_interp(data,  Tm=0.5, t_index=0,)
    assert np.allclose(result, expected, atol=1e-2), f"Error: {result}"


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
