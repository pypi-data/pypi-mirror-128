#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

class EnviromentInterface:
    def model_saving(self, model, path: str):
        # interface
        pass

# # Imput formater

class BaseInputFormater(ABC):
 
    @abstractmethod
    def format_data(self):
        raise Exception("BaseInputFormater format_data Override")
    
    @abstractmethod
    def format_label(self, label):
        raise Exception("BaseInputFormater format_label Override")

# # Loss Function

class BaseLossFunction(ABC):
    @abstractmethod
    def loss(self, preds, labels):
        raise Exception("CustomLossFunction format_data Override")
        
    @abstractmethod
    def get_loss(self):
        raise Exception("CustomLossFunction format_data Override")

# # Accuracy Function

from torchnet import meter

class BaseAccuracyFunction(ABC):
    @abstractmethod
    def get_acc(self, preds, labels):
        raise Exception("AccuracyFunction format_data Override")

# # Optimizer Funtion

class BaseOptimizerFunction(ABC):
    _optimizer = None
    
    _weight_decay = None
    _lr = None
    _lr_decay = None
    
    @abstractmethod
    def create(self, model):
        raise Exception("OptimizerFunction create Override")
        
    @abstractmethod
    def get_optimizer(self):
        raise Exception("OptimizerFunction get_optimizer Override")

# # Sheduler

class BaseSchedulerFuntion(ABC):
    _scheduler = None
    
    _mode = 'min'
    _patience = 1
    _verbose = True
    
    @abstractmethod
    def create(self, optimizer):
        raise Exception("SchedulerFuntion create Override")
        
    @abstractmethod
    def get_scheduler(self):
        raise Exception("SchedulerFuntion get_scheduler Override")
