#!/usr/bin/env python3
"""
Interactive pipeline for WPM data processing.
Supports both interactive mode and configuration file mode.
"""

import argparse
import os
import sys
import subprocess
import time
import json


def main():
    """Main CLI function for interactive pipeline."""
    parser = argparse.ArgumentParser(
        description="Interactive WPM data processing pipeline"
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a sample configuration file and exit'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='JSON configuration file to use'
    )
    
    parser.add_argument(
        '--force-regenerate',
        action='store_true',
        help='Regenerate all files without asking, even if they exist'
    )
    
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        help='Skip files that already exist without asking'
    )
    
    args = parser.parse_args()
    
    # Create sample configuration
    if args.create_config:
        create_sample_config()
        return
    
    # Configuration mode
    if args.config:
        run_from_config(args.config, args.force_regenerate, args.skip_existing)
    else:
        # Interactive mode  
        print("🚀 WPM Interactive Pipeline")
        print("Use --create-config to create a sample configuration file")
        print("Then use --config filename.json to run with configuration")


def create_sample_config(output_file="wpm_pipeline_config.json"):
    """Create a sample configuration file."""
    sample_config = {
        "project": {
            "base_folder": "/Users/antoniolopez/desarrollo_codigo/wearablepermed/uniovi-simur-wearablepermed-utils/tests/sandbox/pipe_test",
            "subject_name": "PMP1020_W1_PI",
            "description": "WPM pipeline configuration for subject PMP1020_W1_PI"
        },
        "stages": [1, 2, 3, 4],
        "parameters": {
            "stage2": {
                "activity_log": "/Users/antoniolopez/desarrollo_codigo/wearablepermed/uniovi-simur-wearablepermed-utils/tests/sandbox/pipe_test/PMP1020_RegistroActividades.xlsx",
                "body_position": "Thigh",
                "sample_init": 13261119
            },
            "stage3": {
                "window_size": 250,
                "step_size": 125
            }
        }
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        print(f"✅ Sample configuration created: {output_file}")
        print("   Edit this file with your specific parameters and use --config to run the pipeline.")
        return True
    except Exception as e:
        print(f"❌ Error creating sample configuration: {e}")
        return False


def check_file_exists(output_file, force_regenerate=False, skip_existing=False):
    """Check if file exists and handle regeneration options."""
    if not os.path.exists(output_file):
        return True  # File doesn't exist, proceed
    
    if force_regenerate:
        print(f"🔄 File exists but regenerating: {os.path.basename(output_file)}")
        return True
    
    if skip_existing:
        print(f"⏭️  File exists, skipping: {os.path.basename(output_file)}")
        return False
    
    # Interactive prompt
    print(f"📄 File already exists: {os.path.basename(output_file)}")
    response = input("   Regenerate? [y/N]: ").strip().lower()
    return response == 'y'


def run_from_config(config_file, force_regenerate=False, skip_existing=False):
    """Run pipeline from configuration file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
    
    print("🚀 WPM Pipeline - Configuration Mode")
    print("=" * 50)
    
    # Get configuration
    project = config.get('project', {})
    base_folder = project.get('base_folder')
    subject_name = project.get('subject_name')
    stages = config.get('stages', [])
    params = config.get('parameters', {})
    
    print(f"📂 Project folder: {base_folder}")
    print(f"👤 Subject: {subject_name}")
    print(f"🔧 Stages to run: {stages}")
    print()
    
    # Execute stages
    success = True
    for stage_num in stages:
        if stage_num == 1:
            success = execute_stage1(base_folder, subject_name, force_regenerate, skip_existing)
        elif stage_num == 2:
            success = execute_stage2(base_folder, subject_name, params.get('stage2', {}), force_regenerate, skip_existing)
        elif stage_num == 3:
            success = execute_stage3(base_folder, subject_name, params.get('stage3', {}), force_regenerate, skip_existing)
        elif stage_num == 4:
            success = execute_stage4(base_folder, subject_name, force_regenerate, skip_existing)
        
        if not success:
            print(f"❌ Stage {stage_num} failed. Stopping pipeline.")
            break
    
    if success:
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")


def run_command(command):
    """Run command and show progress."""
    print(f"🔄 Executing: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ Command completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        print(f"Error: {e.stderr}")
        return False


def execute_stage1(base_folder, subject_name, force_regenerate=False, skip_existing=False):
    """Execute Stage 1: BIN to CSV."""
    print(f"\n🔄 Executing Stage 1 - Binary to CSV...")
    
    bin_file = os.path.join(base_folder, f"{subject_name}.BIN")
    csv_file = os.path.join(base_folder, f"{subject_name}.csv")
    
    if not os.path.exists(bin_file):
        print(f"❌ BIN file not found: {bin_file}")
        return False
    
    # Check if output file exists
    if not check_file_exists(csv_file, force_regenerate, skip_existing):
        return True  # Skip this stage
    
    command = ['sensor_bin_to_csv', bin_file, csv_file]
    return run_command(command)


def execute_stage2(base_folder, subject_name, stage2_params, force_regenerate=False, skip_existing=False):
    """Execute Stage 2: CSV to Segmented."""
    print(f"\n🔄 Executing Stage 2 - CSV to Segmented Activity...")
    
    csv_file = os.path.join(base_folder, f"{subject_name}.csv")
    output_file = os.path.join(base_folder, f"{subject_name}_segmented.npz")
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    # Check if output file exists
    if not check_file_exists(output_file, force_regenerate, skip_existing):
        return True  # Skip this stage
    
    command = [
        'csv_to_segmented_activity', 
        csv_file, 
        stage2_params.get('activity_log'),
        stage2_params.get('body_position', 'Thigh')
    ]
    
    if stage2_params.get('sample_init'):
        command.extend(['--sample-init', str(stage2_params['sample_init'])])
    
    command.extend(['--output', output_file])
    
    return run_command(command)


def execute_stage3(base_folder, subject_name, stage3_params, force_regenerate=False, skip_existing=False):
    """Execute Stage 3: Segmented to Stack."""
    print(f"\n🔄 Executing Stage 3 - Segmented to Stack...")
    
    segmented_file = os.path.join(base_folder, f"{subject_name}_segmented.npz")
    output_file = os.path.join(base_folder, f"{subject_name}_stacked.npz")
    
    if not os.path.exists(segmented_file):
        print(f"❌ Segmented file not found: {segmented_file}")
        return False
    
    # Check if output file exists
    if not check_file_exists(output_file, force_regenerate, skip_existing):
        return True  # Skip this stage
    
    command = ['segmented_activity_to_stack', segmented_file]
    command.extend(['--window-size', str(stage3_params.get('window_size', 250))])
    command.extend(['--step-size', str(stage3_params.get('step_size', 125))])
    command.extend(['--output', output_file])
    
    return run_command(command)


def execute_stage4(base_folder, subject_name, force_regenerate=False, skip_existing=False):
    """Execute Stage 4: Stack to Features."""
    print(f"\n🔄 Executing Stage 4 - Stack to Features...")
    
    stack_file = os.path.join(base_folder, f"{subject_name}_stacked.npz")
    output_file = os.path.join(base_folder, f"{subject_name}_features.npz")
    
    if not os.path.exists(stack_file):
        print(f"❌ Stack file not found: {stack_file}")
        return False
    
    # Check if output file exists
    if not check_file_exists(output_file, force_regenerate, skip_existing):
        return True  # Skip this stage
    
    command = ['stack_to_features', stack_file, '--output', output_file]
    
    return run_command(command)


if __name__ == "__main__":
    main()
