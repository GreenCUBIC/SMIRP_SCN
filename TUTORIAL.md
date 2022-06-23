# Species specific microRNA discovery and mircoRNA target prediction

his tutorila demonstrates how to perform species specific microRNA discovery and microRNA targeting using SMIRP and other methods

## Part 0: Installing Dependacies

1. First download the original SMIRP code from [Github](https://github.com/jrgreen7/SMIRP) in to the progs/SMIRP folder. Following the "Installing SMIRP dependencies" instructions in TUTORIAL.md.
2. Dowload TarPmiR from the [Hu Lab](http://hulab.ucf.edu/research/projects/miRNA/TarPmiR/)  into the progs/TarPmiR folder and follow their setup instructions.
3. Download miRdup from the [Blanchette Lab](https://www.cs.mcgill.ca/~blanchem/mirdup/) into the progs/TarPmiR folder and follow their set up instructions
4. Install cd-hit from the [Weizhong Lab](https://github.com/weizhongli/cdhit). Follow the installation instruction for your system.

# microRNA Discovery

## Part 1: Creating Training Data

Follow the "Building a species-specific model" instructions in the SMIRP TUTORIAL.md file to curate positive and negative training data.

## Part 2: Extract Candidate Hairpins
In order to discover miRNA one must supply the model with potantial hairpins sequences.

### Part 2.1: Extract Sequences
Use the `extract_sequences.py` script from the src/miRNA_Discovery folder to extract sequences from the genome of the target organism.

`python3 extract_sequences.py -i <input_file> -o <output_file>`
>Ex. ```python3 src/miRNA_Discovery/extract_sequences.py -i data/candidate_set_generation/SCN/scn_genome_chromosome_8.fasta -o data/candidate_set_generation/SCN/scn_genome_chromosome_8.seq.fasta```
### Part 2.2: Extract Hairpins
Use the `extract_hairpins.py` script within SMIRP to extract hairpins from the sequences.
>Ex. ```python2 extract_hairpins.py -i scn_genome_chromosome_8.seq.fasta -n 10```

### Part 2.3: Cluster Extracted Hairpins
To reduce ultiple ocpies of the same seqeunce presnet in the candidate set of hairpins we cluster the candidate hairpons using cd-hit then utilize the prepresentative sequence of each cluster.
> First run cd-hit to cluster the sequences at 90% similairty

>`cd-hit -i <input_fasta> -o <output_file> -c 0.9 -M <max_ram_usage> -T <number_of_treads> -d 0`
>>Ex. ```cd-hit -i data/candidate_set_generation/SCN/scn_genome_chromosome_8.seq.fasta.nr.hairpins -o data/candidate_set_generation/SCN/scn_genome_chromosome_8.seq.fasta.nr.hairpins.clustr -c 0.9 -T 16 -M 10000 -d 0```

> Then run the `extract_representative.py` script in the src/miRNA_Discovery folder to extract the represetative hairpins

>`python3 extract_representative.py -i <input_clstr_file> -f <input_fasta_file> -o <output_file>`
>>Ex. ``python3 src/miRNA_Discovery/extract_representative.py -i data/candidate_set_generation/SCN/scn_genome_chromosome_8.seq.fasta.nr.hairpins.clustr.clstr -f data/candidate_set_generation/SCN/scn_genome_chromosome_8.seq.fasta.nr.hairpins.clustr -o data/candidate_set_generation/SCN/scn_genome_chromosome_8.rep.fasta``

### Part 2.4: Extract Festures
Finally use the `build_hmp_features.py` script from SMIRP to extract features from the representative seqeunces

>Ex. `python2 build_hmp_features.py -i scn_genome_chromosome_8.rep.fasta -n 14`

## Part 3: Train and apply model
Use the train_and_predict.ipynb notebook in src/miRNA_Discovery to train your species specifc miRNA discovery model and apply to your candidate hairpin sequences

Run `create_high_confidence_list.py` to create you final high confidence pre-miRNA files

`python3 create_high_confidence_list.py -i <input_file> -f <input_fasta> -o <ouput_file_prefix>`
> Ex. `python3 src/miRNA_Discovery/create_high_confidence_list.py -i data/trained_miRNA_discovery_models/SCN/candidate_set_predictions.csv -f data/candidate_set_generation/SCN/scn_genome_chromosome_8.rep.fasta -o data/trained_miRNA_discovery_models/SCN/scn_genome_chromosome_8.rep.conf.fasta`

# microRNA Targeting

## Part 4: Extract mature microRNA
To perform microRNA target prediction the mature seqeunce of the miRNA are required. Follow the instructions provide by the Blanchette Lab to use miRdup to extract the mature miRNA seqeunces

>Ex. `java -jar miRdup.jar -predict -i ../../data/trained_miRNA_discovery_models/SCN/scn_genome_chromosome_8.rep.conf.fasta.fa -d nematod.model -f ../../data/targeting/SCN/miRNA/scn_genome_chromosome_8.rep.mature -r /usr/local/bin/`

Run the `extract_mature_miRNA.py` script to create the mature miRNA fasta file.

`python3 extract_mature_miRNA.py -i <input_file> -o <output_file>`
>Ex. `python3 src/miRNA_Discovery/extract_mature_miRNA.py -i data/trained_miRNA_discovery_models/SCN/scn_genome_chromosome_8.rep.conf.fasta.fa.miRdup.predictions.txt -o data/trained_miRNA_discovery_models/SCN/scn_genome_chromosome_8.rep.conf.mature.fasta`

## Part 5: Perform microRNA Target Prediction

Follow the instructions provided by the Hu lab to apply TarPmiR to the high confidence mature miRNA and desired mRNA
>Ex. `python3 TarPmiR.py -a ../../../data/targeting/SCN/miRNA/scn_genome_chromosome_8.rep.conf.mature.fasta -b ../../../data/targeting/SCN/mRNA/orderedscngenepredictions_UTR_mRNA_1013GOI.fasta[77] -m models/RF_hsa_cel_May_11_2022.tarpmir.pkl -p 0.01`

Then run the `filter_targets.py` script in the src/targetting folder to filter the result of the microRNA Target predictions

`python3 filter_targets.py -i <input_file> -m <miRNA_fasta> -r <mRNA_fasta> -o <ouput_folder>`

> Ex. `python3 src/targeting/filter_targets.py -i data/targeting/SCN/miRNA/scn_genome_chromosome_8.rep.conf.mature.fasta_orderedscngenepredictions_UTR_mRNA_1013GOI.fasta[77].bp -m data/targeting/SCN/miRNA/scn_genome_chromosome_8.rep.conf.mature.fasta -r data/targeting/SCN/mRNA/orderedscngenepredictions_UTR_mRNA_1013GOI.fasta[77] -o data/targeting/SCN/results`
