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

process_sequence "AP031425.1.fasta"	"AP031425.1_amp_region.fasta"	2179119	2179321
process_sequence "AP031428.1.fasta"	"AP031428.1_amp_region.fasta"	2058513	2058715
process_sequence "CP158110.1.fasta"	"CP158110.1_amp_region.fasta"	1944926	1945128
process_sequence "CP065382.1.fasta"	"CP065382.1_amp_region.fasta"	896167	896372
process_sequence "CP119420.2.fasta"	"CP119420.2_amp_region.fasta"	1342979	1343181
process_sequence "CP107214.1.fasta"	"CP107214.1_amp_region.fasta"	447864	448069
process_sequence "CP155552.1.fasta"	"CP155552.1_amp_region.fasta"	2212108	2212310
process_sequence "CP094466.1.fasta"	"CP094466.1_amp_region.fasta"	813820	814022
process_sequence "CP157286.1.fasta"	"CP157286.1_amp_region.fasta"	1560949	1561154
process_sequence "CP094473.1.fasta"	"CP094473.1_amp_region.fasta"	2124512	2124714
process_sequence "CP107211.1.fasta"	"CP107211.1_amp_region.fasta"	898333	898539
process_sequence "CP094467.1.fasta"	"CP094467.1_amp_region.fasta"	2112998	2113185
process_sequence "CP157369.1.fasta"	"CP157369.1_amp_region.fasta"	1132715	1132902
process_sequence "FP929046.1.fasta"	"FP929046.1_amp_region.fasta"	2671596	2671783
process_sequence "CP107209.1.fasta"	"CP107209.1_amp_region.fasta"	1686802	1686989
process_sequence "CP030777.1.fasta"	"CP030777.1_amp_region.fasta"	1990816	1991003
process_sequence "CP094472.1.fasta"	"CP094472.1_amp_region.fasta"	1200180	1200367
process_sequence "CP094469.1.fasta"	"CP094469.1_amp_region.fasta"	1258354	1258541
process_sequence "CP065376.1.fasta"	"CP065376.1_amp_region.fasta"	910047	910230
process_sequence "LR699017.1.fasta"	"LR699017.1_amp_region.fasta"	2328281	2328464
process_sequence "CP107213.1.fasta"	"CP107213.1_amp_region.fasta"	2639051	2639234
process_sequence "CP157368.1.fasta"	"CP157368.1_amp_region.fasta"	2083356	2083539
process_sequence "CP065381.1.fasta"	"CP065381.1_amp_region.fasta"	840590	840758
process_sequence "CP065380.1.fasta"	"CP065380.1_amp_region.fasta"	841063	841231
process_sequence "CP094468.1.fasta"	"CP094468.1_amp_region.fasta"	910929	911105
process_sequence "FP929045.1.fasta"	"FP929045.1_amp_region.fasta"	90436	90605