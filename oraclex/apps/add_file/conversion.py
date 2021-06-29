from pdf2image import convert_from_path
import pytesseract


def TXTfromPDF(file):
  return TXTfromIMG(IMGfromPDF(file))

def IMGfromPDF(file):
  pages = convert_from_path(file.temporary_file_path())
  return pages

def TXTfromIMG(pages):
  text = ""
  for p in pages:
    text += pytesseract.image_to_string(p, lang='fra')
  return text