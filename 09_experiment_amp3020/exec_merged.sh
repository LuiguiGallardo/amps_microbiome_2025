#!/bin/bash


# Execute python ./plotTestAmp_merged.py with all datasets
./plotTestAmp_merged.py -i1 adr1_s.aureus.tsv -i2 adr2_s.aureus.tsv -i3 bsa_s.aureus.tsv -i4 kanamicina_s.aureus.tsv -i5 ampicilina_s.aureus.tsv --label3 "BSA" --label4 "Kanamicina" --label5 "Ampicilina" -o s.aureus_merged_plots_all.svg -t "Staphylococcus aureus"
./plotTestAmp_merged.py -i1 adr1_s.pneumoniae.tsv -i2 adr2_s.pneumoniae.tsv -i3 bsa_s.pneumoniae.tsv -i4 kanamicina_s.pneumoniae.tsv -i5 ampicilina_s.pneumoniae.tsv --label3 "BSA" --label4 "Kanamicina" --label5 "Ampicilina" -o s.pneumoniae_merged_plots_all.svg -t "Streptococcus pneumoniae"
./plotTestAmp_merged.py -i1 adr1_k.pneumoniae_fmt.tsv -i2 adr2_k.pneumoniae_fmt.tsv -i3 bsa_k.pneumoniae.tsv -i4 kanamicina_k.pneumoniae.tsv -i5 ampicilina_k.pneumoniae.tsv --label3 "BSA" --label4 "Kanamicina" --label5 "Ampicilina" -o k.pneumoniae_merged_plots_all.svg -t "Klebsiella pneumoniae"
./plotTestAmp_merged.py -i1 adr1_p.aeruginosa_fmt.tsv -i2 adr2_p.aeruginosa_fmt.tsv -i3 bsa_p.aeruginosa.tsv -i4 kanamicina_p.aeruginosa.tsv -i5 ampicilina_p.aeruginosa.tsv --label3 "BSA" --label4 "Kanamicina" --label5 "Ampicilina" -o p.aeruginosa_merged_plots_all.svg -t "Pseudomonas aeruginosa"