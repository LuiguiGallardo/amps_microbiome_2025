import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

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

# Rename the groups
df["dose_dataset"] = df["dose_dataset"].replace({"100 µg/mL (adr1)": "ADR1", "100 µg/mL (adr2)": "ADR2"})

# Combine Control groups from both datasets
df.loc[df["dose"] == "Control", "dose_dataset"] = "Control"

# Set Seaborn style
sns.set_theme(style="white")

# Create the plot
plt.figure(figsize=(3, 5))
ax = sns.barplot(
    data=df, x="time", y="od_value", hue="dose_dataset", errorbar="sd", palette="coolwarm",
    hue_order=["Control", "ADR1", "ADR2"]
)

# Annotate significance for each dataset separately
pairs = [((time, "Control"), (time, "ADR1")) for time in df["time"].unique()]
pairs += [((time, "Control"), (time, "ADR2")) for time in df["time"].unique()]
annotator = Annotator(ax, pairs, data=df, x="time", y="od_value", hue="dose_dataset",
                      hue_order=["Control", "ADR1", "ADR2"])
annotator.configure(test="t-test_ind", text_format="star", loc="inside", verbose=2)
annotator.apply_and_annotate()

# Customize plot
if args.title:
    plt.title(args.title, fontstyle="italic")
else:
    plt.title("Comparison of OD Values Between Control and 100 µg/mL by Dataset")

plt.xlabel("Time (hours)")
plt.ylabel("OD Value")
plt.legend(title="", fontsize="xx-small", loc="upper left")
plt.xticks(rotation=0)

# Save the plot
plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")