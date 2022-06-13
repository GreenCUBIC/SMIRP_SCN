import pandas as pd
import getopt, sys

number = [1,4,8,10,25,50,100]

def filter5(O2A_folder):
    miRNA_count = open(f"{O2A_folder}/miRNA.O2A.tarpmir.csv").readlines()
    gff = miRNA_count[0].split(",")[1:]
    miRNA_count = miRNA_count[1:]

    mRNA_count = open(f"{O2A_folder}/mRNA.O2A.tarpmir.csv").readlines()[1:]

    f_out_files = {}
    count = {}
    for c1 in number:
        for c2 in number:
            if c1 not in count:
                count[c1] = {}
                f_out_files[c1] = {}
            if c2 not in count[c1]:
                count[c1][c2] = 0
                f_out_files[c1][c2] = open(f"{O2A_folder}/top_{c1}_by_{c2}.tarpmir.csv","w+")

    for i in range(len(mRNA_count)):
        mRNA_data = mRNA_count[i].split(",")[1:]
        miRNA_data = miRNA_count[i].split(",")[1:]
        for j in range(len(miRNA_data)):
            for c1 in number:
                for c2 in number:
                    if int(miRNA_data[j]) <= c1 and int(mRNA_data[j]) <= c2:
                        count[c1][c2] += 1
                        f_out_files[c1][c2].write(f"{gff[j]},{mRNA_count[i].split(',')[0]}\n")

    pd.DataFrame(count).to_csv(f'{O2A_folder}/top_QRP_count.tarpmir.csv')


def usage():
    print("python3 filter5.py -a <O2A_folder>")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:", ["help","O2A_folder="])
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
        elif o in ("-a", "--O2A_folder"):
            O2A_folder = a
        else:
            assert False, "Unhandled Option"
    filter5(O2A_folder)

if __name__ == "__main__":
    main()