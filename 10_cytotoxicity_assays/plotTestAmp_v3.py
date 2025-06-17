import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot % values for each group and sample from input TSV file and save as PNG.")
parser.add_argument("-i", "--input", required=True, help="Path to input TSV file.")
parser.add_argument("-o", "--output", required=True, help="Path to output PNG file.")
parser.add_argument("-t", "--title", help="Title for the plot.")
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input, sep="\t")

# Convert 'value' from percentage string to float
df["value"] = df["value"].str.rstrip("%").astype(float)

# Set Seaborn style
sns.set_theme(style="white")

# Colors
custom_palette = {
    "ADR1": "#9bb4f0",      # blue
    "ADR2": "#9bf0a6",      # green
    "Control": "#dddcdc",   # gray
    "PMA-IONO": "#e5a089"   # red
}

plt.figure(figsize=(3, 5))
ax = sns.barplot(
    data=df, x="group", y="value", hue="sample", errorbar=None,
    palette=custom_palette,
    hue_order=["Control", "ADR1", "ADR2", "PMA-IONO"]
)

# Annotate significance: compare Control vs each treatment for each group
pairs = []
for group in df["group"].unique():
    for treatment in ["ADR1", "ADR2", "PMA-IONO"]:
        pairs.append(((group, "Control"), (group, treatment)))

annotator = Annotator(
    ax, pairs, data=df, x="group", y="value", hue="sample",
    hue_order=["Control", "ADR1", "ADR2", "PMA-IONO"]
)
annotator.configure(test="t-test_ind", text_format="star", loc="inside", verbose=2, fontsize="x-small")
annotator.apply_and_annotate()

# Customize plot
plt.ylabel("% of dead cells")
plt.xlabel("")
if args.title:
    plt.title(args.title)
else:
    plt.title("Comparison of % Values by Group and Sample")
plt.legend(title="", fontsize="xx-small", loc="upper right")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(args.output, dpi=300)
print(f"Plot saved to {args.output}")