#!/usr/bin/env python3
"""
Script para procesar datos CSV y convertirlos en datos segmentados WPM desde línea de comandos.
Utiliza la función load_segment_wpm_data del módulo file_management.
"""

import os
import sys
import argparse

# Add src directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from uniovi_simur_wearablepermed_utils.file_management import load_segment_wpm_data

def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV WPM data to segmented data: load, scale, segment and optionally plot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic processing with plots
  python csv2segmented_data.py data.csv activities.xlsx Thigh

  # Process and save to file
  python csv2segmented_data.py data.csv activities.xlsx Thigh --output results

  # Process without plots and with custom sample init
  python csv2segmented_data.py data.csv activities.xlsx Wrist --sample-init 1000 --no-plot

  # Process WPM data from examples
  python csv2segmented_data.py \
    ../examples/data/PMP1020_W1_PI.CSV \
    ../examples/data/PMP1020_RegistroActividades.xlsx \
    Thigh --output PMP1020_processed --verbose
        """
    )
    
    # Required arguments
    parser.add_argument(
        'csv_file',
        help='Path to CSV file with MATRIX data'
    )
    
    parser.add_argument(
        'excel_activity_log',
        help='Path to Excel file with activity log'
    )
    
    parser.add_argument(
        'body_segment',
        choices=['Thigh', 'Wrist', 'Hip'],
        help='Body segment where the IMU is placed'
    )
    
    # Optional arguments
    parser.add_argument(
        '--plot',
        action='store_true',
        default=True,
        help='Show plots of segmented data (default: True)'
    )
    
    parser.add_argument(
        '--no-plot',
        action='store_false',
        dest='plot',
        help='Do not show plots of segmented data'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file name (without extension) to save segmented data'
    )
    
    parser.add_argument(
        '--sample-init',
        type=int,
        default=None,
        help='Sample index for "CAMINAR - USUAL SPEED" start'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.excel_activity_log):
        print(f"Error: Excel file not found: {args.excel_activity_log}", file=sys.stderr)
        sys.exit(1)
    
    if not args.csv_file.upper().endswith('.CSV'):
        print(f"Warning: CSV file {args.csv_file} does not have .CSV extension")
    
    if not args.excel_activity_log.upper().endswith(('.XLS', '.XLSX')):
        print(f"Warning: Excel file {args.excel_activity_log} does not have .xls/.xlsx extension")
    
    if args.verbose:
        print("=== CSV to Segmented WPM Data Processing ===")
        print(f"CSV file: {args.csv_file}")
        print(f"Excel file: {args.excel_activity_log}")
        print(f"Body segment: {args.body_segment}")
        print(f"Show plots: {args.plot}")
        print(f"Output file: {args.output if args.output else 'Not specified'}")
        print(f"Sample init: {args.sample_init if args.sample_init else 'Auto'}")
        print()
    
    try:
        if args.verbose:
            print("Starting WPM data processing...")
        
        # Execute main function
        load_segment_wpm_data(
            csv_file=args.csv_file,
            excel_activity_log=args.excel_activity_log,
            body_segment=args.body_segment,
            plot_data=args.plot,
            out_file=args.output,
            sample_init_CAMINAR_USUAL_SPEED=args.sample_init
        )
        
        if args.verbose:
            print("\n✓ Processing completed successfully!")
        else:
            print("✓ Processing completed successfully!")
            
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error during processing: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
