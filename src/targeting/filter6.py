import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import getopt, sys
from FastaOperations import FastaOperations

def filter6(output_folder, miRNA_fa,mRNA_fasta,O2A_folder):
    miRNA_all = FastaOperations(miRNA_fa).get_sequence_dict()
    mRNA_all = FastaOperations(mRNA_fasta).get_sequence_dict()

    miRNA_dict = {}

    checked = []
    for miRNA in miRNA_all:
        if '-'.join(miRNA.split('-')[:-1]) not in checked:
            pre_miRNA = '-'.join(miRNA.split('-')[:-1])
            try:
                data_lines = open(f"{output_folder}/{'-'.join(miRNA.split('-')[:-1])}.tarpmir.csv")
                for line in data_lines:
                    data = line.split(",")
                    if pre_miRNA not in miRNA_dict:
                        miRNA_dict[pre_miRNA] = {}
                    miRNA_dict[pre_miRNA][data[1]] = float(data[-1])
            except:
                print(f"missing: {miRNA}")
            checked.append('-'.join(miRNA.split('-')[:-1]))

    data_list = []

    procesed = []
    for seq in miRNA_all:
        seq1 = '-'.join(seq.split('-')[:-1])
        if seq1 not in procesed:
            procesed.append(seq1)
            for seq2 in mRNA_all:
                if seq1 in miRNA_dict and seq2 in miRNA_dict[seq1]:
                    data_list.append(miRNA_dict[seq1][seq2])
                else:
                    data_list.append(0) 


    sns.set_theme()
    plt.hist(data_list,40)
    plt.savefig(f'{O2A_folder}/histogram_figure.tarpmir.png', bbox_inches = "tight")



def usage():
    print("python3 filter6.py -m <miRNA_fasta> -r <mRNA_fasta> -o <output_folder> -a <O2A_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:o:r:a:", ["help","miRNA_fasta=","mRNA_fasta=","output_folder=","O2A_folder="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output_folder = None
    miRNA_fa = None
    mRNA_fasta = None
    O2A_folder = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output_folder"):
            output_folder = str(a)
        elif o in ("-m", "--miRNA_fasta"):
            miRNA_fa = str(a)
        elif o in ("-r", "--mRNA_fasta"):
            mRNA_fasta = str(a)
        elif o in ("-a", "--O2A_folder"):
            O2A_folder = str(a)
        else:
            assert False, "Unhandled Option"
    filter6(output_folder, miRNA_fa,mRNA_fasta,O2A_folder)

if __name__ == "__main__":
    main()