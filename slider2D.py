# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 17:17:27 2015

@author: armano
"""

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.widgets import Slider
from matplotlib.widgets import Button, RadioButtons, CheckButtons

from utils import str2float, wrapper, unzip2

from view import phidelta as phidelta_view

def ss2phidelta(spec,sens):
  if type(spec) is not np.ndarray: spec = np.array(spec)
  if type(sens) is not np.ndarray: sens = np.array(sens)
  return -spec + sens, spec + sens - 1
  
def ratio2negpos(ratio=1.):
  if ratio == 0.: ratio = 0.00001 # WORKAROUND ...
  neg, pos = float(ratio) / (ratio + 1.), 1. / (ratio + 1.)
  return neg, pos

def phidelta_std(spec,sens):
  "Evaluate phi, delta from sens, spec (standard version)"
  return -spec + sens, spec + sens - 1
  
def phidelta_std2gen(std_phi,std_delta,ratio=1.):
  "Conversion from phidelta standard to phidelta generalized"
  neg, pos = ratio/(1.+ratio), 1./(1.+ratio)  
  gen_phi = [ (neg - pos) * (1. - dlt) + phi for phi, dlt in zip(std_phi,std_delta) ]
  gen_delta = [ dlt - (neg-pos) * phi for phi, dlt in zip(std_phi,std_delta) ]
  return gen_phi, gen_delta


class slider2D(object):
  
  step = 0
  
  def __init__(self, view = None, points = None):
    self.view = view
    self.figure, self.ax = None, None
    self.resetax, self.rax = None, None
    self.neg_axes, self.pos_axes = None, None
    self.reset_button = None
    self.ratio, self.neg, self.pos = 1., 100, 100
    self.sneg, self.spos = None,None
    self.radio_buttons, self.check_options = None, None
    self.active_button_index, self.active_options = 6, (False, False, False, False)
    self.radio_labels = ('1/20','1/10','1/5','1/4','1/3','1/2','1','2','3','4','5','10','20')
    self.view_options = ('axes','crossings','fill')
    self.break_recurrent_calls = False
    self.points = points

  def show(self, figure = None, ax = None):
    wrap = wrapper(self)
    color = 'LightYellow'
    if figure is None: self.figure, self.ax = plt.subplots()
    self.ax.set_aspect('equal')
    plt.subplots_adjust(left=0.25, bottom=0.30)
    self.view.plot(self.figure,self.ax)
    plt.axis([-1, 1, -1, 1])
    self.neg_axes = plt.axes([0.25, 0.1, 0.65, 0.03])
    self.sneg = Slider(self.neg_axes, 'Neg Samples', 0.1, 100., valinit=50., valfmt='%4d')
    self.sneg.on_changed(wrap('update_neg'))
    self.pos_axes = plt.axes([0.25, 0.15, 0.65, 0.03])
    self.spos = Slider(self.pos_axes, 'Pos Samples', 0.1, 100., valinit=50., valfmt='%4d')
    self.spos.on_changed(wrap('update_pos'))
    self.resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    self.reset_button = Button(self.resetax, 'Reset', color=color, hovercolor='0.975')
    self.reset_button.on_clicked(wrap('reset'))
    self.rax = plt.axes([0.05, 0.5, 0.15, 0.4])
    self.rax.text(0., 1.05, r'ratio = neg/pos', fontsize=12, color='black')
    self.radio_buttons = RadioButtons(self.rax, self.radio_labels, active=6)
    self.adjust_radio_buttons()
    self.radio_buttons.on_clicked(wrap('radio'))
    self.cax = plt.axes([0.05, 0.25, 0.15, 0.2])
    self.check_options = CheckButtons(self.cax, self.view_options, self.active_options)
    self.check_options.on_clicked(wrap('check'))
    if self.points:
      phi, delta = self.points
      phi, delta = phidelta_std2gen(phi,delta,ratio=self.ratio)
      self.view.scatter2D(phi,delta,ax=self.ax)
    plt.show()

  def redraw(self, ratio = 1., items = list(), comment=''):
    self.redraw_phidelta(ratio=ratio)
    if 'radio'    in items: self.reset_radio_buttons()
    if 'ratio'    in items: self.redraw_neg_pos(ratio=ratio)
    
  def redraw_phidelta(self,ratio=1.):
    self.view.wipe_out(self.ax)
    self.view.update(ratio=ratio)
    phi, delta = self.points
    self.view.plot(self.figure,self.ax)
    phi, delta = phidelta_std2gen(phi,delta,ratio=ratio)
    self.view.scatter2D(phi,delta,ax=self.ax)
  
  def redraw_neg_pos(self,ratio=1.):
    neg, pos = ratio2negpos(ratio)
    self.break_recurrent_calls = True
    self.sneg.set_val(neg * 100.)
    self.break_recurrent_calls = True
    self.spos.set_val(pos * 100.)

  def adjust_radio_buttons(self):
    for c in self.radio_buttons.circles: c.height = 0.05
      
  def reset_radio_buttons(self):
    "Reset radio buttons (by default in the middle of the list)"
    default_active_index = 6
    active_index = self.active_button_index
    circles = self.radio_buttons.circles
    self.active_button_index = 6
    active_color = circles[active_index].get_facecolor()
    non_active_color = circles[default_active_index].get_facecolor()
    circles[active_index].set_facecolor(non_active_color)
    circles[default_active_index].set_facecolor(active_color)

  # EVENT HANDLERS ... (methods)

  def reset(self,event):
    "Reset the phi-delta diagram (with ratio = 1.0)"
    self.ratio, self.neg, self.pos = 1., 100, 100
    self.redraw(ratio = self.ratio, items = ('radio','ratio'),comment='from reset')
    
  def radio(self,ratio):
    "Handler for radio buttons (controls fixed amounts of neg/pos ratio)"
    self.active_button_index = self.radio_labels.index(ratio)
    self.ratio = str2float(ratio)
    self.redraw(ratio=self.ratio,items=('ratio'),comment='from radio')
    
  def check(self,choice):
    "Handler for check buttons (controls various show options)"
    print "Check ...", choice
    assert choice in self.view_options
    choice = choice.encode('ascii','ignore')
    self.view.toggle(choice)
    self.redraw(ratio = self.ratio,comment='from check')
    
  def update_neg(self,neg):
    "Handler for pos samples (also the ratio changes)"
    self.neg = int(neg)
    self.ratio = float(self.neg)/float(self.pos)
    if not self.break_recurrent_calls:
      self.redraw(ratio = self.ratio,items=('radio'),comment='from update_neg')
    self.break_recurrent_calls = False

  def update_pos(self,pos):
    "Handler for neg samples (also the ratio changes)"
    self.pos = int(pos)
    self.ratio = float(self.neg)/float(self.pos)
    if not self.break_recurrent_calls:
      self.redraw(ratio = self.ratio,items=('radio'),comment='from update_pos')
    self.break_recurrent_calls = False


if __name__ == '__main__':


  from utils import runCtrl

  run = runCtrl() << { 'file' : True, 'four_points' : False } # ONE should be true ...

  def load(filename, path='', sep=',', which=('spec','sens')):
    with open(path+filename) as infile:
      X, Y = unzip2([ line.strip().split(sep) for line in infile ])
      X, Y = [ float(x) for x in X ], [ float(y) for y in Y ]
      if which == ('spec','sens'): X, Y = ss2phidelta(X,Y)
      # print "LOAD X, Y = ", X, Y
      return X, Y

  if run['file']:
    phi, delta = load('test.csv')
  
  elif run['four_points']:
    spec, sens = unzip2 ( [ (0.95,0.95), (0.95,0.05), (0.05,0.95), (0.05,0.05) ] )
    phi, delta = ss2phidelta(spec,sens)
    # phi, delta = phi[1:2], delta[1:2]

  # Running the slider
    
  view = phidelta_view(ratio=1., labels = ('$\phi$','$\delta$', ''))
  view('borders')
  slider = slider2D(view=view,points=(phi,delta))
  slider.show()
  
  
  