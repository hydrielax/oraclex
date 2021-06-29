from math import sqrt
import matplotlib.pyplot as plt

def statistiques(recherche, date_lim = '1900 01', juridiction = '', filename = "resume.txt"):
    file = open(filename, 'r')

    trouve = False
    fav = 0
    for i in range(len(recherche)):
        recherche[i] = recherche[i].upper()
    
    sommes = []
    dossiers = []

    sommes_ign = []
    dossiers_ign = []

    c = -1
    for line in file:
        line = line[:len(line)-1]   # Pour enlever le '\n' à la fin
        c +=1

        if c == 0:
            nom = line
            
        elif c == 1:
            lisible_b = (line == 'True')
                
        elif c == 2:
            issu_b = (line != 'M')
            fav_b = (line == 'F')
            
        elif c == 3: 
            date_b = (line >= date_lim)
                
        elif c == 4:
            jur_b = (line == juridiction or juridiction == '')
                
        elif c == 5:
            mots_b = inclu(recherche, extract(line))
            
        elif c == 6:
            somme = float(line)
            if somme > 5000:
                somme = -5000

            if lisible_b and issu_b and date_b and jur_b and mots_b:
                sommes.append(somme)
                dossiers.append(nom)
                if fav_b:
                    fav += 1
            elif (not lisible_b) and issu_b and date_b and jur_b and mots_b:
                sommes_ign.append(somme)
                dossiers_ign.append(nom)
                if fav_b:
                    fav += 1
        else:
            c = -1

    file.close()

    n = len(sommes) + len(sommes_ign)
    if len(sommes) > 0:
        trouve = True
        
        fav = fav/n*100
        non_expl = len(sommes_ign)/n*100

        mi = Min(sommes)
        Mi = Max(sommes)

        m = mi[1]
        M = Mi[1]
        dossier_min = dossiers[mi[0]]
        dossier_max = dossiers[Mi[0]]
        med = mediane(sommes)
        moy = moyenne(sommes)
        rho = ecart_type(sommes)

        return [trouve, med, moy, rho, m, M, dossier_min, dossier_max, fav, non_expl, dossiers, sommes, dossiers_ign]
        # [est-ce que des fichiers correspondent ?, médiane, moyenne, ecart-type, somme min, somme max, dossier somme min, dossier somme max, % cas favorables, % dossiers non exploitables, dossiers pris en compte, dossiers non pris en compte]
    elif n > 0:
        trouve = False
        non_expl = len(sommes_ign)/n*100
        return [trouve, -1, -1, -1, -1, -1, '', '', -1, non_expl, dossiers, sommes, dossiers_ign]
    else:
        return [trouve, -1, -1, -1, -1, -1, '', '', -1, -1, [], [], []]


def afficher_stats(recherche, date_lim = '1900 01', juridiction = '', filename = "resume.txt", graph = True):
    stats = statistiques(recherche, date_lim, juridiction,filename)
    sommes = stats[11]

    if stats[0]:
        print('mediane :', stats[1], '€')
        print('moyenne :', stats[2], '€')
        print('ecart-type :', stats[3], '€')
        if stats[4] <= 0:
            print('perte maximale :', -stats[4], '€')
        else:
            print('gain minimum :', stats[4], '€')
        print('dossier (min) :', stats[6])
        if stats[5] <= 0:
            print('perte minimale :', -stats[5], '€')
        else:
            print('gain maximum :', stats[5], '€')
        print('dossier (max) :', stats[7])
        print('\n% de cas favorables :', stats[8])
    print('\n    dossiers exploités ', len(stats[10]), ':')
    for i in range(len(stats[10])):
        print(stats[10][i], ' ', stats[11][i], '€')
    print('\n% de dossiers non exploitables :', stats[9])
    print('\n    dossiers non exploités ', len(stats[12]), ':')
    for i in range(len(stats[12])):
        print(stats[12][i])

    if graph:
        graphique_stats(sommes)

def graphique_stats(sommes):
    for i in range(len(sommes)):
        sommes[i] = -sommes[i]
    
    m = sommes[0]
    for s in sommes:
        if s > m:
            m = s
    imax = int(m)//5000 + 2
    
    x = [-2500 + i*5000 for i in range(imax)]
    y = [0 for i in range(imax)]
    
    for s in sommes:
        y[int(s)//5000 + 1] += 1
    ym = y[0]
    for ye in y:
        if ye > ym:
            ym = ye

    plt.bar(x, y, 5000)
    plt.title('Distribution des pertes')
    plt.xlabel('Perte (€)')
    plt.ylabel('Nombre de cas')
    plt.axis([-5000, int(m)+10000, 0, ym+1])
    plt.grid()
    plt.show()
    

    
def inclu(sous_ens, ens):
    res = True
    for el in sous_ens:
        res = res and (el in ens)

    return res

def extract(chcar):
    out = []
    i = 0
    j = 0
    for letter in chcar:
        j += 1
        if letter == ';' or letter == '\n':
            out.append(chcar[i:j-1])
            i = j
            j = i
    return out

def moyenne(tab):
    m = 0
    n = 0
    for e in tab:
        m += e
        n += 1

    if n>0:
        return m/n
    else:
        return 0

def mediane(tab):
    n = len(tab)
    if n%2 == 1:
        return tab[n//2]
    elif n > 0:
        return (tab[n//2-1]+tab[n//2])/2
    else:
        return 0

def ecart_type(tab):
    if (len(tab) > 0):
        v = 0
        m = moyenne(tab)
        for e in tab:
            v += (e - m)*(e - m)

        v = v/len(tab)
        return sqrt(v)
    else:
        return 0

def Min(tab):
    k = 0
    m = tab[0]
    for i in range(len(tab)):
        if tab[i] < m:
            k = i
            m = tab[i]
    return [k, m]

def Max(tab):
    k = 0
    m = tab[0]
    for i in range(len(tab)):
        if tab[i] > m:
            k = i
            m = tab[i]
    return [k, m]
