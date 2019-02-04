#!/usr/bin/env python3
# coding: utf-8
import numpy as np

class SGD:
    def __init__(self, lr):
        self.lr = lr
        
    def update(self, params, grads):
        for key in params.keys():
            params[key] -= self.lr * grads[key]
            
class Momentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None
        
    def update(self, params, grads):
        # 最初に呼ばれた場合は v は params と同じ構造のデータをディクショナリ変数として保持する
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_lize(val)
                
        for key in params.keys():
            self.v[key] = self.momentum * self.v[key] - self.lr * grads[key]
            params[key] += self.v[key]