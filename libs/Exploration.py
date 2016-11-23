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

#-----------------------------------------------------------------------------------------

def GetHypocenter(Db):

  x = Db.Extract('Longitude')
  y = Db.Extract('Latitude')
  z = Db.Extract('Depth')

  return x, y, z

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

      if MC == Code1[0] and MT == Code1[1]:
        m1 = MS
        e1 = ME
      if MC == Code2[0] and MT == Code2[1]:
        m2 = MS
        e2 = ME

    if m1 and m2:
      Mout[0].append(m1)
      Mout[1].append(m2)
      Mout[2].append(e1)
      Mout[3].append(e2)

  return Mout

#-----------------------------------------------------------------------------------------

def AgencyReport(Db, Code, Key=[], LogFile=[], Threshold=0):

  if Code in ['Magnitude','Mag','M']:
    ItL, ItD = Db.Occurrence('MagCode')
  elif Code in ['Location','Loc','L']:
    ItL, ItD = Db.Occurrence('LocCode')
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

  for It in ItL:
    if ItD[It] >= Threshold:
      StrLog += 'Agency: {0} | Occurrence: {1}'.format(It, ItD[It])

      if Code in ['Magnitude','Mag','M']:
        DbC = Db.Filter('MagCode',It,Owrite=False)
        MaL, MaD = DbC.Occurrence('MagType')

        StrLog += ' | Types:'
        for Ma in MaL:
          StrLog += ' {0} ({1})'.format(Ma, MaD[Ma])

      StrLog += '\n'
    else:
      break

  if LogFile:
    # Open input ascii file
    with open(LogFile, 'w') as f:
      f.write(StrLog)
      f.close()
      return
    # Warn user if model file does not exist
    print 'Cannot open file'

  else:
    print StrLog

#-----------------------------------------------------------------------------------------

def TimePlot(Db, Code, Key=[], Year0=[], Year1=[], Delta=5, Threshold=50):

  if not Year0:
    Year0 = min(Db.Extract('Year'))

  if not Year1:
    Year1 = max(Db.Extract('Year'))

  YBins = np.arange(Year0, Year1+Delta, Delta)

  ItL, ItD = Db.Occurrence(Code)

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
  fig = plt.figure(figsize=(8, 5))

  X = YBins
  Y = np.arange(0, len(ItL)+1)
  Z = np.log(Histo.clip(min=1E-10))

  plt.pcolor(X, Y, Z, cmap='Purples',
                      vmin=0,
                      vmax=np.max(Z))

  plt.xticks(X,map(str,X), rotation='45')
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
