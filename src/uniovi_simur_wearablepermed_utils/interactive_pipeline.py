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
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be executed without actually running commands'
    )
    
    args = parser.parse_args()
    
    # Create sample configuration
    if args.create_config:
        create_sample_config()
        return
    
    # Configuration mode
    if args.config:
        run_from_config(args.config, args.force_regenerate, args.skip_existing, args.dry_run)
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
            "project_name": "PMP_Study",
            "description": "WPM pipeline configuration for multiple subjects"
        },
        "subjects": [
            {
                "name": "PMP1020_W1_PI",
                "bin_file": "PMP1020_W1_PI.BIN",
                "body_position": "Thigh",
                "sample_init": 13261119
            },
            {
                "name": "PMP1051_W1_PI", 
                "bin_file": "PMP1051_W1_PI.BIN",
                "body_position": "Thigh",
                "sample_init": None
            }
        ],
        "stages": [1, 2, 3, 4],
        "parameters": {
            "stage2": {
                "activity_log": "/Users/antoniolopez/desarrollo_codigo/wearablepermed/uniovi-simur-wearablepermed-utils/tests/sandbox/pipe_test/PMP1020_RegistroActividades.xlsx"
            },
            "stage3": {
                "window_size": 250,
                "step_size": 125,
                "combined_output": "combined_stacked.npz"
            },
            "stage4": {
                "combined_output": "combined_features.npz"
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


def run_from_config(config_file, force_regenerate=False, skip_existing=False, dry_run=False):
    """Run pipeline from configuration file with multiple subjects support."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
    
    dry_run_text = " (DRY RUN)" if dry_run else ""
    print(f"🚀 WPM Pipeline - Multi-Subject Configuration Mode{dry_run_text}")
    print("=" * (60 + len(dry_run_text)))
    
    # Get configuration
    project = config.get('project', {})
    base_folder = project.get('base_folder')
    project_name = project.get('project_name', 'WPM_Project')
    subjects = config.get('subjects', [])
    stages = config.get('stages', [])
    params = config.get('parameters', {})
    
    print(f"📂 Project folder: {base_folder}")
    print(f"📋 Project name: {project_name}")
    print(f"� Subjects: {len(subjects)}")
    for i, subject in enumerate(subjects, 1):
        sample_init_info = f" (sample_init: {subject.get('sample_init')})" if subject.get('sample_init') else ""
        print(f"   {i}. {subject['name']}{sample_init_info}")
    print(f"🔧 Stages to run: {stages}")
    print()
    
    # Track regeneration cascade
    regenerate_from_stage = None
    
    # Execute stages
    success = True
    for stage_num in stages:
        print(f"\n{'='*60}")
        print(f"📋 STAGE {stage_num}")
        print(f"{'='*60}")
        
        stage_regenerated = False
        
        if stage_num == 1:
            success, stage_regenerated = execute_stage1_multi(base_folder, subjects, force_regenerate, skip_existing, regenerate_from_stage, dry_run)
        elif stage_num == 2:
            success, stage_regenerated = execute_stage2_multi(base_folder, subjects, params.get('stage2', {}), force_regenerate, skip_existing, regenerate_from_stage, dry_run)
        elif stage_num == 3:
            success, stage_regenerated = execute_stage3_multi(base_folder, subjects, params.get('stage3', {}), force_regenerate, skip_existing, regenerate_from_stage, dry_run)
        elif stage_num == 4:
            success, stage_regenerated = execute_stage4_multi(base_folder, subjects, params.get('stage4', {}), force_regenerate, skip_existing, regenerate_from_stage, dry_run)
        
        if not success:
            print(f"❌ Stage {stage_num} failed. Stopping pipeline.")
            break
        
        # If this stage was regenerated, cascade to following stages
        if stage_regenerated and regenerate_from_stage is None:
            regenerate_from_stage = stage_num
            print(f"🔄 Stage {stage_num} regenerated - will cascade to following stages")
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 MULTI-SUBJECT PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📁 Project: {project_name}")
        print(f"👥 Processed {len(subjects)} subjects")
        print("✅ All stages completed")
    
    return success


def run_command(command, dry_run=False):
    """Run a command or show what would be executed in dry-run mode."""
    if dry_run:
        print(f"    [DRY RUN] Would execute: {' '.join(command)}")
        return True
    else:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"    ✅ Command executed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"    ❌ Command failed: {e}")
            print(f"    Error output: {e.stderr}")
            return False


def check_file_exists_dry_run(file_path, force_regenerate, skip_existing, dry_run):
    """Check file existence with dry-run support."""
    if dry_run:
        exists = os.path.exists(file_path)
        if exists:
            if force_regenerate:
                print(f"    [DRY RUN] File exists but would be regenerated: {file_path}")
                return True  # Would regenerate
            elif skip_existing:
                print(f"    [DRY RUN] File exists and would be skipped: {file_path}")
                return False  # Would skip
            else:
                print(f"    [DRY RUN] File exists, would ask user: {file_path}")
                return True  # Would ask, assume regenerate for dry-run
        else:
            print(f"    [DRY RUN] File does not exist, would create: {file_path}")
            return True  # Would create
    else:
        return check_file_exists(file_path, force_regenerate, skip_existing)


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


def execute_stage1_multi(base_folder, subjects, force_regenerate=False, skip_existing=False, regenerate_from_stage=None, dry_run=False):
    """Execute Stage 1 for multiple subjects: BIN to CSV."""
    dry_run_text = " [DRY RUN]" if dry_run else ""
    print(f"\n🔄 Executing Stage 1 - Binary to CSV for {len(subjects)} subjects...{dry_run_text}")
    
    any_regenerated = False
    
    for i, subject in enumerate(subjects, 1):
        subject_name = subject['name']
        print(f"\n  [{i}/{len(subjects)}] Processing {subject_name}...")
        
        bin_file = os.path.join(base_folder, f"{subject_name}.BIN")
        csv_file = os.path.join(base_folder, f"{subject_name}.csv")
        
        if not os.path.exists(bin_file):
            print(f"    ❌ BIN file not found: {bin_file}")
            return False, any_regenerated
        
        # Check if output file exists and decide regeneration
        should_regenerate = force_regenerate or (regenerate_from_stage is not None and regenerate_from_stage <= 1)
        
        if not check_file_exists_dry_run(csv_file, should_regenerate, skip_existing, dry_run):
            print(f"    ⏭️  Skipping {subject_name} (file exists)")
            continue  # Skip this subject
        
        any_regenerated = True
        command = ['sensor_bin_to_csv', bin_file, csv_file]
        if not run_command(command, dry_run):
            print(f"    ❌ Failed processing {subject_name}")
            return False, any_regenerated
        print(f"    ✅ Completed {subject_name}")
    
    return True, any_regenerated


def execute_stage2_multi(base_folder, subjects, stage2_params, force_regenerate=False, skip_existing=False, regenerate_from_stage=None, dry_run=False):
    """Execute Stage 2 for multiple subjects: CSV to Segmented."""
    dry_run_text = " [DRY RUN]" if dry_run else ""
    print(f"\n🔄 Executing Stage 2 - CSV to Segmented Activity for {len(subjects)} subjects...{dry_run_text}")
    
    any_regenerated = False
    
    for i, subject in enumerate(subjects, 1):
        subject_name = subject['name']
        print(f"\n  [{i}/{len(subjects)}] Processing {subject_name}...")
        
        csv_file = os.path.join(base_folder, f"{subject_name}.csv")
        output_file = os.path.join(base_folder, f"{subject_name}_segmented.npz")
        
        if not os.path.exists(csv_file):
            print(f"    ❌ CSV file not found: {csv_file}")
            return False, any_regenerated
        
        # Check if output file exists and decide regeneration
        should_regenerate = force_regenerate or (regenerate_from_stage is not None and regenerate_from_stage <= 2)
        
        if not check_file_exists_dry_run(output_file, should_regenerate, skip_existing, dry_run):
            print(f"    ⏭️  Skipping {subject_name} (file exists)")
            continue  # Skip this subject
        
        any_regenerated = True
        command = [
            'csv_to_segmented_activity', 
            csv_file, 
            stage2_params.get('activity_log')
        ]
        
        # Use subject-specific body_position if available, otherwise use global
        subject_body_position = subject.get('body_position')
        global_body_position = stage2_params.get('body_position', 'Thigh')
        body_position = subject_body_position if subject_body_position is not None else global_body_position
        command.append(body_position)
        
        # Use subject-specific sample_init if available, otherwise use global
        subject_sample_init = subject.get('sample_init')
        global_sample_init = stage2_params.get('sample_init')
        sample_init = subject_sample_init if subject_sample_init is not None else global_sample_init
        
        if sample_init:
            command.extend(['--sample-init', str(sample_init)])
        
        command.extend(['--output', output_file])
        
        if not run_command(command, dry_run):
            print(f"    ❌ Failed processing {subject_name}")
            return False, any_regenerated
        print(f"    ✅ Completed {subject_name}")
    
    return True, any_regenerated


def execute_stage3_multi(base_folder, subjects, stage3_params, force_regenerate=False, skip_existing=False, regenerate_from_stage=None, dry_run=False):
    """Execute Stage 3 for multiple subjects: Segmented to Stack with combination."""
    dry_run_text = " [DRY RUN]" if dry_run else ""
    print(f"\n🔄 Executing Stage 3 - Segmented to Stack for {len(subjects)} subjects...{dry_run_text}")
    
    any_regenerated = False
    combined_output = os.path.join(base_folder, "all_subjects_stacked.npz")
    
    # Check if we need to regenerate the combined file
    should_regenerate = force_regenerate or (regenerate_from_stage is not None and regenerate_from_stage <= 3)
    
    if not check_file_exists_dry_run(combined_output, should_regenerate, skip_existing, dry_run):
        print(f"    ⏭️  Skipping Stage 3 (combined file exists)")
        return True, any_regenerated
    
    any_regenerated = True
    
    # Collect all segmented files
    segmented_files = []
    for i, subject in enumerate(subjects, 1):
        subject_name = subject['name']
        segmented_file = os.path.join(base_folder, f"{subject_name}_segmented.npz")
        
        if not os.path.exists(segmented_file):
            print(f"    ❌ Segmented file not found: {segmented_file}")
            return False, any_regenerated
        
        segmented_files.append(segmented_file)
        print(f"  ✓ Found segmented file for {subject_name}")
    
    # Combine all segmented files directly into stack
    print(f"\n  🔗 Creating combined stack from {len(segmented_files)} segmented files...")
    combine_command = ['segmented_activity_to_stack'] + segmented_files
    combine_command.extend(['--crop-columns', '1:7'])  # Default crop columns
    combine_command.extend(['--window-size', str(stage3_params.get('window_size', 250))])
    combine_command.extend(['--step-size', str(stage3_params.get('step_size', 125))])
    combine_command.extend(['--output', combined_output])
    
    if not run_command(combine_command, dry_run):
        print(f"    ❌ Failed creating combined stack")
        return False, any_regenerated
    
    print(f"    ✅ Combined stack file created: {combined_output}")
    return True, any_regenerated


def execute_stage4_multi(base_folder, subjects, stage4_params, force_regenerate=False, skip_existing=False, regenerate_from_stage=None, dry_run=False):
    """Execute Stage 4 for multiple subjects: Stack to Features with combination."""
    dry_run_text = " [DRY RUN]" if dry_run else ""
    print(f"\n🔄 Executing Stage 4 - Stack to Features for combined data...{dry_run_text}")
    
    any_regenerated = False
    combined_stack = os.path.join(base_folder, "all_subjects_stacked.npz")
    combined_features = os.path.join(base_folder, "all_subjects_features.npz")
    
    if not os.path.exists(combined_stack):
        print(f"    ❌ Combined stack file not found: {combined_stack}")
        print("    💡 Make sure Stage 3 has been completed first")
        return False, any_regenerated
    
    # Check if we need to regenerate the features file
    should_regenerate = force_regenerate or (regenerate_from_stage is not None and regenerate_from_stage <= 4)
    
    if not check_file_exists_dry_run(combined_features, should_regenerate, skip_existing, dry_run):
        print(f"    ⏭️  Skipping Stage 4 (features file exists)")
        return True, any_regenerated
    
    any_regenerated = True
    command = ['stack_to_features', combined_stack]
    
    # Determine number of IMUs
    n_imus_config = stage4_params.get('n_imus', 'auto')
    if n_imus_config == 'auto':
        n_imus = len(subjects)  # Auto-detect: one IMU per subject
    else:
        n_imus = int(n_imus_config)
    
    command.extend(['--n-imus', str(n_imus)])
    command.extend(['--output', combined_features])
    
    if dry_run:
        print(f"    [DRY RUN] Using {n_imus} IMUs (auto-detected from {len(subjects)} subjects)")
    
    if not run_command(command, dry_run):
        print(f"    ❌ Failed generating features")
        return False, any_regenerated
    
    print(f"    ✅ Features file created: {combined_features}")
    return True, any_regenerated


if __name__ == "__main__":
    main()
