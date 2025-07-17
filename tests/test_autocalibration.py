import pytest
from uniovi_simur_wearablepermed_utils.autocalibration import *
import numpy as np
   

#COUNT_STUCK_VALS

def test_count_stuck_vals_no_stuck_values():
    xArray = np.array([0.1, 0.2, 0.3, 0.4])
    yArray = np.array([0.1, 0.2, 0.3, 0.4])
    zArray = np.array([0.1, 0.2, 0.3, 0.4])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == 0, f"Error: {result}"

def test_count_stuck_vals_stuck_x_values():
    xArray = np.array([2.0, 2.0, 2.0, 2.0])
    yArray = np.array([0.1, 0.2, 0.3, 0.4])
    zArray = np.array([0.1, 0.2, 0.3, 0.4])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == len(xArray), f"Error: {result}"

def test_count_stuck_vals_stuck_y_values():
    xArray = np.array([0.1, 0.2, 0.3, 0.4])
    yArray = np.array([-2.0, -2.0, -2.0, -2.0])
    zArray = np.array([0.1, 0.2, 0.3, 0.4])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == len(yArray), f"Error: {result}"

def test_count_stuck_vals_stuck_z_values():
    xArray = np.array([0.1, 0.2, 0.3, 0.4])
    yArray = np.array([0.1, 0.2, 0.3, 0.4])
    zArray = np.array([3.0, 3.0, 3.0, 3.0])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == len(zArray), f"Error: {result}"

def test_count_stuck_vals_max_abs_value_8():
    xArray = np.array([0.1, 0.2, 0.3, 0.4])
    yArray = np.array([0.1, 0.2, 0.3, 0.4])
    zArray = np.array([8.0, 0.2, 0.3, 0.4])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == 1, f"Error: {result}"

def test_count_stuck_vals_multiple_stuck_values():
    xArray = np.array([2.0, 2.0, 2.0, 2.0])
    yArray = np.array([-2.0, -2.0, -2.0, -2.0])
    zArray = np.array([8.0, 0.2, 0.3, 0.4])
    
    result = count_stuck_vals(xArray, yArray, zArray)
    assert result == 1, f"Error: {result}"