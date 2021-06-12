myfile = r'C:\Users\cathe\Documents\P2E\fichier_résumé.txt'
file = open(myfile,"r") 
from copy import deepcopy

#parcourir chaque ligne pour trouver les mots-clés en retirant chaque mot-clé trouvé de la liste, une fois la liste vide retourner la ligne f[i] qui donne le nom du fichier
#à chaque ligne vide ( ='/n') on recrée une copie de la liste des mots-clés et on continue
#on compte également chaque passage à la ligne
#len pour avoir la taille du readlines et du coup arrêter la recherche

f = file.readlines()
##

def search(f,l):
    i = 0 #compteur indice titre document
    j = 0 #compteur lignes
    results = [] #liste résultats
    while j < len(f):
        lbis = deepcopy(l)
        k = 0 #compteur nombre de lignes par sous-résumé
        while j < len(f) and f[j] != '\n' :
            if f[j][:-1] in lbis :
                del lbis[lbis.index(f[j][:-1])]
            j += 1
            k += 1
        if lbis == [] :
            results = results + [f[i][:-1]]
        i = i+k+1
        j += 1
    return results
    
    
#miskine ce code de 2lignes...
