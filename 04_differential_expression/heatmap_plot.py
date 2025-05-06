#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Create a heatmap from a dataset")
parser.add_argument("-i", "--input", required=True, help="Path to the input TSV file")
parser.add_argument("-o", "--output", required=True, help="Path to save the output heatmap image (e.g., heatmap.png)")
parser.add_argument("-t", "--tsv_output", required=True, help="Path to save the updated TSV file (e.g., updated_data.tsv)")
args = parser.parse_args()

# Load the dataset
data = pd.read_csv(args.input, sep="\t", index_col=0)

# Convert data to presence/absence (1 for non-zero, 0 for zero)
data = (data != 0).astype(int)

# Save the updated data to a new TSV file
data.to_csv(args.tsv_output, sep="\t")

# Set up the figure size
plt.figure(figsize=(12, 8))

# Create the heatmap with Seaborn using 'Blues' palette
ax = sns.heatmap(
    data, 
    cmap="Blues", 
    annot=False,  # Do not display values inside each block
    linewidths=0.5, 
    cbar=False,
    xticklabels=False,
    vmin=0, 
    vmax=1  # Set the color scale from 0 to 1
)

# Customize the color bar to show only 0 and 1
# colorbar = ax.collections[0].colorbar
# colorbar.set_ticks([0, 1])  # Show only 0 and 1
# colorbar.set_ticklabels(['0', '1'])  # Label the ticks as '0' and '1'
# colorbar.set_label("Presence/Absence", rotation=90, labelpad=15)

# Customize labels and title
plt.xlabel("Adult metatranscriptome samples")
plt.ylabel("")

# Apply tight layout to ensure everything fits
plt.tight_layout()

# Save the plot to the specified output files
output_png = args.output.replace(".svg", ".png")
output_svg = args.output.replace(".png", ".svg")
plt.savefig(output_png, format="png", dpi=300)
plt.savefig(output_svg, format="svg", dpi=300)
print(f"Heatmap saved to {output_png} and {output_svg}")
print(f"Updated TSV saved to {args.tsv_output}")
