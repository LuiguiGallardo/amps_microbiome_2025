#!/usr/bin/env bash

#!/bin/bash

# Function to process a single sequence
process_sequence() {
    local input_fasta=$1
    local output_fasta=$2
    local start=$3
    local end=$4

    # Extract the region of the protein sequence
    ../src/extract_region.py -i "$input_fasta" -o "$output_fasta" -s "$start" -e "$end"

    # Predict the proteins in the extracted region
    TransDecoder.LongOrfs -t "$output_fasta" -m 9
}

# Process each sequence
process_sequence "BK026787.1.fasta" "BK026787.1_amp_region.fasta" 19543 19898
process_sequence "BK058526.1.fasta" "BK058526.1_amp_region.fasta" 15016 15374
process_sequence "CP133078.1.fasta" "CP133078.1_amp_region.fasta" 2477315 2477669
process_sequence "CP014223.1.fasta" "CP014223.1_amp_region.fasta" 2496741 2497093
