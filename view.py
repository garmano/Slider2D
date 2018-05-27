# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 13:50:14 2014

@author: armano
"""

#import seaborn as sns

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from utils import unzip2, multiple_get
from math_utils import numbers
#from model import phidelta as phidelta_model

from geometry import Geometry


cmaps = { 'Sequential':     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'],
          'Sequential (2)': ['afmhot', 'autumn', 'bone', 'cool', 'copper',
                             'gist_heat', 'gray', 'hot', 'pink',
                             'spring', 'summer', 'winter'],
          'Diverging':      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic'],
          'Qualitative':    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3'],
          'Miscellaneous':  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism']}

class phidelta(Geometry):
  
  __keywords__ = { 'labels', 'mode', 'projection', 'show', 'visible' }

  __enum1__ = { 'mode': set(('ss_grid', 'grid', 'entropy', 'IG')) }
  __enum2__ = { 'labels': (r'$\varphi$',r'$\delta$', r'entropy' or r'IG') }
  __enum3__ = { 'axes':True, 'borders':True, 'crossing':True, 'projection':None }
  
  __exports1__ = [ '__init__', '__call__', 'attach' ]
  __exports2__ = [ 'plot', 'scatter2D', 'scatter3D' ]

  #borders = property(lambda self: self.model.borders) # delegation to model
  #limits = property(lambda self: self.model.limits) # delegation to model

  def __init__(self, ratio=1., labels = (r'$\varphi$',r'$\delta$', '')):
    "Initialize a phidelta_view object"
    super(phidelta,self).__init__(ratio=ratio)
    #self.model = model
    self.labels = labels
    self.projection = '2d' # default
    self.show_options = set(['borders','axes'])
    self.visible = False
    self.points = list()
    self.figure, self.ax = None, None
    
  def __call__(self, *args):
    "Tool for setting which elements should be drawn"
    self.show_options = set(list(args))
    return self
    
  def toggle(self,arg):
    "Tool for controlling which elements should be drawn"
    print "before toggle: show_options", type(self.show_options), self.show_options
    print "before toggle:          arg", type(arg), arg
    if arg in self.show_options: self.show_options.remove(arg)
    else: self.show_options.add(arg)
    print "after  toggle: show_options", type(self.show_options), self.show_options

  def set(self, **kwargs):
    "Tool for setting relevant parameters before visualization"
    for key, val in kwargs.items():
      if key in phidelta.__keywords__:
        setattr(self,key,val)
    return self

  def get(self,*slots):
    if not slots: return None
    return [ getattr(self,slot,None) for slot in slots ]

  def plot(self, figure=None, ax=None):
    "Shows a rhombus"
    if not figure:
      figure = plt.figure()
      projection = '3d' if self.projection == '3d' else None
      ax = figure.add_subplot(111, aspect = 'equal', projection=projection)
      #ax.imshow(self.gradient, aspect='auto', cmap=plt.get_cmap(palette))
      #ax.set_autoscale_on(False)
      #print self.show_options
    self.set_limits(ax, projection = self.projection)
    self.set_labels(ax, projection = self.projection)
    if 'axes'      in self.show_options: self.draw_axes(ax)
    if 'borders'   in self.show_options: self.draw_borders(ax)
    if 'crossings' in self.show_options: self.draw_crossings(ax)
    if 'fill'      in self.show_options: self.fill(ax)
    if 'recall'    in self.show_options: self.draw_recall(ax)
    if 'precision' in self.show_options: self.draw_precision(ax)
    self.visible = True
    return ax

  def draw_lines(self, SRC, DST, ax = None, style = '--' ):
    if not ax: ax = self.plot()
    lineparams = { 'linewidth':1, 'color':'blue', 'linestyle' : style }
    for src, dst in zip(SRC,DST):
      x, y = src ; z, w = dst
      ax.add_line(plt.Line2D((x,z), (y,w), **lineparams))

  def scatter2D ( self, X, Y, colors = None, color = None, title = '', ax = None, legend = False ):
    "Scattering 2D (the optional parameter C may control colors)"
    _size = 8.
    self.projection = '2d'
    if not ax: ax = self.plot()
    if type(color) == int:
      self.points += [ ax.scatter ( X, Y, s = _size, c=str(color), alpha = 0.75, zorder=3 ) ]
    if type(color) == str:
      self.points += [ ax.scatter ( X, Y, s = _size, c=color, alpha = 0.75, zorder=3 ) ]
    else:
      if colors is None: colors = [ 0. for x in X ]
      #colors = [ str(numbers.normalize_value(value)) for value in colors ]
      cm = plt.cm.get_cmap('gnuplot2') # map = 'gnuplot2' | 'RdYlBu' | 'PiYG'
      self.points += [ ax.scatter ( X, Y, s=_size, c = colors, alpha = 0.75, zorder=3, cmap = cm ) ]
      ax.legend()
    if title: self.set_title_options(title,ax=ax)
    plt.show()
    self.ax = ax
    return ax
    
  def set_title_options(self,title,ax=None,pos=(0.35, 1.04)):
    if not ax: return
    options = { 'verticalalignment' : 'bottom', 'horizontalalignment' : 'right',
                'transform' : ax.transAxes, 'color' : 'green', 'fontsize' : 14 }
    xpos, ypos = pos
    ax.text ( xpos, ypos, title, **options )
    return ax

  def scatter3D(self, X, Y, Z, colors = None, ax = None):
    "Scattering 3D (the optional parameter C may control colors)"
    self.projection = '3d'
    if not ax: ax = self.plot()
    zeros = np.zeros(len(X))
    self.points += [ ax.scatter ( X, Y, zeros, color = '0.75', alpha=0.5) ]
    if colors is None: colors = Z
    self.colors = colors = [ numbers.normalize_value(value) + 100. for value in colors ]
    #ax.set_xlim3d(-1.,1.) ; ax.set_ylim3d(-1.,1.) ; ax.set_zlim3d(0.,1.)
    ax.set_ylim3d(-1.,1.) ; ax.set_zlim3d(0.,1.)
    self.points += [ ax.scatter ( X, Y, Z, c=colors, alpha=0.75, zorder=3 ) ]
    #plt.show()
    return ax

  def set_labels(self, ax, projection = '2d', labels = None):
    "Sets labels of a rhombus"
    if not labels: labels = self.labels
    xlabel, ylabel, zlabel = labels
    xfontsize = 22 if len(xlabel) < 5 else 16 
    yfontsize = 22 if len(ylabel) < 5 else 16 
    ax.set_xlabel(xlabel,fontsize=xfontsize)
    ax.set_ylabel(ylabel,fontsize=yfontsize)
    if projection == '3d': ax.set_zlabel(zlabel,fontsize=12)

  def get_labels ( self, mode = ('grid', 'entropy') ):
    Xlabel = 'specificity' if 'ss_grid' in mode else r'$\varphi$'
    Ylabel = 'sensitivity' if 'ss_grid' in mode else r'$\delta$'
    #Xlabel = r'$\bar{\rho}$' if 'ss_grid' in mode else r'$\varphi$'
    #Ylabel = r'$\rho$' if 'grid' in mode else r'$\delta$'
    Zlabel = 'entropy' if 'entropy' in mode else 'IG'
    return Xlabel, Ylabel, Zlabel

  def set_limits(self, ax, projection = '2d'):
    "Sets limits of a rhombus"
    xmin, ymax, xmax, ymin = multiple_get(self.limits,self.limit_keys)
    ax.set_xlim(xmin, xmax) ; ax.set_ylim(ymin, ymax)
    
  def draw_axes(self, ax):
    "Draws axes of a rhombus"
    xmin, ymax, xmax, ymin = multiple_get(self.limits,self.limit_keys)
    ax.plot([0.,0.],[-1.,1.], color = 'b', zorder=1)
    ax.plot([xmin,xmax],[0.,0.], color = 'b', zorder=1)
    
  def draw_borders(self, ax):
    "Draws borders of a rhombus"
    X, Y = unzip2(multiple_get(self.borders,self.border_keys))
    ax.plot ( X + X[:1], Y + Y[:1], color='r', zorder=1 )

  def draw_crossings(self,ax):
    "Draws crossings for a rhombus"
    left, top, right, bottom = multiple_get(self.borders,self.border_keys)
    X, Y = zip(left,right)
    ax.plot ( X, Y, color='0.5', linestyle='dashed', zorder=1 )
    X, Y = zip(top,bottom)
    ax.plot ( X, Y, color='0.5', linestyle='dashed', zorder=1 )

  def draw_recall(self,ax, _which = 'pos'):
    "Draws isometrics of specificity / sensitivity"
    pass
  
  def draw_precision(self,ax, _which = 'pos'):
    "Draws isometrics of negative predictive value / precision"
    pass
  
  def fill(self,ax,color='lightgrey'):
    "Fill the background of a phidelta diagram"
    X, Y = unzip2(multiple_get(self.borders,self.border_keys))
    ax.fill ( X + X[:1], Y + Y[:1], color=color, zorder=0 )

  def wipe_out(self,ax=None):
    if not ax: ax = self.ax
    lines = ax.lines[:]
    [ ax.lines.remove(line) for line in lines ]
    #self.lines = list()
    if self.points:
        for pitem in self.points: pitem.remove()
        self.points = list()
    self.fill(ax,color='white')
    plt.plot()


if __name__ == '__main__':


  from random import randint
  
  from model import eval_coords
  
  phidelta_view = phidelta  
  
  def random_pair(): return (randint(0,100) / 100., randint(0,100) / 100.)

  #phi, delta = unzip2(eval_coords([ random_pair() for k in range(50) ]))
  
  points = [ (0.95,0.95), (0.95,0.05), (0.05,0.95), (0.05,0.05) ]
  
  colors = [ 0., 0.3, 0.6, 0.9 ]
  
  #for ratio in [ 1., 3., 6., 1/6.]:
  for ratio in [ 1., 2. ]:
    
    # model = phidelta_model(ratio=ratio, intervals = 100, _eval = ('grid'))
  
    view = phidelta_view(ratio=ratio, labels = (r'$\varphi_{b}$',r'$\delta_{b}$', 'Entropy'))

    view('axes', 'borders', 'crossings', 'fill')
    #view('axes', 'borders', 'crossings')
    #view('axes', 'borders', 'fill')
    view.projection = '2d'
  
    phi, delta = unzip2(eval_coords(points,ratio))
  
    view.scatter2D(phi,delta,colors=colors)
  
  #ax = view.plot()
  
  #S, D = model.get_iso_recall('specificity')
  #S, D = model.get_iso_precision('precision')
  #S, D = model.get_iso_precision('neg predictive value')
  
  #S, D = model.get_iso_accuracy('accuracy')
  #view.draw_lines(S,D)

  