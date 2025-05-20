import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot OD values from input TSV file and save as PNG.")
parser.add_argument("-i", "--input", required=True, help="Path to input TSV file.")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file.")
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input, sep="\t")

# Filter data for specific time points (5, 7, and 20 hours)
df = df[df["time"].isin([5, 7, 20])]

# Convert 'dose' column to categorical with a meaningful order
df["dose"] = pd.Categorical(df["dose"], categories=[
    "Control", "3.13 µg/mL", "6.25 µg/mL", "12.5 µg/mL",
    "25 µg/mL", "50 µg/mL", "100 µg/mL"
], ordered=True)

# Set Seaborn style
sns.set(style="whitegrid")

# Create the plot
g = sns.catplot(
    data=df, x="dose", y="od_value", col="time", kind="bar",
    palette="coolwarm", height=6, aspect=0.3, ci="sd"
)

# Add pairwise comparisons for each time point
for ax, time in zip(g.axes.flat, df["time"].unique()):
    subset = df[df["time"] == time]
    pairs = [("Control", "3.13 µg/mL"), ("Control", "6.25 µg/mL"), 
             ("Control", "12.5 µg/mL"), ("Control", "25 µg/mL"),
             ("Control", "50 µg/mL"), ("Control", "100 µg/mL")]
    annotator = Annotator(ax, pairs, data=subset, x="dose", y="od_value")
    annotator.configure(test="t-test_ind", text_format="star", loc="inside", verbose=2)
    annotator.apply_and_annotate()

g.set_axis_labels("", "OD Value")
g.set_titles("{col_name} hours")
g.set_xticklabels(rotation=90)

plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")
