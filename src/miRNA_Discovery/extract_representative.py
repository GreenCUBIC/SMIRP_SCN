import getopt, sys
sys.path.append("../..")
from FastaOperations import FastaOperations

def extract_representative(input_file,input_fasta,output_file):
    fi = open(input_file,"r")
    fo = open(output_file, "w+")

    hairpin_dict = FastaOperations(input_fasta).get_sequence_dict()


    clus_lines = fi.readlines()

    for clus_line in clus_lines:
        if "*" in clus_line:
            parts = clus_line.split(" ")
            sequence = parts[-2][1:-3]
            fo.write(f'>{sequence}\n{hairpin_dict[sequence]}\n')


def usage():
    print("python3 extract_representative.py -i <input_clstr_file> -f <input_fasta_file> -o <output_file>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "input_clstr_file=","input_fasta_file=","ouput_file_prefix="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output_file = None
    input_file = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--ouput_file_prefix"):
            ouput_file_prefix = str(a)
        elif o in ("-i", "--input_file"):
            input_file = str(a)
        elif o in ("-f", "--input_fasta"):
            input_fasta = str(a)
        else:
            assert False, "Unhandled Option"
    extract_representative(input_file,input_fasta,ouput_file_prefix)

if __name__ == "__main__":
    main()