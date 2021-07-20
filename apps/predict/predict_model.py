from apps.search.models import MotCle
from apps.search.models import Jugement
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
import random
import numpy as np

#model = tf.keras.models.load_model("predict.model")

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


def model_ia(Xnew):
    print(Xnew)
    Xnew.extend([0,0,0])
    Xnew=np.array(Xnew)
    Xnew=np.asarray(Xnew).astype(np.int)
    model = tf.keras.models.load_model("predict.model")
    ynew = model.predict_proba(np.expand_dims(Xnew, axis=0)) 
    return ynew[0]

#model = tf.keras.models.load_model("predict.model")

def model_ia2(Xnew,model=model):
    X_input=np.array(Xnew)
    given_input=np.shape(X_input)[0]
    X_input=np.asarray(X_input).astype(np.int)
    if model is not None :
        shape_input=model.layers[0].input_shape
        model_input=shape_input[1]
        if given_input == model_input :
            output = model.predict_proba(np.expand_dims(X_input, axis=0)) 
            return output[0]
        else:
            model=train_model()
            return model_ia2(Xnew,model)
    else :
        model = tf.keras.models.load_model("predict.model")
        return model_ia2(Xnew,model)


def train_model():
    #Bring data:
    training_data = Get_training_data_decision()
    random.shuffle(training_data)
    X=[]
    y=[]
    for file_data, categ in training_data :
        X.append(file_data)
        y.append(categ)
    X=np.array(X)
    y=np.array(y)
    N=np.shape(X)[1]
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(input_shape=(N,), units=N, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(2,activation=tf.nn.softmax))
    model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    model.fit(X,y,epochs=50, batch_size=32,validation_split=0.25) #to  change
    #model.save("predict.model")
    #print(model.summary())
    return model #Quoi ?????