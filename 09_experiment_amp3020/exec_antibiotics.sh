#!/env/bin bash


# Execute python ./plotTestAmp_antibiotics.py
./plotTestAmp_antibiotics.py -i1 kanamicina_s.aureus.tsv -i2 ampicilina_s.aureus.tsv -o s.aureus_merged_plots_antibiotics.svg -t "Staphylococcus aureus"

./plotTestAmp_antibiotics.py -i1 kanamicina_s.pneumoniae.tsv -i2 ampicilina_s.pneumoniae.tsv -o s.pneumoniae_merged_plots_antibiotics.svg -t "Streptococcus pneumoniae"

./plotTestAmp_antibiotics.py -i1 kanamicina_k.pneumoniae.tsv -i2 ampicilina_k.pneumoniae.tsv -o k.pneumoniae_merged_plots_antibiotics.svg -t "Klebsiella pneumoniae"

./plotTestAmp_antibiotics.py -i1 kanamicina_p.aeruginosa.tsv -i2 ampicilina_p.aeruginosa.tsv -o p.aeruginosa_merged_plots_antibiotics.svg -t "Pseudomonas aeruginosa"