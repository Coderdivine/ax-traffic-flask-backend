from flask import Flask, jsonify, request
from model import NeuralNetwork
import json
import requests
import pickle
import  numpy as np
import pandas as pd
app = Flask(__name__)
model = NeuralNetwork(lr=0.01,iter=24000)
x  = np.random.randn(4,10)
y = np.random.randn(1,10)
@app.route("/train", methods=['GET'])
def trainData():
    #data = requests.get("https://ax-traffic.herokuapp.com/get-data/passed")
    data = requests.get("https://ax-short.herokuapp.com/link234tools-get")
    json_data = json.loads(data.content)
    #df = pd.read_json(json_data)
    #x =np.array(df.iloc[:,0:6])
    #y = np.array(df.iloc[:,6:])
    #model.fit(x,y)
    #pickle.dump(model,open("model.pkl", "wb"))
    return jsonify({"data":True})
@app.route("/predict", methods=['GET','POST'])
def predict():
    #time = request.form["time"]
    #period =  request.form["period"]
    #long = request.form["long"]
    #lat = request.form["lat"]
    #data = np.array([[time,period,long,lat]])
    #model = pickle.load(open("model.pkl", "rb"))
    #pred = model.predict(data)
    #listed = model.NewRoadSpeed(pred[0])
    x  = np.random.choice([1.85,1.65,1.35,2.23,6.43,0.1,0.25],size=(60,4))
    y = np.random.choice([1.85,2.65,3.35,4.25,5.23,6.43],size=(60,1))
    model = NeuralNetwork(lr=0.01,iter=8000)
    x = x.T
    y = y.T
    xtest = np.random.choice([1.45,3.45,6.97,2.83],size=(3,4)).T
    model.fit(x,y)
    pickle.dump(model,open("models.pkl", "wb"))
    model = pickle.load(open("models.pkl", "rb"))
    a2 = model.predict(xtest)
    
    pred = model.NewRoadSpeed(float(a2[0][2]))
    return jsonify({"data":[{
        "data":xtest[0][0],
        "pred":a2[0][0]
    },{
        "data":x[0][0],
        "pred":y[0][0]
    },{
        "speed":pred
    }]})
    

if __name__ == '__main__':
    app.run(debug=True)
