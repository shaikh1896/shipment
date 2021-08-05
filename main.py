from flask import Flask, render_template, request
import jsonify
import requests
import pickle
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
        Mode_of_Shipment=float(request.form['Mode_of_Shipment'])
        Cost_of_the_Product=int(request.form['Kms_Driven'])
        Discount_offered = int(request.form['Discount_offered'])
        Weight_in_gms=int(request.form['Weight_in_gms'])
        Customer_rating = int(request.form['Customer_rating'])
        Customer_care_calls = int(request.form['Customer_care_calls'])
        Prior_purchases = int(request.form['Prior_purchases'])
        Product_importance=request.form['Product_importance']
        Gender = request.form['Gender']
        if(Gender =='M'):
                Gender = 1
        elif (Gender =='F'):
            Gender = 0
            
        prediction=model.predict([[Warehouse_block, Mode_of_Shipment, Customer_care_calls,
                                   Customer_rating, Cost_of_the_Product, Prior_purchases,
                                   Product_importance, Gender, Discount_offered, Weight_in_gms]])
        output=round(prediction[0],2)
        if output==1:
            return render_template('index.html',prediction_texts="Order will be on time")
        else:
            return render_template('index.html',prediction_text="order will be delayed".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
