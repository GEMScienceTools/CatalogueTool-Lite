#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2017 GEM Foundation
#
# The OQ-CATK (Lite) is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# OQ-CATK (Lite) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Poggi Valerio

import numpy as np
import scipy.odr as odr
import matplotlib.pyplot as plt

import csv


#-----------------------------------------------------------------------------------------

def PolyFun(B, X):
  """
  Arbitrary polynomial of arbitrary degree.
  Degree is taked from the length of the
  coefficient array (B).
  """

  X = np.array(X)
  Y = 0.0

  for d in np.arange(len(B)):
    Y += B[d]*(X**d)

  return Y

def ExpoFun(B, X):
  """
  TODO: 
  Arbitrary polynomial of arbitrary degree.
  Degree is taked from the length of the
  coefficient array (B).
  """
  assert len(B) == 3
  # X = np.array(X)
  Y = 0.0

  Y = np.exp(B[0] + B[1]*X) + B[2]

  return Y


#-----------------------------------------------------------------------------------------

class Data(object):

  def __init__(self, X, Y, Xw=[], Yw=[]):

    self.X = np.array(X)
    self.Y = np.array(Y)

    self.Xw = np.array(Xw)
    self.Yw = np.array(Yw)

    if self.Xw.size == 0:
      self.Xw = np.zeros(self.X.size)
    if self.Yw.size == 0:
      self.Yw = np.zeros(self.Y.size)

    self.B = np.array([])
    self.E = np.array([])
    self.Cov = np.array([])
    self.delta = np.array([])
    self.eps = np.array([])
    self.res = np.array([])
    self.sd = 0.0
    self.perc_X = np.array([])

  #-----------------------------------------------------------------------------------------

  def OrthRegP(self, Deg=1, LogRes =''):
    """
    Orthogonal regressiong of a polynomial of
    arbitrary degree.
    """

    B0 = np.ones(Deg+1)

    PF = odr.Model(PolyFun)

    if (self.Xw.all() == 0) and (self.Yw.all() == 0):
      Data = odr.Data(self.X, self.Y)
    else:
      Wx = 1./np.power(self.Xw,2)
      Wy = 1./np.power(self.Yw,2)
      Data = odr.Data(self.X, self.Y, Wx, Wy)

    Out = odr.ODR(Data, PF, beta0=B0)
    Out.run()

    self.B = Out.output.beta
    self.E = Out.output.sd_beta
    self.Cov = Out.output.cov_beta
    self.delta = Out.output.delta
    self.eps = Out.output.eps
    self.sd = np.std(self.Y - PolyFun(self.B, self.X))

   
    # Residuals + statistics 
    self.res = (self.Y - PolyFun(self.B, self.X)) 
    
    perc_res = np.percentile(self.res, [0,5,50,95,100], axis=None, out=None, 
                        overwrite_input=False, interpolation='linear', keepdims=False)

    self.perc_X = np.percentile(self.X, [0,5,50,95,100], axis=None, out=None, 
                        overwrite_input=False, interpolation='linear', keepdims=False)

    if LogRes:
      self.res = (self.Y - PolyFun(self.B, self.X)) 
      # Open input ascii file
      with open(LogRes, 'w') as f:
          headers = 'M1,M2,RES'
          f.write(headers + '\n')
          writer = csv.writer(f,delimiter=',')
          writer.writerows(zip(self.X,self.Y,self.res))
      f.close
    return

  def OrthRegE(self, LogRes =''):
    """
    Orthogonal regressiong of a polynomial of
    arbitrary degree.
    """

    B0 = [0., 1., 1.]

    PF = odr.Model(ExpoFun)

    if (self.Xw.all() == 0) and (self.Yw.all() == 0):
      Data = odr.Data(self.X, self.Y)
    else:
      Wx = 1./np.power(self.Xw,2)
      Wy = 1./np.power(self.Yw,2)
      Data = odr.Data(self.X, self.Y, Wx, Wy)

    Out = odr.ODR(Data, PF,beta0=B0)
    Out.run()

    self.B = Out.output.beta
    self.E = Out.output.sd_beta
    self.Cov = Out.output.cov_beta
    print self.B
    self.sd = np.std(self.Y - ExpoFun(self.B, self.X))
    print "sd= ",self.sd
    
    # Residuals + statistics 
    self.res = (self.Y - ExpoFun(self.B, self.X))
    
    perc_res = np.percentile(self.res, [0,5,50,95,100], axis=None, out=None, 
                        overwrite_input=False, interpolation='linear', keepdims=False)
    self.perc_X = np.percentile(self.X, [0,5,50,95,100], axis=None, out=None, 
                        overwrite_input=False, interpolation='linear', keepdims=False)

    if LogRes:
      self.res = (self.Y - ExpoFun(self.B, self.X)) 
      print "residuals?", self.res   
      # Open input ascii file
      with open(LogRes, 'w') as f:
          headers = 'M1,M2,E1,E2,RES'
          f.write(headers + '\n')
          writer = csv.writer(f,delimiter=',')
          writer.writerows(zip(self.X,self.Y,self.Xw,self.Yw,self.res))
      f.close

  #-----------------------------------------------------------------------------------------

  def SaveResiduals(self, OutFile=''):
    import csv
    self.res = (self.Y - PolyFun(self.B, self.X))
    # Open input ascii file
    with open(OutFile, 'w') as f:
        headers = 'M1,M2,RES'
        f.write(headers + '\n')
        writer = csv.writer(f,delimiter=',')
        writer.writerows(zip(self.X,self.Y,self.res))
        f.close 
    return

  def PlotBox(self, OutFile=''):

    plt.figure(figsize=(5,5))

    #plt.boxplot(self.res)
    Axis = [np.min(self.X)-1,
            np.max(self.X)+1,
            np.min(self.Y)-1,
            np.max(self.Y)+1]  
      
    plt.boxplot(self.X,vert=0,whis=[15, 85])
    plt.boxplot(self.Y,vert=1,whis=[15, 85])
    #plt.boxplot(self.X, 0, 'rs', 0)
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.grid(True)
    plt.show(block=False)

    if OutFile:
        plt.savefig(OutFile, bbox_inches='tight', dpi=Dpi)

    return

  def PlotWithRes(self, X1label='', Y1label='', Y2label='', Axis=[], OutFile='',
                  Dpi=300,title='', model_type=[]):
    
    if self.X.size != 0 and self.Y.size != 0:
      data_label = 'Data [N=%s] - sd = %.3f'%(self.X.size, self.sd)
      
      #PLOT
      fig1 = plt.figure(figsize=(7,7))

      # Regression
      frame1 = fig1.add_axes((.1,.35,.6,.6))

      plt.errorbar(self.X, self.Y,
                   xerr=self.Xw, yerr=self.Yw,
                   fmt='o', capsize=5, elinewidth=1.0,
                   color=(0.4,0.4,0.4), ecolor=(0.8,0.8,0.8),
                   barsabove=True, label=data_label)
      if not Axis:
        Axis = [np.min(self.X)-1,
                np.max(self.X)+1,
                np.min(self.Y)-1,
                np.max(self.Y)+1]      
      Ax = np.linspace(Axis[0],Axis[1],100)

      # Plotting 1:1 line
      plt.plot(Ax, Ax, color=(1,0,0),
                       linewidth=2,
                       linestyle='dashed',
                       label='1:1')
     
      if model_type == "pr":
        ll = str(Y1label[1] + '= %05.3f + %05.3f*' + X1label[1])%(self.B[0],self.B[1])

      if model_type == "er":
        xl = str('%s = exp(%.3f + %.3f* %s ) + %.3f') %(Y1label[1],
                                                        self.B[0],self.B[1],
                                                        X1label[1],self.B[2])
      if self.B.size != 0:
        if model_type == "pr": 
            plt.plot(Ax, PolyFun(self.B,Ax),
                 color=(0,0,0),
                 linewidth=2,
                 label=ll)
        elif model_type == "er":
            plt.plot(Ax, ExpoFun(self.B,Ax),
                 color=(0,0,0),
                 linewidth=2,
                 label=xl)
        else:
            print "model type not included"

      # Plotting the percentiles [X-> Mobs]          
      Ax5 =np.linspace(0,0,100)
      Ax95 =np.linspace(0,0,100)
 
      Ay = np.linspace(Axis[2],Axis[3],100)

      label05 = 'P-05 [Mobs = %3.1f]'%(self.perc_X[1])
      label95 = 'P-95 [Mobs = %3.1f]'%(self.perc_X[3])
    
      plt.plot(Ax5, Ay, color='w',
                       linewidth=.1,
                       linestyle='dashed',
                       label=label05)
      plt.plot(Ax95, Ay, color='w',
                       linewidth=.1,
                       linestyle='dashed',
                       label=label95)


      plt.legend(loc='upper left', numpoints=1)
      plt.ylabel(Y1label)
      plt.grid(True)
      plt.xlim(Axis[0],Axis[1])
      plt.ylim(Axis[2],Axis[3])
      plt.title(title)

      
      # Residuals
      frame3 = fig1.add_axes((.1,.1,.6,.2))

      Ax = np.linspace(Axis[0],Axis[1],100)
      Ay = np.linspace(0,0,100)

      if self.B.size != 0:
        if model_type == "pr": 
          resid = (self.Y - PolyFun(self.B, self.X))
          resid_sd = np.std(resid, axis = 0, ddof = 1)
          print "resid_sd = ",resid_sd

          plt.errorbar(self.X, resid,
                   xerr=self.Xw, yerr=self.Yw,
                   fmt='s', capsize=3, elinewidth=1.0,
                   color=(0.4,0.4,0.4), ecolor=(0.8,0.8,0.8),
                   barsabove=True, label=data_label)
        
        elif model_type == "er":
          resid = (self.Y - ExpoFun(self.B,self.X))
          resid_sd = np.std(resid, axis = 0, ddof = 1)
          print "resid_sd = ",resid_sd

          plt.errorbar(self.X, resid,
                   xerr=self.Xw, yerr=self.Yw,
                   fmt='s', capsize=3, elinewidth=1.0,
                   color=(0.4,0.4,0.4), ecolor=(0.8,0.8,0.8),
                   barsabove=True, label=data_label)
        else:
            print "model type not included"
      
      Ay1 = np.linspace(resid_sd,resid_sd,100)
      Ay2 = np.linspace(-resid_sd,-resid_sd,100)
      
      plt.plot(Ax, Ay1, color='b',
                       linewidth=2,
                       linestyle='dashed',
                       label='0')
      plt.plot(Ax, Ay2, color='b',
                       linewidth=2,
                       linestyle='dashed',
                       label='0')

      plt.plot(Ax, Ay, color=(1,0,0),
                       linewidth=2,
                       label='0')

     # Plotting the percentiles [X-> Mobs]    
      Ay = np.linspace(np.min(resid),
                       np.max(resid),100)
      Ax5 =np.linspace(0,0,100)
      Ax95 =np.linspace(0,0,100)
      
      plt.plot(Ax5, Ay, color='w',
                       linewidth=0.1,
                       linestyle='dashed',
                       label=label05)
      plt.plot(Ax95, Ay, color='w',
                       linewidth=0.1,
                       linestyle='dashed',
                       label=label95)

      plt.grid(True)
      plt.xlim(Axis[0],Axis[1])
      plt.ylim(np.min(resid)-.1,
               np.max(resid)+.1)
      plt.xlabel(X1label)
      plt.ylabel(Y2label)

      if OutFile:
        plt.savefig(OutFile, bbox_inches='tight', dpi=Dpi)
        print OutFile

#-----------------------------------------------------------------------------------------


  def Plot(self, Xlabel='', Ylabel='', Axis=[], OutFile='', Dpi=300,
           title='', model_type=[]):
    """
    Plot utility to check regression results.
    """

    if self.X.size != 0 and self.Y.size != 0:
      data_label = 'Data [N=%s] - sd = %.3f'%(self.X.size, self.sd)
      print data_label

      plt.figure(figsize=(5,5))

      plt.errorbar(self.X, self.Y,
                   xerr=self.Xw, yerr=self.Yw,
                   fmt='o', capsize=5, elinewidth=1.0,
                   color=(0.4,0.4,0.4), ecolor=(0.8,0.8,0.8),
                   barsabove=True, label=data_label)

      if not Axis:
        Axis = [np.min(self.X)-1,
                np.max(self.X)+1,
                np.min(self.Y)-1,
                np.max(self.Y)+1]
      
      Ax = np.linspace(Axis[0],Axis[1],100)

      plt.plot(Ax, Ax, color=(1,0,0),
                       linewidth=2,
                       label='1:1')
      
      if model_type == "pr":
        ll = str(Ylabel[1] + '= %05.3f + %05.3f*' + Xlabel[1])%(self.B[0],self.B[1])

      if model_type == "er":
        xl = str('%s = exp(%.3f + %.3f* %s ) + %.3f') %(Ylabel[1],
                                                            self.B[0],self.B[1],
                                                            Xlabel[1],self.B[2])
      if self.B.size != 0:
        if model_type == "pr": 
            plt.plot(Ax, PolyFun(self.B,Ax),
                 color=(0,0,0),
                 linewidth=2,
                 label=ll)
        elif model_type == "er":
            plt.plot(Ax, ExpoFun(self.B,Ax),
                 color=(0,0,0),
                 linewidth=2,
                 label=xl)
        else:
            print "model type not included"


      plt.legend(loc='upper left', numpoints=1)
      plt.xlabel(Xlabel)
      plt.ylabel(Ylabel)

      plt.grid(True)
      plt.axis(Axis)
      plt.title(title)

      plt.show(block=False)

      if OutFile:
        plt.savefig(OutFile, bbox_inches='tight', dpi=Dpi)

  #-----------------------------------------------------------------------------------------

  def Close(self):

    plt.close('all')