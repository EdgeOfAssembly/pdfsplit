#!/usr/bin/env python3
import sys
import argparse
import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description='PDF Splitter Script')
    parser.add_argument('input_pdf', help='Path to the input PDF file.')
    parser.add_argument('-p', '--pages', default=None, help='Page specification, e.g., "1,7,67" or "1-10" or "56-".')
    parser.add_argument('-g', '--granularity', type=int, default=1, help='Granularity for splitting the entire PDF (used if no pages specified).')
    parser.add_argument('-d', '--directory', default='.', help='Output directory for the split PDF files (default: current directory).')
    parser.add_argument('--prefix', default=None, help='Custom prefix for output filenames (default: input PDF filename without extension).')
    parser.add_argument('--force', action='store_true', help='Force overwrite of existing output files without prompting.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress all non-error output, including progress bar.')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(2)

    try:
        reader = PdfReader(input_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        sys.exit(3)

    total_pages = len(reader.pages)
    if total_pages == 0:
        print("Error: The PDF is empty.")
        sys.exit(4)

    # Determine padding width based on total pages
    pad_width = len(str(total_pages))

    # Ensure output directory exists
    output_dir = Path(args.directory)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory '{output_dir}': {e}")
        sys.exit(5)

    # Set prefix (default to input filename stem if not provided)
    stem = args.prefix if args.prefix else input_path.stem
    ranges = []

    if args.pages is None:
        gran = max(1, args.granularity)
        start = 1
        while start <= total_pages:
            end = min(start + gran - 1, total_pages)
            ranges.append((start, end))
            start = end + 1
    else:
        parts = args.pages.split(',')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            try:
                if '-' in part:
                    split_part = part.split('-')
                    if len(split_part) != 2:
                        raise ValueError
                    start_str, end_str = split_part
                    start = int(start_str) if start_str else 1
                    end = int(end_str) if end_str else total_pages
                else:
                    start = int(part)
                    end = start
                if start < 1 or end > total_pages or start > end:
                    raise ValueError
                ranges.append((start, end))
            except ValueError:
                print(f"Error: Invalid page specification '{part}'.")
                sys.exit(6)

    # Initialize progress bar unless quiet mode
    if not args.quiet:
        progress_bar = tqdm(total=len(ranges), desc="Splitting PDF", unit="file")

    for start, end in ranges:
        writer = PdfWriter()
        for page_num in range(start - 1, end):
            writer.add_page(reader.pages[page_num])
        if start == end:
            output_filename = f"{stem}_page_{start:0{pad_width}d}.pdf"
        else:
            output_filename = f"{stem}_pages_{start:0{pad_width}d}-{end:0{pad_width}d}.pdf"
        output_path = output_dir / output_filename

        # Check for overwrite
        if output_path.exists() and not args.force:
            print(f"File '{output_path}' already exists. Overwrite? (Y/N): ", end="", flush=True)
            try:
                response = input().strip().lower()
                if response != 'y':
                    print(f"Skipping '{output_path}'.")
                    if not args.quiet:
                        progress_bar.update(1)
                    continue
            except EOFError:
                print("\nInput interrupted. Skipping '{output_path}'.")
                if not args.quiet:
                    progress_bar.update(1)
                continue

        try:
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            if not args.quiet:
                progress_bar.update(1)
        except Exception as e:
            print(f"Error writing '{output_path}': {e}")
            if not args.quiet:
                progress_bar.update(1)

    if not args.quiet:
        progress_bar.close()

if __name__ == "__main__":
    main()