class Cluster:
    def __init__(self, name, representative, sequence_names=None, sequences=None, ncRNA=False):
        self.name = name
        self.representative = representative
        self.sequence_names = sequence_names
        self.sequences = sequences
        self.ncRNA = ncRNA

    def find_specific_species(self, species):
        if not self.sequences:
            print("This function is not applicable")
            return None
        if species == '':
            print("Species empty")
            exit()
        species_list = []
        for miRNA in self.sequences:
            if miRNA.species == species:
                species_list.append(miRNA)
        if not species_list:
            #print("The species specified is not in the cluster")
            return None
        species_list.sort(key=lambda x: x.score, reverse=True)
        return species_list[0]


class MiRNA:
    def __init__(self, name, sequence, species):
        self.name = name
        self.sequence = sequence
        self.species = species


class ScoredMiRNA(MiRNA):
    def __init__(self, name, sequence, species, score):
        super().__init__(name, sequence, species)
        self.score = score


class FastaOperations:
    def __init__(self, file_path):
        fasta_file = open(file_path, 'r')
        self.lines = fasta_file.readlines()
        fasta_file.close()
        self.__set_sequence_dict__()

    def __set_sequence_dict__(self):
        self.sequence_dict = {}
        sequence = ''
        name = ''
        for line in self.lines:
            if '>' in line:
                if sequence != '':
                    self.sequence_dict[name] = sequence
                name = line[1:-1]
                sequence = ''
            else:
                sequence = sequence + line[:-1]
        if sequence != '':
            self.sequence_dict[name] = sequence

    def get_sequence_dict(self):
        return self.sequence_dict.copy()


class ClusOperations:
    def __init__(self, file_path, fasta_file=None, species_dict=None):
        clus_file = open(file_path, 'r')
        self.lines = clus_file.readlines()
        clus_file.close()
        if fasta_file and species_dict:
            fasta = FastaOperations(fasta_file)
            self.miRNA_seq_dict = fasta.get_sequence_dict()
            self.clusters = []
            self.__set_clusters__(species_dict)
        else:
            self.miRNA_seq_dict = None
            self.clusters = []
            self.__set_clusters__()

    def __set_clusters__(self, species_dict=None):
        name = ''
        representative = None
        sequences = None
        sequence_names = None
        ncRNA = False
        for line in self.lines:
            if 'Cluster' in line:
                if name != '' and representative and (sequences or sequence_names):
                    self.clusters.append(Cluster(name, representative, sequences=sequences,
                                                 sequence_names=sequence_names, ncRNA=ncRNA))
                    ncRNA=False
                name = line[:-1]
                representative = None
                sequences = None
                sequence_names = None
            else:
                if "trna" in line.lower() or "rrna" in line.lower():
                    ncRNA=True
                parts = line.split('\t')
                parts = parts[1].split(' ')
                species = None
                if self.miRNA_seq_dict:
                    for spec in species_dict:
                        if species_dict[spec] in line:
                            species = spec
                            break
                    if '*' in line:
                        representative = ScoredMiRNA(parts[1][1:-3], self.miRNA_seq_dict[parts[1][1:-3]], species, 100)
                        if not sequences:
                            sequences = [ScoredMiRNA(parts[1][1:-3], self.miRNA_seq_dict[parts[1][1:-3]], species, 100)]
                        else:
                            sequences.append(ScoredMiRNA(parts[1][:-3], self.miRNA_seq_dict[parts[1][1:-3]]
                                                         , species, 100))
                    else:
                        if not sequences:
                            sequences = [ScoredMiRNA(parts[1][1:-3], self.miRNA_seq_dict[parts[1][1:-3]], species,
                                                     float(parts[3][:-2]))]
                        else:
                            sequences.append(ScoredMiRNA(parts[1][1:-3], self.miRNA_seq_dict[parts[1][1:-3]], species,
                                                         float(parts[3][:-2])))
                else:
                    if '*' in line:
                        representative = parts[1][1:-3]
                    if not sequence_names:
                            sequence_names = [parts[1][1:-3]]
                    else:
                        sequence_names.append(parts[1][1:-3])
        if name != '' and representative and (sequences or sequence_names):
            self.clusters.append(Cluster(name, representative, sequences=sequences,
                                         sequence_names=sequence_names, ncRNA=ncRNA))
        ncRNA=False
    def get_clusters(self):
        return self.clusters.copy()



