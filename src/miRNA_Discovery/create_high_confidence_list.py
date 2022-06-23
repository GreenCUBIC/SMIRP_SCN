from FastaOperations import FastaOperations
import getopt, sys

def create_high_confidence_list(input_file,input_fasta,output_file):
    f_feature_selection = open(input_file).readlines()

    unknown = {}

    for line in f_feature_selection:
        data = line.split(",")
        unknown[data[0]] = float(data[1]) 

    fasta = FastaOperations(input_fasta).get_sequence_dict()

    f_out_csv = open(f'{output_file}.csv', "w+")
    f_out_fa = open(f'{output_file}.fa', "w+")
    for hairpin in unknown:
        if unknown[hairpin] >= 0.9:
            f_out_csv.write(f'{hairpin},{fasta[hairpin]},{unknown[hairpin]}\n')
            f_out_fa.write(f'>{hairpin}\n{fasta[hairpin]}\n')

def usage():
    print("python3 create_high_confidence_list.py -i <input_file> -f <input_fasta> -o <ouput_file_prefix>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "input_file=","input_fasta=","ouput_file_prefix="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    ouput_file_prefix = None
    input_file = None
    input_fasta = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--ouput_file_prefix"):
            ouput_file_prefix = a
        elif o in ("-i", "--input_file"):
            input_file = a
        elif o in ("-f", "--input_fasta"):
            input_fasta = a
        else:
            assert False, "Unhandled Option"
    create_high_confidence_list(input_file,input_fasta,ouput_file_prefix)

if __name__ == "__main__":
    main()