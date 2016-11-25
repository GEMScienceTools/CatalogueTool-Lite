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

import math as ma
import copy as cp
import cPickle as pk

import AsciiTools as AT
import CatUtils as CU

#-----------------------------------------------------------------------------------------

class Database(object):

  def __init__(self, Name=[], Info=[]):

    self.Header = {'Name': Name, 'Info': Info}
    self.Events = []

  #---------------------------------------------------------------------------------------

  def AddEvent(self, Id, Location=[],
                         Magnitude=[],
                         Log='',
                         Append=False):

    Event = {}
    Event['Id'] = CU.CastValue('Id', Id)
    Event['Log'] = Log
    Event['Location'] = []
    Event['Magnitude'] = []

    if Location:

      if type(Location) is dict:
        Location = [Location]

      for L in Location:
        Event['Location'].append(CU.LocationInit())
        for K in L.keys():
          Event['Location'][-1][K] = CU.CastValue(K, L[K])

    if Magnitude:

      if type(Magnitude) is dict:
        Magnitude = [Magnitude]

      for M in Magnitude:
        Event['Magnitude'].append(CU.MagnitudeInit())
        for K in M.keys():
          Event['Magnitude'][-1][K] = CU.CastValue(K, M[K])

    if not Append:

      self.Events.append(Event)

    else:

      I = self.GetIndex(Id)

      if I != []:
        self.Events[I]['Location'] += Event['Location']
        self.Events[I]['Magnitude'] += Event['Magnitude']
      else:
        print 'Warning: Not a valid Id'

  #---------------------------------------------------------------------------------------

  def DelEvent(self, I):

    if CU.IsType(I, 's'):
      I = self.GetIndex(I)
    else:
      I = int(I)

    if I != []:
      del self.Events[I]
    else:
      print 'Warning: Event not found'

  #---------------------------------------------------------------------------------------

  def GetIndex(self, Id):

    try:
      I = [E['Id'] for E in self.Events].index(Id)
    except:
      I = []

    return I

  #---------------------------------------------------------------------------------------

  def PrintEvent(self, I):

    if CU.IsType(I, 's'):
      I = self.GetIndex(I)

    if I != []:
      E = self.Events[I]

      print 'Event Id: {0}'.format(E['Id'])
      print 'Location:'

      for n, L in enumerate(E['Location']):
        print '[{0}] -'.format(n),
        print 'Year: {0}'.format(L['Year']),
        print 'Month: {0}'.format(L['Month']),
        print 'Day: {0}'.format(L['Day']),
        print 'Hour: {0}'.format(L['Hour']),
        print 'Minute: {0}'.format(L['Minute']),
        print 'Second: {0}'.format(L['Second']),
        print 'Latitude: {0}'.format(L['Latitude']),
        print 'Longitude: {0}'.format(L['Longitude']),
        print 'Depth: {0}'.format(L['Depth']),
        print 'Agency: {0}'.format(L['LocCode']),
        print 'Prime: {0}'.format(L['Prime'])

      print 'Magnitude:'
      for m, M in enumerate(E['Magnitude']):
        print '[{0}] -'.format(m),
        print 'Type: {0}'.format(M['MagType']),
        print 'Size: {0}'.format(M['MagSize']),
        print 'Error: {0}'.format(M['MagError']),
        print 'Agency: {0}'.format(M['MagCode'])

      print 'Log:'
      print '{0}'.format(E['Log'])

    else:
      print 'Warning: Event not found'

  #---------------------------------------------------------------------------------------

  def Size(self):

    return len(self.Events)

  #---------------------------------------------------------------------------------------

  def SetKey(self, Key, Value, Match=[]):

    Group = CU.KeyGroup(Key)

    for E in self.Events:
      for P in E[Group]:

        if Match and (P[Match[0]] == Match[1]):
          P[Key] = CU.CastValue(Key, Value)

        if not Match:
          P[Key] = CU.CastValue(Key, Value)

  #---------------------------------------------------------------------------------------

  def SetID(self, Str0='', Str1=''):

    LZ = len(str(self.Size()))

    for I, E in enumerate(self.Events):
      E['Log'] += 'PREID({0});'.format(E['Id'])
      E['Id'] = Str0+str(I).zfill(LZ)+Str1

  #---------------------------------------------------------------------------------------

  def Filter(self,Key, Value, Opr='=',
                              Best=False,
                              All=False,
                              Owrite=True):

    def Search(Event, Value, Str0, Str1, Opr, Best):

      NewE = {}
      NewE[Str1] = []
      NewE[Str0] = []
      Klist = []

      for V in Value:
        for E in Event[Str0]:

          if (Opr == '=') and (E[Key] == V):
              NewE[Str0].append(E)
          if (Opr == '!=') and (E[Key] != V):
              NewE[Str0].append(E)
          if (Opr == '>') and (E[Key] > V):
              NewE[Str0].append(E)
          if (Opr == '<') and (E[Key] < V):
              NewE[Str0].append(E)
          if (Opr == '>=') and (E[Key] >= V):
              NewE[Str0].append(E)
          if (Opr == '<=') and (E[Key] <= V):
              NewE[Str0].append(E)

      Klist = [k[Key] for k in NewE[Str0]]

      if NewE[Str0]:
        NewE['Id'] = Event['Id']
        NewE['Log'] = Event['Log']
        NewE[Str1] = Event[Str1]
        if Best:
          NewE[Str0] = [NewE[Str0][0]]

      return NewE, Klist

    Out = Database()
    Out.Header = cp.deepcopy(self.Header)

    if not CU.IsType(Value, 'l'):
      Value = [Value]

    Group = CU.KeyGroup(Key)

    for E in self.Events:

      if Group == 'Location':
        E, Klist = Search(E, Value, 'Location', 'Magnitude', Opr, Best)

      if Group == 'Magnitude':
        E, Klist = Search(E, Value, 'Magnitude', 'Location', Opr, Best)

      if E['Location'] or E['Magnitude']:
        if All:
          if sorted(Value) == sorted(set(Klist)):
            Out.Events.append(cp.deepcopy(E))
        else:
          Out.Events.append(cp.deepcopy(E))

    if Owrite:
      self.Events = Out.Events
    else:
      return Out

  #---------------------------------------------------------------------------------------

  def Extract(self, Key=[]):

    Group = CU.KeyGroup(Key)

    if Key == 'Id' or Key == 'Log':
      Values = [E[Key] for E in self.Events]
    else:
      Values = [E[Group][0][Key] for E in self.Events]

    return Values

  #---------------------------------------------------------------------------------------

  def Occurrence(self, Key, Verbose=False):

    ItemList = []

    Group = CU.KeyGroup(Key)

    for E in self.Events:
      for P in E[Group]:
        Item = P[Key]
        ItemList.append(Item)

    ItemDict = {i:ItemList.count(i) for i in set(ItemList)}
    ItemList = sorted(ItemDict, key=ItemDict.get, reverse=True)

    if Verbose:
      print Key, ': Occurrence'
      print '----------------------'
      for w in ItemList:
        print w, ':', ItemDict[w]

    return ItemList, ItemDict

  #---------------------------------------------------------------------------------------

  def Append(self, NewDb):

    for n in range(NewDb.Size()):
      self.Events.append(NewDb.Events[n])

  #---------------------------------------------------------------------------------------

  def Copy(self):

    NewCat = Database()
    NewCat.Header = cp.deepcopy(self.Header)
    NewCat.Events = cp.deepcopy(self.Events)
    return NewCat

  #---------------------------------------------------------------------------------------

  def Sort(self):

    Sec = []
    for E in self.Events:

      L = E['Location'][0]
      S = CU.DateToSec(L['Year'],
                       L['Month'],
                       L['Day'],
                       L['Hour'],
                       L['Minute'],
                       L['Second'])
      Sec.append(S)

    # Get indexes of the sorted list
    Ind = sorted(range(len(Sec)), key=lambda k: Sec[k])

    Events = []
    for I in Ind:
      Events.append(self.Events[I])

    self.Events = cp.deepcopy(Events)

  #---------------------------------------------------------------------------------------

  def Import(self, FileName, Header=[],
                             Delimiter=',',
                             SkipLine=0,
                             Comment='#'):

    tab = AT.AsciiTable()
    tab.Import(FileName, header=Header,
                         delimiter=Delimiter,
                         skipline=SkipLine,
                         comment=Comment,
                         dtype='s')

    for D in tab.data:

      L = CU.LocationInit()
      M = CU.MagnitudeInit()

      for K in tab.header:
        if K in L:
          L[K] = D[K]
        if K in M:
          M[K] = D[K]

      self.AddEvent(D['Id'], L, M)

  #---------------------------------------------------------------------------------------

  def Export(self, FileName):

    tab = AT.AsciiTable()

    tab.header = ['Id',
                  'Year',
                  'Month',
                  'Day',
                  'Hour',
                  'Minute',
                  'Second',
                  'Latitude',
                  'Longitude',
                  'Depth',
                  'SecError',
                  'LatError',
                  'LonError',
                  'DepError',
                  'LocCode',
                  'MagSize',
                  'MagError',
                  'MagType',
                  'MagCode',
                  'Log']

    for Id, E in enumerate(self.Events):
      Data = [E['Id'],
              E['Location'][0]['Year'],
              E['Location'][0]['Month'],
              E['Location'][0]['Day'],
              E['Location'][0]['Hour'],
              E['Location'][0]['Minute'],
              E['Location'][0]['Second'],
              E['Location'][0]['Latitude'],
              E['Location'][0]['Longitude'],
              E['Location'][0]['Depth'],
              E['Location'][0]['SecError'],
              E['Location'][0]['LatError'],
              E['Location'][0]['LonError'],
              E['Location'][0]['DepError'],
              E['Location'][0]['LocCode'],
              E['Magnitude'][0]['MagSize'],
              E['Magnitude'][0]['MagError'],
              E['Magnitude'][0]['MagType'],
              E['Magnitude'][0]['MagCode'],
              E['Log']]

      tab.AddElement(Data)

    tab.Export(FileName)

  #---------------------------------------------------------------------------------------

  def Dump(self, FileName):

    with open(FileName, 'wb') as f:
      C = (self.Header, self.Events)
      pk.dump(C, f, protocol=2)
      f.close()
      return

    # Warn user if model file does not exist
    print 'Warning: Cannot open file'

  #---------------------------------------------------------------------------------------

  def Load(self, FileName):

    with open(FileName, 'rb') as f:
      C = pk.load(f)
      self.Header = C[0]
      self.Events = C[1]
      f.close()
      return

    # Warn user if model file does not exist
    print 'Warning: Cannot open file'

