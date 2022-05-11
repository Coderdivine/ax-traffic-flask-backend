from flask import Flask, jsonify, request
from model import NeuralNetwork
import json
import requests
import pickle
import  numpy as np
import pandas as pd
app = Flask(__name__)
model = NeuralNetwork(lr=0.01,iter=100)
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
    return jsonify({"data":json_data})
@app.route("/predict", methods=['GET','POST'])
def predict():
    time = request.form["time"]
    period =  request.form["period"]
    long = request.form["long"]
    lat = request.form["lat"]
    data = np.array([[time,period,long,lat]])
    model = pickle.load(open("model.pkl", "rb"))
    pred = model.predict(data)
    listed = model.NewRoadSpeed(pred[0])
    return jsonify({"data":listed})
    

if __name__ == '__main__':
    app.run(debug=True)
