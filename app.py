from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_classification_model.pkl', 'rb'))
@app.route('/',methods=['GET'])

def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])

def predict():
    if request.method == 'POST':
        Warehouse_block = request.form['Warehouse_block']
        if Warehouse_block == 'B':
            Warehouse_block_B = 1
            Warehouse_block_C = 0
            Warehouse_block_D = 0
            Warehouse_block_F = 0
        elif Warehouse_block == 'C':
            Warehouse_block_C = 1
            Warehouse_block_B = 0
            Warehouse_block_D = 0
            Warehouse_block_F = 0
        elif Warehouse_block == 'D':
            Warehouse_block_D = 1
            Warehouse_block_B = 0
            Warehouse_block_C = 0
            Warehouse_block_F = 0
        elif Warehouse_block == 'F':
            Warehouse_block_F = 1
            Warehouse_block_B = 0
            Warehouse_block_C = 0
            Warehouse_block_D = 0
        else:
            Warehouse_block_B = 0
            Warehouse_block_C = 0
            Warehouse_block_D = 0
            Warehouse_block_F = 0
            
        Mode_of_Shipment = request.form['Mode_of_Shipment']
        if Mode_of_Shipment == 'Flight':
            Mode_of_Shipment = 0
        elif Mode_of_Shipment == 'Road':
            Mode_of_Shipment = 1
        elif Mode_of_Shipment == 'Ship':
            Mode_of_Shipment = 2
        Cost_of_the_Product=int(request.form['Cost_of_the_Product'])
        Discount_offered = int(request.form['Discount_offered'])
        Weight_in_gms=int(request.form['Weight_in_gms'])
        Customer_rating = int(request.form['Customer_rating'])
        Customer_care_calls = int(request.form['Customer_care_calls'])
        Prior_purchases = int(request.form['Prior_purchases'])
        Product_importance=request.form['Product_importance']
        if Product_importance == 'low':
            Product_importance = 0
        elif Product_importance == 'medium':
            Product_importance = 1
        elif Product_importance == 'high':
            Product_importance = 2
        Gender = request.form['Gender']
        if Gender == 'M':
            Gender = 1
        elif Gender == 'F':
            Gender = 0
        
        prediction=model.predict([[Mode_of_Shipment,Customer_care_calls,Customer_rating,Cost_of_the_Product,Prior_purchases,
                                   Product_importance,Gender,Discount_offered,Weight_in_gms,Warehouse_block_B,
                                   Warehouse_block_C,Warehouse_block_D,Warehouse_block_F]])
        output=prediction[0]
        if output == 1:
            return render_template('index.html',prediction_texts="Order will be on time")
        elif output == 0:
            return render_template('index.html',prediction_text="order will be delayed")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

