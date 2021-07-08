from pdf2image import convert_from_bytes
from pytesseract import image_to_string

def extractText(file):
  text = ''
  pages = convert_from_bytes(file.read())
  for page in pages:
      text += image_to_string(page, lang='fra')
  return text

def findKeywords(text, keywords):
    keywords_found = set()
    for keyword in keywords:
        for word in keyword.variantes.values_list('name'):
            if word in text:
                keywords_found.add(keyword)
    return keywords_found