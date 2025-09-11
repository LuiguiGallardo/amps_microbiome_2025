#!/env/bin bash


# Execute python ./plotTestAmp_bsa.py
./plotTestAmp_bsa.py -i1 adr1_s.aureus.tsv -i2 adr2_s.aureus.tsv -i3 bsa_s.aureus.tsv -o s.aureus_merged_plots_bsa.svg -t "Staphylococcus aureus"
./plotTestAmp_bsa.py -i1 adr1_s.pneumoniae.tsv -i2 adr2_s.pneumoniae.tsv -i3 bsa_s.pneumoniae.tsv -o s.pneumoniae_merged_plots_bsa.svg -t "Streptococcus pneumoniae"
./plotTestAmp_bsa.py -i1 adr1_k.pneumoniae_fmt.tsv -i2 adr2_k.pneumoniae_fmt.tsv -i3 bsa_k.pneumoniae.tsv -o k.pneumoniae_merged_plots_bsa.svg -t "Klebsiella pneumoniae"
./plotTestAmp_bsa.py -i1 adr1_p.aeruginosa_fmt.tsv -i2 adr2_p.aeruginosa_fmt.tsv -i3 bsa_p.aeruginosa.tsv -o p.aeruginosa_merged_plots_bsa.svg -t "Pseudomonas aeruginosa"