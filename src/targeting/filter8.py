import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import getopt, sys
from src.classes.FastaOperations import FastaOperations

def filter8(output_folder, miRNA_fa,image_folder):

    miRNA_all = FastaOperations(miRNA_fa).get_sequence_dict()

    miRNA_dict = {}
    mRNA_dict = {}
    checked = []
    for miRNA in miRNA_all:
        if '-'.join(miRNA.split('-')[:-1]) not in checked:
            pre_miRNA = '-'.join(miRNA.split('-')[:-1])
            data_lines = open(f"{output_folder}/{'-'.join(miRNA.split('-')[:-1])}.tarpmir.csv")
            for line in data_lines:
                data = line.split(",")
                if pre_miRNA not in miRNA_dict:
                    miRNA_dict[pre_miRNA] = []
                if data[1] not in mRNA_dict:
                    mRNA_dict[data[1]] = []
                miRNA_dict[pre_miRNA].append(float(data[-1]))
                mRNA_dict[data[1]].append(float(data[-1]))

    sns.set_theme()

    for i,seq in enumerate(miRNA_dict):
        if i < 40:
            plt.scatter((1-pd.DataFrame(miRNA_dict[seq]).rank(pct=True,method='first')),miRNA_dict[seq])
            plt.xlabel('1 - Percentile')
            plt.ylabel('Confidence')
            plt.xlim([-0.1,1.1])
            plt.ylim([-0.1,1.1])
            plt.title(seq)
            plt.savefig(f'{image_folder}/{seq}.O2A.png')
            plt.clf()

    for i,seq in enumerate(mRNA_dict):
        if i < 40:
            plt.scatter((1-pd.DataFrame(mRNA_dict[seq]).rank(pct=True,method='first')),mRNA_dict[seq])
            plt.xlabel('1 - Percentile')
            plt.ylabel('Confidence')
            plt.xlim([-0.1,1.1])
            plt.ylim([-0.1,1.1])
            plt.title(seq)
            plt.savefig(f'{image_folder}/{seq}.O2A.png')
            plt.clf()

def usage():
    print("python3 filter8.py -m <miRNA_fasta> -r <mRNA_fasta> -o <output_folder> -a <image_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:o:r:p:", ["help","miRNA_fasta=","mRNA_fasta=","output_folder=","image_folder="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output_folder"):
            output_folder = a
        elif o in ("-m", "--miRNA_fasta"):
            miRNA_fa = a
        elif o in ("-r", "--mRNA_fasta"):
            mRNA_fasta = a
        elif o in ("-p", "--image_folder"):
            image_folder = a
        else:
            assert False, "Unhandled Option"
    filter8(output_folder, miRNA_fa,mRNA_fasta,image_folder)

if __name__ == "__main__":
    main()
            
