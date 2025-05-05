#!/usr/bin/env python

# Imports
import argparse
from Bio.SeqUtils import ProtParam
from Bio import SeqIO

# Arguments definition
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input", help="Input file with amino acids sequences in fasta format")
argParser.add_argument("-o", "--output", help="Output file with GRAVY index")

args = argParser.parse_args()

# Function definition
def calculate_gravy_index(sequence):
    """
    Calculate the GRAVY index for a given amino acid sequence.

    Args:
        sequence (str): The amino acid sequence of the protein/peptide.

    Returns:
        float: The GRAVY index of the sequence.
    """
    # Replace or remove 'X' (ambiguous residues) from the sequence
    sequence = sequence.replace('X', '')  # Remove 'X' completely
    sequence = sequence.replace('U', '')  # Remove 'U' completely
    sequence = sequence.replace('Z', '')  # Remove 'Z' completely

    # Create a ProtParam object
    param = ProtParam.ProteinAnalysis(sequence)

    # Calculate the GRAVY index
    gravy_index = param.gravy()

    return gravy_index

def calculate_gravy_for_file(file_path):
    """
    Calculate the GRAVY index for all sequences in a given file.

    Args:
        file_path (str): The path to the input FASTA file.

    Returns:
        dict: A dictionary with sequence headers as keys and GRAVY indices as values.
    """
    # Create a dictionary to store GRAVY indices
    gravy_indices = {}

    # Read the file
    with open(file_path, 'r') as file:
        sequence = ""
        current_header = None

        for line in file:
            if line.startswith('>'):
                # Process the previous sequence if there was one
                if current_header is not None:
                    gravy_indices[current_header] = calculate_gravy_index(sequence)

                # Start a new sequence
                current_header = line.strip()
                sequence = ""
            else:
                sequence += line.strip()

        # Process the last sequence in the file
        if current_header is not None:
            gravy_indices[current_header] = calculate_gravy_index(sequence)

    return gravy_indices

# Execution
gravy_results = calculate_gravy_for_file(args.input)

# Create output file
with open(args.output, "w") as output:
    output.write('sequence\tGRAVY index\n')
    for key, value in gravy_results.items():
        output.write('%s\t%s\n' % (key, value))

output.close()
