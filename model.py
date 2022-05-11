import numpy as np
import pickle
import requests
class NeuralNetwork:
    def __init__(self,lr=0.01,hidden=5,iter=3500):
        self.iter = iter
        self.lr =lr
        self.hidden = hidden
        self.w1 =None
        self.w2 =None
        self.b1 =None
        self.b2 =None
        
    def fit(self,x,y):
        self.w1 =np.random.randn(self.hidden,len(x))*0.01
        self.w2 =np.random.randn(1,self.hidden)*0.01
        self.b1 =np.zeros((self.hidden,1))
        self.b2 =np.zeros((1,1))
        
        for _ in range(self.iter):
            z1 =np.dot(self.w1,x)+self.b1
            a1 =np.tanh(z1)
            z2 =np.dot(self.w2,a1)+self.b2
            a2=1/(1+np.exp(-z2))
            m =y.shape[1]
            dz2 = a2-y
            dw2 = (1/m)*np.dot(dz2,a1.T)
            db2 = (1/m)*np.sum(dz2,axis=1,keepdims=True)

            dz1 = np.dot(self.w2.T,dz2) * (1-np.power(z1,2))
            dw1 = (1/m)*np.dot(dz1,x.T)
            db1 = (1/m)*np.sum(dz1,axis=1,keepdims=True)
            self.w1 = self.w1 - (self.lr*dw1)
            self.w2 = self.w2 - (self.lr*dw2)
            self.b1 = self.b1 - (self.lr*db1)
            self.b2 = self.b2 - (self.lr*db2)
         

    def predict(self,x):
        z1 =np.dot(self.w1,x)+self.b1
        a1 =np.tanh(z1)
        z2 =np.dot(self.w2,a1)+self.b2
        a2=1/(1+np.exp(-z2))
        return a2
    def NewRoadSpeed(self,pred):
        #pred = pred[0] if len(pred)>1 else pred
        ts = 120
        yhat = pred*100
        a0 = pred*yhat
        eq0 = pred+ts
        eq1 = pred/(ts-eq0)
        eq2 = ((ts-yhat)/eq1)*((ts+yhat)/eq1)
        eq3 = eq2*ts
        eq4  = (ts+yhat)/eq3
        eq5 = a0 - (eq4*3.9)
        cd  = round(eq5)
        new_var =[cd]
        for i in range(5):
            values = new_var[len(new_var)-1] + cd
            new_var.append(values)
        how = ""
        if pred <= 35:
            how = "normal"
        elif pred <= 50:
            how = "low"
        else:
            how = "high"
        caching = {
            "pred":pred,
            "speed_limits":new_var,
            "how":how
        }
        return caching
print("working")
x  = np.random.randn(4,10)
y = np.random.randn(1,10)
#model = NeuralNetwork()
#model.fit(x,y)
#pickle.dump(model,open("model.pkl", "wb"))
data = np.array([[1.3,2.4,1.6,1.12]]).T
#model = pickle.load(open("model.pkl", "rb"))
#a2 = model.predict(data)
#a2 = model.NewRoadSpeed(float(a2[0]))


