# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 GEM Foundation
#
# The CATK (Lite) is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# CATK is distributed in the hope that it will be useful,
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
import math as ma

import Catalogue as Cat
import CatUtils as CU

#-----------------------------------------------------------------------------------------

def GardnerKnopoff(M):
  Swin = 10**(0.1238*M+0.983)
  if M >= 6.5:
    Twin = 10.**(0.032*M+2.7389)*84600.
  else:
    Twin = 10.**(0.5409*M-0.547)*84600.
  return Twin, Swin

def Grunthal(M):
  Swin = np.exp(1.77+(0.037+1.02*M)**2)
  if M >= 6.5:
    Twin = np.exp(-3.95+(0.62+17.32*M)**2)*84600.
  else:
    Twin = 10**(2.8+0.024*M)*84600.
  return Twin, Swin

def Uhrhammer(M):
  Swin = np.exp(-1.024+0.804*M)
  Twin = np.exp(-2.87+1.235*M)*84600.
  return Twin, Swin

#-----------------------------------------------------------------------------------------

def WindowSearch(Db, WinFun=GardnerKnopoff):
  """
  """

  def GetDate(Event):

    L = Event['Location'][0]
    S = CU.DateToSec(L['Year'],
                     L['Month'],
                     L['Day'],
                     L['Hour'],
                     L['Minute'],
                     L['Second'])
    return S

  def GetCoor(Event):
    X = Event['Location'][0]['Longitude']
    Y = Event['Location'][0]['Latitude']
    return [X, Y]

  def GetSize(Event):
    M = Event['Magnitude'][0]['MagSize']
    return M

  def DeltaSec(S0, S1):
    Sec = ma.fabs(S1-S0)
    return Sec

  def DeltaLen(C0, C1):
    Dis = CU.WgsDistance(C0[1],C0[0],C1[1],C1[0])
    return Dis

  def WhichShock(T0, T1):
    if T1 > T0:
      Type = 'AS'
    else:
      Type = 'FS'
    return Type

  def LogInfo(Type, Event, dT, dC):
    L = []
    L.append(Type)
    L.append(Event['Id'])
    L.append(Event['Location'][0]['Latitude'])
    L.append(Event['Location'][0]['Longitude'])
    L.append(Event['Magnitude'][0]['MagSize'])
    L.append(dT)
    L.append(dC)
    return L

  #---------------------------------------------------------------------------------------

  DbS = Db.Sort(Key='Magnitude', Owrite=0)
  Ind = np.zeros(DbS.Size())

  Events = []
  Log = []

  for J, E0 in enumerate(DbS.Events[:-1]):
    if not Ind[J]:
      T0 = GetDate(E0)
      C0 = GetCoor(E0)
      M0 = GetSize(E0)

      Twin, Swin = WinFun(M0)

      Events.append(E0)

      Log.append([])
      Log[-1].append(LogInfo('MS', E0, 0, 0))

      for I, E1 in enumerate(DbS.Events[J+1:]):
        if not Ind[I+J+1]:
          T1 = GetDate(E1)
          C1 = GetCoor(E1)

          dC = DeltaLen(C0, C1)
          dT = DeltaSec(T0, T1)

          if dC <= Swin and dT <= Twin:
            Ind[I+J+1] = 1
            Type = WhichShock(T0, T1)
            Log[-1].append(LogInfo(Type, E1, dT, dC))

  DbS.Events = Events
  DbS.Sort()

  return DbS, Log

#-----------------------------------------------------------------------------------------

def PlotLog(Log):
  """
  For Debug
  """

  FS = [[],[]]
  AS = [[],[]]
  MS = [[],[]]

  plt.figure()

  for L in Log:
    if len(L) > 1:
      for S in L:
        if S[0] == 'FS':
          FS[0].append(S[3])
          FS[1].append(S[2])
        if S[0] == 'AS':
          AS[0].append(S[3])
          AS[1].append(S[2])
        if S[0] == 'MS':
          MS[0].append(S[3])
          MS[1].append(S[2])

  plt.plot(AS[0], AS[1], 'b.', markersize=2)
  plt.plot(FS[0], FS[1], 'g.', markersize=2)
  plt.plot(MS[0], MS[1], 'r*', markersize=3)

  plt.show(block=False)