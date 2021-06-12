import os

def fusionFiles(fname1, fname2):

    # Defining directories
    Python_dirname = './TXT_UTF'
    f1 = os.path.basename(fname1.name)
    f2 = os.path.basename(fname2.name)
    outName = f1[0:f1.find('.txt')] + f2[f2.find('_page_'):]

    finalName = os.path.join(Python_dirname, outName)

    f = open(finalName, 'w', encoding="utf8")

    with f as outfile:
        for line in fname1:
            outfile.write(line)
        for line in fname2:
            outfile.write(line)