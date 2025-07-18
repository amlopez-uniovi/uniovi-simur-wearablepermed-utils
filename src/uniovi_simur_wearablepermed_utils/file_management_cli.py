#!/usr/bin/env python3
"""
CLI wrapper for file_management load_segment functionality.
"""

import argparse
import os
import sys
from .file_management import load_segment_wpm_data


def main():
    """Main CLI function for CSV to segmented activity conversion."""
    parser = argparse.ArgumentParser(
        description="Procesa datos WPM: carga, escala, segmenta y opcionalmente grafica los datos."
    )
    
    parser.add_argument(
        "csv_file", 
        type=str, 
        help="Ruta al archivo CSV con datos de MATRIX"
    )
    parser.add_argument(
        "excel_activity_log", 
        type=str, 
        help="Ruta al archivo Excel con el registro de actividades"
    )
    parser.add_argument(
        "body_segment", 
        choices=['Thigh', 'Wrist', 'Hip'],
        help="Segmento corporal donde está colocado el IMU"
    )
    
    parser.add_argument(
        "--plot", 
        action="store_true",
        help="Mostrar gráficos de los datos segmentados"
    )
    parser.add_argument(
        "--no-plot", 
        action="store_true",
        help="No mostrar gráficos"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Nombre del archivo de salida"
    )
    parser.add_argument(
        "--sample-init",
        type=int,
        help="Índice de muestra para el inicio de \"CAMINAR - USUAL SPEED\""
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(args.excel_activity_log):
        print(f"Error: Excel file not found: {args.excel_activity_log}", file=sys.stderr)
        sys.exit(1)
    
    # Determine plot setting
    plot = True
    if args.no_plot:
        plot = False
    elif args.plot:
        plot = True
    
    if args.verbose:
        print("=== CSV to Segmented Activity Processing ===")
        print(f"CSV file: {args.csv_file}")
        print(f"Excel activity log: {args.excel_activity_log}")
        print(f"Body segment: {args.body_segment}")
        print(f"Plot: {plot}")
        if args.output:
            print(f"Output: {args.output}")
        if args.sample_init:
            print(f"Sample init: {args.sample_init}")
        print()
    
    try:
        # Call the main processing function
        result = load_segment_wpm_data(
            csv_file=args.csv_file,
            excel_activity_log=args.excel_activity_log,
            body_segment=args.body_segment,
            plot_data=plot,
            out_file=args.output,
            sample_init_CAMINAR_USUAL_SPEED=args.sample_init
        )
        
        if args.verbose:
            print("✓ Processing completed successfully!")
            if args.output:
                print(f"✓ Results saved to: {args.output}")
        
        return result
        
    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
