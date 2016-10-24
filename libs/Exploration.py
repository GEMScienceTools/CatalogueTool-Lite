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

import copy as cp

import Catalogue as Cat
import CatUtils as CU

#-----------------------------------------------------------------------------------------

def AreaSelect(Db, XY, File=[], Owrite=False):

  P = CU.Polygon()

  if File:
    P.Import(XY, Type=File)
  else:
    P.Load(XY)

  DbC = Cat.Database()
  DbC.Header = cp.deepcopy(Db.Header)

  for E in Db.Events:

    Event = {}
    Event['Id'] = E['Id']
    Event['Location'] = []
    Event['Magnitude'] = E['Magnitude']

    for L in E['Location']:

      x = L['Longitude'];
      y = L['Latitude']

      if P.IsInside(x,y):
        Event['Location'].append(L)

    if Event['Location']:
      DbC.Events.append(cp.deepcopy(Event))

  if Owrite:
    Db.Events = DbC.Events
  else:
    return DbC

#-----------------------------------------------------------------------------------------

def MagRangeSelect(Db, MinMag, MaxMag, Owrite=False):

  DbC = cp.deepcopy(Db)

  DbC.Filter('Magnitude','Size',MinMag,Is='>=')
  DbC.Filter('Magnitude','Size',MaxMag,Is='<')

  if Owrite:
    Db.Events = DbC.Events
  else:
    return DbC

#-----------------------------------------------------------------------------------------

def TimeSelect(Db, Date0, Date1):

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

  def GetSec(Event):
    L = Event['Location'][0]
    S = CU.DateToSec(int(L['Year']),
                     int(L['Month']),
                     int(L['Day']),
                     int(L['Hour']),
                     int(L['Minute']),
                     int(L['Second']))
    return S

  Sec = []
  for E in Db.Events:
    Sec.append(GetSec(E))

  Ind = [I for I,S in enumerate(Sec) if S>=Sec0 and S<=Sec1]

  DbN = Cat.Database()
  DbN.Header = cp.deepcopy(Db.Header)

  for I in Ind:
    DbN.Events.append(cp.deepcopy(Db.Events[I]))

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

def MagnitudeReport(Db):

  ItL, ItD = Db.Occurrence('Magnitude','Code')

  for It in ItL:
    DbC = Db.Filter('Magnitude','Code',It,Owrite=False)
    MaL, MaD = DbC.Occurrence('Magnitude','Type')

    print 'Agency: {0}, Events: {1}'.format(It, ItD[It])
    print 'Types: ',
    for Ma in MaL:
      print '{0} ({1})'.format(Ma, MaD[Ma]),
    print ''

#-----------------------------------------------------------------------------------------

def GetHypocenter(Db):

  x = Db.Extract('Location','Longitude')
  y = Db.Extract('Location','Latitude')
  z = Db.Extract('Location','Depth')

  return x, y, z

