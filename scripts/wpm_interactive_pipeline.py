#!/usr/bin/env python3
"""
Interactive pipeline script for WPM data processing.
Standalone version that can be run directly.
"""

import sys
import os

# Add the package to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from uniovi_simur_wearablepermed_utils.interactive_pipeline import main

if __name__ == "__main__":
    main()
