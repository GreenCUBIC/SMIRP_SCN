import getopt, sys
from src.classes.FastaOperations import FastaOperations

def filter2(input_file,output_folder, miRNA_fa):
    miRNA_total = FastaOperations(miRNA_fa).get_sequence_dict()
    miRNA_files = {}
    procesed = []
    for miRNA in miRNA_total:
        if  "-".join(miRNA.split("-")[:-1]) not in procesed:
            miRNA_files["-".join(miRNA.split("-")[:-1])] = open(f'{output_folder}/{"-".join(miRNA.split("-")[:-1])}',"w+")
            procesed.append("-".join(miRNA.split("-")[:-1]))

    f_in = open(input_file)
    for line in f_in:
        data = line.split("\t")
        if "-".join(data[0].split("-")[:-1]) in miRNA_files:
            miRNA_files["-".join(data[0].split("-")[:-1])].write(line)
    f_in.close()

    for seq in miRNA_files:
        miRNA_files[seq].close()


def usage():
    print("python3 filter2.py -i <input_file> -m <miRNA_fasta> -o <output_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:m:o:", ["help", "input_file","miRNA_fasta=","output_folder="])
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
        elif o in ("-i", "--input_file"):
            input_file = a
        else:
            assert False, "Unhandled Option"
    filter2(input_file,output_folder, miRNA_fa)

if __name__ == "__main__":
    main()