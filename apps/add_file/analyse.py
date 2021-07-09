from pdf2image import convert_from_bytes
from pytesseract import image_to_data
import re


def extract_text(file):
    text = ""
    good = total = 0
    for page in convert_from_bytes(file.read()):
        data = image_to_data(page, lang='fra', output_type='dict')
        for word, conf in zip(data['text'], map(float, data['conf'])):
            text += word + " "
            good += (conf > 75)
            total += 1
    return text, good / total


def find_keywords(text, keywords):
    keywords_found = set()
    for keyword in keywords:
        for word in keyword.variantes.values_list('name'):
            if re.search("\W" + word[0] + "\W", text, re.IGNORECASE):
                keywords_found.add(keyword)
    return keywords_found
