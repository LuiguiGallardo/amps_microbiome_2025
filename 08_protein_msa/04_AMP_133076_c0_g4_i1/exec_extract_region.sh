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
process_sequence "AP027446.1.fasta" "AP027446.1_amp_region.fasta"   3671835 3672199
process_sequence "CP121673.1.fasta" "CP121673.1_amp_region.fasta"   1137609 1137973
process_sequence "CP162406.1.fasta" "CP162406.1_amp_region.fasta"   1127065 1127428
process_sequence "CP077281.1.fasta" "CP077281.1_amp_region.fasta"   4611274 4611637
process_sequence "OY754443.1.fasta" "OY754443.1_amp_region.fasta"   961268  961631
process_sequence "CP095088.1.fasta" "CP095088.1_amp_region.fasta"   1018784 1019147
process_sequence "CP139853.1.fasta" "CP139853.1_amp_region.fasta"   5014887 5015250
process_sequence "LR778153.1.fasta" "LR778153.1_amp_region.fasta"   1275118 1275481
process_sequence "CP126300.1.fasta" "CP126300.1_amp_region.fasta"   3186147 3186510
process_sequence "AP022120.1.fasta" "AP022120.1_amp_region.fasta"   999280  999643
process_sequence "CP062203.1.fasta" "CP062203.1_amp_region.fasta"   1057345 1057708
process_sequence "CP164187.1.fasta" "CP164187.1_amp_region.fasta"   3210554 3210917
process_sequence "CP123277.1.fasta" "CP123277.1_amp_region.fasta"   2924240 2924603
process_sequence "CP141100.1.fasta" "CP141100.1_amp_region.fasta"   3950352 3950715
process_sequence "CP138412.1.fasta" "CP138412.1_amp_region.fasta"   2141499 2141862
process_sequence "CP124487.1.fasta" "CP124487.1_amp_region.fasta"   1109045 1109408
process_sequence "CP061226.1.fasta" "CP061226.1_amp_region.fasta"   1159896 1160259
process_sequence "CP110015.1.fasta" "CP110015.1_amp_region.fasta"   3017400 3017763
process_sequence "CP134389.1.fasta" "CP134389.1_amp_region.fasta"   1166477 1166840
process_sequence "CP146893.1.fasta" "CP146893.1_amp_region.fasta"   958535  958898
process_sequence "CP025627.1.fasta" "CP025627.1_amp_region.fasta"   1067117 1067480
process_sequence "CP028126.1.fasta" "CP028126.1_amp_region.fasta"   3929773 3930136
process_sequence "CP163693.1.fasta" "CP163693.1_amp_region.fasta"   1106397 1106760
process_sequence "AP025662.1.fasta" "AP025662.1_amp_region.fasta"   1075530 1075893
process_sequence "CP099078.1.fasta" "CP099078.1_amp_region.fasta"   1014698 1015061
process_sequence "CP135706.1.fasta" "CP135706.1_amp_region.fasta"   1080078 1080441
process_sequence "LR890536.1.fasta" "LR890536.1_amp_region.fasta"   1197597 1197960
process_sequence "CP146665.1.fasta" "CP146665.1_amp_region.fasta"   1018522 1018885
process_sequence "CP055768.1.fasta" "CP055768.1_amp_region.fasta"   983971  984334
process_sequence "CP088820.1.fasta" "CP088820.1_amp_region.fasta"   1168106 1168469
process_sequence "CP091704.1.fasta" "CP091704.1_amp_region.fasta"   1087005 1087368
process_sequence "CP057922.1.fasta" "CP057922.1_amp_region.fasta"   1011517 1011880
process_sequence "CP035846.1.fasta" "CP035846.1_amp_region.fasta"   3727467 3727830
process_sequence "CP044311.1.fasta" "CP044311.1_amp_region.fasta"   2648476 2648839
process_sequence "CP165349.1.fasta" "CP165349.1_amp_region.fasta"   998368  998731
process_sequence "CP164179.1.fasta" "CP164179.1_amp_region.fasta"   4411179 4411542
process_sequence "CP054169.1.fasta" "CP054169.1_amp_region.fasta"   3271769 3272132
process_sequence "LR890270.1.fasta" "LR890270.1_amp_region.fasta"   1654610 1654973
process_sequence "OZ043856.1.fasta" "OZ043856.1_amp_region.fasta"   1185788 1186151
process_sequence "OZ039993.1.fasta" "OZ039993.1_amp_region.fasta"   1136781 1137144
process_sequence "CP097721.1.fasta" "CP097721.1_amp_region.fasta"   1028518 1028881
process_sequence "AP027612.1.fasta" "AP027612.1_amp_region.fasta"   2111154 2111517
process_sequence "OZ001728.1.fasta" "OZ001728.1_amp_region.fasta"   2321048 2321411
process_sequence "CP092703.1.fasta" "CP092703.1_amp_region.fasta"   2932997 2933360
process_sequence "CP116159.1.fasta" "CP116159.1_amp_region.fasta"   1060511 1060874
process_sequence "CP062838.1.fasta" "CP062838.1_amp_region.fasta"   1036505 1036868
process_sequence "CP099166.1.fasta" "CP099166.1_amp_region.fasta"   4026855 4027218
process_sequence "AP026794.1.fasta" "AP026794.1_amp_region.fasta"   1157110 1157473
process_sequence "CP158429.1.fasta" "CP158429.1_amp_region.fasta"   1043254 1043617
process_sequence "AP027440.1.fasta" "AP027440.1_amp_region.fasta"   4263608 4263971