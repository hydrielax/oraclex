import csv
import cv2    
import numpy as np
import pytesseract
from statistics import mean
from pytesseract import Output
from pdf2image import convert_from_path

#### Note : we have not yet taken into account the readability criteria, we must do so, via the confidence coefficient.

#this function can identify the placement of the text, and can take as an input colored pdf too

def pdf_to_txt2(file):
    """Take as an argument the file ,
    comme sortie, elle donne le texte et deux critères de lisibilité et le texte."""
    text = ""
    L=[]
    
    good = total = 0
    pages = convert_from_path(file.read(), 350)
    for page in pages:
        image = np.array(page) 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        data = pytesseract.image_to_data(threshold_img, output_type = Output.DICT, config=custom_config, lang='fra')
        L.append(mean(list(map(float,data['conf']))))
        for word, conf in zip(data['text'], map(float, data['conf'])):
            if word: text += word + " "
            good += (conf > 75)
            total += 1
        
    return text,mean(L),good/total
            


def extract_text2(file):
    """Take as an argument the file , better quality than the usual conversion
    comme sortie, elle donne le texte et deux critères de lisibilité et le texte."""
    L=[]
    pages = convert_from_path(pdfs, 350)
    for page in pages:
        good=total=0
        image = np.array(page) 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(threshold_img, output_type = Output.DICT, config=custom_config, lang='fra')
        L.append(mean(list(map(float,details['conf']))))
        total_boxes = len(details['text'])
        for sequence_number in range(total_boxes):
            if int(float(details['conf'][sequence_number]) )>30:
                (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for word, conf in zip(details['text'], map(float, details['conf'])):
            good += (conf > 75)
            total += 1
        parse_text = []
        
        word_list = []
        
        last_word = ''
        for word in details['text']:
            if word!='':
                word_list.append(word)
                last_word = word
            if (last_word!='' and word == '') or (word==details['text'][-1]):
                parse_text.append(word_list)
                word_list = []
        with open(txt_path,  'a', newline="") as file:
                  csv.writer(file, delimiter=" ").writerows(parse_text)
            
    return mean(L),good/total


"""
# to test it we tested with many files, while showing a pregression bar and the total time
import time                
from progressbar import progressbar
start_time = time.time()

for i in progressbar(range(10)):
    pdfs = r"C:\Users\anass\Programmation\Extract info\{0}.pdf".format(i+1) 
    txt_path = r"C:\Users\anass\Programmation\Extract info\output-{}.txt".format(i+40)
    H=pdf_to_txt(pdfs,txt_path)
    print(i+1,"\n","max confidence:", max(H) , "\n","min confidence", min(H) , "\n","average confidence", mean(H) , "\n")


print("Total time : %s seconds" % (time.time() - start_time))


"""
