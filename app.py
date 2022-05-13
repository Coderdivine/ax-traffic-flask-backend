from flask import Flask, jsonify, request
from model import NeuralNetwork
import json
import requests
import pickle
import  numpy as np
import pandas as pd
app = Flask(__name__)
model = NeuralNetwork(lr=0.01,iter=200)
#x  = np.random.randn(4,10)
y = np.random.randn(1,)
@app.route("/train", methods=['GET'])
def trainData():
    #data = requests.get("https://ax-traffic.herokuapp.com/get-data/passed")
    data = requests.get("https://ax-short.herokuapp.com/link234tools-get")
    json_data = json.loads(data.content)
    result = list(json_data)
    df = pd.DataFrame(json_data)
    df = df.drop(["longURL","date","shortURL"], axis=1)
    x =np.array(df.iloc[:,0:3].astype(int)).T
    y = np.array(df.iloc[:,3:].astype(int)).T
    model.fit(x,y)
    pickle.dump(model,open("models.pkl", "wb"))
    return jsonify({"data":{
        "length_of_data":len(result),
        "accuracy":"check prediction"
    }})
@app.route("/predict", methods=['GET','POST'])
def predict():
    """
    time = request.form["time"]
    period =  request.form["period"]
    long = request.form["long"]
    lat = request.form["lat"]
    data = np.array([[time,period,long,lat]])
    model = pickle.load(open("model.pkl", "rb"))
    pred = model.predict(data)
    listed = model.NewRoadSpeed(pred[0])
    """
    xtest = np.random.choice([1.45,3.45,6.97,2.83],size=(1,3)).T
    model = pickle.load(open("models.pkl", "rb"))
    a2 = model.predict(xtest) 
    cost = model.cost(y,a2)  
    pred = model.NewRoadSpeed(float(a2[0][0]))
    return jsonify({"data":[{
        "data":xtest[0][0],
        "pred":a2[0][0]
    },
    {
        "speed":pred,
        "cost":cost
    }]})
    

if __name__ == '__main__':
    app.run(debug=True)
