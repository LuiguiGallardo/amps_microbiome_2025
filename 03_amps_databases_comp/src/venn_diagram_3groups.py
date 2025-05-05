#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn3_unweighted

def calculate_sizes_and_percentages(macrel, axpep, amp_scanner):
    # Calculate the different set intersections
    A = macrel
    B = axpep
    C = amp_scanner

    # Intersection of all three sets
    A_int_B_int_C = len(A & B & C)

    # Pairwise intersections (excluding the triple intersection)
    A_int_B = len((A & B) - (A & B & C))
    B_int_C = len((B & C) - (A & B & C))
    A_int_C = len((A & C) - (A & B & C))

    # Elements only in each set (excluding any intersections)
    only_A = len(A - (B | C))
    only_B = len(B - (A | C))
    only_C = len(C - (A | B))

    # Total number of unique elements across all sets
    total_elements = len(A | B | C)

    # Calculate the percentage for each section
    perc_only_A = (only_A / total_elements) * 100
    perc_only_B = (only_B / total_elements) * 100
    perc_only_C = (only_C / total_elements) * 100
    perc_A_int_B = (A_int_B / total_elements) * 100
    perc_B_int_C = (B_int_C / total_elements) * 100
    perc_A_int_C = (A_int_C / total_elements) * 100
    perc_A_int_B_int_C = (A_int_B_int_C / total_elements) * 100

    # Return the sizes and percentages for the Venn diagram sections
    sizes = (only_A, only_B, A_int_B, only_C, A_int_C, B_int_C, A_int_B_int_C)
    percentages = (perc_only_A, perc_only_B, perc_A_int_B, perc_only_C, perc_A_int_C, perc_B_int_C, perc_A_int_B_int_C)

    return sizes, percentages

def main(file1, file2, file3, output_filename, title):
    # Read the input files as sets
    macrel = pd.read_csv(file1, header=None)
    macrel = set(macrel[0])

    axpep = pd.read_csv(file2, header=None)
    axpep = set(axpep[0])

    amp_scanner = pd.read_csv(file3, header=None)
    amp_scanner = set(amp_scanner[0])

    # Calculate sizes and percentages for each part of the Venn diagram
    sizes, percentages = calculate_sizes_and_percentages(macrel, axpep, amp_scanner)

    # Create the Venn diagram
    venn = venn3_unweighted(sizes, ('Macrel', 'AxPEP', "AMP Scanner v2"))

    # Add percentage labels to each section
    venn.get_label_by_id('100').set_text(f'{sizes[0]}\n({percentages[0]:.1f}%)')
    venn.get_label_by_id('010').set_text(f'{sizes[1]}\n({percentages[1]:.1f}%)')
    venn.get_label_by_id('110').set_text(f'{sizes[2]}\n({percentages[2]:.1f}%)')
    venn.get_label_by_id('001').set_text(f'{sizes[3]}\n({percentages[3]:.1f}%)')
    venn.get_label_by_id('101').set_text(f'{sizes[4]}\n({percentages[4]:.1f}%)')
    venn.get_label_by_id('011').set_text(f'{sizes[5]}\n({percentages[5]:.1f}%)')
    venn.get_label_by_id('111').set_text(f'{sizes[6]}\n({percentages[6]:.1f}%)')

    # Add the title to the Venn diagram
    plt.title(title, fontweight='bold')

    # Save the diagram as SVG and PNG
    plt.savefig(output_filename + ".svg")
    plt.savefig(output_filename + ".png")
    
    # Show the diagram
    plt.show()
    
    # Clear the figure to free up memory
    plt.clf()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate a Venn diagram (unweighted) from three sets of IDs.")
    
    # Add arguments for each input file
    parser.add_argument("-1", "--file1", required=True, help="Path to the first input file (Macrel).")
    parser.add_argument("-2", "--file2", required=True, help="Path to the second input file (AxPEP).")
    parser.add_argument("-3", "--file3", required=True, help="Path to the third input file (AMP Scanner).")
    
    # Add argument for output file name (without extension)
    parser.add_argument("-o", "--output", required=True, help="Base name for the output files (SVG and PNG).")
    
    # Add argument for the title of the figure
    parser.add_argument("-t", "--title", required=False, default="Venn Diagram", help="Title for the Venn diagram.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.file1, args.file2, args.file3, args.output, args.title)
