from pdf2image import convert_from_bytes
from pytesseract import image_to_string
import re

def extractText(file):
  text = ''
  pages = convert_from_bytes(file.read())
  for page in pages:
      text += image_to_string(page, lang='fra')
  return text

def findKeywords1(text, keywords):
    keywords_found = set()
    for keyword in keywords:
        for word in keyword.variantes.values_list('name'):
            if word in text:
                keywords_found.add(keyword)
    return keywords_found



def findKeywords(text, keywords):
    keywords_found = set()
    #keywords=set(keywords)
    for MotCle in keyword.variantes.values_list('name'):
        mot= "\W"+MotCle+"\W"
        found=re.search(mot, text, re.IGNORECASE)
        if found :
                keywords_found.add(MotCle)
    return keywords_found