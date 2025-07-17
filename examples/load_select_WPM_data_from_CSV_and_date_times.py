"""
This example:
- Load a CSV MATRIX/WPM data.
- Extracts the Matrix "Sit to Stand" activity data, located betwwen timestamp dates 2024/7/3-12:18:47 and 2024/7/3-12:19:17
  The data consists of Time Stamp, IMU data, temperatures and PPG data.
- Plots the data (except the time stamp).
"""

import sys  # Import the sys module for system-specific parameters and functions
import os  # Import the os module for interacting with the operating system
import datetime  # Import the datetime module for manipulating dates and times
import matplotlib.pyplot as plt  # Import pyplot from matplotlib for data visualization
import uniovi_simur_wearablepermed_utils as wpm 



# Load IMU data from the CSV file for the "Wrist" segment
WPM_data = wpm.file_management.load_WPM_data("./examples/data/PMP1020_W1_PI.CSV", "Thigh")

# Define the initial datetime for the sit-stand activity
sit_stand_init = datetime.datetime(2024, 7, 3, 12, 18, 47)
# Define the end datetime for the sit-stand activity
sit_stand_end = datetime.datetime(2024, 7, 3, 12, 19, 17)

# Segment the IMU data based on the specified start and end times for the sit-stand activity
sit_stand_data = wpm.segmentation.segment_MATRIX_data_by_dates(WPM_data, sit_stand_init, sit_stand_end)

fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# First subplot: sit-stand data (excluding the first column)
axs[0].plot(sit_stand_data[:, 1:7])
axs[0].set_title('Sit-Stand Data')
axs[0].set_ylabel('Sit-Stand Values')

# Second subplot: temperature data
axs[1].plot(sit_stand_data[:, 7:9])
axs[1].set_title('Temperature Data')
axs[1].set_ylabel('Temperature Values')

# Third subplot: PPG data
axs[2].plot(sit_stand_data[:, 9:])
axs[2].set_title('PPG Data')
axs[2].set_ylabel('PPG Values')

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the final plot with subplots
plt.show()