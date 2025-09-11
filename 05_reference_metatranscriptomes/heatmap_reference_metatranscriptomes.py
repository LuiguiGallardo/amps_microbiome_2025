#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Create a heatmap from a dataset")
parser.add_argument("-i", "--input", required=True, help="Path to the input TSV file")
parser.add_argument("-o", "--output", required=True, help="Path to save the output heatmap image (e.g., heatmap.png)")
parser.add_argument("-t", "--tsv_output", required=True, help="Path to save the updated TSV file (e.g., updated_data.tsv)")
parser.add_argument("-y", "--ylabel", default="", help="Label for the y-axis")
parser.add_argument("-g", "--group_file", required=False, help="TSV file with 'sample' and 'group' columns to order samples by group")
args = parser.parse_args()


# Load the dataset
data = pd.read_csv(args.input, sep="\t", index_col=0)

# If group file is provided, reorder columns
if args.group_file:
    group_df = pd.read_csv(args.group_file, sep="\t")
    # Ensure columns exist
    if "sample" in group_df.columns and "group" in group_df.columns:
        # Controls first, then NASH
        control_samples = group_df[group_df["group"].str.lower() == "control"]["sample"].tolist()
        nash_samples = group_df[group_df["group"].str.lower() == "nash"]["sample"].tolist()
        ordered_samples = control_samples + nash_samples
        # Only keep samples present in data
        ordered_samples = [s for s in ordered_samples if s in data.columns]
        # Reorder columns
        data = data[ordered_samples + [c for c in data.columns if c not in ordered_samples]]
    else:
        print("Group file must have 'sample' and 'group' columns.")

# Convert data to presence/absence (1 for non-zero, 0 for zero)
data = (data != 0).astype(int)

# Save the updated data to a new TSV file
data.to_csv(args.tsv_output, sep="\t")


used_split = False

if args.group_file:
    group_df = pd.read_csv(args.group_file, sep="\t")
    if "sample" in group_df.columns and "group" in group_df.columns:
        # Only consider Control and NASH (case-insensitive)
        group_df = group_df[group_df["group"].str.lower().isin(["control", "nash"])].copy()
        sample_to_group = dict(zip(group_df["sample"], group_df["group"].str.lower()))
        control_cols = [c for c in data.columns if sample_to_group.get(c) == "control"]
        nash_cols = [c for c in data.columns if sample_to_group.get(c) == "nash"]

        # Create two subplots side by side sharing the y-axis
        fig, axes = plt.subplots(1, 2, figsize=(12, 8), sharey=True)

        # Control heatmap
        if control_cols:
            sns.heatmap(
                data[control_cols], cmap="Blues", annot=False, linewidths=0.5,
                cbar=False, vmin=0, vmax=1, ax=axes[0], xticklabels=False,
            )
            axes[0].set_title("Control")
            axes[0].tick_params(axis='x', rotation=90)
        else:
            axes[0].axis('off')
            axes[0].set_title("Control (no samples)")

        # NASH heatmap
        if nash_cols:
            sns.heatmap(
                data[nash_cols], cmap="Blues", annot=False, linewidths=0.5,
                cbar=False, vmin=0, vmax=1, ax=axes[1], xticklabels=False,
            )
            axes[1].set_title("NASH")
            axes[1].tick_params(axis='x', rotation=90)
        else:
            axes[1].axis('off')
            axes[1].set_title("NASH (no samples)")

        # Labels and layout for split view
        axes[0].set_ylabel(args.ylabel)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        used_split = True

if not used_split:
    # Single heatmap fallback (no group file or invalid columns)
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        data,
        cmap="Blues", 
        annot=False,  # Do not display values inside each block
        linewidths=0.5,
        cbar=False,
        vmin=0, 
        vmax=1  # Set the color scale from 0 to 1
    )
    ax.tick_params(axis='x', rotation=90)

## Removed vertical line splitting control and NASH groups

# Customize the color bar to show only 0 and 1
# colorbar = ax.collections[0].colorbar
# colorbar.set_ticks([0, 1])  # Show only 0 and 1
# colorbar.set_ticklabels(['0', '1'])  # Label the ticks as '0' and '1'
# colorbar.set_label("Presence/Absence", rotation=90, labelpad=15)

# Apply tight layout to ensure everything fits
plt.tight_layout()

# Save the plot to the specified output files
output_png = args.output.replace(".svg", ".png")
output_svg = args.output.replace(".png", ".svg")
plt.savefig(output_png, format="png", dpi=300)
plt.savefig(output_svg, format="svg", dpi=300)
print(f"Heatmap saved to {output_png} and {output_svg}")
print(f"Updated TSV saved to {args.tsv_output}")
