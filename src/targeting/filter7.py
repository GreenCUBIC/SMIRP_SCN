import getopt, sys
from src.classes.FastaOperations import FastaOperations

number = [1,4,8,10,25,50,100]

def filter7(output_folder, miRNA_fa,mRNA_fasta,O2A_folder):
    miRNA_all = FastaOperations(miRNA_fa).get_sequence_dict()
    mRNA_all = FastaOperations(mRNA_fasta).get_sequence_dict()

    miRNA_dict = {}
    checked = []
    for miRNA in miRNA_all:
        if '-'.join(miRNA.split('-')[:-1]) not in checked:
            pre_miRNA = '-'.join(miRNA.split('-')[:-1])
            data_lines = open(f"{output_folder}/{'-'.join(miRNA.split('-')[:-1])}.tarpmir.csv")
            for line in data_lines:
                data = line.split(",")
                if pre_miRNA not in miRNA_dict:
                    miRNA_dict[pre_miRNA] = {}
                miRNA_dict[pre_miRNA][data[1]] = ','.join(data[:-1]) + ',' + miRNA_all[data[0]][int(data[2])-1 : int(data[3])-1] + ',' + mRNA_all[data[1]][int(data[4])-1 : int(data[5])-1] + ',' + data[-1]  
        checked.append('-'.join(miRNA.split('-')[:-1]))


    for c1 in number:
        for c2 in number:
            f_in = open(f"{O2A_folder}/top_{c1}_by_{c2}.tarpmir.csv")
            f_out = open(f"{O2A_folder}/top_{c1}_by_{c2}.results.csv","w+")
            for line in f_in:
                data = line[:-1].split(",")
                if data[1] in miRNA_dict and data[0] in miRNA_dict[data[1]]:
                    f_out.write(miRNA_dict[data[1]][data[0]])

def usage():
    print("python3 filter7.py -m <miRNA_fasta> -r <mRNA_fasta> -o <output_folder> -a <O2A_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:o:r:a:", ["help","miRNA_fasta=","mRNA_fasta=","output_folder=","O2A_folder="])
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
        elif o in ("-a", "--O2A_folder"):
            O2A_folder = a
        else:
            assert False, "Unhandled Option"
    filter7(output_folder, miRNA_fa,mRNA_fasta,O2A_folder)

if __name__ == "__main__":
    main()