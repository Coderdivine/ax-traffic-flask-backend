from flask import Flask, jsonify, request
from model import NeuralNetwork
import json
import requests
import pickle
import  numpy as np
import pandas as pd
app = Flask(__name__)
model = NeuralNetwork(lr=0.01,iter=31000)
#x  = np.random.randn(4,10)
#y = np.random.randn(1,)
@app.route("/train", methods=['GET'])
def trainData():
    data = requests.get("https://ax-traffic.herokuapp.com/get-data/passed")
    #data = requests.get("https://ax-short.herokuapp.com/link234tools-get")
    json_data = json.loads(data.content)
    result = list(json_data)
    df = pd.DataFrame(json_data)
    df = df.drop(["id"], axis=1)
    x =np.array(df.iloc[:,0:5].astype(int)).T
    y = np.array(df.iloc[:,5:].astype(int)).T
    model.fit(x,y)
    print(x)
    print(y)
    pickle.dump(model,open("models.pkl", "wb"))
    return jsonify({"data":{
        "length_of_data":len(result),
        "accuracy":"check prediction"
    }})
@app.route("/predict", methods=['GET','POST'])
def predict():
    data = np.array([[1,2,3,4,]]).T
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        print(json)
    """
    if request.method =="POST":
        jsons = request.get_json()
        print(jsons)
        period,long,lat,date = jsons
        data = np.array([[period,long,lat,date]]).T
    """
    model = pickle.load(open("model.pkl", "rb"))
    pred = model.prediction(data)
    preds = model.NewRoadSpeed(float(pred[0][0]))
    return jsonify({
        "data":[{
            "pred":pred[0][0],
            "speedlimits":preds
        }]
    })
    

if __name__ == '__main__':
    app.run(debug=True)
