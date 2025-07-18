#!/usr/bin/env python3
"""
Script para convertir archivos .BIN a .CSV desde línea de comandos.
Utiliza la función bin2csv del módulo bin2csv.
"""

import os
import sys
import argparse

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from uniovi_simur_wearablepermed_utils.bin2csv import bin2csv

def main():
    parser = argparse.ArgumentParser(
        description="Convert a .BIN file to .CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a BIN file to CSV
  python convert_bin_to_csv.py input.BIN output.csv

  # Using relative paths
  python convert_bin_to_csv.py ../data/sensor_data.BIN ../output/converted_data.csv
        """
    )
    
    parser.add_argument(
        'bin_file',
        type=str,
        help='Path to the input .BIN file'
    )
    
    parser.add_argument(
        'csv_file',
        type=str,
        help='Path to the output .CSV file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.bin_file):
        print(f"Error: Input file not found: {args.bin_file}", file=sys.stderr)
        sys.exit(1)
    
    if not args.bin_file.upper().endswith('.BIN'):
        print(f"Warning: Input file {args.bin_file} does not have .BIN extension")
    
    # Validate output directory
    output_dir = os.path.dirname(args.csv_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            if args.verbose:
                print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error: Cannot create output directory {output_dir}: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.verbose:
        print(f"Converting {args.bin_file} to {args.csv_file}")
    
    try:
        result = bin2csv(args.bin_file, args.csv_file)
        
        if result == 0:
            if args.verbose:
                print("✓ Conversion completed successfully!")
            else:
                print("Conversion completed successfully!")
        else:
            print(f"✗ Conversion failed with error code: {result}", file=sys.stderr)
            sys.exit(result)
            
    except Exception as e:
        print(f"✗ Error during conversion: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
