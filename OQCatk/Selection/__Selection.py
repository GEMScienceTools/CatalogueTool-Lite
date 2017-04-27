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

import copy as cp
import math as ma

import OQCatk.Catalogue as Cat
import OQCatk.CatUtils as CU

#-----------------------------------------------------------------------------------------

def AreaSelect(Db, XY, File=[], Owrite=False, Any=False):

  P = CU.Polygon()

  if File:
    P.Import(XY, Type=File)
  else:
    P.Load(XY)

  DbC = Cat.Database()
  DbC.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:
    Event = {}
    Event['Location'] = []

    for L in E['Location']:
      x = L['Longitude'];
      y = L['Latitude']

      if P.IsInside(x,y):
        Event['Location'].append(L)

    if Event['Location']:
      Event['Id'] = E['Id']
      Event['Log'] = E['Log']
      Event['Magnitude'] = E['Magnitude']
      if Any:
        Event['Location'] = E['Location']
      DbC.Events.append(cp.deepcopy(Event))

  if Owrite:
    Db.Events = DbC.Events
  else:
    return DbC

#-----------------------------------------------------------------------------------------

def MagRangeSelect(Db, MinMag, MaxMag, Owrite=False, Any=False):

  DbC = Cat.Database()
  DbC.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:
    Event = {}
    Event['Magnitude'] = []

    for M in E['Magnitude']:
      m = M['MagSize'];

      if m >= MinMag and m < MaxMag:
        Event['Magnitude'].append(M)

    if Event['Magnitude']:
      Event['Id'] = E['Id']
      Event['Log'] = E['Log']
      Event['Location'] = E['Location']
      if Any:
        Event['Magnitude'] = E['Magnitude']
      DbC.Events.append(cp.deepcopy(Event))

  if Owrite:
    Db.Events = DbC.Events
  else:
    return DbC

#-----------------------------------------------------------------------------------------

def DepRangeSelect(Db, MinDep, MaxDep, Owrite=False):

  if Owrite:
    DbC = Db
  else:
    DbC = Db.Copy()

  DbC.Filter('Depth',MinDep,Opr='>=')
  DbC.Filter('Depth',MaxDep,Opr='<')

  if not Owrite:
    return DbC

#-----------------------------------------------------------------------------------------

def MagCodeSelect(Db, MagList, Best=False, Owrite=False):

  if type(MagList) != list:
    MagList = [MagList]

  Code = [M[0] for M in MagList]
  Type = [M[1:] for M in MagList]

  Db0 = Cat.Database()
  Db0.Header = cp.deepcopy(Db.Header)

  Db1 = Cat.Database()
  Db1.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:

    Event = {}
    Event['Id'] = E['Id']
    Event['Log'] = E['Log']
    Event['Location'] = E['Location']
    Event['Magnitude'] = []
    Stop = False

    for I,C in enumerate(Code):
      for M in E['Magnitude']:
        if C == M['MagCode']:
          for T in Type[I]:
            if T == M['MagType']:

              Event['Magnitude'].append(M)
              if Best:
                Stop = True

            if Stop: break
        if Stop: break
      if Stop: break

    if Event['Magnitude']:
      Db0.Events.append(cp.deepcopy(Event))
    else:
      Db1.Events.append(cp.deepcopy(E))

  if Owrite:
    Db.Events = Db0.Events
  else:
    return Db0, Db1

#-----------------------------------------------------------------------------------------

def LocCodeSelect(Db, LocList, Best=False, Owrite=False):

  if type(LocList) != list:
    LocList = [LocList]

  Db0 = Cat.Database()
  Db0.Header = cp.deepcopy(Db.Header)

  Db1 = Cat.Database()
  Db1.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:

    Event = {}
    Event['Id'] = E['Id']
    Event['Log'] = E['Log']
    Event['Location'] = []
    Event['Magnitude'] = E['Magnitude']
    Stop = False

    for C in LocList:
      for L in E['Location']:
        if C == L['LocCode']:

          Event['Location'].append(L)
          if Best:
           Stop = True

        if Stop: break
      if Stop: break

    if Event['Location']:
      Db0.Events.append(cp.deepcopy(Event))
    else:
      Db1.Events.append(cp.deepcopy(E))

  if Owrite:
    Db.Events = Db0.Events
  else:
    return Db0, Db1

#-----------------------------------------------------------------------------------------

def TimeSelect(Db, Date0, Date1, Owrite=False):

  Def0 = [1900,1,1,0,0,0]
  Def1 = [2000,12,31,23,59,59]

  if type(Date0) != list:
    Date0 = [Date0]
  if type(Date1) != list:
    Date1 = [Date1]

  for N in range(len(Date0),6):
    Date0.append(Def0[N])
  for N in range(len(Date1),6):
    Date1.append(Def1[N])

  Sec0 = CU.DateToSec(Date0[0],
                      Date0[1],
                      Date0[2],
                      Date0[3],
                      Date0[4],
                      Date0[5])

  Sec1 = CU.DateToSec(Date1[0],
                      Date1[1],
                      Date1[2],
                      Date1[3],
                      Date1[4],
                      Date1[5])

  """
  # OLD VERSION (COMPARE ONLY FIRST LOCATION)
  def GetSec(Event):
    L = Event['Location'][0]
    S = CU.DateToSec(L['Year'],
                     L['Month'],
                     L['Day'],
                     L['Hour'],
                     L['Minute'],
                     L['Second'])
    return S

  Sec = []
  for E in Db.Events:
    Sec.append(GetSec(E))

  Ind = [I for I,S in enumerate(Sec) if S>=Sec0 and S<=Sec1]

  DbN = Cat.Database()
  DbN.Header = cp.deepcopy(Db.Header)

  for I in Ind:
    DbN.Events.append(cp.deepcopy(Db.Events[I]))
  """

  DbN = Cat.Database()
  DbN.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:
    Event = {}
    Event['Location'] = []

    for L in E['Location']:
      S = CU.DateToSec(L['Year'],
                       L['Month'],
                       L['Day'],
                       L['Hour'],
                       L['Minute'],
                       L['Second'])

      if S>=Sec0 and S<=Sec1:
        Event['Location'].append(L)

    if Event['Location']:
      Event['Id'] = E['Id']
      Event['Log'] = E['Log']
      Event['Magnitude'] = E['Magnitude']
      DbN.Events.append(cp.deepcopy(Event))

  if Owrite:
    Db.Events = DbN.Events
  else:
    return DbN

#-----------------------------------------------------------------------------------------

def SplitPrime(Db):

  OutP = Cat.Database()
  OutN = Cat.Database()

  OutP.Header = cp.deepcopy(Db.Header)
  OutN.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:

    Event = {}
    Event['Id'] = E['Id']
    Event['Magnitude'] = E['Magnitude']
    Event['Location'] = []
    Event['Log'] = E['Log']

    for L in E['Location']:
      if L['Prime']:
        Event['Location'].append(L)

    if Event['Location']:
      OutP.Events.append(cp.deepcopy(Event))
    else:
      Event['Location'] = E['Location']
      OutN.Events.append(cp.deepcopy(Event))

  return OutP, OutN

#-----------------------------------------------------------------------------------------

def MergeDuplicate(DbA, DbB=[],
                        Twin=60.,
                        Swin=50.,
                        Mwin=[],
                        Zwin=[],
                        Tunit='Second',
                        Owrite=True,
                        Log=False,
                        LogFile=[]):

  #---------------------------------------------------------------------------------------

  if Tunit not in ['Second','Minute','Hour','Day','Month','Year']:
    print 'Warning: not a valid time'
    return

  # Converting current-units to seconds
  if Tunit == 'Second':
    Twin *= 1
  if Tunit == 'Minute':
    Twin *= 60
  if Tunit == 'Hour':
    Twin *= 60*60
  if Tunit == 'Day':
    Twin *= 60*60*24
  if Tunit == 'Month':
    Twin *= 60*60*24*12
  if Tunit == 'Year':
    Twin *= 60*60*24*12*365

  #---------------------------------------------------------------------------------------

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

  def GetMag(Event):
    M = Event['Magnitude'][0]['MagSize']
    return M

  def GetDep(Event):
    Z = Event['Location'][0]['Depth']
    return Z

  #---------------------------------------------------------------------------------------

  def DeltaSec(S0, S1):
    Sec = ma.fabs(S1-S0)
    return Sec

  def DeltaLen(C0, C1):
    Dis = CU.WgsDistance(C0[1],C0[0],C1[1],C1[0])
    return Dis

  def DeltaMag(M0, M1):
    Mag = ma.fabs(M1-M0)
    return Mag

  def DeltaDep(Z0, Z1):
    Dep = ma.fabs(Z1-Z0)
    return Dep

  #---------------------------------------------------------------------------------------
  # Preallocation

  Db0 = DbA.Copy()
  Enum0 = Db0.Size()
  T0 = [0]*Enum0
  S0 = [0]*Enum0
  M0 = [0]*Enum0
  Z0 = [0]*Enum0

  for I in range(0,Enum0):
    E0 = Db0.Events[I]
    T0[I] = GetDate(E0)
    S0[I] = GetCoor(E0)
    M0[I] = GetMag(E0)
    Z0[I] = GetDep(E0)

  if DbB:
    Db1 = DbB.Copy()
    Enum1 = Db1.Size()
    T1 = [0]*Enum1
    S1 = [0]*Enum1
    M1 = [0]*Enum1
    Z1 = [0]*Enum1

    for I in range(0,Enum1):
      E1 = Db1.Events[I]
      T1[I] = GetDate(E1)
      S1[I] = GetCoor(E1)
      M1[I] = GetMag(E1)
      Z1[I] = GetDep(E1)

  else:
    Db1 = Db0.Copy()
    Enum1 = Enum0
    T1 = T0
    S1 = S0
    M1 = M0
    Z1 = Z0

  #---------------------------------------------------------------------------------------

  LogE = []
  Ind = []
  Name = Db1.Header['Name']

  for I in range(0,Enum0):
    Start = 0 if DbB else I+1

    for J in range(Start,Enum1):
      Tpass = False
      Spass = False
      Mpass = False
      Zpass = False

      dT = DeltaSec(T0[I], T1[J])
      if (dT <= Twin):
        Tpass = True

        dS = DeltaLen(S0[I], S1[J])
        if (dS <= Swin):
          Spass = True

          dM = DeltaMag(M0[I], M1[J])
          if Mwin:
            if (dM <= Mwin):
              Mpass = True
          else:
            Mpass = True

          dZ = DeltaDep(Z0[I], Z1[J])
          if Zwin:
            if (dZ <= Zwin):
              Zpass = True
          else:
            Zpass = True

      if all([Tpass, Spass, Mpass, Zpass]):
        E0 = Db0.Events[I]
        E1 = Db1.Events[J]

        E0['Location'].extend(E1['Location'])
        E0['Magnitude'].extend(E1['Magnitude'])
        E0['Log'] += 'MERGED({0}:{1});'.format(Name, E1['Id'])

        LogE.append((I, E0['Id'], J, E1['Id'], dT, dS, dM, dZ))
        Ind.append(J)

  #---------------------------------------------------------------------------------------

  if DbB:
    # Append non-duplicate events to catalogue A
    for I in range(0,Enum1):
      if I not in Ind:
        Db0.Events.append(Db1.Events[I])
        Db0.Events[-1]['Log'] += 'ADDED({0});'.format(Name)

  else:
    # Remove duplicated events from catalogue A
    for I in Ind:
      Db0.Events[I] = []
    Db0.Events = [e for e in Db0.Events if e]

  if LogFile:
    # Open output ascii file
    with open(LogFile, 'w') as f:
      f.write('N1,ID1,N2,ID2,DT,DS\n')
      for L in LogE:
        f.write('{0},{1},'.format(L[0],L[1]))
        f.write('{0},{1},'.format(L[2],L[3]))
        f.write('{0},{1},'.format(L[4],L[5]))
        f.write('{0},{1}\n'.format(L[6],L[7]))
      f.close()

  if Owrite:
    DbA.Events = Db0.Events
    if Log:
      return LogE

  else:
    if Log:
      return Db0, LogE
    else:
      return Db0

#-----------------------------------------------------------------------------------------

def MagConvert(Db, MagAgency, MagOld, MagNew, ConvFun, Owrite=True):

  if type(MagOld) != list:
    MagOld = [MagOld]

  if type(MagOld) != list:
    MagOld = [MagOld]

  if Owrite:
    DbC = Db
  else:
    DbC = Db.Copy()

  Cnt = 0

  for E in DbC.Events:
    for A in E['Magnitude']:

      for Agn in MagAgency:
        if A['MagCode'] == Agn or Agn == '*':

          for Mag in MagOld:
            if A['MagType'] == Mag or Mag == '*':

              MS = A['MagSize']
              ME = A['MagError']

              if not MS: MS = None
              if not ME: ME = 0

              ms,me = ConvFun(MS,ME)
              Cnt += 1

              # Rounding
              if ms != None:
                ms = float(format(ms,'.2f'))
              if me != None:
                me = float(format(me,'.2f'))

              E['Log'] += 'MAGCONV({0}:{1});'.format(A['MagCode'],A['MagType'])
              A['MagSize'] = CU.CastValue('MagSize', ms)
              A['MagError'] = CU.CastValue('MagError', me)
              A['MagType'] = CU.CastValue('MagType', MagNew)

  print "Converting {0} to {1}: {2} events found".format(MagOld, MagNew, Cnt)

  if not Owrite:
    return DbC