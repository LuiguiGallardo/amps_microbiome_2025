#!/usr/bin/env python

import argparse
from Bio import SeqIO

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Filter FASTA sequences shorter than a specified minimum length.")
parser.add_argument("-i", "--input", required=True, help="Path to the input FASTA file.")
parser.add_argument("-o", "--output", required=True, help="Path to the output FASTA file.")
parser.add_argument("-m", "--min-length", type=int, required=True, help="Minimum sequence length to keep.")
args = parser.parse_args()

# Filter sequences
with open(args.input, "r") as infile, open(args.output, "w") as outfile:
    for record in SeqIO.parse(infile, "fasta"):
        if len(record.seq) >= args.min_length:
            SeqIO.write(record, outfile, "fasta")

print(f"Filtered sequences saved to {args.output}")

