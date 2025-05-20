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
# process_sequence "BK026787.1.fasta" "BK026787.1_amp_region.fasta" 19543 19898

process_sequence "CP103114.1.fasta" "CP103114.1_amp_region.fasta"   609071	609776
process_sequence "CP103130.1.fasta" "CP103130.1_amp_region.fasta"   5650222	5650926
process_sequence "CP103206.1.fasta" "CP103206.1_amp_region.fasta"   3305513	3306216
process_sequence "CP103191.1.fasta" "CP103191.1_amp_region.fasta"   608925	609629
process_sequence "CP041230.1.fasta" "CP041230.1_amp_region.fasta"   5582882	5583585
process_sequence "CP113514.1.fasta" "CP113514.1_amp_region.fasta"   5661338	5662042
process_sequence "CP103094.1.fasta" "CP103094.1_amp_region.fasta"   3371281	3371985
process_sequence "CP143941.1.fasta" "CP143941.1_amp_region.fasta"   4648422	4649126
process_sequence "CP046425.1.fasta" "CP046425.1_amp_region.fasta"   1630673	1631416
process_sequence "CP103166.1.fasta" "CP103166.1_amp_region.fasta"   3179575	3180279
process_sequence "CP103082.1.fasta" "CP103082.1_amp_region.fasta"   2905574	2906317
process_sequence "CP126057.1.fasta" "CP126057.1_amp_region.fasta"   71409	72152
process_sequence "CP103125.1.fasta" "CP103125.1_amp_region.fasta"   5391998	5392741
process_sequence "CP083680.1.fasta" "CP083680.1_amp_region.fasta"   5750504	5751247
process_sequence "CP083675.1.fasta" "CP083675.1_amp_region.fasta"   217666	218409
