from apps.search.models import MotCle
from apps.search.models import Jugement
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
from threading import Timer, Thread
# import tensorflow.keras as tk
import random
import numpy as np



model_file = None

def Get_training_data_decision():
    Data=[] 
    for jugement in  Jugement.objects.all() :
        MotsCles_jugement = jugement.mots_cles.all()
        decision = jugement.decision
        in_data = [int(motCle in MotsCles_jugement) for motCle in MotCle.objects.all()] 
        out_data=[0,0]
        if decision == 'D':
            out_data[0]=1
        elif decision == 'M':
            continue
            out_data[0]=0.5
            out_data[1]=0.5
        elif decision =='F':
            out_data[1]=1
        else:
            continue
        Data.append([in_data,out_data])
    return Data





def model_ia(Xnew):
    X_input=np.array(Xnew)
    given_input=np.shape(X_input)[0]
    X_input=np.asarray(X_input).astype(np.int)
    global model_file
    if model_file :
        shape_input=model_file.layers[0].input_shape
        model_input=shape_input[1]
        if given_input == model_input :
            output = model_file.predict_proba(np.expand_dims(X_input, axis=0)) 
            return output[0]
        else:
            model_file=train_model()
            return model_ia(Xnew)
    else :
        try :
            model_file = load_model('media/predict/prediction_model')
        except :
            model_file=train_model()
        finally:
            return model_ia(Xnew)


def train_model():
    #Bring data:
    training_data = Get_training_data_decision()
    #randomize the order
    random.shuffle(training_data)
    X=[]
    y=[]
    for file_data, categ in training_data :
        X.append(file_data)
        y.append(categ)
    X=np.array(X)
    y=np.array(y)
    N=np.shape(X)[1]
    #create and train the model
    model_file = tf.keras.models.Sequential()
    model_file.add(tf.keras.layers.Dense(input_shape=(N,), units=N, activation=tf.nn.relu))
    #model_file.add(tf.keras.layers.Dense(N-7, activation=tf.nn.relu))
    model_file.add(tf.keras.layers.Dense(2,activation=tf.nn.softmax))
    model_file.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    model_file.fit(X,y,epochs=50, batch_size=32,validation_split=0.25) #to  change
    model_file.save("media/predict/prediction_model")
    #print(model.summary())
    return model_file 



def retraining():
    while True:
        last_file_count = Jugement.objects.all().count()
        now = datetime.now()
        delta = (6 - now.weekday()) % 7
        week = timedelta(days=7) if delta==0 else timedelta(days=delta)
        def retrain():
            if last_file_count < Jugement.objects.all().count(): train_model()
        thread = Timer(week.total_seconds(), retrain)
        thread.start()
        thread.join()

Thread(target=retraining, daemon=True).start()



#########Pour La Somme########
def Get_training_data_somme():
    Data=[] 
    for jugement in  Jugement.objects.all() :
        MotsCles_jugement = jugement.mots_cles()
        jugement.decision = 'F'|'M'|'D'
        in_data = [int(motCle in MotsCles_jugement) for motCle in MotCle.objects.all()] #in_data = [motCle in MotsCles_jugement for motCle in MotCle.objects.all()]
        out_data=jugement.gain
        Data.append([in_data,out_data])
    return Data