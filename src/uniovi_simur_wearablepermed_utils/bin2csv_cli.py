#!/usr/bin/env python3
"""
CLI wrapper for bin2csv functionality.
"""

import argparse
import os
import sys
from .bin2csv import bin2csv


def main():
    """Main CLI function for bin2csv conversion."""
    parser = argparse.ArgumentParser(
        description="Convert a .BIN file to .CSV using bin2csv."
    )
    parser.add_argument(
        "bin_file", 
        type=str, 
        help="Path to the input .BIN file"
    )
    parser.add_argument(
        "csv_file", 
        type=str, 
        help="Path to the output .CSV file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.bin_file):
        print(f"Error: Input file not found: {args.bin_file}", file=sys.stderr)
        sys.exit(1)
    
    if not args.bin_file.upper().endswith('.BIN'):
        print(f"Warning: Input file {args.bin_file} does not have .BIN extension")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.csv_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if args.verbose:
            print(f"Created output directory: {output_dir}")
    
    try:
        if args.verbose:
            print(f"Converting {args.bin_file} to {args.csv_file}")
        
        # Call the main conversion function
        result = bin2csv(args.bin_file, args.csv_file)
        
        if args.verbose:
            print(f"✓ Conversion completed successfully!")
            if os.path.exists(args.csv_file):
                file_size = os.path.getsize(args.csv_file)
                print(f"✓ Output file size: {file_size} bytes")
        
        return result
        
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
