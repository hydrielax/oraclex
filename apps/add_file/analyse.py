from pdf2image import convert_from_bytes
import pytesseract

def extractText(file):
  text = ''
  pages = convert_from_bytes(file.read())
  for page in pages:
      text += pytesseract.image_to_string(page, lang='fra')
  return text

def findKeywords(text, keywords):
    keywords_found = set()
    for word in text.split():
        for keyword in keywords:
            if word.upper() in keyword.variantes:
                keywords_found.add(keyword)
    return keywords_found