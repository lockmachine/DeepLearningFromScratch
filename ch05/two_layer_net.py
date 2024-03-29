#!/usr/bin/env python3
# coding: utf-8
import sys, os
sys.path.append(os.pardir)
import numpy as np
#from common.layers import *
from my_layers import *
#from common.gradient import numerical_gradient
from ch04.numerical_gradient import numerical_gradient
from collections import OrderedDict

class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        # 重みの初期化
        self.param = {}
        self.param["W1"] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.param["W2"] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.param["b1"] = np.zeros(hidden_size)
        self.param["b2"] = np.zeros(output_size)
        
        # レイヤの生成
        self.layers = OrderedDict()
        self.layers["Affine1"] = myAffine(self.param["W1"], self.param["b1"])
        self.layers["Relu1"] = myRelu()
        self.layers["Affine2"] = myAffine(self.param["W2"], self.param["b2"])
        
        self.lastLayer = mySoftmaxWithLoss()
        
    def predict(self, x):
        """
        z1 = self.layers["Affine1"].forward(x)
        z2 = self.layers["Relu1"].forward(z1)
        y = self.layers["Affine2"].forward(z2)
        
        return y
        """
        for layer in self.layers.values():
            x = layer.forward(x)
        
        return x
        
    # x:入力データ, t:教師データ
    def loss(self, x, t):
        y = self.predict(x)
        
        return self.lastLayer.forward(y, t)
        
    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        if t.ndim != 1 : t = np.argmax(t, axis=1)
        
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy
        
    # x:入力データ, t:教師データ
    def numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss(x, t)
        
        grads = {}
        grads["W1"] = numerical_gradient(loss_W, self.param["W1"])
        grads["b1"] = numerical_gradient(loss_W, self.param["b1"])
        grads["W2"] = numerical_gradient(loss_W, self.param["W2"])
        grads["b2"] = numerical_gradient(loss_W, self.param["b2"])
        
        return grads
        
    def gradient(self, x, t):
        # forward
        self.loss(x, t)
        
        # backward
        dout = 1
        dout = self.lastLayer.backward(dout)
        
        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)
            
        # 設定
        grads = {}
        grads["W1"] = self.layers["Affine1"].dW
        grads["b1"] = self.layers["Affine1"].db
        grads["W2"] = self.layers["Affine2"].dW
        grads["b2"] = self.layers["Affine2"].db
        
        return grads
