#-*- coding utf-8 -*-
#la date sera notée dans le fichier résumé sous la forme aaaa mm


import os
import re
import codecs
import sys


TAILLE_MAX = 1000

chiffres = [str(k) for k in range(10)]

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
    
def compter_chiffres(somme_re):
    c = 0
    for car in somme_re.group():
        if car in chiffres:
            c+=1
    return c
    
##
repertoire = '/Users/aurelehainaut/Desktop/Centrale/P2E/Fichiers_SNCF/TXT'

liste_mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
liste_mc = ['ABSENCE IRREGULIERE','ACCROISSEMENT','ACCROISSEMENT TEMPORAIRE','ACTION EN JUSTICE','ACTIVITE NORMALE ET PERMANENTE','ACTIVITE SYNDICALE','AGE','ALCOOL','ANCIENNETE','ANNULATION DE SANCTION','APPARTENANCE SYNDICALE','APPRENTI','APPRENTISSAGE','APTITUDE','ATTACHE CADRE','ATTACHE OP','ATTACHE TS',"ATTENTE DE L'ENTREE EN SERVICE",'AVANCEMENT','AVANCEMENT EN GRADE','AVERTISSEMENT','BLAME','BONNE FOI','C.D.D.','CANDIDATURE','CARENCE','CCE','CDD',"CESSATION PROGRESSIVE D’ACTIVITE",'CHARGE DE LA PREUVE','CHSCT','CODE DE DEONTOLOGIE','COMITE DE CARRIERE','COMMISSION DE NOTATION','COMMISSIONNEMENT','CONGES','CONSEIL DE DISCIPLINE','CONTRACTUEL','CONTRAT A DUREE DETERMINEE','CONTRAT DE MISSION','DEDIT FORMATION','DELEGUE DU PERSONNEL','DEMISSION',"DEMISSION D'OFFICE",'DEPART EN RETRAITE','DEPART NEGOCIE','DEPART VOLONTAIRE','DEPLACEMENT','DEPLACEMENT PAR MESURE DISCIPLINAIRE','DEROULEMENT DE CARRIERE','DEVOIR DE RESERVE','DIFFERENCE DE TRAITEMENT','DIGNITE','DIPLOME',"DISCRIMINATION A L'EMBAUCHE",'DISCRIMINATION DIRECTE','DISCRIMINATION INDIRECTE','DISCRIMINATIONS','DISCRIMINATION','DISCRIMINATOIRES','DISCRIMINATOIRE','DOCUMENTS ADMINISTRATIFS','EGALITE DE TRAITEMENT','EMBAUCHE','ENGAGEMENT SYNDICAL','ENTRAVE','ENTRETIEN','ENTRETIEN DISCIPLINAIRE','ENTRETIEN INDIVIDUEL ANNUEL','ENTRETIEN PREALABLE','ENTREVUE','ETAT DE SANTE','ETHIQUE','EVOLUTION DE CARRIERE','EXAMEN','FAUTE DE SECURITE','FONCTIONS SYNDICALES','FORFAIT JOURS','FORMATION','GREVE','GROSSESSE','HABILITATION','HANDICAP','HARCELEMENT','HARCELEMENT MORAL','HARCELEMENT SEXUEL','HORAIRE','IMPARTIALITE','INAPTE','INAPTITUDE','INEGALITE','INSUFFISANCE PROFESSIONNELLE','INSUFFISSANCE PROFESSIONNELLE','INTERET COLLECTIF DE LA PROFESSION','INTERIM','INTERIMAIRE','INTERVENTION VOLONTAIRE','JEUNE CADRE','LICENCIEMENT','LICENCIEMENT SANS CAUSE REELLE ET SERIEUSE','LIEN DE CAUSALITE','LOYAUTE',"MAITRISE DE L'EMPLOI TENU",'MARCHANDAGE','MATERNITE','MESURE CONSERVATOIRE','MISE A DISPOSITION','MISE A PIED','MI-TEMPS THERAPEUTIQUE','MOBILITE','MODIFICATION DU CONTRAT','MUTATION','MUTATION PAR MESURE DISCIPLINAIRE','NON CONCURRENCE','NOTATION','OBLIGATION DE LOYAUTE','OBLIGATION DE SECURITE','ORIGINE',"PERIODE D'ESSAI","PERIODE D'INTERRUPTION",'POSTE VACANT','PREAVIS','PRECARITE',"PRET DE MAIN D'OEUVRE",'PREUVE',"PRISE D'ACTE",'PROMESSE',"PROMESSE D'EMBAUCHE",'PROMOTION','QUALIFICATION','QUALIFICATION INFERIEURE','QUALIFICATION SUPERIEURE','QUALITE DE SERVICE','QUALITE DES SERVICES','RADIATION DES CADRES','RAPPEL DE SALAIRE','RECLASSEMENT','RECONNAISSANCE DE DIPLÔME','RECRUTEMENT','REFORME','REGIME DE TRAVAIL','REGLEMENT INTERIEUR','REINTEGRATION','RELIGION','REMIS CONTRAT','REMISE CONTRAT','REMPLACEMENT,REMUNERATION','RENOUVELLEMENT','REPOS','REQUALIFICATION','RESERVE','RETRAITE','REVOCATION','ROULEMENT','RUPTURE','RUPTURE CONVENTIONNELLE',"RUPTURE DE LA PERIODE D'ESSAI",'SAISONNIER','SALARIE ABSENT','SANCTIONS','SECRET MEDICAL',"SURCROIT D'ACTIVITE",'SUSPENSION',"TABLEAU D'APTITUDE",'TEMPS PARTIEL','TRAVAIL DE NUIT','TRAVAIL DISSIMULE','TRAVAIL TEMPORAIRE','VACANCE DE POSTE','VIE PRIVEE']
noms_sncf =["établissement SNCF",'EPIC','epic','E.P.I.C','e.p.i.c','E.P.I.C.','e.p.i.c.','SNCF','S.N.C.F','S.N.C.F.','sncf','s.n.c.f','Société Nationale des Chemins de Fer Français','Société Nationale des Chemins de Fer Francais','société nationale des chemins de fer français','société nationale des chemins de fer francais','SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','MOBILITES','MOBILITéS','RESEAU','RéSEAU','groupe','EPIC Société Nationale des Chemins de Fer Français','EPIC Société Nationale des Chemins de Fer Francais','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','EPIC SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','EPIC MOBILITES','EPIC MOBILITÉS','EPIC RESEAU','EPIC RÉSEAU','EPIC GROUPE','E.P.I.C Société Nationale des Chemins de Fer Français','E.P.I.C Société Nationale des Chemins de Fer Francais','E.P.I.C Société Nationale des Chemins de Fer Francais','E.P.I.C société nationale des chemins de fer français','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C SOCIETE NATIONALE DES CHEMINS DE FER FRANcAIS','E.P.I.C MOBILITES','E.P.I.C MOBILITÉS','E.P.I.C RESEAU','E.P.I.C RESEAU','E.P.I.C Groupe','e.p.i.c Société Nationale des Chemins de Fer Français','e.p.i.c Société Nationale des Chemins de Fer Francais','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c MOBILITES','e.p.i.c MOBILITÉS','e.p.i.c Mobilités','e.p.i.c mobilités','e.p.i.c mobilites','e.p.i.c Mobilites','e.p.i.c RESEAU','e.p.i.c RÉSEAU','e.p.i.c réseau','e.p.i.c réseau','e.p.i.c reseau','e.p.i.c Réseau','e.p.i.c Reseau','e.p.i.c Groupe','e.p.i.c GROUPE', 'E.P.I.C. Société Nationale des Chemins de Fer Français','E.P.I.C. Société Nationale des Chemins de Fer Francais','E.P.I.C. société nationale des chemins de fer français','E.P.I.C. société nationale des chemins de fer francais','E.P.I.C. SOCIéTé NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','E.P.I.C. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','E.P.I.C. MOBILITES','E.P.I.C. MOBILITÉS','E.P.I.C. Mobilités','E.P.I.C. mobilités','E.P.I.C. mobilites','E.P.I.C. Mobilites','E.P.I.C. RESEAU','E.P.I.C. RÉSEAU','E.P.I.C. réseau','E.P.I.C. reseau','E.P.I.C. Réseau','E.P.I.C. Reseau','E.P.I.C. Groupe','E.P.I.C. GROUPE','e.p.i.c. Société Nationale des Chemins de Fer Français','e.p.i.c. Société Nationale des Chemins de Fer Francais','e.p.i.c. société nationale des chemins de fer français','e.p.i.c. société nationale des chemins de fer francais','e.p.i.c. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. SOCIÉTÉ NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRANÇAIS','e.p.i.c. SOCIETE NATIONALE DES CHEMINS DE FER FRANCAIS','e.p.i.c. MOBILITES','e.p.i.c. MOBILITÉS','e.p.i.c. Mobilités','e.p.i.c. mobilités','e.p.i.c. mobilites','e.p.i.c. Mobilites','e.p.i.c. RESEAU','e.p.i.c. RÉSEAU','e.p.i.c. réseau','e.p.i.c. reseau','e.p.i.c. Réseau','e.p.i.c. Reseau','e.p.i.c. Groupe', 'e.p.i.c. GROUPE','SNCF MOBILITES','SNCF MOBILITÉS','SNCF Mobilités','SNCF mobilités','SNCF mobilites','SNCF Mobilites','SNCF RESEAU','SNCF RÉSEAU','SNCF réseau','SNCF reseau','SNCF Réseau','SNCF Reseau','SNCF Groupe','SNCF GROUPE','S.N.C.F MOBILITES','S.N.C.F MOBILITÉS','S.N.C.F Mobilités','S.N.C.F mobilités','S.N.C.F mobilites','S.N.C.F Mobilites','S.N.C.F RESEAU','S.N.C.F RÉSEAU','S.N.C.F réseau','S.N.C.F reseau','S.N.C.F Réseau','S.N.C.F Reseau','S.N.C.F Groupe', 'S.N.C.F GROUPE', 'S.N.C.F. MOBILITES','S.N.C.F. MOBILITÉS','S.N.C.F. Mobilités','S.N.C.F. mobilités','S.N.C.F. mobilites','S.N.C.F. Mobilites','S.N.C.F. RESEAU','S.N.C.F. RÉSEAU','S.N.C.F. réseau','S.N.C.F. reseau','S.N.C.F. Réseau','S.N.C.F. Reseau','S.N.C.F. Groupe','S.N.C.F. GROUPE','sncf MOBILITES','sncf MOBILITÉS','sncf Mobilités','sncf mobilités','sncf mobilites','sncf Mobilites','sncf RESEAU','sncf RÉSEAU','sncf réseau','sncf reseau','sncf Réseau','sncf Reseau','sncf Groupe','sncf GROUPE','s.n.c.f. MOBILITES','s.n.c.f. MOBILITÉS','s.n.c.f. Mobilités','s.n.c.f. mobilités','s.n.c.f. mobilites','s.n.c.f. Mobilites','s.n.c.f. RESEAU','s.n.c.f. RÉSEAU','s.n.c.f. réseau','s.n.c.f. reseau','s.n.c.f. Réseau','s.n.c.f. Reseau','s.n.c.f. Groupe','s.n.c.f. GROUPE','Société Nationale des Chemins de Fer Français MOBILITES','Société Nationale des Chemins de Fer Français MOBILITÉS','Société Nationale des Chemins de Fer Français Mobilités','Société Nationale des Chemins de Fer Français mobilités','Société Nationale des Chemins de Fer Français mobilites','Société Nationale des Chemins de Fer Français Mobilites','Société Nationale des Chemins de Fer Français RESEAU','Société Nationale des Chemins de Fer Français RÉSEAU','Société Nationale des Chemins de Fer Français réseau','Société Nationale des Chemins de Fer Français reseau','Société Nationale des Chemins de Fer Français Réseau','Société Nationale des Chemins de Fer Français Reseau','Société Nationale des Chemins de Fer Français Groupe','Société Nationale des Chemins de Fer Français GROUPE','Société Nationale des Chemins de Fer Francais MOBILITES','Société Nationale des Chemins de Fer Francais MOBILITÉS','Société Nationale des Chemins de Fer Francais Mobilités','Société Nationale des Chemins de Fer Francais mobilités','Société Nationale des Chemins de Fer Francais mobilites','Société Nationale des Chemins de Fer Francais Mobilites','Société Nationale des Chemins de Fer Francais RESEAU','Société Nationale des Chemins de Fer Francais RÉSEAU','Société Nationale des Chemins de Fer Francais réseau','Société Nationale des Chemins de Fer Francais reseau','Société Nationale des Chemins de Fer Francais Réseau','Société Nationale des Chemins de Fer Francais Reseau','Société Nationale des Chemins de Fer Francais Groupe','Société Nationale des Chemins de Fer Francais GROUPE','société nationale des chemins de fer français MOBILITES','société nationale des chemins de fer français MOBILITÉS','société nationale des chemins de fer français Mobilités','société nationale des chemins de fer français mobilités','société nationale des chemins de fer français mobilites','société nationale des chemins de fer français Mobilites','société nationale des chemins de fer français RESEAU','société nationale des chemins de fer français RÉSEAU','société nationale des chemins de fer français réseau','société nationale des chemins de fer français reseau','société nationale des chemins de fer français Réseau','société nationale des chemins de fer français Reseau','société nationale des chemins de fer français Groupe','société nationale des chemins de fer français GROUPE','société nationale des chemins de fer francais MOBILITES','société nationale des chemins de fer francais MOBILITÉS','société nationale des chemins de fer francais Mobilités','société nationale des chemins de fer francais mobilités','société nationale des chemins de fer francais mobilites','société nationale des chemins de fer francais Mobilites','société nationale des chemins de fer francais RESEAU','société nationale des chemins de fer francais RÉSEAU','société nationale des chemins de fer francais réseau','société nationale des chemins de fer francais reseau','société nationale des chemins de fer francais Réseau','société nationale des chemins de fer francais Reseau','société nationale des chemins de fer francais Groupe','société nationale des chemins de fer francais GROUPE','Groupe  EPIC','Groupe  epic','Groupe  E.P.I.C','Groupe  e.p.i.c','Groupe  E.P.I.C.','Groupe  e.p.i.c.','Groupe  SNCF','Groupe  S.N.C.F','Groupe  S.N.C.F.','Groupe  sncf','Groupe  s.n.c.f.','Groupe  Société Nationale des Chemins de Fer Français','Groupe  Société Nationale des Chemins de Fer Francais','Groupe  société nationale des chemins de fer français','Groupe  société nationale des chemins de fer francais','GROUPE  MOBILITES','GROUPE  MOBILITÉS','GROUPE  Mobilités','GROUPE  mobilités','GROUPE  mobilites','GROUPE  Mobilites','GROUPE  RESEAU','GROUPE  RÉSEAU','GROUPE  réseau','GROUPE  reseau','GROUPE  Réseau','GROUPE  Reseau']
chiffres = [str(k) for k in range(10)]


##définition des fonctions
def lisible(file, seuil, alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789éàèçù€ .,:;\"'()-"):

    n = 0
    nChar = 0

    for line in file:
        line = line[:len(line)-2]
        for char in line:
            n += 1
            if special_character(char, alphabet):
                nChar += 1

    if n==0:
        return True
    else:
        return (nChar/n) <= seuil

def special_character(char, alphabet):
    return not (char in alphabet)



def extraction_nom(nom):#prend en argument le nom du fichier et renvoie une chaine contenant le nom
    test =False
    res =''
    if nom[-5] == '1' and nom[-6] not in chiffres:#première page du fichier
        test = True
    if test == True:
        res = nom[:len(nom)-11]+".pdf"#nom du fichier sans le num de la page et avec bonne extension
    return res
    
def extraction_jugement(nom):
    test =False
    res =''
    if nom[-5] == '1' and nom[-6] not in chiffres:#première page du fichier
        test = True
    
    if test == True:
        fav = re.search(" [FDM][ \.]",nom)#ATTENTION PEUT ETRE MODIFIER L'AJOUT DU POINT
        if fav != None:
            res = nom[fav.start()+1:fav.start()+2]
            
    return res
    
def extraction_date(nom):
    test =False
    res =''
    if nom[-5] == '1' and nom[-6] not in chiffres:#première page du fichier
        test = True
    if test == True:
        date1_re = '(\d{4})[\. ](\d{2})'# format aaaa mm
        date2_re = '(\d{2})[\. /](\d{2})[\. /](\d{4})' #formt jj/mm/aaaa
        recherche_date = re.search(date1_re,nom)
        if recherche_date == None:
            recherche_date = re.search(date2_re,nom)
            if recherche_date != None:
                res = recherche_date.group(3) + ' '+recherche_date.group(2)
            else:
                res = "date inconnue"
        else:
            res = recherche_date.group(1) + ' '+recherche_date.group(2)
    return res
    
def extraction_mc(contenu):
    res = ''
    for mc in liste_mc :
        expression = '' #re a  rechercher
        for car in mc :
            if (car == 'o') or (car == 'ô') or (car == 'ò') or (car =='ó') or (car=='ö') or (car =='Ö') or (car =='Ô') :
                expression += '[oe0ôòóö]'
            elif (car == 'a') or (car =='ä') or (car=='à ') or (car =='á') or (car == 'â') :
                expression += '[saàäáâ]'
            elif (car == 'e') or (car =='é') or (car=='è') or (car =='ê') or (car =='ë'):
                expression += '[eéèëêÉÈ]'
            elif (car == 'i') or (car == 'î') or (car =='ï') or (car=='í') or (car =='ì'):
                expression += '[iíîìï]'
            elif (car == 'u') or (car == 'û') or (car =='ü') or (car=='ù') or (car =='ú'):
                expression += '[uùûüú]'
            elif (car == "'"):
                expression +='.'#l'apostrophe est représentée par n'importe quel caractère
            elif (car == 'l'):
                expression += '[I1l]'
                
            elif (car == 't'):
                expression += '[t+]'
            
            else :
                expression += car
    

            
            
        p = re.compile((' '+expression+' ' ),re.IGNORECASE) #les majuscules et minuscules ne sont pas différenciées + ne recherchee pas de sous mot dans un mot (ex age dans partage) 
        if (re.search(p,contenu) != None) :
            res = res + mc + ';'
    
    return res#on laisse le point virgule en trop a la fin, il sera enlever dans la fct doublons
    
def extraction_somme(contenu,ofi):
   
    limite = "([EP]ar ces m[oÛÜ]t[fi]fs)"
    somme = 0 #somme perdue par la sncf
    somme_re = '[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{0,3}[\., ]?[0-9]{1,3}[\., ]?((euros)|[\.,])?[0-9]{0,2} ?((euros)|[€ÄÊ])?'#somme en re
    q = re.compile(limite,re.IGNORECASE)
    qs = re.search(q,contenu)
    dernier_condamne = 0#permet d'avoir le veritable rang du condamne
    
    if (qs == None) or (lisible(ofi,0.9))==False:#si 'Par ces motifs' est mal écrit, le fichier est considéré comme endommagé + critere de lisibilité
        return (False,-1)
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
                        print(multiplicateur_somme(somme,contenu,dernier_condamne,rs.end()+i + ss.end()))
                        
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
                        print(multiplicateur_somme(somme,contenu,dernier_condamne,len(contenu)-1))
                    rang_somme = recherche_somme.end()+rang_somme
                    recherche_somme = re.search(somme_re,contenu[rang_somme:])
                        
    return (True,somme)
    
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
        
    if rang_sncf<=rang_civil:
        multiplicateur = -1
    return multiplicateur
    
def extraction_juridiction(nom):
    juri = '(CPH|CASS|CA|TGI|C\.CASS)'
    juri_re = re.compile(juri,re.IGNORECASE)
    rch = re.search(juri_re,nom)
    if rch != None:
        return rch.group()
    else : 
        return 'Juridiction inconnue'
    
    
"""renvoie l'indice de la ligne sur laquelle les infos d'un fichier ont déja été ecrites renvoie true si une page a deja ete analysée et false sinon avec indice ds tab"""
        

def nouvelle_ligne(tab,nom):
    page  = '(_page_[0-9]{0,2}\.txt)'
    rnom = nom[:re.search(page,nom).start()] + '.pdf'
    for k in range(len(tab)) :
        if rnom == tab[k][0]:
            return (True,k)

    return (False,-1)


def remplissage_tab():
    #nom;lisible;fav;date;juridiction;mc;somme
    tab = []
    donnee_fic = (False,-1)

    c = 0#derniere ligne ecrite dans la matrice
    for k in range(TAILLE_MAX):
        tab += [['',True,'','','','',0]]
    
    for nom in os.listdir(
        repertoire) :
        ofi=codecs.open(repertoire+"/"+nom,'r',encoding = 'utf-8')
        print(repertoire+"/"+nom)
        contenu = ofi.read()                            
        donnee_fic = nouvelle_ligne(tab,nom)

        if donnee_fic[0] == False:
            tab[c][0] = extraction_nom(nom)
            
            tab[c][2] = extraction_jugement(nom)
            tab[c][3] = extraction_date(nom)
            tab[c][4] = extraction_juridiction(nom)
            tab[c][5] = extraction_mc(contenu)
            (tab[c][1],tab[c][6]) = extraction_somme(contenu,ofi)

            c+=1
        
        else:
            tab[donnee_fic[1]][5] += extraction_mc(contenu)
            if tab[donnee_fic[1]][1]!=True:
                tab[donnee_fic[1]][1],tab[donnee_fic[1]][6] = extraction_somme(contenu,ofi)
        
        
        ofi.close()
        
    return tab
        

def doublons_mc(mcs):#renvoie une chaîne de mc sans les doublons/utilisation lors de l'écriture dans le fichier
    res = ''
    doublons = [0 for k in range(len(liste_mc))]
    rang_mot = 0
    mot = re.compile('[^;]{0,100};',re.IGNORECASE)
    rch_mot = re.search(mot,mcs)
    while rch_mot != None:
        for mc in liste_mc:
            
            if (rch_mot.group()[:len(rch_mot.group())-1] == mc):#on retire le point virgule à la fin
                if  doublons[liste_mc.index(mc)] == 0 :
                    res = res + mc + ';'
                
                    doublons[liste_mc.index(mc)] = 1
            
            
        
        rang_mot += rch_mot.end()
        rch_mot = re.search(mot,mcs[rang_mot:])
    
    return res[:len(res)-1]#pour supprimer le point virgule en trop a la fin
    

def fichier_res(tab):
    i = 0
    fichier_resume = codecs.open('/Users/aurelehainaut/Desktop/Centrale/P2E/Fichiers_SNCF/fichier_résumé2.txt','w',encoding = 'utf-8')
    while i<TAILLE_MAX-1 and tab[i][0] != '':
        for j in range(7):
            if type(tab[i][j]) !=str :
                fichier_resume.write(str(tab[i][j]) +"\n")

            elif j == 5:
                fichier_resume.write(doublons_mc(tab[i][j]) +"\n")

            else:
                fichier_resume.write(tab[i][j] +"\n")
        fichier_resume.write("\n")
        i+=1
    fichier_resume.close()
  
#On définit une nouvelle fonction (utilisée dans la vue ajouts) qui permet d'extraire les informations qu'on cherche à ajouter dans la base de données à partir des jugements ajoutés dans le fichier media/jugements et qui les stocke sous la forme d'une matrice 
def remplissage_tab_bis():
    #nom;lisible;fav;date;juridiction;mc;somme
    tab = []
    donnee_fic = (False,-1)

    c = 0#derniere ligne ecrite dans la matrice
    for k in range(TAILLE_MAX):
        tab += [['',True,'','','','',0]]
    
    for nom in os.listdir('media/jugements'):
        ofi=codecs.open(repertoire+"/"+nom,'r',encoding = 'utf-8')
        print(repertoire+"/"+nom)
        contenu = ofi.read()                            
        donnee_fic = nouvelle_ligne(tab,nom)

        if donnee_fic[0] == False:
            tab[c][0] = extraction_nom(nom)
            
            tab[c][2] = extraction_jugement(nom)
            tab[c][3] = extraction_date(nom)
            tab[c][4] = extraction_juridiction(nom)
            tab[c][5] = extraction_mc(contenu)
            (tab[c][1],tab[c][6]) = extraction_somme(contenu,ofi)

            c+=1
        
        else:
            tab[donnee_fic[1]][5] += extraction_mc(contenu)
            if tab[donnee_fic[1]][1]!=True:
                tab[donnee_fic[1]][1],tab[donnee_fic[1]][6] = extraction_somme(contenu,ofi)
        
        
        ofi.close()
        
    return tab


#On définit la fonction qui utilise la matrice extraite par remplissage_tab_bis pour l'utilisation dans la vue ajouts 
def page_ajout():
  # on cherche les fichiers à ajouter dans le dossier jugement dans media 
  #Les données sont organisées dans la matrice selon l'enchainement nom;lisible;fav;date;juridiction;mc;somme
  tab=remplissage_tab_bis()
  jugements= []
  form=[0,0,0,0,0]
  i = 0
  while i<TAILLE_MAX-1 and tab[i][0] != '':
        for j in range(7):
            if j==0 : 
              form[j]=tab[i][j]
            elif j==1: 
              form[j]=tab[i][j]
            elif j==3:
              form[j]=tab[i][j]
            elif j==4:
              form[j]=tab[i][j]
            elif j==6:
              form[j]=tab[i][j]
        jugements.append(form)
        i+=1
    




