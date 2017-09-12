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

import matplotlib.pyplot as plt
import numpy as np
import csv
#import pandas as pd
import scipy.signal as sig

import OQCatk.Selection as Sel

#-----------------------------------------------------------------------------------------

def GetHypocenter(Db, All=False):

  x = Db.Extract('Longitude', All)
  y = Db.Extract('Latitude', All)
  z = Db.Extract('Depth', All)

  return x, y, z

#-----------------------------------------------------------------------------------------

def GetMagnitudePairID(Db, Code1, Code2,LogFile=[]):

  Mout = [[],[],[],[],[],[],[],[]]

  for E in Db.Events:
    m1 = None
    m2 = None
    im1 = None
    im2 = None
    ie1 = None
    ie2 = None

    for M in E['Magnitude']:
      MC = M['MagCode']
      MT = M['MagType']
      MS = M['MagSize']
      ME = M['MagError']
      MI = M['MagId']
      EI = E['Id']

      if (MC == Code1[0] or Code1[0] == '*') and MT == Code1[1]:
        m1 = MS
        # setting a default value = 0.1 
        if ME is None or ME < 1E-20:
          e1 = 0.1
        else:
          e1 = ME  
        im1 = MI
        ie1 = EI
      if (MC == Code2[0] or Code2[0] == '*') and MT == Code2[1]:
        m2 = MS
        # setting a default value = 0.1 
        if ME is None or ME < 1E-20:
          e2 = 0.1
        else:
          e2 = ME  
        im2 = MI
        ie2 = EI

    if m1 and m2:
      if np.abs(m1-m2) < 1.0:          
        Mout[0].append(m1)
        Mout[1].append(m2)
        Mout[2].append(e1)
        Mout[3].append(e2)
        Mout[4].append(im1)
        Mout[5].append(im2)
        Mout[6].append(ie1)
        Mout[7].append(ie2)
      else:
        print "posible outlier!!!"
  
  if LogFile:
    SaveMagnitudePair(Mout, LogFile)

  return Mout

def SaveMagnitudePair(Mout, OutFile=[]):
  import csv
  # Open input ascii file
  with open(OutFile, 'w') as f:
    headers = 'M1,M2,E1,E2,IDm1,IDm2,ID1,ID2'
    f.write(headers + '\n')
    writer = csv.writer(f,delimiter=',')
    writer.writerows(zip(*Mout))
  f.close
  return

#-----------------------------------------------------------------------------------------

def GetMagnitudePair(Db, Code1, Code2):

  Mout = [[],[],[],[]]

  for E in Db.Events:
    m1 = None
    m2 = None

    for M in E['Magnitude']:
      MC = M['MagCode']
      MT = M['MagType']
      MS = M['MagSize']
      ME = M['MagError']

      if (MC == Code1[0] or Code1[0] == '*') and MT == Code1[1]:
        m1 = MS
        e1 = ME
      if (MC == Code2[0] or Code2[0] == '*') and MT == Code2[1]:
        m2 = MS
        e2 = ME

    if m1 and m2:
      Mout[0].append(m1)
      Mout[1].append(m2)
      Mout[2].append(e1)
      Mout[3].append(e2)  

  
  return Mout



def GetKeyHisto(Db, Key, Bins=[], Bmin=[], Bmax=[], Bnum=10, Blog=False,
                         Norm=True, Plot=True, OutFile=[]):

  Data = Db.Extract(Key)

  # Remove Nans
  Data = [D for D in Data if D is not None]

  if not Bins:
    if not Bmin:
      Bmin = min(Data)
    if not Bmax:
      Bmax = max(Data)
    if Blog:
      Bins = np.logspace(np.log10(Bmin), np.log10(Bmax), Bnum)
    else:
      Bins = np.linspace(Bmin, Bmax, Bnum)

  Hist = np.histogram(Data, Bins)[0]
  Bmid = np.diff(Bins)/2.+Bins[:-1]
  Bdlt = np.diff(Bins)

  if Norm:
   Hist = Hist.astype('float32') / len(Data)

  # Plot time histogram
  if Plot:
    fig = plt.figure(figsize=(6,3.5))

    plt.bar(Bmid, Hist, Bdlt, color=[1,0,0], edgecolor=[1,1,1])

    plt.xlabel(Key, fontsize=14, fontweight='bold')
    plt.ylabel('Nr. Events', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.show(block=False)

    if OutFile:
      plt.savefig(OutFile, bbox_inches='tight', dpi=150)

  return Hist, Bmid

#-----------------------------------------------------------------------------------------

def AgencyReport(Db, Code, Key=[], LogFile=[], Threshold=0):

  if Code in ['Magnitude','Mag','M']:
    ItL, ItD = Db.KeyStat('MagCode')
  elif Code in ['Location','Loc','L']:
    ItL, ItD = Db.KeyStat('LocCode')
  else:
    print 'Error: No valid code'
    return

  # Report only specific keys
  if Key:
    ItLs = []
    ItDs = {}

    if type(Key) != list:
      Key = [Key]

    for K in Key:
     if K in ItL:
       ItLs.append(K)
       ItDs[K] = ItD[K]
    ItL = ItLs
    ItD = ItDs

  StrLog = ''
  #JG Lista con los codigos
  LMlist = []

  for It in ItL:
    if ItD[It] >= Threshold:
      StrLog += 'Agency: {0} | Occurrence: {1}'.format(It, ItD[It])
      #JG creo una lista per utilizarla inmediatamente
      LMlist.append(It)

      if Code in ['Magnitude','Mag','M']:
        DbC = Db.Filter('MagCode',It,Owrite=False)
        MaL, MaD = DbC.KeyStat('MagType')
        StrLog += ' | Types:'
        for Ma in MaL:
          StrLog += ' {0} ({1})'.format(Ma, MaD[Ma])

      StrLog += '\n'
    else:
      break

  if LogFile:
    print StrLog
    if LMlist:
        name = Db.Header['Name']
        print '{} : {}'.format(name,LMlist)

    # Open input ascii file
    with open(LogFile, 'w') as f:
      f.write(StrLog)
      f.close()
      return
    # Warn user if model file does not exist
    print 'Cannot open file'

  else:
    print StrLog
    if LMlist:
       name = Db.Header['Name']
       print '{} : {}'.format(name,LMlist)
#

#-----------------------------------------------------------------------------------------

def KeyTimeHisto(Db, Code, Key=[],
                           Year0=[], Year1=[], Delta=5,
                           Threshold=0, OutFile=[]):

  if not Year0:
    Year0 = min(Db.Extract('Year'))
  if not Year1:
    Year1 = max(Db.Extract('Year'))
  YBins = np.arange(Year0, Year1+Delta, Delta)

  ItL, ItD = Db.KeyStat(Code)

  # Filter by threshold
  ItL = [K for K in ItL if ItD[K] > Threshold]
  ItD = {K:V for (K,V) in ItD.items() if V > Threshold}

  # Filter by key
  if Key:
    ItL = [K for K in ItL if K in Key]
    ItD = {K:ItD[K] for K in ItL}

  for N, Agn in enumerate(ItL):

    DbA = Db.Filter(Code, Agn, Owrite=0)
    YearArray = DbA.Extract('Year')
    NewRow = np.histogram(YearArray, YBins)

    if N == 0:
      Histo = NewRow[0]
    else:
      Histo = np.vstack([Histo, NewRow[0]])

  # Plot time histogram
  # JG: Add the possibility of change the FigSize
  if  N < 10:
      fig = plt.figure(figsize=(8, 6))
  else:
      fig = plt.figure(figsize=(12, 7))


  X = YBins
  Y = np.arange(0, len(ItL)+1)
  Z = np.log(Histo.clip(min=1E-10))

  plt.pcolor(X, Y, Z, cmap='Purples',
                      vmin=0,
                      vmax=np.max(Z))
 
  if Delta < 10:
    XX = X[::20]
    plt.xticks(XX, map(str,XX),rotation='45')
  else:
    plt.xticks(X, map(str,X), rotation='45')

  plt.yticks(Y+0.5, ItL, rotation='horizontal')
  plt.margins(0)

  plt.gca().yaxis.tick_right()
  plt.axes().yaxis.grid(True)

  plt.gca().xaxis.set_ticks_position('none')
  plt.gca().yaxis.set_ticks_position('none')

  plt.xlabel('Year', fontsize=14, fontweight='bold')
  plt.ylabel('Agency Code', fontsize=14, fontweight='bold')

  plt.tight_layout()

  plt.show(block=False)

  if OutFile:
    plt.savefig(OutFile, bbox_inches='tight', dpi=150)

#-----------------------------------------------------------------------------------------

def MagTimeBars(Db, Mag0=[], Mag1=[], MBin=0.5,
                    Year0=[], Year1=[], Delta=5,
                    OutFile=[]):

  if not Mag0:
    Mag0 = min(Db.Extract('MagSize'))
  if not Mag1:
    Mag1 = max(Db.Extract('MagSize'))
  MBins = np.arange(Mag0, Mag1+MBin, MBin)

  if not Year0:
    Year0 = min(Db.Extract('Year'))
  if not Year1:
    Year1 = max(Db.Extract('Year'))
  YBins = np.arange(Year0, Year1+Delta, Delta)

  plt.figure(figsize=(8, 4))

  for C,MB in enumerate(MBins):

    DbM = Db.Filter('MagSize', MB, Opr='>=', Owrite=0)
    YArray = DbM.Extract('Year')
    YHist = np.histogram(YArray, YBins)[0]

    Cnum = float(len(MBins))
    C = (Cnum-C)/Cnum

    X = YBins[:-1]
    Y = YHist

    if any(Y):
      plt.bar(X, Y, Delta, color=[C,C,C],
                           log=True,
                           label=r'$\geq${0}'.format(MB))

  if Delta < 10:
    XX = X[::20]
    plt.xticks(XX, map(str,XX),rotation='45')
  else:
    plt.xticks(X, map(str,X), rotation='45')



  #plt.xticks(X, map(str,X), rotation='45')
  plt.margins(0)

  plt.gca().yaxis.tick_right()

  plt.gca().xaxis.set_ticks_position('none')
  plt.gca().yaxis.set_ticks_position('none')

  plt.xlabel('Years', fontsize=14, fontweight='bold')
  plt.ylabel('Nr. Events', fontsize=14, fontweight='bold')

  plt.tight_layout()
  plt.legend(loc=2)
  plt.show(block=False)

  if OutFile:
    plt.savefig(OutFile, bbox_inches='tight', dpi=150)

#-----------------------------------------------------------------------------------------

def MagTimePlot(Db, Mag0=[], Mag1=[],
                    Year0=[], Year1=[],
                    CompTable=[], 
                    OutFile=[],
                    Title=[]):

  if not Mag0:
    Mag0 = min(Db.Extract('MagSize'))
  if not Mag1:
    Mag1 = max(Db.Extract('MagSize'))

  if not Year0:
    Year0 = min(Db.Extract('Year'))
  if not Year1:
    Year1 = max(Db.Extract('Year'))

  DbS = Sel.MagRangeSelect(Db, Mag0, Mag1, Owrite=0, TopEdge=True)
  DbS = Sel.TimeSelect(DbS, Year0, Year1, Owrite=0)

  X = DbS.Extract('Year')
  Y = DbS.Extract('MagSize')

  plt.figure(figsize=(4, 3))

  plt.plot(X, Y, 'o',markersize=2,
                  color=[0,0,0],
                  markeredgecolor=[0,0,0],
                  markeredgewidth=1.5)

  # Plot completeness
  if CompTable:
    PlotCompTable(CompTable)

  plt.gca().yaxis.grid(color='0.',linestyle='-')
  plt.gca().xaxis.grid(color='0.65',linestyle='--')

  plt.gca().xaxis.set_ticks_position('none')
  plt.gca().yaxis.set_ticks_position('none')

  if Title:
    plt.title(Title, fontsize=12, fontweight='bold')
  else:
    plt.title('Time-Magnitude Distribution', fontsize=14, fontweight='bold')
  
  plt.xlabel('Years', fontsize=14, fontweight='bold')
  plt.ylabel('Magnitude', fontsize=14, fontweight='bold')

  plt.axis([Year0, Year1, Mag0, Mag1])
  # plt.tight_layout()
  plt.show(block=False)

  if OutFile:
    plt.savefig(OutFile, bbox_inches='tight', dpi=150)

#-----------------------------------------------------------------------------------------

def RateDensityPlot(Db, Mag0=[], Mag1=[], MBin=0.25,
                        Year0=[], Year1=[], Delta=2,
                        CompTable=[], 
                        Normalise=True,
                        OutFile=[],
                        Title=[]):

  if not Mag0:
    Mag0 = min(Db.Extract('MagSize'))
  if not Mag1:
    Mag1 = max(Db.Extract('MagSize'))
  MBins = np.arange(Mag0, Mag1+MBin, MBin)

  if not Year0:
    Year0 = min(Db.Extract('Year'))
  if not Year1:
    Year1 = max(Db.Extract('Year'))
  YBins = np.arange(Year0, Year1+Delta, Delta)

  Histo = np.zeros((np.size(MBins), np.size(YBins)))

  # Catalogue selection (Magnitude-Year)
  DbM = Sel.MagRangeSelect(Db, Mag0, Mag1, TopEdge=True)
  DbY = Sel.TimeSelect(DbM, Year0, Year1)

  M = DbY.Extract('MagSize')
  Y = DbY.Extract('Year')

  Hist = np.histogram2d(Y, M, bins=(YBins, MBins))[0]
  Hist = np.transpose(Hist)

  if Normalise:
    for I in range(0,len(Hist)):
      Max = np.max(Hist[I])
      if Max > 0:
        Hist[I] = Hist[I]/Max

  # Plot
  plt.figure(figsize=(6, 4))

  plt.pcolormesh(YBins, MBins, Hist, cmap='Greys', vmin=0)

  # Plot completeness
  if CompTable:
    PlotCompTable(CompTable)

  plt.gca().xaxis.grid(color='0.65',linestyle='--')
  plt.gca().yaxis.grid(color='0.',linestyle='-')

  plt.gca().xaxis.set_ticks_position('none')
  plt.gca().yaxis.set_ticks_position('none')

  if Title:
    title = 'Occ. Rate Density - %s' % (Title)
    plt.title(title, fontsize=14, fontweight='bold')
  else:
    plt.title('Occurrence Rate Density', fontsize=14, fontweight='bold')


  plt.xlabel('Years', fontsize=12, fontweight='bold')
  plt.ylabel('Magnitude', fontsize=12, fontweight='bold')

  plt.gca().xaxis.grid(color='0.65',linestyle='-')
  plt.gca().yaxis.grid(color='0.65',linestyle='-')

  plt.axis([Year0, Year1, Mag0, Mag1])
  # plt.tight_layout()
  plt.show(block=False)

  if OutFile:
    plt.savefig(OutFile, bbox_inches = 'tight', dpi = 150)


def PlotCompTable(CompTable):

  for CT in CompTable:

    X = [CT[2], CT[3], CT[3], CT[2], CT[2]]
    Y = [CT[0], CT[0], CT[0]+CT[1], CT[0]+CT[1], CT[0]]

    plt.plot(X, Y, 'r--', linewidth=2)
    plt.fill(X, Y, color='y',alpha=0.1)

#-----------------------------------------------------------------------------------------

def DuplicateCheck(Log, Tmax=[], Smax=[],
                        Tnum=[], Snum=[],
                        Smooth=[],
                        OutFile=[]):
  """
  """

  dT = [I[4] for I in Log if I[4] > 0]
  dS = [I[5] for I in Log if I[5] > 0]

  if not Tmax:
    Tmax = np.max(dT)
  if not Smax:
    Smax = np.max(dS)
  if not Tnum:
    Tnum = 100
  if not Snum:
    Snum = 100

  XBins = np.linspace(0, Tmax, Tnum)
  YBins = np.linspace(0, Smax, Snum)

  H = np.histogram2d(dT, dS, [YBins, XBins])

  def Gaussian(Size,Sigma):
    x = np.arange(0, Size[0], 1, float)
    y = np.arange(0, Size[1], 1, float)
    Gx = np.exp(-(x-Size[0]/2)**2/Sigma[0]**2)
    Gy = np.exp(-(y-Size[1]/2)**2/Sigma[1]**2)
    return np.outer(Gy,Gx)

  if any(Smooth):
    # kern = np.ones((Smooth,Smooth))/Smooth
    kern = Gaussian((Tnum,Snum),Smooth)
    H0 = sig.convolve2d(H[0], kern, mode='same')
  else:
    H0 = H[0]

  # Plot time histogram
  fig = plt.figure(figsize=(5, 5))

  plt.pcolor(XBins, YBins, H0, cmap='Purples')

  plt.xlabel('Time', fontsize=12, fontweight='bold')
  plt.ylabel('Distance', fontsize=12, fontweight='bold')

  plt.grid('on')

  plt.tight_layout()

  plt.show(block=False)

  if OutFile:
    plt.savefig(OutFile, bbox_inches='tight', dpi=150)