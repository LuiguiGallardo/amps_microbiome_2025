import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator
from scipy import stats
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot OD values for 100 µg/mL and Control groups from two input TSV files and save as PNG.")
parser.add_argument("-i1", "--input1", required=True, help="Path to first input TSV file.")
parser.add_argument("-i2", "--input2", required=True, help="Path to second input TSV file.")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file.")
parser.add_argument("-t", "--title", help="Title for the plot.")
args = parser.parse_args()

# Load the data from both input files and add a 'dataset' column
df1 = pd.read_csv(args.input1, sep="\t")
df1["dataset"] = "adr1"

df2 = pd.read_csv(args.input2, sep="\t")
df2["dataset"] = "adr2"

# Combine the datasets
df = pd.concat([df1, df2], ignore_index=True)

# Filter data for specific time points (5, 7, and 20 hours) and doses (Control and 100 µg/mL)
df = df[(df["time"].isin([5, 7, 20])) & (df["dose"].isin(["Control", "100 µg/mL"]))]

# Create a new column combining 'dose' and 'dataset'
df["dose_dataset"] = df["dose"] + " (" + df["dataset"] + ")"

# Rename the groups - keep controls separate for statistics but merge for visualization
df["dose_dataset"] = df["dose_dataset"].replace({
    "100 µg/mL (adr1)": "ADR1", 
    "100 µg/mL (adr2)": "ADR2",
    "Control (adr1)": "Control ADR1",
    "Control (adr2)": "Control ADR2"
})

# Create a copy for visualization with merged controls
df_plot = df.copy()
df_plot["dose_dataset_plot"] = df_plot["dose_dataset"].replace({
    "Control ADR1": "Control",
    "Control ADR2": "Control"
})

# Set Seaborn style
sns.set_theme(style="white")

# Colors
custom_palette = {
    "ADR1": "#9bb4f0",        # blue
    "ADR2": "#9bf0a6",        # green
    "Control": "#d4d4d4"      # gray
}

# Create the plot using merged controls for visualization
plt.figure(figsize=(3, 5))
ax = sns.barplot(
    data=df_plot, x="time", y="od_value", hue="dose_dataset_plot", errorbar="se", palette=custom_palette,
    hue_order=["Control", "ADR1", "ADR2"]
)

# Add individual data points as dots
sns.stripplot(
    data=df_plot, x="time", y="od_value", hue="dose_dataset_plot", 
    dodge=True, size=3, color="black", alpha=0.7,
    hue_order=["Control", "ADR1", "ADR2"], ax=ax
)

# Custom statistical annotation - compare separate controls to treatments but display on merged plot

# Calculate p-values manually for each comparison
def get_pvalue_text(pval):
    if pval < 0.001:
        return "***"
    elif pval < 0.01:
        return "**"
    elif pval < 0.05:
        return "*"
    else:
        return "ns"

# Add statistical annotations manually
base_offset = df_plot['od_value'].max() * 0.015

for i, time in enumerate(sorted(df['time'].unique())):
    # Get merged control data for this time point for consistent positioning
    merged_control_data = df[(df['time'] == time) & (df['dose_dataset'].isin(['Control ADR1', 'Control ADR2']))]['od_value']
    merged_control_max = merged_control_data.max() if len(merged_control_data) > 0 else 0
    
    # Control ADR1 vs ADR1
    control_adr1_data = df[(df['time'] == time) & (df['dose_dataset'] == 'Control ADR1')]['od_value']
    adr1_data = df[(df['time'] == time) & (df['dose_dataset'] == 'ADR1')]['od_value']
    if len(control_adr1_data) > 0 and len(adr1_data) > 0:
        _, pval1 = stats.ttest_ind(control_adr1_data, adr1_data)
        # Calculate dynamic height based on the data being compared
        max_height_1 = max(control_adr1_data.max(), adr1_data.max())
        y_line_1 = max_height_1 + base_offset
        y_text_1 = y_line_1 + base_offset
        
        # Position annotation above Control bar for this comparison
        x_start = i - 0.27  # Control bar position
        x_end = i           # ADR1 bar position  
        x_center = (x_start + x_end) / 2  # Center of the line
        # Position text and line based on merged control max
        y_line_1 = merged_control_max + base_offset # Increased by 20%
        y_text_1 = y_line_1 + base_offset * 0.2   # Closer to the line
        
        ax.annotate(get_pvalue_text(pval1), xy=(x_center, y_text_1), 
                   ha='center', va='bottom', fontsize='x-small')
        ax.plot([x_start, x_end], [y_line_1, y_line_1], 'k-', linewidth=0.5)
    
    # Control ADR2 vs ADR2  
    control_adr2_data = df[(df['time'] == time) & (df['dose_dataset'] == 'Control ADR2')]['od_value']
    adr2_data = df[(df['time'] == time) & (df['dose_dataset'] == 'ADR2')]['od_value']
    if len(control_adr2_data) > 0 and len(adr2_data) > 0:
        _, pval2 = stats.ttest_ind(control_adr2_data, adr2_data)
        # Calculate dynamic height based on the data being compared
        max_height_2 = max(control_adr2_data.max(), adr2_data.max())
        y_line_2 = max_height_2 + base_offset
        y_text_2 = y_line_2 + base_offset
        
        # Position annotation above Control bar for this comparison
        x_start = i - 0.27  # Control bar position
        x_end = i + 0.27    # ADR2 bar position
        x_center = (x_start + x_end) / 2  # Center of the line
        # Position text and line based on merged control max, offset higher than first comparison
        y_line_2 = merged_control_max + base_offset * 4  # Increased by 20%
        y_text_2 = y_line_2 + base_offset * 0.2   # Closer to the line
        
        # If first comparison exists, make sure second is higher
        if len(control_adr1_data) > 0 and len(adr1_data) > 0:
            first_comparison_height = merged_control_max + base_offset * 3.6  # Increased by 20%
            y_line_2 = max(y_line_2, first_comparison_height)
            y_text_2 = y_line_2 + base_offset * 0.2
        
        ax.annotate(get_pvalue_text(pval2), xy=(x_center, y_text_2), 
                   ha='center', va='bottom', fontsize='x-small')
        ax.plot([x_start, x_end], [y_line_2, y_line_2], 'k-', linewidth=0.5)

# Customize plot
if args.title:
    plt.title(args.title, fontstyle="italic")
else:
    plt.title("Comparison of OD Values Between Control and 100 µg/mL by Dataset")

plt.xlabel("Time (hours)")
plt.ylabel("OD Value")

# Handle legend - remove duplicate entries from stripplot
handles, labels = ax.get_legend_handles_labels()
# Keep only the first 3 handles/labels (from barplot)
plt.legend(handles[:3], labels[:3], title="", fontsize="xx-small", loc="upper left")
plt.xticks(rotation=0)

# Save the plot
plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")