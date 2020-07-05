#!/usr/bin/env python
# coding: utf-8




from flask import Flask, jsonify, request
import pyrebase
import os as os
import parselmouth
from parselmouth.praat import call, run_file
import glob
import pandas as pd
import numpy as np
import scipy
from scipy.stats import binom
from scipy.stats import ks_2samp
from scipy.stats import ttest_ind
import os

from flask import Flask, jsonify, request
import pickle


config={
    "apiKey": "AIzaSyDeFLJFr2aqcAK40nZOmBtEDNYij49yyAk",
    "authDomain": "healdon-916dd.firebaseapp.com",
    "databaseURL": "https://healdon-916dd.firebaseio.com",
    "projectId": "healdon-916dd",
    "storageBucket": "healdon-916dd.appspot.com",
    "messagingSenderId": "756073662506",
    "appId": "1:756073662506:web:2f4cb2e5e93f1d4b9d1b53"
}
firebase=pyrebase.initialize_app(config)

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = request.get_json(force=True)

    path=os.getcwd()
    
    p="27 sec clip"
    c=path
    
    ar_rate=obj.articulation_rate(p,c)
    
    #storage = firebase.storage()
    #storage.child("Audio/27 sec clip.wav").download("downloaded.wav")
    # predictions
    #result = model.predict(data_df)

    # send back to browser
    #output = {'results': int(result[0])}
    output = {'articulation rate': ar_rate}
    
    # return data
    return jsonify(results=output)

def articulation_rate(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[3]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        print ("articulation_rate=",z3,"# syllables/sec speaking duration")
    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3;

if __name__ == '__main__':
    app.run(port = 5000, debug=True,use_reloader=False)


# In[ ]:
