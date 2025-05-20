import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from statannotations.Annotator import Annotator

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot growth curves from input TSV file and save as PNG.")
parser.add_argument("-i", "--input", required=True, help="Path to input TSV file.")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file.")
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input, sep="\t")

# Convert 'dose' column to categorical with a meaningful order
df["dose"] = pd.Categorical(df["dose"], categories=[
    "Control", "3.13 µg/mL", "6.25 µg/mL", "12.5 µg/mL",
    "25 µg/mL", "50 µg/mL", "100 µg/mL"
], ordered=True)

# Group by dose and time, calculating the mean and standard deviation
df_grouped = df.groupby(["dose", "time"]).agg({"od_value": ["mean", "std"]}).reset_index()
df_grouped.columns = ["dose", "time", "mean_od", "std_od"]

# Set Seaborn style
sns.set(style="whitegrid")

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Line plot
sns.lineplot(data=df_grouped, x="time", y="mean_od", hue="dose", marker="o", linewidth=2, palette="coolwarm", ax=ax1)
ax1.set_xlabel("Time")
ax1.set_ylabel("OD Value")
ax1.set_title("Growth Curve")
ax1.legend(title="Dose", bbox_to_anchor=(1.05, 1), loc="upper left")

# Boxplot for time 20
df_time_20 = df[df["time"] == 20]
sns.boxplot(data=df_time_20, x="dose", y="od_value", palette="coolwarm", ax=ax2)
ax2.set_xlabel("")
ax2.set_ylabel("OD Value")
ax2.set_title("OD Value at Time 20")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=33)

# Define comparisons: Control vs each treatment group
control_group = "Control"
treatment_groups = [dose for dose in df["dose"].unique() if dose != control_group]
box_pairs = [(control_group, group) for group in treatment_groups]

# Perform statistical annotation
annotator = Annotator(ax2, box_pairs, data=df_time_20, x="dose", y="od_value")
annotator.configure(test="t-test_ind", text_format="star", loc="inside", verbose=2)
annotator.apply_and_annotate()

plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")
