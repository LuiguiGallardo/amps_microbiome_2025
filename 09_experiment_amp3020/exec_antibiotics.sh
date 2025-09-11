#!/env/bin bash


# Execute python ./plotTestAmp_antibiotics.py
./plotTestAmp_antibiotics.py -i1 adr1_s.aureus.tsv -i2 adr2_s.aureus.tsv -i3 kanamicina_s.aureus.tsv -i4 ampicilina_s.aureus.tsv -o s.aureus_merged_plots_antibiotics.svg -t "Staphylococcus aureus"
./plotTestAmp_antibiotics.py -i1 adr1_s.pneumoniae.tsv -i2 adr2_s.pneumoniae.tsv -i3 kanamicina_s.pneumoniae.tsv -i4 ampicilina_s.pneumoniae.tsv -o s.pneumoniae_merged_plots_antibiotics.svg -t "Streptococcus pneumoniae"
./plotTestAmp_antibiotics.py -i1 adr1_k.pneumoniae_fmt.tsv -i2 adr2_k.pneumoniae_fmt.tsv -i3 kanamicina_k.pneumoniae.tsv -i4 ampicilina_k.pneumoniae.tsv -o k.pneumoniae_merged_plots_antibiotics.svg -t "Klebsiella pneumoniae"
./plotTestAmp_antibiotics.py -i1 adr1_p.aeruginosa_fmt.tsv -i2 adr2_p.aeruginosa_fmt.tsv -i3 kanamicina_p.aeruginosa.tsv -i4 ampicilina_p.aeruginosa.tsv -o p.aeruginosa_merged_plots_antibiotics.svg -t "Pseudomonas aeruginosa"