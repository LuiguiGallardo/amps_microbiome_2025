#!/usr/bin/env python

# Imports
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from scipy.stats import mannwhitneyu

# Define colors for each group
colors = {
    'Our AMPs': 'darkcyan',
    'APD3': 'darkorchid',
    'dbAMP': 'red',
    'DRAMP': 'darkorange'
}

# Rename the groups for better readability
group_replacements = {
    'apd3': 'APD3',
    'dbamp': 'dbAMP',
    'dramp': 'DRAMP',
    'our_amps': 'Our AMPs'
}

def add_pvalue_annotations(ax, data, x, y, pairs):
    for pair in pairs:
        group1 = data[data[x] == pair[0]][y]
        group2 = data[data[x] == pair[1]][y]
        stat, pvalue = mannwhitneyu(group1, group2)
        
        if pvalue > 0.05:
            annotation = 'ns'
        elif pvalue > 0.01:
            annotation = '*'
        elif pvalue > 0.001:
            annotation = '**'
        elif pvalue > 0.0001:
            annotation = '***'
        else:
            annotation = '****'
        
        # Get the y position for the annotation
        y_max = max(data[y])
        y_pos = y_max + (y_max * 0.15) * (pairs.index(pair) + 1)
        
        # Add the annotation
        ax.annotate(annotation, xy=((data[x].unique().tolist().index(pair[0]) + data[x].unique().tolist().index(pair[1])) / 2, y_pos), 
                    ha='center', va='bottom', fontsize=12, color='black')
        
        # Add a line connecting the groups
        ax.plot([data[x].unique().tolist().index(pair[0]), data[x].unique().tolist().index(pair[1])], [y_pos, y_pos], lw=1.5, color='black')

    # Adjust the y-axis limit to give more space for annotations
    ax.set_ylim(top=y_pos + (y_max * 0.1))

def create_box_plot(data, output_file, y, title, ylabel):
    # Set the style
    sns.set_style("white")

    # Rename the groups for better readability
    data['group'] = data['group'].replace(group_replacements)

    # Create the box plot
    plt.figure(figsize=(5, 5))
    ax = sns.boxplot(x='group', y=y, data=data, hue='group', palette=colors, legend=False)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel(ylabel, fontweight='bold')
    
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')

    # Perform pairwise statistical tests and add annotations
    pairs = list(combinations(data['group'].unique(), 2))
    add_pvalue_annotations(ax, data, 'group', y, pairs)

    # Save the plot as SVG and PNG
    plt.tight_layout()
    plt.savefig(f"{output_file}_{y}_box_plot.svg")
    plt.savefig(f"{output_file}_{y}_box_plot.png")
    plt.show()
    plt.clf()

# Function to perform pairwise statistical tests (Mann-Whitney U test)
def perform_statistical_tests(data, output_file):
    groups = data['group'].unique()
    results = []

    for group1, group2 in combinations(groups, 2):
        group1_data = data[data['group'] == group1]
        group2_data = data[data['group'] == group2]

        group1_gravy = group1_data['gravy_index']
        group2_gravy = group2_data['gravy_index']
        group1_net = group1_data['net_charge']
        group2_net = group2_data['net_charge']

        # Check sample size before performing the test
        if len(group1_gravy) < 20 or len(group2_gravy) < 20:
            p_gravy = float('nan')
        else:
            stat_gravy, p_gravy = mannwhitneyu(group1_gravy, group2_gravy)

        if len(group1_net) < 20 or len(group2_net) < 20:
            p_net = float('nan')
        else:
            stat_net, p_net = mannwhitneyu(group1_net, group2_net)

        results.append([group1, group2, p_gravy, p_net])

    # Save results to a TSV file
    results_df = pd.DataFrame(results, columns=['Group 1', 'Group 2', 'Gravy Index P-value', 'Net Charge P-value'])
    results_df.to_csv(output_file, sep='\t', index=False)

def load_data(input_file):
    return pd.read_csv(input_file, sep='\t')

def generate_jointplot(data, output_file):
    # Set the style
    sns.set_style("white")

    # Rename the groups for better readability
    data['group'] = data['group'].replace(group_replacements)

    # Create a FacetGrid to plot each group separately with shared axes
    g = sns.FacetGrid(data, col="group", col_wrap=2, sharey=True, sharex=True, aspect=1, height=5)
    g.map_dataframe(sns.scatterplot, x="net_charge", y="gravy_index", hue="group", palette=colors, legend=False, alpha=0.3)
    g.map_dataframe(sns.kdeplot, x="net_charge", y="gravy_index", hue="group", fill=True, palette=colors, alpha=0.8)

    # Add axis labels and titles
    g.set_axis_labels("Net charge", "Hydrophobicity")
    g.set_titles(col_template="{col_name}", fontweight='bold', size=20)

    # Increase the size of the text
    for ax in g.axes.flat:
        ax.axhline(y=0, color='lightgray', linestyle='-', zorder=0)
        ax.axvline(x=0, color='lightgray', linestyle='-', zorder=0)
        ax.set_xlabel(ax.get_xlabel(), fontsize=22, fontweight='bold')
        ax.set_ylabel(ax.get_ylabel(), fontsize=22, fontweight='bold')
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(22)

    # Save the plot as SVG and PNG
    plt.figure(figsize=(5, 5))
    g.savefig(f"{output_file}.svg")
    g.savefig(f"{output_file}.png")
    plt.show()
    plt.clf()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate jointplot and perform statistical tests on datasets.")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file with datasets.")
    parser.add_argument("-o", "--output", required=True, help="Base name for saving the output plots and statistical test results.")

    # Parse arguments
    args = parser.parse_args()

    # Load the data
    both_datasets = load_data(args.input)

    # Generate the jointplot and save the plots
    generate_jointplot(both_datasets, args.output)

    # Generate individual violin plots and save them
    create_box_plot(both_datasets, args.output, 'net_charge', 'Net Charge Distribution', 'Net Charge')
    create_box_plot(both_datasets, args.output, 'gravy_index', 'Hydrophobicity Distribution', 'Hydrophobicity')

    # Output TSV filename for the statistical results
    output_results_file = f"{args.output}_statistical_tests.tsv"

    # Perform statistical tests and save the results to a TSV file
    perform_statistical_tests(both_datasets, output_results_file)

if __name__ == "__main__":
    main()