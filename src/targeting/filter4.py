import getopt, sys
from FastaOperations import FastaOperations

def filter4(output_folder, miRNA_fa,mRNA_fasta,O2A_folder):
    miRNA_total = FastaOperations(miRNA_fa).get_sequence_dict()
    mRNA_all = FastaOperations(mRNA_fasta).get_sequence_dict()

    procesed = []
    miRNA_dict = {}
    mRNA_dict_data = {}
    mRNA_dict = {}
    for miRNA in miRNA_total:
        if  "-".join(miRNA.split("-")[:-1]) not in procesed:
            pre_miRNA =  "-".join(miRNA.split("-")[:-1])
            procesed.append("-".join(miRNA.split("-")[:-1]))
            f_in = open(f'{output_folder}/{"-".join(miRNA.split("-")[:-1])}.tarpmir.csv')
            count = 0
            for line in f_in:
                data = line.split(",")
                if data[1] not in mRNA_dict_data:
                    mRNA_dict_data[data[1]] = []
                mRNA_dict_data[data[1]].append(data)
                if pre_miRNA not in miRNA_dict:
                    miRNA_dict[pre_miRNA] = {}
                miRNA_dict[pre_miRNA][data[1]] = count
                count += 1

    for seq2 in mRNA_dict_data:
        mRNA_dict_data[seq2].sort(key=lambda x: float(x[-1]),reverse=True)
        count = 0
        for data in mRNA_dict_data[seq2]:
            if data[1] not in mRNA_dict:
                mRNA_dict[data[1]] = {}
            mRNA_dict[data[1]]["-".join(data[0].split("-")[:-1])] = count
            count += 1

    del mRNA_dict_data

    f_o_miRNA = open(f"{O2A_folder}/miRNA.O2A.tarpmir.csv","w+")
    f_o_mRNA = open(f"{O2A_folder}/mRNA.O2A.tarpmir.csv","w+")
    for seq2 in mRNA_all:
        f_o_miRNA.write(f",{seq2}")
        f_o_mRNA.write(f",{seq2}")
    f_o_miRNA.write(f"\n")
    f_o_mRNA.write(f"\n")

    procesed = []
    for seq in miRNA_total:
        seq1 = "-".join(seq.split("-")[:-1])
        if seq1 not in procesed:
            procesed.append(seq1)
            f_o_miRNA.write(f"{seq1}")
            f_o_mRNA.write(f"{seq1}")
            for seq2 in mRNA_all:
                if seq1 in miRNA_dict and seq2 in miRNA_dict[seq1]:
                    f_o_miRNA.write(f",{miRNA_dict[seq1][seq2]}")
                else:
                    f_o_miRNA.write(f",1000000")
                if seq2 in mRNA_dict and seq1 in mRNA_dict[seq2]:
                    f_o_mRNA.write(f",{mRNA_dict[seq2][seq1]}")
                else:
                    f_o_mRNA.write(f",1000000")
            f_o_miRNA.write(f"\n")
            f_o_mRNA.write(f"\n")



def usage():
    print("python3 filter4.py -m <miRNA_fasta> -r <mRNA_fasta> -o <output_folder> -a <O2A_folder>")


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
    filter4(output_folder, miRNA_fa,mRNA_fasta,O2A_folder)

if __name__ == "__main__":
    main()