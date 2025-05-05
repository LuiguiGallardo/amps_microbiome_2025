#!/usr/bin/env python 

# Imports
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import SeqIO
from itertools import combinations
from scipy.stats import mannwhitneyu

# Define colors for each group
colors = {
    'Our AMPs': 'darkcyan',
    'APD3': 'darkorchid',
    'dbAMP': 'red',
    'DRAMP': 'darkorange'
}

def parse_fasta_lengths(file_path, group_name):
    lengths = [len(record.seq) for record in SeqIO.parse(file_path, "fasta")]
    return pd.DataFrame({"Length": lengths, "Group": group_name})

def calculate_pvalues(data, x, y, pairs):
    pvalues = []
    for pair in pairs:
        group1 = data[data[x] == pair[0]][y]
        group2 = data[data[x] == pair[1]][y]
        stat, pvalue = mannwhitneyu(group1, group2)
        pvalues.append((pair[0], pair[1], pvalue))
    return pvalues

def add_pvalue_annotations(ax, data, x, y, pairs):
    for pair in pairs:
        group1 = data[data[x] == pair[0]][y]
        group2 = data[data[x] == pair[1]][y]
        stat, pvalue = mannwhitneyu(group1, group2)
        
        if pvalue > 0.05:
            annotation = 'ns'
        elif pvalue > 0.01:
            annotation = '*'
        elif pvalue > 0.001:
            annotation = '**'
        elif pvalue > 0.0001:
            annotation = '***'
        else:
            annotation = '****'
        
        # Get the y position for the annotation
        y_max = max(data[y])
        y_pos = y_max + (y_max * 0.15) * (pairs.index(pair) + 1)
        
        # Add the annotation
        ax.annotate(annotation, xy=((data[x].unique().tolist().index(pair[0]) + data[x].unique().tolist().index(pair[1])) / 2, y_pos), 
                    ha='center', va='bottom', fontsize=12, color='black')
        
        # Add a line connecting the groups
        ax.plot([data[x].unique().tolist().index(pair[0]), data[x].unique().tolist().index(pair[1])], [y_pos, y_pos], lw=1.5, color='black')

    # Adjust the y-axis limit to give more space for annotations
    ax.set_ylim(top=y_pos + (y_max * 0.1))

def main():
    parser = argparse.ArgumentParser(description="Plot length distribution of sequences from FASTA files.")
    parser.add_argument("-1", "--file1", required=True, help="Path to the first FASTA file.")
    parser.add_argument("-1n", "--name1", required=True, help="Group name for the first FASTA file.")
    parser.add_argument("-2", "--file2", required=True, help="Path to the second FASTA file.")
    parser.add_argument("-2n", "--name2", required=True, help="Group name for the second FASTA file.")
    parser.add_argument("-3", "--file3", required=True, help="Path to the third FASTA file.")
    parser.add_argument("-3n", "--name3", required=True, help="Group name for the third FASTA file.")
    parser.add_argument("-4", "--file4", required=True, help="Path to the fourth FASTA file.")
    parser.add_argument("-4n", "--name4", required=True, help="Group name for the fourth FASTA file.")
    parser.add_argument("-o", "--output", required=True, help="Output file for the plot (e.g., 'output.png').")
    args = parser.parse_args()

    # Prepare list of files and group names
    fasta_files = [
        (args.file1, args.name1),
        (args.file2, args.name2),
        (args.file3, args.name3),
        (args.file4, args.name4)
    ]

    # Parse all files and combine into a single DataFrame
    all_data = pd.concat([
        parse_fasta_lengths(file_path, group_name)
        for file_path, group_name in fasta_files
    ], ignore_index=True)

    # Create the histogram plot
    plt.figure(figsize=(18, 6))
    gs = plt.GridSpec(1, 2, width_ratios=[3, 1])

    sns.set_style("white")
    sns.set_context("notebook", font_scale=1.2, rc={"xtick.labelsize": 12, "ytick.labelsize": 12, "ytick.labelweight": 'bold'})

    ax0 = plt.subplot(gs[0])
    sns.histplot(data=all_data, x="Length", hue="Group", palette=colors, bins=100, ax=ax0, alpha=0.25)
    ax0.set_title("Length Distribution of AMPs", fontweight="bold")
    ax0.set_xlabel("Sequence Length", fontweight="bold")
    ax0.set_ylabel("AMPs", fontweight="bold")

    # Add lines for the average length of each group
    means = all_data.groupby("Group")["Length"].mean()
    for i, (group, mean) in enumerate(means.items()):
        ax0.axvline(mean, color=colors[group], linestyle='dashed', linewidth=2)
        y_pos = ax0.get_ylim()[1] * (0.9 - i * 0.05)  # Stagger the y position to avoid overlap
        ax0.text(mean + 4, y_pos, f'{mean:.0f}', color=colors[group], ha='center', va='bottom', fontsize=12)

    # Create the boxplot for length distribution
    ax1 = plt.subplot(gs[1])
    sns.boxplot(data=all_data, x="Group", y="Length", hue="Group", palette=colors, legend=False, ax=ax1)
    ax1.set_title("Length Distribution by Group", fontweight="bold")
    ax1.set_xlabel("")
    ax1.set_ylabel("Sequence Length", fontweight="bold")

    # Perform pairwise statistical tests and add annotations
    pairs = list(combinations(all_data['Group'].unique(), 2))
    add_pvalue_annotations(ax1, all_data, 'Group', 'Length', pairs)

    # Save the plot as PNG and SVG
    output_base = args.output.rsplit('.', 1)[0]
    plt.tight_layout()
    plt.savefig(f"{output_base}.png", format="png")
    plt.savefig(f"{output_base}.svg", format="svg")
    plt.show()

if __name__ == "__main__":
    main()
