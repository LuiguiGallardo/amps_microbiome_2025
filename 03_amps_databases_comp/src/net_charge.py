#!/usr/bin/env python

# Imports
import argparse
from Bio.SeqUtils import ProtParam
from Bio import SeqIO

# Arguments definition
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input", help="Input file with aminoacid sequences in fasta format")
argParser.add_argument("-o", "--output", help="Output file with the net charge")
argParser.add_argument("-p", "--pH", help="pH value", default=7)

args = argParser.parse_args()

# Function definition
def calculate_net_charge_for_peptides_in_file(file_path, pH=7.0):
    """
    Calculate the net charge of peptides in a file at a given pH.

    Args:
        file_path (str): The path to the file containing multiple peptide sequences (in FASTA format).
        pH (float): The pH value at which to calculate the charge (default is 7.0).

    Returns:
        dict: A dictionary mapping sequence headers to their net charges at the given pH.
    """
    peptide_net_charges = {}

    # Read the FASTA file and calculate charges for each sequence
    for record in SeqIO.parse(file_path, "fasta"):
        sequence = str(record.seq)
        header = record.description
        net_charge = calculate_peptide_net_charge(sequence, pH)
        peptide_net_charges[header] = net_charge

    return peptide_net_charges

def calculate_peptide_net_charge(peptide_sequence, pH=7.0):
    """
    Calculate the net charge of a peptide at a given pH.

    Args:
        peptide_sequence (str): The amino acid sequence of the peptide.
        pH (float): The pH value at which to calculate the charge (default is 7.0).

    Returns:
        float: The net charge of the peptide at the given pH.
    """
    # Create a ProtParam object
    param = ProtParam.ProteinAnalysis(peptide_sequence)

    # Calculate the net charge at the specified pH
    amino_acid_charges = param.charge_at_pH(pH)

    return amino_acid_charges

# Execution
peptide_net_charges = calculate_net_charge_for_peptides_in_file(args.input, args.pH)

# Print the results
with open(args.output, "w") as output:
    output.write(f'sequence\tNet charge at pH {args.pH}\n')
    for header, net_charge in peptide_net_charges.items():
        output.write('%s\t%s\n' % (header, net_charge))

output.close()