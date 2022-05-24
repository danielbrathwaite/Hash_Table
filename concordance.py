from hash_quad import *
import string

class Concordance:

    def __init__(self):
        self.stop_table = None          # hash table for stop words
        self.concordance_table = None   # hash table for concordance

    def load_stop_table(self, filename):
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        self.stop_table=HashTable(191)

        with open(filename, 'r') as file:
            text=file.read()
        text=text.split()
        for word in text: 
            self.stop_table.insert(word, '')


    def load_concordance_table(self, filename):
        """ Read words from input text file (filename) and insert them into the concordance hash table, 
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)
        Starting size of hash table should be 191: self.concordance_table = HashTable(191)
        Process of adding new line numbers for a word (key) in the concordance:
            If word is in table, get current value (list of line numbers), append new line number, insert (key, value)
            If word is not in table, insert (key, value), where value is a Python List with the line number
        If file does not exist, raise FileNotFoundError"""
        self.concordance_table=HashTable(191)

        with open(filename) as file:
            text=file.readlines()
        for i, line in enumerate(text):
            line=[w.lower() for w in line.translate(line.maketrans('''!"#$%&()*+,-./:;<=>?@[\]^_`{|}~''', '                               ', "'")).split() if len(w)>0 and w.isalpha()] 
            
            for word in line:
                if not self.stop_table.in_table(word): 
                    val=self.concordance_table.get_index(word)
                    if val is None:
                        self.concordance_table.insert(word, [i+1])
                    elif i+1!=self.concordance_table.hash_table[val][1][-1]:
                        self.concordance_table.hash_table[val][1].append(i+1)


            

    def write_concordance(self, filename):
        """ Write the concordance entries to the output file(filename)
        See sample output files for format."""

        wlist=sorted(self.concordance_table.get_all_keys())
        wstr=''.join([key+': '+" ".join([str(num) for num in self.concordance_table.get_value(key)])+'\n' for key in wlist])
        with open(filename, 'w+') as file:
            file.write(wstr[:-1])

'''
for s in ['file1.txt', 'file2.txt', 'declaration.txt', 'War_And_Peace.txt']:
    f1=s
    f2='what.txt'
    conc=Concordance()
    conc.load_stop_table('stop_words.txt')
    conc.load_concordance_table(f1)
    conc.write_concordance(f2)

    with open(f1.removesuffix('.txt')+'_sol.txt', 'r') as read1:
        with open(f2, 'r') as read2:
            l1=read1.readlines()
            l2=read2.readlines()

            print(len(l1)==len(l2))

            for i in range(max(len(l2), len(l1))):
                if not l1[i]==l2[i]:
                    print('Error diff | line #: '+str(i))
'''
