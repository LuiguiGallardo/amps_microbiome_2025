#!/usr/bin/env python3

import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline

def run_msa(input_fasta, output_aln, clustal_exe="clustalo"):
    """
    Perform multiple sequence alignment (MSA) using Clustal Omega.

    :param input_fasta: Path to input FASTA file with amino acid sequences.
    :param output_aln: Path to output alignment file (.aln format).
    :param clustal_exe: Path to the Clustal Omega executable (default assumes it's in PATH).
    """
    if not os.path.exists(input_fasta):
        print(f"Error: Input file '{input_fasta}' not found.")
        return

    # Ensure the output file has the .aln extension
    if not output_aln.endswith(".aln"):
        output_aln += ".aln"

    # Run Clustal Omega
    clustal_cmd = ClustalOmegaCommandline(infile=input_fasta, outfile=output_aln, verbose=True, auto=True, outfmt="clustal")
    stdout, stderr = clustal_cmd()

    if stderr:
        print(f"Clustal Omega Error:\n{stderr}")
    else:
        print(f"Alignment completed. Output saved to: {output_aln}")
    
    # Plot the MSA after alignment
    plot_msa(output_aln, format="clustal", title="Aligned Sequences")


def plot_msa(input_file, format="clustal", title=""):
    """
    Plots the Multiple Sequence Alignment (MSA) with hydropathy-based coloring.

    :param input_file: Path to the alignment file.
    :param format: Format of the alignment file (default: clustal).
    :param title: Title for the plot.
    """
    # Read the alignment file
    alignment = AlignIO.read(input_file, format)

    # Hydropathy dictionary
    hydropathy = {
        'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
        'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
        'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
        'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5,
        '-': 0  # Neutral value for gaps
    }

    cmap = plt.get_cmap('RdYlBu_r')  # Red for hydrophobic, blue for hydrophilic
    norm = mcolors.Normalize(vmin=-5, vmax=5)  # Normalize to the range of hydropathy values
    
    # Create a sequence alignment matrix
    alignment_matrix = [list(record.seq) for record in alignment]

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(15, len(alignment) / 2 + 0.5))

    # Plot the alignment matrix
    for i, row in enumerate(alignment_matrix):
        for j, char in enumerate(row):
            ax.text(j, i, char, ha='center', va='center', fontsize=8, color='black')
            color = 'white' if char == '-' else cmap(norm(hydropathy.get(char, 0)))  # Default to 0 if char not in dict
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True, edgecolor='black', lw=0.5, facecolor=color))

    # Set plot limits and labels
    ax.set_xlim(-0.5, len(alignment_matrix[0]) - 0.5)
    ax.set_ylim(-0.5, len(alignment_matrix) - 0.5)

    # X-axis ticks
    x_min, x_max, x_step = 0, len(alignment_matrix[0]), 5
    ax.set_xticks(range(x_min, x_max + 1, x_step))
    ax.set_xticklabels(range(x_min + 1, x_max + 2, x_step))

    # Y-axis labels
    ax.set_yticks(range(len(alignment_matrix)))
    ax.set_yticklabels([record.id for record in alignment], fontsize=10)

    ax.invert_yaxis()

    # Create a colorbar
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', pad=0.01)
    cbar.set_label('Hydropathy')

    plt.xlabel('Amino acid position')
    plt.ylabel('')
    plt.title('Multiple Sequence Alignment ' + title)

    # Save the plot
    fig.tight_layout()
    plt.savefig(input_file + '.svg', format='svg')
    plt.savefig(input_file + '.png', format='png')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform MSA using Clustal Omega and visualize alignment.")
    
    parser.add_argument("-i", "--input", required=True, help="Path to the input FASTA file containing amino acid sequences.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output alignment file (.aln format).")

    args = parser.parse_args()

    run_msa(args.input, args.output)
