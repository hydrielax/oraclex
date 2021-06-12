from Bio import pairwise2

def ressemblance(filename1, filename2):
# Donne le % de ressemblance entre deux fichiers
    file1 = open(filename1, 'r')
    file2 = open(filename2, 'r')

    txt1 = ''
    txt2 = ''

    for line in file1:
        txt1 += line
    for line in file2:
        txt2 += line

    file1.close()
    file2.close()

    alignment = pairwise2.align.globalxx(txt1, txt2)

    return alignment[0][2]/max(len(txt1), len(txt2))*100
