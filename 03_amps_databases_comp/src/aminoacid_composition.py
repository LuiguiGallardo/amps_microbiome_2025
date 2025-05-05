#!/usr/bin/env python

# Imports
import argparse

# Arguments definition
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input", help="Input file with aminoacid sequences in fasta format")
argParser.add_argument("-o", "--output", help="Output file with aminoacid distribution")

args = argParser.parse_args()

# Function definition
def calculate_amino_acid_composition(input):
    # Create a dictionary to store amino acid counts
    amino_acid_counts = {}

    # Read the file
    with open(input, "r") as file:
        sequence = ""
        for line in file:
            # Skip lines starting with '>'
            if line.startswith(">"):
                continue
            sequence += line.strip()

        # Calculate total amino acid count
        total_aa_count = len(sequence)

        # Count amino acids
        for aa in sequence:
            if aa in amino_acid_counts:
                amino_acid_counts[aa] += 1
            else:
                amino_acid_counts[aa] = 1

        # Calculate composition as a percentage
        amino_acid_composition = {
            aa: (count / total_aa_count) * 100
            for aa, count in amino_acid_counts.items()
        }

    return amino_acid_composition


# Execution
composition = calculate_amino_acid_composition(args.input)

# Create output file
with open(args.output, "w") as output:
    output.write('aa\tfraction\n')
    for key, value in composition.items():
        output.write('%s\t%s\n' % (key, value))

output.close()