from apps.search.models import MotCle
from apps.search.models import Jugement

def machinelearning(a,b):
    
    return a+b


def Get_training_data_decision():
    Data=[] 
    for jugement in  Jugement.objects.all() :
        MotsCles_jugement = jugement.mots_cles()
        jugement.decision = 'F'|'M'|'D'
        in_data = [int(motCle in MotsCles_jugement) for motCle in MotCle.objects.all()] #in_data = [motCle in MotsCles_jugement for motCle in MotCle.objects.all()]
        out_data=[0,0]
        if jugement.decision == 'D':
            out_data[0]=1
        elif jugement.decision == 'M':
            continue
            out_data=0.5
        elif jugement.decision =='F':
            out_data[1]=1
        else:
            continue
        Data.append([in_data,out_data])
    return Data

def Get_training_data_somme():
    Data=[] 
    for jugement in  Jugement.objects.all() :
        MotsCles_jugement = jugement.mots_cles()
        jugement.decision = 'F'|'M'|'D'
        in_data = [int(motCle in MotsCles_jugement) for motCle in MotCle.objects.all()] #in_data = [motCle in MotsCles_jugement for motCle in MotCle.objects.all()]
        out_data=jugement.gain
        Data.append([in_data,out_data])
    return Data



