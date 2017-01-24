#!/usr/bin/env python
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Poggi Valerio

"""
Module for Format Conversion
"""

import AsciiTools as AT

#-----------------------------------------------------------------------------------------

def Catk2Hmtk(InputFile, OutputFile):

  tab = AT.AsciiTable()
  tab.Import(InputFile, dtype='s')

  tab.RenameKey('Id','eventID')
  tab.RenameKey('Year','year')
  tab.RenameKey('Month','month')
  tab.RenameKey('Day','day')
  tab.RenameKey('Hour','hour')
  tab.RenameKey('Minute','minute')
  tab.RenameKey('Second','second')
  tab.RenameKey('Latitude','latitude')
  tab.RenameKey('Longitude','longitude')
  tab.RenameKey('Depth','depth')
  tab.RenameKey('SecError','timeError')
  tab.RenameKey('DepError','depthError')
  tab.RenameKey('MagSize','magnitude')
  tab.RenameKey('MagError','sigmaMagnitude')

  tab.AddKey('Agency',index=1)
  tab.AddKey('SemiMajor90',index=11)
  tab.AddKey('SemiMinor90',index=12)
  tab.AddKey('ErrorStrike',index=13)

  for D in tab.data:
    D['Agency']=D['LocCode']+'|'+D['MagCode']
    D['SemiMajor90'] = None
    D['SemiMinor90'] = None
    D['ErrorStrike'] = None

  tab.RemoveKey('LatError')
  tab.RemoveKey('LonError')
  tab.RemoveKey('LocCode')
  tab.RemoveKey('MagType')
  tab.RemoveKey('MagCode')
  tab.RemoveKey('Log')

  tab.Export(OutputFile)
