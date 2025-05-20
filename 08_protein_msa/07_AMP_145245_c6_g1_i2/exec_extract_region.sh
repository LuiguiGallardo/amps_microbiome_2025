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

process_sequence "MK232155.1.fasta"	"MK232155.1_amp_region.fasta"	6496	7104
process_sequence "AP031426.1.fasta"	"AP031426.1_amp_region.fasta"	1384679	1385287
process_sequence "MK232331.1.fasta"	"MK232331.1_amp_region.fasta"	6891	7499
process_sequence "CP102267.1.fasta"	"CP102267.1_amp_region.fasta"	1345724	1346332
process_sequence "MK232411.1.fasta"	"MK232411.1_amp_region.fasta"	7903	8499
process_sequence "MK232153.1.fasta"	"MK232153.1_amp_region.fasta"	4829	5425
process_sequence "CP098409.1.fasta"	"CP098409.1_amp_region.fasta"	2068384	2068980
process_sequence "MK232296.1.fasta"	"MK232296.1_amp_region.fasta"	1873	2469
process_sequence "AP031426.1.fasta"	"AP031426.1_amp_region.fasta"	3046136	3046390
process_sequence "CP102267.1.fasta"	"CP102267.1_amp_region.fasta"	3047129	3047383
process_sequence "CP098409.1.fasta"	"CP098409.1_amp_region.fasta"	3696848	3697104