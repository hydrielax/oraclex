from apps.search.models import MotCle
from apps.search.models import Jugement
from pdf2image import convert_from_bytes
from pytesseract import image_to_data
from dateparser.search import search_dates
from dateparser import parse
import re
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')

def detect_doublon(text):
    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map) , language='french'))
    
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    
    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]

    L=[]
    for textes in Jugement.objects.all().values_list('text',flat=True):
        L.append(cosine_sim(text, textes))
    
    if max(L)>0.95 :
        return True
    
    return False


def analyse(jugement):
    print('Start')
    jugement.text, jugement.quality = extract_text(jugement.file.file)
    jugement.date_jugement = extract_date(jugement.text)
    jugement.gain = extraction_somme(jugement.text)
    print(jugement.gain)
    jugement.mots_cle.set(find_keywords(jugement.text, MotCle.objects.all()))
    jugement.register()
    print('End')


def extract_text(file):
    text = ""
    good = total = 0
    for page in convert_from_bytes(file.read()):
        data = image_to_data(page, lang='fra', config=r'--oem 3 --psm 6', output_type='dict')
        for word, conf in zip(data['text'], map(float, data['conf'])):
            if word: text += word + " "
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


#def extract_date(text):
#    dates = search_dates(text, languages=['fr'], settings={'STRICT_PARSING': True})
#    return dates[0][1]

def extract_date(file,text):
    #extraire la date du fichier texte
    nom=file.name
    #Le try except c'est pour éviter un bug dans dateparser, il est possible que ce problème soit résolu avec les prochaines versions de dateparser.
    try :
        dates = search_dates(text, languages=['fr'], settings={'STRICT_PARSING': True,'PREFER_DATES_FROM': 'past'})
        if dates:
            date_text = dates[0][1].date()
    except :
        dates= None
    #extraire la date du nom du fichier
    file_name = nom.replace("-", " ")
    L=[str(int(s)) for s in file_name.split() if s.isdigit()]
    name = ' '.join(L)
    date1 = parse(name, settings={'PREFER_DATES_FROM': 'past','PREFER_DAY_OF_MONTH': 'first'})
    if date1:
        date_name = date1.date()
        date2 = None
    #Si la méthode parse n'a pas fonctionné, nous utiliserons les expressions régulières.
    else :
        name_of_file=re.search("(([0-9]{4}|[0-9]{2})\W[0-9]{2}\W([0-9]{2})?)", nom)
        if name_of_file:
            date2 = search_dates(name_of_file.group(), languages=['fr'], settings={'PREFER_DATES_FROM': 'past','PREFER_DAY_OF_MONTH': 'first'})
        if date2:
            date_name = date2[0][1].date()
    #Comparaisons:
    if not dates :
        return date_name
    elif (bool(date1) | bool(date2) ) & bool(dates):
        if ((date_name.year == date_text.year) & (date_name.month == date_text.month)) :
            return date_text
        else:
            return date_name
    else:
        return date_text

    

def extraction_jugement(file,text):
    nom=file.name
    fav = re.search("\W*[FDM]\W",nom) #ATTENTION PEUT ETRE MODIFIER L'AJOUT DU POINT
    if fav != None:
        res = nom[fav.start()+1:fav.start()+2]
            
        return res
    return extraction_jugement2(text)

noms_sncf = ["établissement SNCF",'EPIC','epic','E.P.I.C','e.p.i.c','E.P.I.C.','e.p.i.c.','SNCF','S.N.C.F','S.N.C.F.','sncf','s.n.c.f','Société Nationale des Chemins de Fer Français','Société Nationale des Chemins de Fer Francais','société nationale des chemins de fer français','société nationale des chemins de fer francais','SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','MOBILITES','MOBILITéS','RESEAU','RéSEAU','groupe','EPIC Société Nationale des Chemins de Fer Français','EPIC Société Nationale des Chemins de Fer Francais','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','EPIC MOBILITES','EPIC MOBILITÉS','EPIC RESEAU','EPIC RÉSEAU','EPIC GROUPE','E.P.I.C Société Nationale des Chemins de Fer Français','E.P.I.C Société Nationale des Chemins de Fer Francais','E.P.I.C Société Nationale des Chemins de Fer Francais','E.P.I.C société nationale des chemins de fer français','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRANcAIS','E.P.I.C MOBILITES','E.P.I.C MOBILITÉS','E.P.I.C RESEAU','E.P.I.C RESEAU','E.P.I.C Groupe','e.p.i.c Société Nationale des Chemins de Fer Français','e.p.i.c Société Nationale des Chemins de Fer Francais','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c MOBILITES','e.p.i.c MOBILITÉS','e.p.i.c Mobilités','e.p.i.c mobilités','e.p.i.c mobilites','e.p.i.c Mobilites','e.p.i.c RESEAU','e.p.i.c RÉSEAU','e.p.i.c réseau','e.p.i.c réseau','e.p.i.c reseau','e.p.i.c Réseau','e.p.i.c Reseau','e.p.i.c Groupe','e.p.i.c GROUPE', 'E.P.I.C. Société Nationale des Chemins de Fer Français','E.P.I.C. Société Nationale des Chemins de Fer Francais','E.P.I.C. société nationale des chemins de fer français','E.P.I.C. société nationale des chemins de fer francais','E.P.I.C. SOCIéTé NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. MOBILITES','E.P.I.C. MOBILITÉS','E.P.I.C. Mobilités','E.P.I.C. mobilités','E.P.I.C. mobilites','E.P.I.C. Mobilites','E.P.I.C. RESEAU','E.P.I.C. RÉSEAU','E.P.I.C. réseau','E.P.I.C. reseau','E.P.I.C. Réseau','E.P.I.C. Reseau','E.P.I.C. Groupe','E.P.I.C. GROUPE','e.p.i.c. Société Nationale des Chemins de Fer Français','e.p.i.c. Société Nationale des Chemins de Fer Francais','e.p.i.c. société nationale des chemins de fer français','e.p.i.c. société nationale des chemins de fer francais','e.p.i.c. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. MOBILITES','e.p.i.c. MOBILITÉS','e.p.i.c. Mobilités','e.p.i.c. mobilités','e.p.i.c. mobilites','e.p.i.c. Mobilites','e.p.i.c. RESEAU','e.p.i.c. RÉSEAU','e.p.i.c. réseau','e.p.i.c. reseau','e.p.i.c. Réseau','e.p.i.c. Reseau','e.p.i.c. Groupe', 'e.p.i.c. GROUPE','SNCF MOBILITES','SNCF MOBILITÉS','SNCF Mobilités','SNCF mobilités','SNCF mobilites','SNCF Mobilites','SNCF RESEAU','SNCF RÉSEAU','SNCF réseau','SNCF reseau','SNCF Réseau','SNCF Reseau','SNCF Groupe','SNCF GROUPE','S.N.C.F MOBILITES','S.N.C.F MOBILITÉS','S.N.C.F Mobilités','S.N.C.F mobilités','S.N.C.F mobilites','S.N.C.F Mobilites','S.N.C.F RESEAU','S.N.C.F RÉSEAU','S.N.C.F réseau','S.N.C.F reseau','S.N.C.F Réseau','S.N.C.F Reseau','S.N.C.F Groupe', 'S.N.C.F GROUPE', 'S.N.C.F. MOBILITES','S.N.C.F. MOBILITÉS','S.N.C.F. Mobilités','S.N.C.F. mobilités','S.N.C.F. mobilites','S.N.C.F. Mobilites','S.N.C.F. RESEAU','S.N.C.F. RÉSEAU','S.N.C.F. réseau','S.N.C.F. reseau','S.N.C.F. Réseau','S.N.C.F. Reseau','S.N.C.F. Groupe','S.N.C.F. GROUPE','sncf MOBILITES','sncf MOBILITÉS','sncf Mobilités','sncf mobilités','sncf mobilites','sncf Mobilites','sncf RESEAU','sncf RÉSEAU','sncf réseau','sncf reseau','sncf Réseau','sncf Reseau','sncf Groupe','sncf GROUPE','s.n.c.f. MOBILITES','s.n.c.f. MOBILITÉS','s.n.c.f. Mobilités','s.n.c.f. mobilités','s.n.c.f. mobilites','s.n.c.f. Mobilites','s.n.c.f. RESEAU','s.n.c.f. RÉSEAU','s.n.c.f. réseau','s.n.c.f. reseau','s.n.c.f. Réseau','s.n.c.f. Reseau','s.n.c.f. Groupe','s.n.c.f. GROUPE','Société Nationale des Chemins de Fer Français MOBILITES','Société Nationale des Chemins de Fer Français MOBILITÉS','Société Nationale des Chemins de Fer Français Mobilités','Société Nationale des Chemins de Fer Français mobilités','Société Nationale des Chemins de Fer Français mobilites','Société Nationale des Chemins de Fer Français Mobilites','Société Nationale des Chemins de Fer Français RESEAU','Société Nationale des Chemins de Fer Français RÉSEAU','Société Nationale des Chemins de Fer Français réseau','Société Nationale des Chemins de Fer Français reseau','Société Nationale des Chemins de Fer Français Réseau','Société Nationale des Chemins de Fer Français Reseau','Société Nationale des Chemins de Fer Français Groupe','Société Nationale des Chemins de Fer Français GROUPE','Société Nationale des Chemins de Fer Francais MOBILITES','Société Nationale des Chemins de Fer Francais MOBILITÉS','Société Nationale des Chemins de Fer Francais Mobilités','Société Nationale des Chemins de Fer Francais mobilités','Société Nationale des Chemins de Fer Francais mobilites','Société Nationale des Chemins de Fer Francais Mobilites','Société Nationale des Chemins de Fer Francais RESEAU','Société Nationale des Chemins de Fer Francais RÉSEAU','Société Nationale des Chemins de Fer Francais réseau','Société Nationale des Chemins de Fer Francais reseau','Société Nationale des Chemins de Fer Francais Réseau','Société Nationale des Chemins de Fer Francais Reseau','Société Nationale des Chemins de Fer Francais Groupe','Société Nationale des Chemins de Fer Francais GROUPE','société nationale des chemins de fer français MOBILITES','société nationale des chemins de fer français MOBILITÉS','société nationale des chemins de fer français Mobilités','société nationale des chemins de fer français mobilités','société nationale des chemins de fer français mobilites','société nationale des chemins de fer français Mobilites','société nationale des chemins de fer français RESEAU','société nationale des chemins de fer français RÉSEAU','société nationale des chemins de fer français réseau','société nationale des chemins de fer français reseau','société nationale des chemins de fer français Réseau','société nationale des chemins de fer français Reseau','société nationale des chemins de fer français Groupe','société nationale des chemins de fer français GROUPE','société nationale des chemins de fer francais MOBILITES','société nationale des chemins de fer francais MOBILITÉS','société nationale des chemins de fer francais Mobilités','société nationale des chemins de fer francais mobilités','société nationale des chemins de fer francais mobilites','société nationale des chemins de fer francais Mobilites','société nationale des chemins de fer francais RESEAU','société nationale des chemins de fer francais RÉSEAU','société nationale des chemins de fer francais réseau','société nationale des chemins de fer francais reseau','société nationale des chemins de fer francais Réseau','société nationale des chemins de fer francais Reseau','société nationale des chemins de fer francais Groupe','société nationale des chemins de fer francais GROUPE','Groupe  EPIC','Groupe  epic','Groupe  E.P.I.C','Groupe  e.p.i.c','Groupe  E.P.I.C.','Groupe  e.p.i.c.','Groupe  SNCF','Groupe  S.N.C.F','Groupe  S.N.C.F.','Groupe  sncf','Groupe  s.n.c.f.','Groupe  Société Nationale des Chemins de Fer Français','Groupe  Société Nationale des Chemins de Fer Francais','Groupe  société nationale des chemins de fer français','Groupe  société nationale des chemins de fer francais','GROUPE  MOBILITES','GROUPE  MOBILITÉS','GROUPE  Mobilités','GROUPE  mobilités','GROUPE  mobilites','GROUPE  Mobilites','GROUPE  RESEAU','GROUPE  RÉSEAU','GROUPE  réseau','GROUPE  reseau','GROUPE  Réseau','GROUPE  Reseau']


def extraction_jugement2(txt):
    """Cette fonction extrait le jugement du fichier s'il n'a pas été extrait du nom du fichier,
     sa précision est de 81.73% en général et de 86.44% pour le jugement favorable vs défavorable seulement."""
    limite = re.compile("([EP][aà]r\W+ces\W+m[oÛÜ]t[fi][fe]s)",re.IGNORECASE)
    possibilite_de_rechreche = re.search(limite,txt)
    if (possibilite_de_rechreche == None) :#si "Par ces motifs" n'est pas trouvée
        return None
    else :
        i = possibilite_de_rechreche.end()
        s=1
        condamnations = re.finditer("condamne\W",txt[i:], re.IGNORECASE)
        for m in [k for k in condamnations]:
            rang=m.end()+i
            words = re.compile("(\w)+(\W)+(\w)+(\W)+(\w)+(\W)",re.IGNORECASE)
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
                    elif car in ['e','é','É','È','è']:
                        pseudo_re+='[eéèÉÈ]'
                    else :
                        pseudo_re += car
                ts = re.compile('('+pseudo_re+')',re.IGNORECASE)
                sncf = re.search(ts,words_found.group())
                if sncf:
                    s-=5
                    break
 
        deboutements = re.finditer("d[eéÉÈè]bout[ceéÉÈè]\W",txt[i:], re.IGNORECASE)
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
                    elif car in ['e','é','É','È','è']:
                        pseudo_re+='[eéèÉÈ]'
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

### H=extraction_somme(txt), type(txt) == string , as a result : (False, 0) : somme non trouvée, (True:+s) : somme gagnée , (True:+s) : somme perdue



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
    c2 = 0 #compteur pour les caractères non chiffres
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
    euros = '((euros)|[€ÄÊ])'
    somme_c = recherche_somme.group()
    search = re.search(euros,somme_c)
    if search == None:
        verif = False
    return verif


def extraction_somme(contenu):
    
    limite = "([EP][aà]r\W+ces\W+m[oÛÜ]t[fi][fe]s)"
    somme = 0 #somme perdue par la sncf
    somme_re = '[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{1,3}[\., ]?((euros)|[\.,])?[0-9]{0,2} ?((euros)|[€ÄÊ])?'#somme en re
    q = re.compile(limite,re.IGNORECASE)
    qs = re.search(q,contenu)
    dernier_condamne = 0#permet d'avoir le veritable rang du condamne

    if (qs == None) :#si 'Par ces motifs' est mal écrit, le fichier est considéré comme endommagé + critere de lisibilité
        return None
    else :
        i = qs.end()# mm probleme que rang_somme
        r = re.compile("(condamn[ ]?[eèéÉÈËÊêë])",re.IGNORECASE)
        rs = re.search(r,contenu[i:])#On recherche Ã  partir de "Par ces motifs" pour éviter les autres chiffres
        if rs != None:
            dernier_condamne = rs.end() +i#rang du dernier condamne
            rang_somme = rs.end()+ i
            ss = re.search(r,contenu[i+rs.end():])#on recherche jusqu'à une éventuelle autre condamnation pour n'inclure que des chiffres
            while ss != None:

                recherche_somme = re.search(somme_re,contenu[dernier_condamne:ss.end()+dernier_condamne])
                while recherche_somme != None:
                    rang_somme = rang_somme + recherche_somme.end()


                    if verif_somme(recherche_somme):
                        somme += conv_euros_re(recherche_somme)*(multiplicateur_somme(somme,contenu,dernier_condamne,rs.end()+i + ss.end()))
                        #print(multiplicateur_somme(somme,contenu,dernier_condamne,rs.end()+i + ss.end()))

                    recherche_somme = re.search(somme_re,contenu[rang_somme:dernier_condamne + ss.end()])#borne superieure doit etre fixe
                dernier_condamne += ss.end()
                rang_somme=dernier_condamne
                ss = re.search(r,contenu[dernier_condamne:])
            if ss==None:

                recherche_somme = re.search(somme_re,contenu[dernier_condamne:])
                rang_somme = dernier_condamne
                while recherche_somme != None:

                    if verif_somme(recherche_somme):

                        somme +=  conv_euros_re(recherche_somme)*(multiplicateur_somme(somme,contenu,dernier_condamne,len(contenu)-1))
                        #print(multiplicateur_somme(somme,contenu,dernier_condamne,len(contenu)-1))
                    rang_somme = recherche_somme.end()+rang_somme
                    recherche_somme = re.search(somme_re,contenu[rang_somme:])
            return somme

    return 0



"""Pour savoir qui paye, on recherche les noms des deux partis et celui qui est trouvé en premier est celui qui paye"""

def multiplicateur_somme(somme,contenu,i,j):#i et j sont les rangs de débuts et de fin entre lesquels regardé

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
            elif car in ['e','é','É','È','è']:
                pseudo_re+='[eéèÉÈ]'
            else :
                pseudo_re += car
        ts = re.compile('('+pseudo_re+')',re.IGNORECASE)

        sncf = re.search(ts,contenu[i:j])
        if sncf != None:
            rang_sncf = sncf.end()

    if rang_sncf <= rang_civil:
        multiplicateur = -1
    return multiplicateur

