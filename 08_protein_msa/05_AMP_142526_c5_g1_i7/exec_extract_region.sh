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
# process_sequence "BK038133.1.fasta" "BK038133.1_amp_region.fasta" 116	463

process_sequence    "LN555523.1.fasta"  "LN555523.1_amp_region.fasta"	190978	191519
process_sequence    "CP048741.1.fasta"  "CP048741.1_amp_region.fasta"	190858	191401
process_sequence    "CP048742.1.fasta"  "CP048742.1_amp_region.fasta"	190908	191451
process_sequence    "CP048740.1.fasta"  "CP048740.1_amp_region.fasta"	190867	191401