# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:38:52 2015

@author: armano
"""

import numpy as np

import math, cmath


# LOGARITHMS ...

def log2(x):    # evaluates log(p)
  if x < 0. or x > 1.: raise Exception
  if numbers.approx(x,0): return numbers.minimum
  return math.log(x,2)

def plog2(x,y=1.,z=1.):   # evaluates p*log(p)
  _min, _max = min(x,y,z), max(x,y,z)
  if _min < 0. or _max > 1.: raise Exception
  if numbers.approx(_min,0): return numbers.minimum
  _prod = x * y * z
  return _prod * math.log(_prod,2)


# NUMBERS ...

class numbers(object):

  maximum, minimum, epsilon = 10000000., -10000000., 0.00000001

  keys = [ 'linear', 'square', 'exp', 'log', 'log2' ]

  functions = [ lambda x: x, lambda x: x**2, math.exp, math.log, log2 ]
  
  fundict = { k : v for k, v in zip(keys,functions) }

  @staticmethod
  def approx(var,val):
    return abs(var-float(val)) < 0.0000001
  
  @staticmethod
  def erange(_min,_max,_intervals=10):
    _delta = abs(_max - _min) / _intervals
    _array = np.zeros(_intervals + 1)
    for k in xrange(_intervals+1): _array[k] = k * _delta
    return _array

  @classmethod
  def normalize_value(cls, value, _min = 0., _max = 1., _mode = 'linear'):
    _percent = abs ( value - _min ) / ( _max - _min )
    return cls.fundict[_mode] ( _percent )
  
  @staticmethod
  def normalize_values(values, _min = 0., _max = 1., _mode = 'linear'):
    fun = numbers.fundict[_mode]
    _out = [ fun ( abs ( val - _min ) / ( _max - _min ) ) for val in values ]
    return _out

  @staticmethod
  def check(fval, fvalues):
    for fvalue in fvalues:
      if numbers.approx(fval,fvalue): return True
    return False

    
# ARITHMETIC OPERATIONS ...

def mul(values):
  if values == list(): raise Exception
  _outvalue = 1.
  for v in values: _outvalue *= v
  return v
    

# STATS ...    

def average(X):
  return sum(X) / len(X)

def variance(X):
  if len(X) == 0: return 0.
  avg = average(X)
  _sum2 = sum([ (x -avg)**2 for x in X ])
  return _sum2 / ( len(X) - 1)

def std_deviation(X,Y):
  v2 = variance2(X,Y)
  return math.sqrt(v2)

def variance2(X,Y):
  if len(X) <> len(Y): raise Exception
  if len(X) == 0: return 0.
  Xavg, Yavg = average(X), average(Y)
  _sum2 = sum([ distance2((x,y),(Xavg,Yavg)) for x,y in zip(X,Y) ])
  return _sum2 / ( len(X) - 1)
  
def distance2(p1,p2):
  x,y = p1 ; z, w = p2
  return (x-z)**2 + (y-w)**2
  
def distance(p1,p2):
  d2 = distance2(p1,p2)
  return cmath.sqrt(d2)
  

if __name__ == '__main__':

  
  X, Y = range(10), range(10)
    
  Xavg, Yavg = average(X), average(Y)
  
  print "average X, Y"  
  print Xavg, Yavg
  
  
  v2 = variance2(X,Y)
  
  print "variance", v2
  
  d = std_deviation(X,Y)
  
  print "standard deviation", d
