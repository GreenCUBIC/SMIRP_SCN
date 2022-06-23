import getopt, sys

def extract_sequences(file_in, file_out):
    fi = open(file_in, "r")
    fo = open(file_out, "w+")

    nucleotide = {}
    possible_sequences = []

    for line in fi:
        if ">" in line:
            name = line[1:-1]
        else:
            for character in line:
                if character != "\n":
                    if character == "t":
                        character = "u"
                    elif character == "T":
                        character = "U"
                    if name in nucleotide:
                        nucleotide[name].append(character)
                    else:
                        nucleotide[name] = [character]

    for name in nucleotide:
        for i in range(round(len(nucleotide[name])/250) + 1):
            if len(nucleotide[name][i*250:]) < 500:
                seq_list = nucleotide[name][i*250:]
            else:
                seq_list = nucleotide[name][i*250:i*250 + 500]
            seq = ""
            for k in range(len(seq_list)):
                if seq_list[-(k+1)] == 'G':
                    seq = seq + 'C'
                elif seq_list[-(k+1)] == 'g':
                    seq = seq + 'c'
                elif seq_list[-(k+1)] == 'C':
                    seq = seq + 'G'
                elif seq_list[-(k+1)] == 'c':
                    seq = seq + 'g'
                elif seq_list[-(k+1)] == 'A':
                    seq = seq + 'U'
                elif seq_list[-(k+1)] == 'a':
                    seq = seq + 'u'
                elif seq_list[-(k+1)] == 'U':
                    seq = seq + 'A'
                elif seq_list[-(k+1)] == 'u':
                    seq = seq + 'a'
                elif seq_list[-(k+1)] == 'N':
                    seq = seq + 'N'
                elif seq_list[-(k+1)] == 'n':
                    seq = seq + 'n'
            fo.write(f'>{name}_{i}a' + "\n")
            fo.write(f'{"".join(seq_list)}\n')
            fo.write(f'>com_{name}_{i}b' + "\n")
            fo.write(seq + "\n")

def usage():
    print("python3 extract_sequences.py -i <input_file> -o <output_file>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "input_file=","ouput_file="])
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
        elif o in ("-o", "--ouput_file"):
            ouput_file_prefix = str(a)
        elif o in ("-i", "--input_file"):
            input_file = str(a)
        else:
            assert False, "Unhandled Option"
    extract_sequences(input_file,ouput_file_prefix)

if __name__ == "__main__":
    main()