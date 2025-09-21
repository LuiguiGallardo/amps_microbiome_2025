#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot OD values for 100 µg/mL and Control groups from multiple input TSV files and save as PNG/SVG.")

# AMP files (required)
parser.add_argument("-i1", "--input1", required=True, help="Path to ADR1 input TSV file.")
parser.add_argument("-i2", "--input2", required=True, help="Path to ADR2 input TSV file.")

# Additional datasets (optional)
parser.add_argument("-i3", "--input3", help="Path to third input TSV file (e.g., BSA, Kanamicina).")
parser.add_argument("-i4", "--input4", help="Path to fourth input TSV file (e.g., Ampicilina).")
parser.add_argument("-i5", "--input5", help="Path to fifth input TSV file.")

# Dataset labels (optional, will use defaults if not provided)
parser.add_argument("--label1", default="ADR1", help="Label for first dataset (default: ADR1).")
parser.add_argument("--label2", default="ADR2", help="Label for second dataset (default: ADR2).")
parser.add_argument("--label3", help="Label for third dataset.")
parser.add_argument("--label4", help="Label for fourth dataset.")
parser.add_argument("--label5", help="Label for fifth dataset.")

# Output arguments
parser.add_argument("-o", "--output", required=True, help="Path to output PNG/SVG file.")
parser.add_argument("-t", "--title", help="Title for the plot.")

# Plot customization
parser.add_argument("--figsize", nargs=2, type=float, default=[3, 5], help="Figure size as width height (default: 3 5).")
parser.add_argument("--time-points", nargs='+', type=int, default=[5, 7, 20], help="Time points to include (default: 5 7 20).")
parser.add_argument("--doses", nargs='+', default=["Control", "100 µg/mL"], help="Doses to include (default: Control '100 µg/mL').")

args = parser.parse_args()

# Function to load and label datasets
def load_dataset(file_path, label, dataset_name):
    if file_path:
        df = pd.read_csv(file_path, sep="\t")
        df["dataset"] = dataset_name
        df["label"] = label
        return df
    return None

# Load datasets
datasets = []
ordered_labels = []  # Keep track of input order
dataset_info = [
    (args.input1, args.label1, "adr1"),
    (args.input2, args.label2, "adr2"),
    (args.input3, args.label3, "dataset3"),
    (args.input4, args.label4, "dataset4"),
    (args.input5, args.label5, "dataset5")
]

# Collect all provided datasets in order
for file_path, label, dataset_name in dataset_info:
    if file_path:
        if not label:  # Auto-generate label if not provided
            if "bsa" in file_path.lower():
                label = "BSA"
            elif "kanamicina" in file_path.lower():
                label = "Kanamicina"
            elif "ampicilina" in file_path.lower():
                label = "Ampicilina"
            else:
                label = dataset_name.upper()
        
        df = load_dataset(file_path, label, dataset_name)
        if df is not None:
            datasets.append(df)
            ordered_labels.append(label)  # Preserve input order

# Combine all datasets
if not datasets:
    raise ValueError("At least one input file must be provided")

df = pd.concat(datasets, ignore_index=True)

# Filter data for specific time points and doses
df = df[(df["time"].isin(args.time_points)) & (df["dose"].isin(args.doses))]

# Create a new column combining 'dose' and 'label'
df["dose_dataset"] = df["dose"] + " (" + df["label"] + ")"

# Create mapping for renaming groups
rename_mapping = {}
control_mapping = {}

# Get unique labels from the datasets
unique_labels = df["label"].unique()

for label in unique_labels:
    treatment_key = f"100 µg/mL ({label})"
    control_key = f"Control ({label})"
    
    rename_mapping[treatment_key] = label
    rename_mapping[control_key] = f"Control {label}"
    control_mapping[f"Control {label}"] = "Control"

# Apply renaming
df["dose_dataset"] = df["dose_dataset"].replace(rename_mapping)

# Create a copy for visualization with merged controls
df_plot = df.copy()
df_plot["dose_dataset_plot"] = df_plot["dose_dataset"].replace(control_mapping)

# Set Seaborn style
sns.set_theme(style="white")

# Define color palette - extend as needed
base_colors = ["#9bb4f0", "#9bf0a6", "#ea9648", "#f24949", "#8e44ad", "#e74c3c", "#f39c12", "#27ae60"]

# Create custom palette using input order
custom_palette = {"Control": "#d4d4d4"}  # gray for control
for i, label in enumerate(ordered_labels):
    if i < len(base_colors):
        custom_palette[label] = base_colors[i]
    else:
        # Generate additional colors if needed
        custom_palette[label] = plt.cm.Set3(i % 12)

# Create plot order - Control first, then in input order
plot_order = ["Control"] + ordered_labels

# Create the plot using merged controls for visualization
plt.figure(figsize=args.figsize)
ax = sns.barplot(
    data=df_plot, x="time", y="od_value", hue="dose_dataset_plot", errorbar="se", 
    palette=custom_palette, hue_order=plot_order, dodge=True, width=0.8
)

# Add individual data points as dots
sns.stripplot(
    data=df_plot, x="time", y="od_value", hue="dose_dataset_plot", 
    dodge=True, size=3, alpha=0.7, palette='dark:black',
    hue_order=plot_order, ax=ax
)

# Statistical annotation functions
def get_pvalue_text(pval):
    if pval < 0.001:
        return "***"
    elif pval < 0.01:
        return "**"
    elif pval < 0.05:
        return "*"
    else:
        return "ns"

# Perform statistical tests for each time point
for i, time in enumerate(sorted(args.time_points)):
    # Get data for this time point
    time_data = df[df['time'] == time]
    
    if len(time_data) == 0:
        continue
    
    # Calculate base offset for annotations
    merged_control_data = df_plot[(df_plot['time'] == time) & (df_plot['dose_dataset_plot'] == 'Control')]
    if len(merged_control_data) > 0:
        merged_control_max = merged_control_data['od_value'].max()
        base_offset = 0.0075
    else:
        base_offset = 0.1
    
    # Perform comparisons for each treatment vs its corresponding control
    comparison_height = 1
    for label in ordered_labels:
        control_label = f"Control {label}"
        
        # Get control and treatment data
        control_data = time_data[time_data['dose_dataset'] == control_label]['od_value']
        treatment_data = time_data[time_data['dose_dataset'] == label]['od_value']
        
        if len(control_data) > 0 and len(treatment_data) > 0:
            # Perform t-test
            _, pval = stats.ttest_ind(control_data, treatment_data)
            
            # Position annotation
            treatment_idx = plot_order.index(label)
            control_idx = plot_order.index("Control")
            
            # Calculate positions for the bars
            n_groups = len(plot_order)
            bar_width = 0.8 / n_groups
            
            x_control = i + (control_idx - n_groups/2 + 0.5) * bar_width
            x_treatment = i + (treatment_idx - n_groups/2 + 0.5) * bar_width
            
            x_center = (x_control + x_treatment) / 2
            
            # Set annotation height
            y_line = merged_control_max + base_offset * (3 + comparison_height * 4)
            y_text = y_line + base_offset * 0.5
            
            # Add annotation
            ax.annotate(get_pvalue_text(pval), xy=(x_center, y_text), 
                       ha='center', va='bottom', fontsize='x-small')
            ax.plot([x_control, x_treatment], [y_line, y_line], 'k-', linewidth=0.5)
            
            comparison_height += 1

# Customize plot
if args.title:
    plt.title(args.title, fontstyle="italic")
else:
    plt.title("Comparison of OD Values Between Control and Treatment Groups")

plt.xlabel("Time (hours)")
plt.ylabel("OD Value")

# Handle legend - remove duplicate entries from stripplot
handles, labels = ax.get_legend_handles_labels()
n_groups = len(plot_order)
plt.legend(handles[:n_groups], labels[:n_groups], title="", fontsize="xx-small", loc="upper left")
plt.xticks(rotation=0)

# Save the plot
plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")