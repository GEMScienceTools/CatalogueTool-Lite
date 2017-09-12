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
Module for Specific Catalogue Parsers
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

  def ImportIscGemExt(self, FileName):

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

    tab = AT.AsciiTable()
    tab.Import(FileName, header=Header,
                         delimiter=',',
                         skipline=1,
                         comment='#',
                         dtype='s')

    for I,D in enumerate(tab.data):

      D['MagCode'] = _GetMagCode(D['MagCode'])

      if 'Id' in D.keys():
        I = D['Id']
      else:
        I += 1
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


