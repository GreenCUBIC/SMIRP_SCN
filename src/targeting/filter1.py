import getopt, sys
from src.classes.FastaOperations import FastaOperations

def fix_bp(file,file_out):
    lines = open(file).readlines()
    f_out = open(file_out,"w+")
    for line1 in lines:
        data1 = line1.split("\t")
        if len(data1) > 17:
            count = 0
            for item in data1:
                if item[-1] == "\n":
                    f_out.write(f'{item}')
                    count = 0
                else:
                    if count <=16:
                        f_out.write(f'{item}\t')
                        count += 1
                    else:
                        f_out.write(f'{item[0]}\n{item[1:]}\t')
                        count = 1
        else:
            f_out.write(line1)
            if line1[-1] != "\n":
                f_out.write("\n")

def filter1(input_file,output_file):
    fix_bp(input_file,output_file) 

def usage():
    print("python3 filter1.py -i <input_file> -o <output_file>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=","output="])
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
        elif o in ("-o", "--output"):
            output_file = a
        elif o in ("-i", "--input"):
            input_file = a
        else:
            assert False, "Unhandled Option"
    filter1(input_file,output_file)

if __name__ == "__main__":
    main()