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

"""
Module for Specific Global Catalogue Parsers
"""

import math as mt
import OQCatk.Catalogue as Cat
import OQCatk.AsciiTools as AT
import OQCatk.CatUtils as CU

#-----------------------------------------------------------------------------------------

class Database(Cat.Database):

  def __init__(self, Name=[], Info=[]):

    super(Database, self).__init__(Name)
    super(Database, self).__init__(Info)

  #---------------------------------------------------------------------------------------

  def ImportIsf(self, file_name):

    def _GetHeader(f):
      Header = f.readline().strip()
      IscType = f.readline().strip()
      return IscType

    def _SplitEvents(f):
      Event = ''
      for Line in f:
        Event += Line
      Event = Event.split('Event ')
      return Event

    def _SplitBlock(Event):
      Id = []
      LocBlock = []
      MagBlock = []
      if Event:
        Rows = Event.split('\n')
        Id = Rows[0].split()[0]
        for R in Rows[1:]:
          if  '(' not in R:
            if (len(R) == 136) and ('Date' not in R):
              LocBlock.append(_GetLocation(R))
            if (len(R) == 38) and ('Magnitude' not in R):
              MagBlock.append(_GetMagnitude(R))
          if '#PRIME' in R:
            LocBlock[-1]['Prime'] = True
      return Id, LocBlock, MagBlock

    def _GetLocation(IsfLoc):
      L = {}
      if IsfLoc:
        L['Year'] = IsfLoc[0:4].strip(' ')
        L['Month'] = IsfLoc[5:7].strip(' ')
        L['Day'] = IsfLoc[8:10].strip(' ')
        L['Hour'] = IsfLoc[10:13].strip(' ')
        L['Minute'] = IsfLoc[14:16].strip(' ')
        L['Second'] = IsfLoc[17:22].strip(' ')
        L['Latitude'] = IsfLoc[36:44].strip(' ')
        L['Longitude'] = IsfLoc[45:54].strip(' ')
        L['Depth'] = IsfLoc[71:76].strip(' ')
        L['SecError'] = IsfLoc[24:29].strip(' ')
        L['DepError'] = IsfLoc[78:82].strip(' ')
        L['LocCode'] = IsfLoc[118:127].strip(' ')
      return L

    def _GetMagnitude(IsfMag):
      M = {}
      if IsfMag:
        M['MagType'] = IsfMag[0:5].strip(' ')
        M['MagSize'] = IsfMag[6:10].strip(' ')
        M['MagError'] = IsfMag[11:14].strip(' ')
        M['MagCode'] = IsfMag[20:29].strip(' ')
      return M

    # Open ISF file
    with open(file_name, 'r') as f:

      _GetHeader(f)
      Event = _SplitEvents(f)

      for E in Event:
        Id, LocBlock, MagBlock = _SplitBlock(E)
        if Id:
          self.AddEvent(Id, LocBlock, MagBlock)

      f.close()
      return

    # Warn user if model file does not exist
    print 'File not found.'

  #---------------------------------------------------------------------------------------

  def ImportNdk(self, file_name):

    def _GetLocation(HypoStr):
      L = {}
      if HypoStr:
        L['Year'] = HypoStr[5:9].strip(' ')
        L['Month'] = HypoStr[10:12].strip(' ')
        L['Day'] = HypoStr[13:15].strip(' ')
        L['Hour'] = HypoStr[16:18].strip(' ')
        L['Minute'] = HypoStr[19:21].strip(' ')
        L['Second'] = HypoStr[22:26].strip(' ')
        L['Latitude'] = HypoStr[27:33].strip(' ')
        L['Longitude'] = HypoStr[34:41].strip(' ')
        L['Depth'] = HypoStr[42:47].strip(' ')
        L['LocCode'] = HypoStr[0:4].strip(' ')
      return L

    def _GetId(CmtStr):
      I = []
      if CmtStr:
        I = CmtStr[0:16].strip(' ')
      return I

    def _GetExponent(CmtStr):
      E = []
      if CmtStr:
        E = float(CmtStr[0:2])
      return E

    def _GetMagnitude(CmtStr, E):
      M = {}
      if CmtStr:
        # Hanks & Kanamori equation
        Moment = float(CmtStr[49:56])*(10.**E)
        Mw = ((2./3.)*mt.log10(Moment))-10.7

        M['MagSize'] = float(format(Mw,'.2f'))
        M['MagType'] = 'MW'
        M['MagError'] = 0.
        M['MagCode'] = 'GCMT-NDK'
      return M

    # Open NDK file
    with open(file_name, 'r') as f:

      while True:

        HypoStr = f.readline().strip('\n')
        Cmt1Str = f.readline().strip('\n')
        Cmt2Str = f.readline().strip('\n')
        Cmt3Str = f.readline().strip('\n')
        Cmt4Str = f.readline().strip('\n')

        L = _GetLocation(HypoStr)
        I = _GetId(Cmt1Str)
        E = _GetExponent(Cmt3Str)
        M = _GetMagnitude(Cmt4Str, E)

        if I:
          self.AddEvent(I, L, M)
        else:
          break

      f.close()
      return

    # Warn user if model file does not exist
    print 'File not found.'

  #---------------------------------------------------------------------------------------

  def ImportIscExt  (self,file_name):
  
    # Defining the headers/estruture
    Header = ['Id','LocCode','MagCode','','Year','Month','Day','Hour','Minute','Second',
              'SecError','Longitude','Latitude','','','','Depth','DepError','MagSize',
              'MagError']

    def _GetMagCode(MagCode):
        try:
           MC = MagCode.split('|')[1]
        except:
           MC = ''
        return MC
    
    # Open/importing ISC_GEM_EXT csv file
    tab = AT.AsciiTable()
    tab.Import(file_name, header=Header,
                         delimiter=',',
                         skipline=1,
                         comment='#',
                         dtype='s')

    for I,D in enumerate(tab.data):
          if 'Id' in D.keys():
             I = D['Id']
          else:
             I += 1            
          # Changing the Magcode [Identifier]
          D['MagCode'] = _GetMagCode(D['MagCode'])
          L = CU.LocationInit()
          M = CU.MagnitudeInit()
      
          for K in tab.header:
              if K in L:
                  L[K] = D[K]
              if K in M:
                  M[K] = D[K]
          if 'Log' in D.keys():
              O = D['Log']
          else:
              O = ''
          self.AddEvent(I, L, M, O)
    return

    # Warn user if model file does not exist
    print 'File not found.'

  #---------------------------------------------------------------------------------------

  def ImportIscGem  (self,file_name):
    """
        to import the original ISC-GEM catalogue
    """
  
    # Defining the headers/estruture
    Header = ['date','lat','lon','smajax','sminax','strike','','depth','dep_unc','','mw',
              'mw_unc','','s','mo','fac','mo_auth','mpp','mpr','mrr','mrt','mtp','mtt',
              'eventid']
    
    def _SplitDate(date):
        Date = ''
        Time = ''
        string = []
        if date:
            string = date.split(' ')
            Date = string[0].strip(' ')
            Time = string[1].strip(' ')
        return Date,Time

    def _GetLocation(date,lat,lon,depth,dep_unc):
        """
        """
        Date = ''
        Time = ''
        strD = []
        strT = []
        L = {}
        Date,Time = _SplitDate(date)
        
        L['LocCode'] = 'ISC-GEM'

        #splitting the Date
        if Date:
            strD = Date.split('-')
            L['Year'] = strD[0].strip(' ')
            L['Month'] = strD[1].strip(' ')
            L['Day'] = strD[2].strip(' ')   

        #splitting the Time
        if Time:
            strT = Time.split(':')
            L['Hour'] = strT[0].strip(' ')
            L['Minute'] = strT[1].strip(' ')
            L['Second'] = strT[2].strip(' ')       

        #get location
        if lat:
            L['Latitude'] = float(lat.strip(' '))
        if lon:
            L['Longitude'] = float(lon.strip(' '))        
        if depth:
            L['Depth'] = float(depth.strip(' '))
        if dep_unc:
            L['DepError'] = float(dep_unc.strip(' '))
        return L

    def _GetMagnitude(mw,mw_unc,s):
        M = {}
        if mw:
            M['MagType'] = 'Mw' + s.strip(' ')
            M['MagSize'] = float(mw.strip(' '))
            M['MagError'] = float(mw_unc.strip(' '))
            M['MagCode'] = 'ISC-GEM'
        return M
    
    # Open/importing ISC_GEM csv file
    tab = AT.AsciiTable()
    tab.Import(file_name, header=Header,
                         delimiter=',',
                         skipline=0,
                         comment='#',
                         dtype='s')

    for I,D in enumerate(tab.data):
        if 'eventid' in D.keys():
            I = D['eventid']
        else:
            I += 1            
        
        L = _GetLocation(D['date'],D['lat'],D['lon'],D['depth'],D['dep_unc'])
        M = _GetMagnitude(D['mw'],D['mw_unc'],D['s'])
      
        for K in tab.header:
            if K in L:
               L[K] = D[K]
            if K in M:
               M[K] = D[K]
            if 'Log' in D.keys():
               O = D['Log']
            else:
               O = ''
        self.AddEvent(I, L, M, O)
    return 
  #---------------------------------------------------------------------------------------
