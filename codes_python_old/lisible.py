# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:32:25 2021

@author: anass
"""



try:
    from PIL import Image
except ImportError:
    import Image

import re

import cv2 
import pytesseract
from pytesseract import Output

from pdf2image import convert_from_path

from statistics import mean


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def pdf_to_txt(pdfs,txt_path):
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    pages = convert_from_path(pdfs, 350)
    i = 1
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg" 
        img = cv2.imread(image_name)
        #page.save(image_name, "JPEG")
        i = i+1
        f = open(txt_path, "a")
        f.write(pytesseract.image_to_string(img, config=custom_config, lang='fra'))
        #f.write(pytesseract.image_to_string(Image.open(image_name), lang='fra'))
        print(mean(list(map(float, pytesseract.image_to_data(Image.open(image_name), output_type = Output.DICT, config=custom_config, lang='fra')['conf']))))
        f.close()

   

pdfs = r"C:\Users\anass\Programmation\Extract info\input.pdf"  
txt_path = r"C:\Users\anass\Programmation\Extract info\output2.txt"
pdf_to_txt(pdfs,txt_path)
        
myfile = txt_path

f = open(myfile,"r") 




def reader(s):
    L=[]
    f = open(s,'r', encoding="utf8")
    for line in f:
        if line != '\n' :
            newline=line
            if '\n' in newline :
                newline=newline.replace('\n','')
            L.append(newline)
    return L

s='MotsCles.txt' 
      
MotsCles= reader(s)

def search(txt_path,MotsCles):
    #re.split('; |, |\*|\n',L) possible
    """L=[]
    f = open(txt_path,"r") 
    texte = f.read().replace("\n", " ")
    texte = re.split('; |, |\*|\n',texte)
    MotsCles = set(MotsCles)
    for mot in texte :
        print(mot, '\n')
        if mot in MotsCles:
            L.append(mot)
    return L"""
    L=set()
    for mot in MotsCles:
        with open(txt_path, 'r') as inF:
            for line in inF:
                if mot in line.upper():
                    L.add(mot)
                
    return L


L=search(myfile,MotsCles)
print(L)



################################################################################################
# -*- coding: utf-8 -*- Mieux
"""
Created on Wed Jul  7 11:36:40 2021

@author: anass
"""
import csv
import cv2    
import pytesseract
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pytesseract import Output
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def pdf_to_txt(pdfs,txt_path):
    "https://www.opcito.com/blogs/extracting-text-from-images-with-tesseract-ocr-opencv-and-python"
    
    pages = convert_from_path(pdfs, 350)
    i = 1
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg" 
        image = cv2.imread(image_name)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #cv2.imshow('threshold image', threshold_img)
        #imgplot = plt.imshow(gray_image)
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(threshold_img, output_type = Output.DICT, config=custom_config)
        total_boxes = len(details['text'])
        for sequence_number in range(total_boxes):
            if int(float(details['conf'][sequence_number]) )>30:
                (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                     
        #imgplot = plt.imshow(threshold_img)
        #plt.show()
        
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
        with open(txt_path,  'w', newline="") as file:
                  csv.writer(file, delimiter=" ").writerows(parse_text)


#########################################################
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:32:25 2021

@author: anass
"""



try:
    from PIL import Image
except ImportError:
    import Image

import re

import cv2 
import pytesseract
from pytesseract import Output

from pdf2image import convert_from_path

from statistics import mean


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def pdf_to_txt(pdfs,txt_path):
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    pages = convert_from_path(pdfs, 350)
    i = 1
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg" 
        img = cv2.imread(image_name)
        #page.save(image_name, "JPEG")
        i = i+1
        f = open(txt_path, "a")
        f.write(pytesseract.image_to_string(img, config=custom_config, lang='fra'))
        #f.write(pytesseract.image_to_string(Image.open(image_name), lang='fra'))
        print(mean(list(map(float, pytesseract.image_to_data(Image.open(image_name), output_type = Output.DICT, config=custom_config, lang='fra')['conf']))))
        f.close()

   

pdfs = r"C:\Users\anass\Programmation\Extract info\input.pdf"  
txt_path = r"C:\Users\anass\Programmation\Extract info\output2.txt"
pdf_to_txt(pdfs,txt_path)
        
myfile = txt_path

f = open(myfile,"r") 




def reader(s):
    L=[]
    f = open(s,'r', encoding="utf8")
    for line in f:
        if line != '\n' :
            newline=line
            if '\n' in newline :
                newline=newline.replace('\n','')
            L.append(newline)
    return L

s='MotsCles.txt' 
      
MotsCles= reader(s)

def search(txt_path,MotsCles):
    #re.split('; |, |\*|\n',L) possible
    """L=[]
    f = open(txt_path,"r") 
    texte = f.read().replace("\n", " ")
    texte = re.split('; |, |\*|\n',texte)
    MotsCles = set(MotsCles)
    for mot in texte :
        print(mot, '\n')
        if mot in MotsCles:
            L.append(mot)
    return L"""
    L=set()
    for mot in MotsCles:
        with open(txt_path, 'r') as inF:
            for line in inF:
                if mot in line.upper():
                    L.add(mot)
                
    return list(L)


L=search(myfile,MotsCles)
print(L)