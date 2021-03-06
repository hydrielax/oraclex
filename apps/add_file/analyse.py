from apps.search.models import MotCle
from apps.search.models import Jugement, Juridiction
from unidecode import unidecode
from pdf2image import convert_from_bytes
from pytesseract import image_to_data
from datetime import datetime
from dateparser.search import search_dates
from dateparser_data.settings import default_parsers
import re
import fitz
from difflib import SequenceMatcher


sep = r"(?:^|\W|\_|$)+"  # Regular expression for separator


def analyse(jugement):
    try:
        print('Started analysing', jugement.name)
        jugement.text, jugement.quality = extract_text(jugement.file.file)
        jugement.date_jugement = extract_date(jugement.name, jugement.text)
        jugement.decision = extraction_jugement(jugement.name, jugement.text)
        jugement.gain = extraction_somme(jugement.text)
        jugement.juridiction = find_juridiction(jugement, Juridiction.objects.all())
        jugement.mots_cles.set(find_keywords(jugement.text, MotCle.objects.all()))
        jugement.lisible = jugement.quality > 0.6 and jugement.date_jugement is not None and jugement.juridiction is not None
        jugement.doublon = detect_doublon(jugement.text)
        if jugement.doublon: jugement.save()
        else: jugement.register()
        print('Ended analysing', jugement.name)
    except BaseException as exc:
        print('Error analysing', jugement.name, ':', exc)
        jugement.delete()


def extract_text_ocr(file):
    text = ""
    good = total = 0
    for page in convert_from_bytes(file.read()):
        data = image_to_data(page, lang='fra', config=r'--oem 3 --psm 6', output_type='dict')
        for word, conf in zip(data['text'], map(float, data['conf'])):
            if word: text += word + " "
            good += (conf > 75)
            total += 1
    return text, good / total


def get_text_percentage(file):
    """
    If the returned percentage of text is very low, the document is a scanned PDF
    """
    total_page_area = 0.0
    total_text_area = 0.0

    doc = fitz.open(file)

    for page_num, page in enumerate(doc):
        total_page_area += abs(page.rect)
        for b in page.getTextBlocks():
            if b[6] == 0:
                r = fitz.Rect(b[:4])  # rectangle where block text appears
                total_text_area += abs(r)
    return total_text_area / total_page_area 

def extract_text(file, limit_perc=0.2):
    text_perc = get_text_percentage(file)
    if text_perc < limit_perc:
        return extract_text_ocr(file)
    else:
        return extract_from_pdf(file), 0.99

def extract_from_pdf(file):
    text = ""
    doc = fitz.open(file)
    for page in doc:
        text += page.getText()
    return text


def simplify(text):
    text = unidecode(text)
    text = re.sub(r'(\W|\_)', ' ', text)
    return text


def find_keywords(text, keywords):
    keywords_found = set()
    for keyword in keywords:
        for word in keyword.variantes.values_list('name', flat=True):
            if re.search(sep+simplify(word)+sep, simplify(text), re.IGNORECASE):
                keywords_found.add(keyword)
    return keywords_found


def find_juridiction(jugement, juridictions):
    juridiction_name = find_juridiction_name(jugement.name, juridictions)
    if juridiction_name:
        return juridiction_name
    else:
        return find_juridiction_text(jugement.text, juridictions)

def find_juridiction_name(filename, juridictions):
    for juridiction in juridictions:
        regex = juridiction.type_juridiction.regex
        if (juridiction.type_juridiction.cle != 'CC'):
            regex += sep + simplify(juridiction.ville)
        if re.search(regex, simplify(filename), re.IGNORECASE):
            return juridiction

def find_juridiction_text(text, juridictions):
    for juridiction in juridictions:
        if juridiction.type_juridiction.cle != 'CC':
            if re.search(simplify(juridiction.nom), simplify(text), re.IGNORECASE):
                return juridiction


def detect_doublon(text):
    "detection de doublons avec SequenceMatcher"
    for jugement in Jugement.objects.all():
        if SequenceMatcher(None, text, jugement.text).ratio() > 0.85:
            return jugement


def extract_date(filename,text):

    normal_date_regex = re.search(sep+r"(?:(\d{2}) )?(\d{2}) (\d{4})"+sep, simplify(filename))
    if normal_date_regex:
        date_fields = normal_date_regex.groups()
        day = int(date_fields[0]) if date_fields[0] else 1
        month = int(date_fields[1])
        year = int(date_fields[2])
        date_name = datetime(year, month, day)
    if not normal_date_regex or date_name.year < 1900 or date_name > datetime.now():
        inverse_date_regex = re.search(sep+r"(\d{4}|\d{2})(?: (\d{2}))?(?: (\d{2}))?"+sep, simplify(filename))
        if inverse_date_regex:
            date_fields = inverse_date_regex.groups()
            year = int('20' + date_fields[0]) if len(date_fields[0]) == 2 else int(date_fields[0])
            month = int(date_fields[1]) if date_fields[1] else 1
            day = int(date_fields[2]) if date_fields[2] else 1
            date_name = datetime(year, month, day)
        if not inverse_date_regex or date_name.year < 1900 or date_name > datetime.now():
            date_name = None

    parsers = [parser for parser in default_parsers if parser != 'relative-time']
    dates_text = search_dates(text, settings={'STRICT_PARSING': True, 'DATE_ORDER': 'DMY', 'PARSERS': parsers})
    for date_text in dates_text:
        if date_name:
            def same(attr): return getattr(date_name, attr) == getattr(date_text[1], attr)
            if same('year') and (not date_fields[1] or same('month')) and (not date_fields[2] or same('day')):
                return date_text[1]
        elif date_text[1].year > 1900 and date_text[1] < datetime.now():
            return date_text[1]
    return date_name if date_name else None


def extraction_jugement(filename,text):
    fav = re.search(sep+r'([FDM])'+sep, simplify(filename))
    if fav:
        return fav.groups()[0]
    return extraction_jugement2(text)

noms_sncf = ["??tablissement SNCF",'EPIC','epic','E.P.I.C','e.p.i.c','E.P.I.C.','e.p.i.c.','SNCF','S.N.C.F','S.N.C.F.','sncf','s.n.c.f','Soci??t?? Nationale des Chemins de Fer Fran??ais','Soci??t?? Nationale des Chemins de Fer Francais','soci??t?? nationale des chemins de fer fran??ais','soci??t?? nationale des chemins de fer francais','SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','MOBILITES','MOBILIT??S','RESEAU','R??SEAU','groupe','EPIC Soci??t?? Nationale des Chemins de Fer Fran??ais','EPIC Soci??t?? Nationale des Chemins de Fer Francais','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','EPIC MOBILITES','EPIC MOBILIT??S','EPIC RESEAU','EPIC R??SEAU','EPIC GROUPE','E.P.I.C Soci??t?? Nationale des Chemins de Fer Fran??ais','E.P.I.C Soci??t?? Nationale des Chemins de Fer Francais','E.P.I.C Soci??t?? Nationale des Chemins de Fer Francais','E.P.I.C soci??t?? nationale des chemins de fer fran??ais','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRANcAIS','E.P.I.C MOBILITES','E.P.I.C MOBILIT??S','E.P.I.C RESEAU','E.P.I.C RESEAU','E.P.I.C Groupe','e.p.i.c Soci??t?? Nationale des Chemins de Fer Fran??ais','e.p.i.c Soci??t?? Nationale des Chemins de Fer Francais','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c MOBILITES','e.p.i.c MOBILIT??S','e.p.i.c Mobilit??s','e.p.i.c mobilit??s','e.p.i.c mobilites','e.p.i.c Mobilites','e.p.i.c RESEAU','e.p.i.c R??SEAU','e.p.i.c r??seau','e.p.i.c r??seau','e.p.i.c reseau','e.p.i.c R??seau','e.p.i.c Reseau','e.p.i.c Groupe','e.p.i.c GROUPE', 'E.P.I.C. Soci??t?? Nationale des Chemins de Fer Fran??ais','E.P.I.C. Soci??t?? Nationale des Chemins de Fer Francais','E.P.I.C. soci??t?? nationale des chemins de fer fran??ais','E.P.I.C. soci??t?? nationale des chemins de fer francais','E.P.I.C. SOCI??T?? NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. SOCI??T?? NATIONALE DES CHEMINS DE FER FRAN??AIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. MOBILITES','E.P.I.C. MOBILIT??S','E.P.I.C. Mobilit??s','E.P.I.C. mobilit??s','E.P.I.C. mobilites','E.P.I.C. Mobilites','E.P.I.C. RESEAU','E.P.I.C. R??SEAU','E.P.I.C. r??seau','E.P.I.C. reseau','E.P.I.C. R??seau','E.P.I.C. Reseau','E.P.I.C. Groupe','E.P.I.C. GROUPE','e.p.i.c. Soci??t?? Nationale des Chemins de Fer Fran??ais','e.p.i.c. Soci??t?? Nationale des Chemins de Fer Francais','e.p.i.c. soci??t?? nationale des chemins de fer fran??ais','e.p.i.c. soci??t?? nationale des chemins de fer francais','e.p.i.c. SOCI??T?? NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. SOCI??T?? NATIONALE DES CHEMINS DE FER FRAN??AIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRAN??AIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. MOBILITES','e.p.i.c. MOBILIT??S','e.p.i.c. Mobilit??s','e.p.i.c. mobilit??s','e.p.i.c. mobilites','e.p.i.c. Mobilites','e.p.i.c. RESEAU','e.p.i.c. R??SEAU','e.p.i.c. r??seau','e.p.i.c. reseau','e.p.i.c. R??seau','e.p.i.c. Reseau','e.p.i.c. Groupe', 'e.p.i.c. GROUPE','SNCF MOBILITES','SNCF MOBILIT??S','SNCF Mobilit??s','SNCF mobilit??s','SNCF mobilites','SNCF Mobilites','SNCF RESEAU','SNCF R??SEAU','SNCF r??seau','SNCF reseau','SNCF R??seau','SNCF Reseau','SNCF Groupe','SNCF GROUPE','S.N.C.F MOBILITES','S.N.C.F MOBILIT??S','S.N.C.F Mobilit??s','S.N.C.F mobilit??s','S.N.C.F mobilites','S.N.C.F Mobilites','S.N.C.F RESEAU','S.N.C.F R??SEAU','S.N.C.F r??seau','S.N.C.F reseau','S.N.C.F R??seau','S.N.C.F Reseau','S.N.C.F Groupe', 'S.N.C.F GROUPE', 'S.N.C.F. MOBILITES','S.N.C.F. MOBILIT??S','S.N.C.F. Mobilit??s','S.N.C.F. mobilit??s','S.N.C.F. mobilites','S.N.C.F. Mobilites','S.N.C.F. RESEAU','S.N.C.F. R??SEAU','S.N.C.F. r??seau','S.N.C.F. reseau','S.N.C.F. R??seau','S.N.C.F. Reseau','S.N.C.F. Groupe','S.N.C.F. GROUPE','sncf MOBILITES','sncf MOBILIT??S','sncf Mobilit??s','sncf mobilit??s','sncf mobilites','sncf Mobilites','sncf RESEAU','sncf R??SEAU','sncf r??seau','sncf reseau','sncf R??seau','sncf Reseau','sncf Groupe','sncf GROUPE','s.n.c.f. MOBILITES','s.n.c.f. MOBILIT??S','s.n.c.f. Mobilit??s','s.n.c.f. mobilit??s','s.n.c.f. mobilites','s.n.c.f. Mobilites','s.n.c.f. RESEAU','s.n.c.f. R??SEAU','s.n.c.f. r??seau','s.n.c.f. reseau','s.n.c.f. R??seau','s.n.c.f. Reseau','s.n.c.f. Groupe','s.n.c.f. GROUPE','Soci??t?? Nationale des Chemins de Fer Fran??ais MOBILITES','Soci??t?? Nationale des Chemins de Fer Fran??ais MOBILIT??S','Soci??t?? Nationale des Chemins de Fer Fran??ais Mobilit??s','Soci??t?? Nationale des Chemins de Fer Fran??ais mobilit??s','Soci??t?? Nationale des Chemins de Fer Fran??ais mobilites','Soci??t?? Nationale des Chemins de Fer Fran??ais Mobilites','Soci??t?? Nationale des Chemins de Fer Fran??ais RESEAU','Soci??t?? Nationale des Chemins de Fer Fran??ais R??SEAU','Soci??t?? Nationale des Chemins de Fer Fran??ais r??seau','Soci??t?? Nationale des Chemins de Fer Fran??ais reseau','Soci??t?? Nationale des Chemins de Fer Fran??ais R??seau','Soci??t?? Nationale des Chemins de Fer Fran??ais Reseau','Soci??t?? Nationale des Chemins de Fer Fran??ais Groupe','Soci??t?? Nationale des Chemins de Fer Fran??ais GROUPE','Soci??t?? Nationale des Chemins de Fer Francais MOBILITES','Soci??t?? Nationale des Chemins de Fer Francais MOBILIT??S','Soci??t?? Nationale des Chemins de Fer Francais Mobilit??s','Soci??t?? Nationale des Chemins de Fer Francais mobilit??s','Soci??t?? Nationale des Chemins de Fer Francais mobilites','Soci??t?? Nationale des Chemins de Fer Francais Mobilites','Soci??t?? Nationale des Chemins de Fer Francais RESEAU','Soci??t?? Nationale des Chemins de Fer Francais R??SEAU','Soci??t?? Nationale des Chemins de Fer Francais r??seau','Soci??t?? Nationale des Chemins de Fer Francais reseau','Soci??t?? Nationale des Chemins de Fer Francais R??seau','Soci??t?? Nationale des Chemins de Fer Francais Reseau','Soci??t?? Nationale des Chemins de Fer Francais Groupe','Soci??t?? Nationale des Chemins de Fer Francais GROUPE','soci??t?? nationale des chemins de fer fran??ais MOBILITES','soci??t?? nationale des chemins de fer fran??ais MOBILIT??S','soci??t?? nationale des chemins de fer fran??ais Mobilit??s','soci??t?? nationale des chemins de fer fran??ais mobilit??s','soci??t?? nationale des chemins de fer fran??ais mobilites','soci??t?? nationale des chemins de fer fran??ais Mobilites','soci??t?? nationale des chemins de fer fran??ais RESEAU','soci??t?? nationale des chemins de fer fran??ais R??SEAU','soci??t?? nationale des chemins de fer fran??ais r??seau','soci??t?? nationale des chemins de fer fran??ais reseau','soci??t?? nationale des chemins de fer fran??ais R??seau','soci??t?? nationale des chemins de fer fran??ais Reseau','soci??t?? nationale des chemins de fer fran??ais Groupe','soci??t?? nationale des chemins de fer fran??ais GROUPE','soci??t?? nationale des chemins de fer francais MOBILITES','soci??t?? nationale des chemins de fer francais MOBILIT??S','soci??t?? nationale des chemins de fer francais Mobilit??s','soci??t?? nationale des chemins de fer francais mobilit??s','soci??t?? nationale des chemins de fer francais mobilites','soci??t?? nationale des chemins de fer francais Mobilites','soci??t?? nationale des chemins de fer francais RESEAU','soci??t?? nationale des chemins de fer francais R??SEAU','soci??t?? nationale des chemins de fer francais r??seau','soci??t?? nationale des chemins de fer francais reseau','soci??t?? nationale des chemins de fer francais R??seau','soci??t?? nationale des chemins de fer francais Reseau','soci??t?? nationale des chemins de fer francais Groupe','soci??t?? nationale des chemins de fer francais GROUPE','Groupe  EPIC','Groupe  epic','Groupe  E.P.I.C','Groupe  e.p.i.c','Groupe  E.P.I.C.','Groupe  e.p.i.c.','Groupe  SNCF','Groupe  S.N.C.F','Groupe  S.N.C.F.','Groupe  sncf','Groupe  s.n.c.f.','Groupe  Soci??t?? Nationale des Chemins de Fer Fran??ais','Groupe  Soci??t?? Nationale des Chemins de Fer Francais','Groupe  soci??t?? nationale des chemins de fer fran??ais','Groupe  soci??t?? nationale des chemins de fer francais','GROUPE  MOBILITES','GROUPE  MOBILIT??S','GROUPE  Mobilit??s','GROUPE  mobilit??s','GROUPE  mobilites','GROUPE  Mobilites','GROUPE  RESEAU','GROUPE  R??SEAU','GROUPE  r??seau','GROUPE  reseau','GROUPE  R??seau','GROUPE  Reseau']

def extraction_jugement2(txt):
    """Cette fonction extrait le jugement du fichier s'il n'a pas ??t?? extrait du nom du fichier,
     avec une pr??cision de 81.73%"""
    limite = re.compile("([EP][a??]r"+sep+"ces"+sep+"m[o????]t[fi][fe]s)",re.IGNORECASE)
    possibilite_de_rechreche = re.search(limite,txt)
    if (possibilite_de_rechreche == None) :#si "Par ces motifs" n'est pas trouv??e
        return None
    else :
        i = possibilite_de_rechreche.end()
        s=1
        condamnations = re.finditer("condamne"+sep,txt[i:], re.IGNORECASE)
        for m in [k for k in condamnations]:
            rang=m.end()+i
            words = re.compile("\w+\W+\w+\W+\w+\W",re.IGNORECASE)
            words_found = re.search(words,txt[rang:])
            civil_re = re.compile('(M\.|Mme|Madame|Mlle|Monsieur|Mr|CFDT|CGT|SYNDICAT)',re.IGNORECASE)
            civil = re.search(civil_re, words_found.group())
            if civil:
                s+=3
            for pseudo in noms_sncf:
                pseudo_re=''
                for car in pseudo:
                    if car in [' ',',','-','_']:
                        pseudo_re += '[ ,-_]'
                    elif car == "'":
                        pseudo_re += '.'
                    elif car in ['e','??','??','??','??']:
                        pseudo_re+='[e????????]'
                    else :
                        pseudo_re += car
                ts = re.compile('('+pseudo_re+')',re.IGNORECASE)
                sncf = re.search(ts,words_found.group())
                if sncf:
                    s-=5
                    break
 
        deboutements = re.finditer("d[e????????]bout[ce????????]"+sep,txt[i:], re.IGNORECASE)
        for m in [k2 for k2 in deboutements]:
            rang=m.end()+i
            words = re.compile("\w+\W+\w+\W+\w+\W",re.IGNORECASE)
            words_found = re.search(words,txt[rang:])
            civil_re = re.compile('(M\.|Mme|Madame|Mlle|Monsieur|Mr|CFDT|CGT|SYNDICAT )',re.IGNORECASE)
            civil = re.search(civil_re, words_found.group())
            if civil:
                s+=1
            for pseudo in noms_sncf:
                pseudo_re=''
                for car in pseudo:
                    if car in [' ',',','-','_']:
                        pseudo_re += '[ ,-_]'
                    elif car == "'":
                        pseudo_re += '.'
                    elif car in ['e','??','??','??','??']:
                        pseudo_re+='[e????????]'
                    else :
                        pseudo_re += car
                ts = re.compile('('+pseudo_re+')',re.IGNORECASE)
                sncf = re.search(ts,words_found.group())
                if sncf:
                    s-=1
                    break
        if s>0:
            return 'F'
        elif s== 0 : 
            return 'M'
        else : 
            return 'D'    

########################################################################################################################
    ##### #   #  #####  ####      #    #### ##### #  ###  #   #     #####  #####      ####  ###  #   # #   # #####
    #     #   #   #    #   #    #   # #       #   # #   # ##  #      #  #  #         #     #   # ## ## ## ## #
    ####    #     #    #####    ##### #       #   # #   # # # #      #  #  ####        #   #   # # # # # # # ####
    #     #   #   #    #    #   #   # #       #   # #   # #  ##      #  #  #            #  #   # #   # #   # #
    ##### #   #   #    #     #  #   #  ####   #   #  ###  #   #     ###    #####      ####  ###  #   # #   # #####
########################################################################################################################


chiffres = [str(k) for k in range(10)]

def compter_chiffres(somme_re):
    c = 0
    for car in somme_re.group():
        if car in chiffres:
            c+=1
    return c


def conv_euros_re(somme_re):#fonctionnel
    if somme_re.group()[0] not in chiffres:#cas ou la chaine commence par un espace
        somme2= somme_re.group()[1:]
    else:
        somme2 = somme_re.group()
    res = 0
    c1 = compter_chiffres(somme_re) #nombre de chiffres dans la chaine de caracteres
    c2 = 0 #compteur pour les caract??res non chiffres
    for k in range(len(somme2)):
        if somme2[k] in chiffres:
            res += int(somme2[k])*(10**(c1 +c2 - k-1))
        else:
            c2+=1
    if len(somme2) >2:
        centimes = re.search('\D[0-9][0-9]\D',somme2)
        if centimes == None:
            centimes = re.search('\D[0-9][0-9]',somme2)
            if centimes !=None:
                if centimes.end() == len(somme2):
                    res = res*(10**(-2))

        else:
            res = res*(10**(-2))

    return res


def verif_somme(recherche_somme):#renvoie True si somme_re est effectivement une somme, False sinon
    if recherche_somme == None:
        return False

    verif = True
    euros = '((euros)|[???????])'
    somme_c = recherche_somme.group()
    search = re.search(euros,somme_c)
    if search == None:
        verif = False
    return verif


def extraction_somme(contenu):
    
    limite = "([EP][a??]r\W+ces\W+m[o????]t[fi][fe]s)"
    somme = 0 #somme perdue par la sncf
    somme_re = '[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{1,3}[\., ]?((euros)|[\.,])?[0-9]{0,2} ?((euros)|[???????])?'#somme en re
    q = re.compile(limite,re.IGNORECASE)
    qs = re.search(q,contenu)
    dernier_condamne = 0#permet d'avoir le veritable rang du condamne

    if (qs == None) :#si 'Par ces motifs' est mal ??crit, le fichier est consid??r?? comme endommag?? + critere de lisibilit??
        return None
    else:
        i = qs.end()# mm probleme que rang_somme
        r = re.compile("(condamn[ ]?[e????????????????])",re.IGNORECASE)
        rs = re.search(r,contenu[i:])#On recherche ??  partir de "Par ces motifs" pour ??viter les autres chiffres
        if rs != None:
            dernier_condamne = rs.end() +i#rang du dernier condamne
            rang_somme = rs.end()+ i
            ss = re.search(r,contenu[i+rs.end():])#on recherche jusqu'?? une ??ventuelle autre condamnation pour n'inclure que des chiffres
            while ss != None:

                recherche_somme = re.search(somme_re,contenu[dernier_condamne:ss.end()+dernier_condamne])
                while recherche_somme != None:
                    rang_somme = rang_somme + recherche_somme.end()


                    if verif_somme(recherche_somme):
                        somme += conv_euros_re(recherche_somme)*(multiplicateur_somme(contenu,dernier_condamne,rs.end()+i + ss.end()))
                        #print(multiplicateur_somme(contenu,dernier_condamne,rs.end()+i + ss.end()))

                    recherche_somme = re.search(somme_re,contenu[rang_somme:dernier_condamne + ss.end()])#borne superieure doit etre fixe
                dernier_condamne += ss.end()
                rang_somme=dernier_condamne
                ss = re.search(r,contenu[dernier_condamne:])
            if ss==None:

                recherche_somme = re.search(somme_re,contenu[dernier_condamne:])
                rang_somme = dernier_condamne
                while recherche_somme != None:

                    if verif_somme(recherche_somme):

                        somme +=  conv_euros_re(recherche_somme)*(multiplicateur_somme(contenu,dernier_condamne,len(contenu)-1))
                        #print(multiplicateur_somme(contenu,dernier_condamne,len(contenu)-1))
                    rang_somme = recherche_somme.end()+rang_somme
                    recherche_somme = re.search(somme_re,contenu[rang_somme:])
            return round(somme, 2)

    return 0



"""Pour savoir qui paye, on recherche les noms des deux partis et celui qui est trouv?? en premier est celui qui paye"""

def multiplicateur_somme(contenu,i,j):#i et j sont les rangs de d??buts et de fin entre lesquels regard??

    civil_re = re.compile('(M\.|Mme|Madame|Monsieur|Mr|CFDT|CGT)',re.IGNORECASE)
    civil = re.search(civil_re,contenu[i:j+1])
    multiplicateur = 1
    rang_civil=j+1
    if civil != None:
        rang_civil = civil.end()

    rang_sncf = j+1
    for pseudo in noms_sncf:
        pseudo_re=''
        for car in pseudo:
            if car in [' ',',','-','_']:
                pseudo_re += '[ ,-_]'

            elif car == "'":
                pseudo_re += '.'
            elif car in ['e','??','??','??','??']:
                pseudo_re+='[e????????]'
            else :
                pseudo_re += car
        ts = re.compile('('+pseudo_re+')',re.IGNORECASE)

        sncf = re.search(ts,contenu[i:j])
        if sncf != None:
            rang_sncf = sncf.end()

    if rang_sncf <= rang_civil:
        multiplicateur = -1
    return multiplicateur



# ~ Extrait du Site de Pierre Corneille ~
# - Don Di??gue ?? l'issue de son P2E -


# ?? rage ! ?? d??sespoir ! P2E ennemi !
# N???ai-je donc tant v??cu que pour cette infamie ?
# Et ne suis-je blanchi dans les tutos Django
# Que pour voir qu'Oraclex ne fonctionne pas trop ?
# Django, qu'avec orgueil tous les devs ont ?? c??ur,
# Django, qui tant de fois a pourri mon serveur,
# Serveur qu???SNCF jamais ne d??ploiera
# Car Franck trahit sa cause et ne fait rien pour ??a.
# ?? cruel souvenir du P2E pass?? !
# ??uvre de tant de jours ?? ce jour effac??e !
# Floril??ge de scripts, tous ??perdument vides !
# Leur boycott a laiss?? Oraclex invalide.
# Faudra-t-il, dans mon stage, faire fonctionner le site
# Et mourir de col??re en attendant Repl.it ?
# Et, en ces jours, Sarah ma coll??gue sera,
# Mais son nom, pour autant, qui donc le conna??tra ?
# Quant au fier Olivier, brillant par son absence,
# Qu'il soit l?? ou pas l??, quelle est la diff??rence ?
# Et toi, unique exploit, interface si belle,
# Aux fonctionnalit??s toutes non fonctionnelles,
# Je t'ai si bien vendue, au fil de ces rapport
# Servant de couverture ?? l'absence d'effort.
# La v??rit??, pourtant, est cach??e en annexe,
# Au fin fond des archives de l?????quipe Branlex.
