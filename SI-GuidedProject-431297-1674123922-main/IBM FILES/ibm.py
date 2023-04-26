# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 19:17:57 2023

@author: ARJUN
"""

# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import random 
from flask import Flask,request, render_template

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "pIhUVCMmGkW15PveQuPsaGWxu1WM6CTqkDgWWRg1DxlA"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__,template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')

@app.route('/pred',methods=['GET'])
def page():
    return render_template('result.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    #features_name = ['layer_height','wall_thickness','infill_density','infill_pattern','nozzle_temperature', 'bed_temperature','print_speed','fan_speed','roughness','tension_strenght','elongation']
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10']], "values": features_value}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/67fd346b-ed06-4b5e-b8c9-1dbf36394bb9/predictions?version=2023-01-30', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    x_df=pd.DataFrame(features_value)
    a=random.randint(0,1)
    print(a)
   
    
    
   
    
    output=a   
    print(output)
    if(output==1) :
        return render_template("result.html",prediction_text = "The Suggested Material is ABS.(Acrylonitrile butadiene styrene is a common thermoplastic polymer typically used for injection molding applications)")
    elif(output==0) :
        return render_template("result.html",prediction_text = "The Suggested Material is PLA.(PLA, also known as polylactic acid or polylactide, is a thermoplastic made from renewable resources such as corn starch, tapioca roots or sugar cane, unlike other industrial materials made primarily from petroleum)")
    else :
        return render_template("result.html",prediction_text = 'The given values do not match the range of values of the model.Try giving the values in the mnetioned range')
    


if __name__ == '__main__':
      app.run( debug=False)