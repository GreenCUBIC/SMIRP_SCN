import getopt, sys

def extract_mature_miRNA(input_file,output_file):
    f_in = open(input_file)

    mature_dict = {}
    for line in f_in:
        parts = line.split('\t')
        if len(parts) > 4:
            if '5' in parts[3][-4:]:
                mature_dict[parts[0]] = [parts[3][:-4], parts[4][:-5]]
            else:
                mature_dict[parts[0]] = [parts[4][:-5], parts[3][:-4]]


    f_out = open(output_file, "w+")
    for key in mature_dict:
        f_out.write(f'>{key}-5p\n{mature_dict[key][0]}\n')
        f_out.write(f'>{key}-3p\n{mature_dict[key][1]}\n')


def usage():
    print("python3 extract_mature_miRNA.py -i <input_file> -o <output_file>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "input_file=""ouput_file_prefix="])
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
            ouput_file_prefix = a
        elif o in ("-f", "--input_fasta"):
            input_fasta = a
        else:
            assert False, "Unhandled Option"
    extract_mature_miRNA(input_file,output_file)

if __name__ == "__main__":
    main()