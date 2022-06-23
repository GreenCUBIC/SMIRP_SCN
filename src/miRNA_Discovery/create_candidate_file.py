import getopt, sys
def create_candidate_file(headers_file,hmp20_file,outfile_name):
    hmp20 = open(hmp20_file).readlines()
    headers = open(headers_file).readlines()

    headers_list = []
    for line in headers:
        if ">" in line:
            headers_list.append(line[1:-1])
        else:
            headers_list.pop()
    print(len(headers_list))
    print(len(hmp20))
    with open(outfile_name,"w+") as f_out:
        for i in range(len(headers_list)):
            f_out.write(f"{headers_list[i]},{','.join(hmp20[i].split(',')[:-1])}\n")

def usage():
    print("python3 create_candidate_file.py -i <hmp20_file> -f <headers_file> -o <ouput_file>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "hmp20_file=","headers_file=","ouput_file_prefix="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    ouput_file_prefix = None
    hmp20_file = None
    headers_file = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--ouput_file_prefix"):
            ouput_file_prefix = a
        elif o in ("-i", "--hmp20_file"):
            hmp20_file = a
        elif o in ("-f", "--headers_file"):
            headers_file = a
        else:
            assert False, "Unhandled Option"
    create_candidate_file(headers_file,hmp20_file,ouput_file_prefix)

if __name__ == "__main__":
    main()
