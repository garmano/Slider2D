# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 15:36:48 2014

@author: armano
"""

import datetime

import math

import numpy as np

from itertools import chain, combinations

# INSPECTING OBJECTS ...

def keys(obj):
  if type(obj) == str: return "string"
  if type(obj) == tuple: return "tuple"
  if type(obj) == list: return "list"
  if type(obj) == dict: return obj.keys()
  return obj.__dict__.keys()

def summary(obj, _to = 80):
  if type(obj) == str: return "string"
  if type(obj) == tuple: return "tuple"
  if type(obj) == list: return "list"
  if type(obj) == dict: return obj.keys()
  return [ ( key, str(val)[:_to] ) for key, val in obj.__dict__.items() ]

# LISTS, TUPLES AND SETS ...

def powerset(items, duplicates = True):
  _powerset = chain(*map(lambda k: combinations(items,k),range(len(items)+1)))
  if duplicates: return list(_powerset)
  return list(_powerset)[1:2**len(items)/2]

# EVENTS HANDLING ...

class singleton(object):

  def __init__(self, cls):
    self.cls, self.obj = cls, None
    
  def __call__(self, *args, **kwargs):
    if not self.obj: self.obj = self.cls(*args,**kwargs)
    return self.obj

class eventHandler(object):
  
  "Event Handler"
  
  def __init__(self,obj,method_name):
    "Initialize an eventHandler with dst object and method name"
    self.obj, self.method_name = obj, method_name
    
  def __call__(self, *args, **kwargs):
    "Perform delegation on the dst object"
    return getattr(self.obj,self.method_name)(*args,**kwargs)

class wrapper(object):

  "Wrapper of methods (from method to function object)"
  
  def __init__(self, obj):
    "Initialize a wrapper (remember the dst object)"
    self.obj = obj
    
  def __call__(self, methodname):
    "Generate the function object that will handle the event"
    #print "WRAPPER: wrapping method %s for object %s" % ( methodname, self )
    return eventHandler(self.obj,methodname)

# KWARGS HANDLING ...

def check_kwargs(kwargs, default_kwargs):
  for key, val in default_kwargs.items():
    if not key in kwargs: kwargs[key] = val
  return kwargs

def get_kwargs(kwargs, *keys):
  return [ kwargs.get(key,None) for key in keys ]

class runCtrl(object):
  
  "Utility for selecting which SW procedures should be run"
  
  def __init__(self,*args,**kwargs):
    if not hasattr(self,'runDict'): self.runDict = dict()
    for key, val in kwargs.items():
      self.runDict[key] = bool(val)
    for arg in args: self.runDict[arg] = True
    return
    
  def __call__(self,*args,**kwargs):
    self.__init__(*args,**kwargs)
    
  def __lshift__(self,kwargs):
    if not kwargs: return
    if type(kwargs) is str: kwargs = { kwargs : True }
    if type(kwargs) in [tuple,list]: kwargs = { key : True for key in kwargs }
    self.__init__(**kwargs)
    return self
    
  def __getitem__(self,key):
    return self.runDict.get(key)
    
  def __delitem__(self,key):
    if key in self.runDict: del self.runDict[key]
      
  def __str__(self):
    return str(self.runDict)

# DATE AND TIME

def get_date_and_time():
  dt = datetime.datetime.now()
  dt = str(dt)[:-10]
  dt = ''.join(c if not c in ':' else ' ' for c in dt)
  return dt


# STRINGS ...

def str2float(val):
  if not '/' in val: return float(val)
  a,b = val.split('/')
  return float(a)/float(b)


# LISTS / TUPLES / ARRAYS ...

def unzip(values): # NOT WORKING ON ARRAYS 
  if type(values) in (tuple,list) and len(values) == 0: return list() 
  num_lists = len(values[0])
  _outlist = [ list() for k in xrange(num_lists) ]
  for item in values:
    for k in range(num_lists):
      _outlist[k] += [ item[k] ]
  return _outlist

def unzip2(values):
  xy_values = values  
  xvalues = [ x for x, y in xy_values ]
  yvalues = [ y for x, y in xy_values ]
  return xvalues, yvalues
  
def flatten(values): # for arrays only ...
  _shape = values.shape
  values.shape = values.size
  return _shape

# DICTIONARIES ...

def multiple_get(dictionary,keywords,default=None):
  if not type(default) in (tuple,list): default = [ default for k in keywords ]
  return [ dictionary.get(key,value) for key, value in zip(keywords,default) ]

# NUMBERS, etc.

def numeric(item):
  if type(item) == str: return False
  try: float(item)
  except: return False
  return True


