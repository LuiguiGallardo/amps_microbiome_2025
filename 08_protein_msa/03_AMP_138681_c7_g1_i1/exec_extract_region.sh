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
process_sequence "BK038133.1.fasta" "BK038133.1_amp_region.fasta" 116	463
process_sequence "CP107216.1.fasta" "CP107216.1_amp_region.fasta" 2213911	2214257
process_sequence "BK027835.1.fasta" "BK027835.1_amp_region.fasta" 14793 15140
process_sequence "BK026979.1.fasta" "BK026979.1_amp_region.fasta" 117	462
process_sequence "BK025808.1.fasta" "BK025808.1_amp_region.fasta" 117	462
process_sequence "BK033981.1.fasta" "BK033981.1_amp_region.fasta" 13506 13835	

# BK038133.1	116	463
# CP107216.1	2213911	2214257
# BK027835.1	15140	14793
# BK026979.1	117	462
# BK025808.1	117	462
# BK033981.1	13835	13506