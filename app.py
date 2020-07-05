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
    filename=data[14:-2]
    storage_path="Audio/"+filename
    try:
        storage = firebase.storage()
        storage.child(storage_path).download("downloaded.wav")
    except:
        print("Download Failed")
    
    
    p="downloaded"
    c=os.getcwd()
    
    ar_rate=articulation_rate(p,c)
    rate_sph=rate_of_speech(p,c)
    no_pause=number_of_pauses(p,c)
    speak_dur=speaking_duration(p,c)
    org_dur=original_duration(p,c)

    # send back to browser
    output = {'articulation rate': ar_rate,
             'rate of speech': rate_sph,
             'number of pauses': no_pause,
             'speking duration':speak_dur,
             'original duration': org_dur}
    
    # return data
    return output

######################################################

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

def rate_of_speech(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[2]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        print ("rate_of_speech=",z3,"# syllables/sec original duration")
    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3;

def number_of_pauses(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[1]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        print ("number_of_pauses=",z3)
    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3;

def speaking_duration(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[3]) # will be the integer number 10
        z4=float(z2[4]) # will be the floating point number 8.3
        print ("speaking_duration=",z4,"# sec only speaking duration without pauses")
    except:
        z4=0
        print ("Try again the sound of the audio was not clear")
    return z4;


def original_duration(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[3]) # will be the integer number 10
        z4=float(z2[5]) # will be the floating point number 8.3
        print ("original_duration=",z4,"# sec total speaking duration with pauses")
    except:
        z4=0
        print ("Try again the sound of the audio was not clear")
    return z4;

if __name__ == '__main__':
    app.run(port = 5000, debug=True,use_reloader=False)


# In[ ]:
