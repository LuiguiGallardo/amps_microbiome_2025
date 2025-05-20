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

process_sequence "CP046425.1.fasta"	"CP046425.1_amp_region.fasta"	1630673	1631416
process_sequence "CP046426.1.fasta"	"CP046426.1_amp_region.fasta"	1629639	1630382
process_sequence "CP046424.1.fasta"	"CP046424.1_amp_region.fasta"	1750994	1751737
process_sequence "CP046176.1.fasta"	"CP046176.1_amp_region.fasta"	3593899	3594115
process_sequence "CP102257.1.fasta"	"CP102257.1_amp_region.fasta"	5400765	5400981
process_sequence "CP096965.1.fasta"	"CP096965.1_amp_region.fasta"	4160017	4160233
process_sequence "AP025232.1.fasta"	"AP025232.1_amp_region.fasta"	4910336	4910552
process_sequence "CP046425.1.fasta"	"CP046425.1_amp_region.fasta"	3678716	3678932
process_sequence "CP068489.1.fasta"	"CP068489.1_amp_region.fasta"	2897406	2897622
process_sequence "CP083689.1.fasta"	"CP083689.1_amp_region.fasta"	4128845	4129061
process_sequence "CP046426.1.fasta"	"CP046426.1_amp_region.fasta"	3673772	3673988
process_sequence "CP046424.1.fasta"	"CP046424.1_amp_region.fasta"	3796210	3796426
process_sequence "CP046428.1.fasta"	"CP046428.1_amp_region.fasta"	1682938	1683154
process_sequence "CP103197.1.fasta"	"CP103197.1_amp_region.fasta"	5136495	5136711
process_sequence "CP007619.1.fasta"	"CP007619.1_amp_region.fasta"	3261958	3262174
process_sequence "CP126056.1.fasta"	"CP126056.1_amp_region.fasta"	4168303	4168519
process_sequence "CP043529.1.fasta"	"CP043529.1_amp_region.fasta"	1714375	1714591
process_sequence "CP013020.1.fasta"	"CP013020.1_amp_region.fasta"	4168305	4168521
process_sequence "CP103067.1.fasta"	"CP103067.1_amp_region.fasta"	3112537	3112753
process_sequence "CP072246.1.fasta"	"CP072246.1_amp_region.fasta"	2148679	2148895
process_sequence "CP000139.1.fasta"	"CP000139.1_amp_region.fasta"	4991555	4991771
process_sequence "LR699004.1.fasta"	"LR699004.1_amp_region.fasta"	5287905	5288121
process_sequence "CP081912.1.fasta"	"CP081912.1_amp_region.fasta"	2962834	2963050
process_sequence "CP143952.1.fasta"	"CP143952.1_amp_region.fasta"	5133452	5133668
process_sequence "CP072234.1.fasta"	"CP072234.1_amp_region.fasta"	1454781	1454997
process_sequence "AP025240.1.fasta"	"AP025240.1_amp_region.fasta"	4794240	4794456
process_sequence "CP008741.1.fasta"	"CP008741.1_amp_region.fasta"	5079495	5079711
process_sequence "CP011531.1.fasta"	"CP011531.1_amp_region.fasta"	5149291	5149507
process_sequence "CP068488.1.fasta"	"CP068488.1_amp_region.fasta"	2187039	2187255
process_sequence "CP046427.1.fasta"	"CP046427.1_amp_region.fasta"	3888142	3888358
process_sequence "AP025235.1.fasta"	"AP025235.1_amp_region.fasta"	4822370	4822586
process_sequence "CP126064.1.fasta"	"CP126064.1_amp_region.fasta"	3039711	3039927
process_sequence "OY725990.1.fasta"	"OY725990.1_amp_region.fasta"	149879	150095
process_sequence "OY764215.1.fasta"	"OY764215.1_amp_region.fasta"	3259816	3260030