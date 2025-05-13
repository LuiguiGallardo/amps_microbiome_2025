#!/usr/bin/env python3

import argparse
from Bio import SeqIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Calculate sequence lengths from a FASTA file, plot histogram, and export stats.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file")
    parser.add_argument("-o", "--output", required=True, help="Output file prefix (no extension)")

    args = parser.parse_args()

    # Extract sequence lengths
    records = [{"Sequence_ID": record.id, "Length": len(record.seq)}
               for record in SeqIO.parse(args.input, "fasta")]
    df = pd.DataFrame(records)

    # Output 1: Save sequence lengths
    tsv_file = args.output + ".tsv"
    df.to_csv(tsv_file, sep="\t", index=False)

    # Output 2: Save length distribution (count of each length)
    dist_df = df['Length'].value_counts().sort_index().reset_index()
    dist_df.columns = ["Length", "Count"]
    dist_file = args.output + "_length_distribution.tsv"
    dist_df.to_csv(dist_file, sep="\t", index=False)

    # Output 3: Plot histogram
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Length"], bins=30, kde=False)
    plt.title("Sequence Length Distribution")
    plt.xlabel("Sequence Length")
    plt.ylabel("Count")

    plot_file = args.output + ".png"
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()

    # Confirm outputs
    print(f"Saved sequence lengths to: {tsv_file}")
    print(f"Saved length distribution to: {dist_file}")
    print(f"Saved histogram plot to: {plot_file}")

if __name__ == "__main__":
    main()
