#!/usr/bin/env python3

import argparse
from Bio import SeqIO

def extract_region(input_file, output_file, start, end):
    """
    Extracts a specific region from sequences in a FASTA file.

    Args:
        input_file (str): Path to the input FASTA file.
        output_file (str): Path to the output FASTA file.
        start (int): Start position of the region (1-based).
        end (int): End position of the region (1-based).
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for record in SeqIO.parse(infile, 'fasta'):
            # Adjust for 0-based indexing in Python
            region = record.seq[start - 1:end]
            record.seq = region
            record.description += f" region:{start}-{end}"
            SeqIO.write(record, outfile, 'fasta')

def main():
    parser = argparse.ArgumentParser(description="Extract a region from a FASTA file.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file.")
    parser.add_argument("-o", "--output", required=True, help="Output FASTA file.")
    parser.add_argument("-s", "--start", type=int, required=True, help="Start position (1-based).")
    parser.add_argument("-e", "--end", type=int, required=True, help="End position (1-based).")

    args = parser.parse_args()

    extract_region(args.input, args.output, args.start, args.end)

if __name__ == "__main__":
    main()
