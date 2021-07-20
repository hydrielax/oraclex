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



import tensorflow as tf

from tensorflow.keras.callbacks import TensorBoard

import random
import time
import numpy as np
import pickle
def model_ia(Xnew):
    print(Xnew)
    Xnew.extend([0,0,0])
    
    Xnew=np.array(Xnew)
    
    Xnew=np.asarray(Xnew).astype(np.int)
    print(Xnew)
    model = tf.keras.models.load_model(r"C:\Users\anass\Programmation\ML\predict.model")
    #with open('./predict.model', 'r') as f:
    #    model = tf.keras.models.load_model(f.read())
    ynew = model.predict_proba(np.expand_dims(Xnew, axis=0)) 
    return ynew[0]
Xnew = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]

#ynew = model.predict_proba(np.expand_dims(Xnew, axis=0))
#print(ynew)
