#!/usr/bin/env python3
"""
CLI wrapper for segmentation functionality.
"""

import argparse
import sys
import os
import numpy as np
from .segmentation import load_concat_window_stack


def parse_crop_columns(crop_str):
    """Parse crop columns argument from string to slice or list."""
    if crop_str is None:
        return slice(None)
    
    try:
        # Try to parse as slice notation (e.g., "1:7")
        if ':' in crop_str:
            parts = crop_str.split(':')
            if len(parts) == 2:
                start = int(parts[0]) if parts[0] else None
                end = int(parts[1]) if parts[1] else None
                return slice(start, end)
            elif len(parts) == 3:
                start = int(parts[0]) if parts[0] else None
                end = int(parts[1]) if parts[1] else None
                step = int(parts[2]) if parts[2] else None
                return slice(start, end, step)
        else:
            # Try to parse as comma-separated list (e.g., "1,2,3,4,5,6")
            return [int(x.strip()) for x in crop_str.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid crop columns format: {crop_str}")


def main():
    parser = argparse.ArgumentParser(
        description="Load, concatenate, window, and stack WPM data from NPZ files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with two files
  segmented_activity_to_stack file1.npz file2.npz --crop-columns 1:7 --window-size 250

  # With step size and output file
  segmented_activity_to_stack file1.npz file2.npz --crop-columns 1:7 --window-size 250 --step-size 125 --output result.npz

  # Using specific columns
  segmented_activity_to_stack file1.npz file2.npz --crop-columns 1,2,3,4,5,6 --window-size 250
        """
    )
    
    parser.add_argument(
        'npz_files', 
        nargs='+',
        help='Paths to NPZ files to process'
    )
    
    parser.add_argument(
        '--crop-columns', '-c',
        type=parse_crop_columns,
        default=slice(1, 7),
        help='Columns to select from arrays. Format: "start:end" or "col1,col2,col3". Default: "1:7"'
    )
    
    parser.add_argument(
        '--window-size', '-w',
        type=int,
        required=True,
        help='Window size in number of samples'
    )
    
    parser.add_argument(
        '--step-size', '-s',
        type=int,
        default=None,
        help='Step size for windowing (default: same as window size for no overlap)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file name to save results (.npz format)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    for file_path in args.npz_files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        if not file_path.endswith('.npz'):
            print(f"Warning: File {file_path} does not have .npz extension")
    
    # Validate window size
    if args.window_size <= 0:
        print("Error: Window size must be positive", file=sys.stderr)
        sys.exit(1)
    
    # Validate step size
    if args.step_size is not None and args.step_size <= 0:
        print("Error: Step size must be positive", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print("=== Segmented Activity to Stack Processing ===")
        print(f"Processing {len(args.npz_files)} files:")
        for i, file_path in enumerate(args.npz_files, 1):
            print(f"  {i}. {file_path}")
        print(f"Crop columns: {args.crop_columns}")
        print(f"Window size: {args.window_size}")
        print(f"Step size: {args.step_size if args.step_size else 'same as window size'}")
        if args.output:
            print(f"Output file: {args.output}")
        print()
    
    try:
        # Execute the main function
        stacked_data, labels = load_concat_window_stack(
            npz_file_paths=args.npz_files,
            crop_columns=args.crop_columns,
            window_size_samples=args.window_size,
            step_size_samples=args.step_size,
            save_file_name=args.output
        )
        
        if args.verbose:
            print("✓ Processing completed successfully!")
            print(f"✓ Stacked data shape: {stacked_data.shape}")
            print(f"✓ Number of labels: {len(labels)}")
            
            # Show unique activities
            unique_activities = np.unique(labels)
            print(f"✓ Unique activities: {len(unique_activities)}")
            
            # Show label distribution
            print("\nLabel distribution:")
            for label in unique_activities:
                count = np.sum(labels == label)
                print(f"  {label}: {count} windows")
            print()
        
        if args.output:
            if args.verbose:
                print(f"✓ Results saved to: {args.output}")
        else:
            if args.verbose:
                print("Results not saved (use --output to save)")
            
    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
