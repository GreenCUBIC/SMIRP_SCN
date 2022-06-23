import getopt, sys
import os
from filter1 import filter1
from filter2 import filter2
from filter3 import filter3
from filter4 import filter4
from filter5 import filter5
from filter6 import filter6
from filter7 import filter7
from filter8 import filter8

def filter_targets(input_file,output_folder, miRNA_fa,mRNA_fasta):
    # make miRNA,O2A,image folder
    for folder in ['miRNA','O2A','images']:
        dirName = f'{output_folder}/{folder}'
        if not os.path.exists(dirName):
            os.makedirs(dirName)
    fixed_input_file = f'{".".join(input_file.split(".")[:-1])}.fixed.{input_file.split(".")[-1]}'
    miRNA_folder = f'{output_folder}/miRNA'
    O2A_folder = f'{output_folder}/O2A'
    image_folder = f'{output_folder}/images'
    filter1(input_file,fixed_input_file)
    filter2(fixed_input_file,f'{output_folder}/miRNA', miRNA_fa)
    filter3(miRNA_folder, miRNA_fa)
    filter4(miRNA_folder, miRNA_fa,mRNA_fasta,O2A_folder)
    filter5(O2A_folder)
    filter6(miRNA_folder, miRNA_fa,mRNA_fasta,O2A_folder)
    filter7(miRNA_folder, miRNA_fa,mRNA_fasta,O2A_folder)
    filter8(miRNA_folder, miRNA_fa,image_folder)


def usage():
    print("python3 filter_targets.py -i <input_file> -m <miRNA_fasta> -r <mRNA_fasta> -o <ouput_folder")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:r:m:", ["help","miRNA_fasta=","mRNA_fasta=","output_folder="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output_folder = None
    miRNA_fa = None
    mRNA_fasta = None
    input_file = None
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
        elif o in ("-i", "--input_file"):
            input_file = str(a)
        else:
            assert False, "Unhandled Option"
    filter_targets(input_file,output_folder, miRNA_fa,mRNA_fasta)

if __name__ == "__main__":
    main()