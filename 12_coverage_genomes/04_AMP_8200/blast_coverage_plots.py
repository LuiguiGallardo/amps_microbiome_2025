#!/usr/bin/env python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set_style("white")

def parse_blast_tab(filename):
    """
    Parse BLAST tabular (format 6) output.
    Returns: dict { query : list of (qstart, qend) }
    """
    cols = [
        'qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen',
        'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'
    ]
    df = pd.read_csv(filename, sep='\t', header=None, names=cols)

    hits_by_query = {}
    for query, group in df.groupby('qseqid'):
        hits = []
        for _, row in group.iterrows():
            start = min(row['qstart'], row['qend'])
            end = max(row['qstart'], row['qend'])
            hits.append((start, end))
        hits_by_query[query] = hits

    return hits_by_query

def plot_coverage(hits_by_query, output_prefix, title, xlabel, ylabel, genome_length):
    """
    Generate coverage plots for each query.
    """
    for query, hits in hits_by_query.items():
        if not hits:
            continue

        # Use given genome length or infer from hits
        max_pos = genome_length if genome_length else max([e for _, e in hits])
        max_pos *= 1.05  # add 5% padding

        fig, ax = plt.subplots(figsize=(10, 2))
        for start, end in hits:
            ax.hlines(y=1, xmin=start, xmax=end, lw=6, color='turquoise')

        ax.set_xlim(0, max_pos)
        ax.set_ylim(0, 2)

        ax.set_xlabel(xlabel or f"{query} position (bp)", fontsize=12)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        else:
            ax.set_ylabel("")
            ax.set_yticks([])

        ax.set_title(title or f"BLAST Hit Coverage for {query}", fontsize=14, pad=20)

        # Remove top and right spines for cleaner look
        sns.despine()
        plt.tight_layout()
        
        # Save both PNG and SVG files
        outfile_png = f"{output_prefix}.png"
        outfile_svg = f"{output_prefix}.svg"
        plt.savefig(outfile_png, dpi=300, bbox_inches='tight')
        plt.savefig(outfile_svg, bbox_inches='tight')
        plt.close()
        print(f"Saved: {outfile_png}")
        print(f"Saved: {outfile_svg}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate coverage plots from BLAST format 6 output."
    )
    parser.add_argument("-i", "--input", required=True,
                        help="BLAST tabular (format 6) input file")
    parser.add_argument("-o", "--output", default="coverage",
                        help="Output prefix for image files (default: 'coverage')")
    parser.add_argument("--title", default=None,
                        help="Custom plot title")
    parser.add_argument("--xlabel", default=None,
                        help="Custom X-axis label")
    parser.add_argument("--ylabel", default=None,
                        help="Custom Y-axis label")
    parser.add_argument("--genome_length", type=int, default=None,
                        help="Explicit total genome length for X-axis")

    args = parser.parse_args()

    hits_by_query = parse_blast_tab(args.input)
    plot_coverage(
        hits_by_query,
        output_prefix=args.output,
        title=args.title,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
        genome_length=args.genome_length
    )

if __name__ == "__main__":
    main()
