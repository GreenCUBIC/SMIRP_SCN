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