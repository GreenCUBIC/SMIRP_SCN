import getopt, sys
from FastaOperations import FastaOperations

def filter3(output_folder, miRNA_fa):
    miRNA_total = FastaOperations(miRNA_fa).get_sequence_dict()
    procesed = []
    for miRNA in miRNA_total:
        if  "-".join(miRNA.split("-")[:-1]) not in procesed:
            f_in = open(f'{output_folder}/{"-".join(miRNA.split("-")[:-1])}').readlines()
            accepted_data = []
            for line in f_in:
                data = line.split("\t")
                if abs(int(data[3].split(",")[0]) - int(data[3].split(",")[1])) >= 6:
                    accepted_data.append(data[:5])
            data_dict = {}
            for item in accepted_data:
                if item[1] not in data_dict:
                    data_dict[item[1]] = item
                elif float(item[-1]) > float(data_dict[item[1]][-1]):
                    data_dict[item[1]] = item
            
            accepted_data = []
            for seq in data_dict:
                accepted_data.append(data_dict[seq])
            accepted_data.sort(key = lambda x: float(x[-1]),reverse = True)

            f_out = open(f'{output_folder}/{"-".join(miRNA.split("-")[:-1])}.tarpmir.csv',"w+")
            for item in accepted_data:
                f_out.write(f'{",".join(item)}\n')


def usage():
    print("python3 filter3.py -m <miRNA_fasta> -o <output_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:m:o:", ["help","miRNA_fasta=","output_folder="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output_folder = None
    miRNA_fa = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output_folder"):
            output_folder = str(a)
        elif o in ("-m", "--miRNA_fasta"):
            miRNA_fa = str(a)
        else:
            assert False, "Unhandled Option"
    filter3(output_folder, miRNA_fa)

if __name__ == "__main__":
    main()