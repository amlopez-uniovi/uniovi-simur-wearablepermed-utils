"""
This example:
- Converts a .BIN Matrix file to CSV format.
"""

import sys  # Import the sys module for system-specific parameters and functions
import os  # Import the os module for interacting with the operating system
import uniovi_simur_wearablepermed_utils as wpm  # Import the simur_wpm_utils module for wearable permed utilities



# Convert a binary file to CSV format using a function from the simur_hmc module
wpm.bin2csv.bin2csv("./examples/data/PMP1020_W1_PI.BIN", "./examples/data/PMP1020_W1_PI.CSV")
