try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import os, shutil, glob
from wand.image import Image as getToImg

def savingPages(pages, directory):
    i = 1
    for img in pages.sequence:
        single_page = getToImg(image=img)
        # Below we define the img file name as ./IMG/fileName_page_x.jpg
        single_page_name = os.path.join(directory, fileName[0:fileName.find(".pdf")] + '_page_' + str(i) + '.jpg')
        single_page.save(filename=single_page_name)
        i += 1

def writeDownTextFile(img):
    # Verifying if the file is really a good file
    if os.path.isfile(img):
        # Getting the name of the image
        imgBaseName = os.path.basename(img)

        # Variable that holds the text of the image
        ImgConvertedToTXT = pytesseract.image_to_string(Image.open(os.path.join(dst, imgBaseName)), lang='fra')
        # Writing text file name as ./TXT/fileName_page_x.txt
        txtFileName = os.path.join(txtDst, imgBaseName[0:imgBaseName.find(".jpg")] + '.txt')

        # Opening file
        f = open(txtFileName, "w+")

        for s in ImgConvertedToTXT:
            # We try to write down the character. If it is not possible, we write an space instead
            try:
                f.write(s)
            except:
                f.write(" ")
        # Closing file -> then end of page
        f.close()

def isConverted(textDirectory, currentfileName):
    filesConvertedIntoText = glob.iglob(os.path.join(textDirectory, "*.txt"))

    isNotYetConverted = True

    # This down loop is to able file convertion only if it's not been converted yet
    previous_Converted_FileName = ''

    for fileConverted in filesConvertedIntoText:
        fileConverted_name_with_Extension = os.path.basename(fileConverted)
        fileConverted_name_without_Extension = fileConverted_name_with_Extension[0 : fileConverted_name_with_Extension.find('_page_')]

        # This 'if' go on files of the directory and it jumps files with
        # same prefix (it ignores the _page_X part)
        if( fileConverted_name_without_Extension == previous_Converted_FileName):
            continue

        # If we find file converted already
        if (fileName[0:fileName.find(".pdf")] == fileConverted_name_without_Extension):
            isNotYetConverted = False
            break

        # We update the previousFile analysed
        previous_Converted_FileName = fileConverted_name_without_Extension

    return isNotYetConverted

# Defining directories
Python_dirname = os.path.dirname(__file__)

source_dir = os.path.join(Python_dirname, 'PDF')
dst = os.path.join(Python_dirname, 'IMG')
txtDst = os.path.join(Python_dirname, 'TXT')

files = glob.iglob(os.path.join(source_dir, "*.pdf"))

for file in files:
    fileName = os.path.basename(file)

    isNotYetConverted = isConverted(txtDst, fileName)

    if(isNotYetConverted):
        pdfAddress = os.path.join(source_dir, fileName)

        try:
            pages = getToImg(filename=pdfAddress, resolution=300)
        except:
            continue

        # Getting sequence of images (file's pages) and saving them
        savingPages(pages, dst)

        filesImages = glob.iglob(os.path.join(dst, "*.jpg"))

        for img in filesImages:
            writeDownTextFile(img)

