#!/usr/bin/env python3
"""
Script para extraer features desde un archivo NPZ de stack de datos enventanados.
Utiliza la función extract_features_from_stack del módulo feature_extraction.
"""

import os
import sys
import argparse
import numpy as np

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from uniovi_simur_wearablepermed_utils.feature_extraction import extract_features_from_stack


def main():
    parser = argparse.ArgumentParser(
        description="Extract features from a stacked NPZ file containing windowed data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default parameters
  python stack_to_features.py data_stack.npz --output features.npz

  # Specify number of IMUs
  python stack_to_features.py data_stack.npz --n-imus 1 --output features.npz

  # With verbose output
  python stack_to_features.py data_stack.npz --n-imus 2 --output features.npz --verbose

  # Real example with project data
  python stack_to_features.py ../examples/data/stacks/data_tot_PMP1020_1051.npz --output features_extracted.npz --verbose
        """
    )
    
    parser.add_argument(
        'stack_file',
        type=str,
        help='Path to the NPZ file containing stacked windowed data'
    )
    
    parser.add_argument(
        '--n-imus',
        type=int,
        default=2,
        help='Number of IMUs in the stack data (default: 2)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Output NPZ file path to save extracted features'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.stack_file):
        print(f"Error: Stack file not found: {args.stack_file}", file=sys.stderr)
        sys.exit(1)
    
    if not args.stack_file.endswith('.npz'):
        print(f"Warning: Input file {args.stack_file} does not have .npz extension")
    
    # Validate n_imus
    if args.n_imus <= 0:
        print("Error: Number of IMUs must be positive", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if args.verbose:
            print(f"Created output directory: {output_dir}")
    
    if args.verbose:
        print("=== Stack to Features Extraction ===")
        print(f"Stack file: {args.stack_file}")
        print(f"Number of IMUs: {args.n_imus}")
        print(f"Output file: {args.output}")
        print()
    
    try:
        # Extract features from stack
        result = extract_features_from_stack(args.stack_file, n_imus=args.n_imus)
        
        if args.verbose:
            print("✓ Feature extraction completed successfully!")
            print(f"✓ Features shape: {result['features'].shape}")
            print(f"✓ Number of windows: {result['num_windows']}")
            print(f"✓ Data shape: {result['data_shape']}")
            print(f"✓ Unique labels: {len(result['unique_labels'])}")
            print(f"✓ Labels: {list(result['unique_labels'])}")
            print()
            
            # Show label distribution
            unique_labels, counts = np.unique(result['labels'], return_counts=True)
            print("Label distribution:")
            for label, count in zip(unique_labels, counts):
                print(f"  {label}: {count} windows")
            print()
        
        # Save results to NPZ file
        np.savez(
            args.output,
            features=result['features'],
            labels=result['labels'],
            windowed_data=result['windowed_data'],
            data_shape=result['data_shape'],
            num_windows=result['num_windows'],
            unique_labels=result['unique_labels']
        )
        
        if args.verbose:
            print(f"✓ Results saved to: {args.output}")
            file_size = os.path.getsize(args.output)
            print(f"✓ Output file size: {file_size} bytes")
        else:
            print(f"Features extracted and saved to: {args.output}")
            
    except Exception as e:
        print(f"Error during feature extraction: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
