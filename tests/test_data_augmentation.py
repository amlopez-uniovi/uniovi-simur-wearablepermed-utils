import pytest
from uniovi_simur_wearablepermed_utils.data_augmentation import *
from uniovi_simur_wearablepermed_utils.feature_extraction import *
import numpy as np

#test jitter

def test_jitter_output_shape():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = jitter(X, sigma=0.5)
    assert result.shape == X.shape, "Output shape does not match input shape."

def test_jitter_adds_noise():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = jitter(X, sigma=0.5)
    assert not np.array_equal(result, X), "Jitter did not add noise to the data."

def test_jitter_with_zero_sigma():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = jitter(X, sigma=0.0)
    np.testing.assert_array_equal(result, X)

def test_jitter_with_different_sigma():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result1 = jitter(X, sigma=0.1)
    result2 = jitter(X, sigma=1.0)
    assert not np.array_equal(result1, result2), "Jitter with different sigma values produced the same result."

#test magnitude_warp


def test_magnitude_warp_output_shape():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = magnitude_warp(X, sigma=0.2)
    assert result.shape == X.shape, "Output shape does not match input shape"

def test_magnitude_warp_output_values_change():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = magnitude_warp(X, sigma=0.2)
    assert not np.array_equal(result, X), "Output values did not change"

def test_magnitude_warp_sigma_effect():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result_low_sigma = magnitude_warp(X, sigma=0.1)
    result_high_sigma = magnitude_warp(X, sigma=1.0)
    distortion_low_sigma = np.abs(result_low_sigma - X).mean()
    distortion_high_sigma = np.abs(result_high_sigma - X).mean()
    assert distortion_high_sigma > distortion_low_sigma, "Higher sigma did not result in larger distortions"

def test_magnitude_warp_no_distortion_with_zero_sigma():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = magnitude_warp(X, sigma=0.0)
    np.testing.assert_array_almost_equal(result, X, err_msg="Sigma=0 resulted in distortion")

#time shift


def test_time_shift_output_shape():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = time_shift(X, shift_max=2)
    assert result.shape == X.shape, "Output shape does not match input shape"

def test_time_shift_values_preserved():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = time_shift(X, shift_max=2)
    assert np.all(np.sort(result, axis=1) == np.sort(X, axis=1)), "Time shift altered the values in the data"

def test_time_shift_no_shift_with_zero_shift_max():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = time_shift(X, shift_max=0)
    np.testing.assert_array_equal(result, X, "Time shift altered the data when shift_max=0")

def test_time_shift_different_shifts():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result1 = time_shift(X, shift_max=1)
    result2 = time_shift(X, shift_max=2)
    assert not np.array_equal(result1, result2), "Time shift with different shift_max values produced the same result"

#scale
def test_scale_output_shape():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = scale(X, sigma=0.1)
    assert result.shape == X.shape, "Output shape does not match input shape"

def test_scale_values_change():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = scale(X, sigma=0.1)
    assert not np.array_equal(result, X), "Scale did not change the values in the data"

def test_scale_with_zero_sigma():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = scale(X, sigma=0.0)
    np.testing.assert_array_almost_equal(result, X, err_msg="Sigma=0 resulted in scaling")

def test_scale_sigma_effect():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result_low_sigma = scale(X, sigma=0.1)
    result_high_sigma = scale(X, sigma=1.0)
    distortion_low_sigma = np.abs(result_low_sigma - X).mean()
    distortion_high_sigma = np.abs(result_high_sigma - X).mean()
    assert distortion_high_sigma > distortion_low_sigma, "Higher sigma did not result in larger distortions"

#permute
def test_permute_output_shape():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = permute(X, max_segments=3)
    assert result.shape == X.shape, "Output shape does not match input shape"

def test_permute_values_preserved():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = permute(X, max_segments=3)
    assert np.all(np.sort(result, axis=1) == np.sort(X, axis=1)), "Permute altered the values in the data"

def test_permute_no_segments_change_with_one_segment():
    # Set a random seed for reproducibility
    np.random.seed(42)
    X = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                  [[10, 11, 12], [13, 14, 15], [16, 17, 18]]], dtype=float)
    result = permute(X, max_segments=1)
    assert np.array_equal(result, X), "Permute changed the data when max_segments=1"