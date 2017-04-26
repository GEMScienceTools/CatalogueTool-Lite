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

import math as ma
import re

#-----------------------------------------------------------------------------------------

def LocationInit():

  L = {'Year': None,
       'Month': None,
       'Day': None,
       'Hour': None,
       'Minute': None,
       'Second': None,
       'Latitude': None,
       'Longitude': None,
       'Depth': None,
       'SecError': None,
       'LatError': None,
       'LonError': None,
       'DepError': None,
       'LocCode': None,
       'Prime': False}

  return L

#-----------------------------------------------------------------------------------------

def MagnitudeInit():

  M = {'MagSize': None,
       'MagError': None,
       'MagType': None,
       'MagCode': None}

  return M

#-----------------------------------------------------------------------------------------

def CastValue(key, value):

  C = {'Id': 's',
       'Log': 's',
       'Year': 'i',
       'Month': 'i',
       'Day': 'i',
       'Hour': 'i',
       'Minute': 'i',
       'Second': 'f',
       'Latitude': 'f',
       'Longitude': 'f',
       'Depth': 'f',
       'SecError': 'f',
       'LatError': 'f',
       'LonError': 'f',
       'DepError': 'f',
       'LocCode': 's',
       'Prime': 'b',
       'MagSize': 'f',
       'MagError': 'f',
       'MagType': 's',
       'MagCode': 's'}

  if not IsEmpty(value):
    if C[key] == 'i':
      value = int(value)
    if C[key] == 'f':
      value = float(value)
    if C[key] == 's':
      value = str(value)
    if C[key] == 'b':
      value = bool(value)
  else:
    value = None

  return value

#-----------------------------------------------------------------------------------------

def KeyGroup(key):

  L = LocationInit()
  M = MagnitudeInit()
  G = []

  if key in L.keys():
    G = 'Location'

  if key in M.keys():
    G = 'Magnitude'

  return G

#-----------------------------------------------------------------------------------------

def IsEmpty(number):

  C0 = (number == [])
  C1 = (number == '')
  C2 = (number != number)
  C3 = (number == None)
  C4 = (number == 'None')

  return (C0 or C1 or C2 or C3 or C4)

#-----------------------------------------------------------------------------------------

def IsType(value, dtype):

  Out = False

  if dtype in ['Bool','bool','B','b']:
    if type(value) == bool:
      Out = True
  if dtype in ['Int','int','I','i']:
    if type(value) == int:
      Out = True
  if dtype in ['Float','float','F','f']:
    if type(value) == float:
      Out = True
  if dtype in ['String','string','S','s']:
    if type(value) == str:
      Out = True
  if dtype in ['List','list','L','l']:
    if type(value) == list:
      Out = True
  if dtype in ['Tuple','tuple','T','t']:
    if type(value) == tuple:
      Out = True

  return Out

#-----------------------------------------------------------------------------------------

def WgsDistance(Lat1, Lon1, Lat2, Lon2):

    # Author: Salvador Dali
    # http://stackoverflow.com/users/1090562/salvador-dali
    p = 0.017453292519943295

    c1 = ma.cos((Lat2 - Lat1) * p)
    c2 = ma.cos(Lat1 * p)
    c3 = ma.cos(Lat2 * p)
    c4 = ma.cos((Lon2 - Lon1) * p)

    a = 0.5 - c1/2 + c2 * c3 * (1 - c4) / 2

    return 12742 * ma.asin(ma.sqrt(a))

#-----------------------------------------------------------------------------------------

def LeapCheck(Year):

  C0 = (Year % 4 == 0)
  C1 = (Year % 100 != 0)
  C2 = (Year % 400 == 0)

  return (C0 and C1) or C2

def LeapNum(Year):

  N0 = (Year-1)//4
  N1 = (Year-1)//100
  N2 = (Year-1)//400

  return N0 - N1 + N2

#-----------------------------------------------------------------------------------------

def DateToSec(Year, Month, Day, Hour, Minute, Second):

  if Year < 1:
    print 'Warning: Year must be > 1'
    return None

  if not Year: Year = 1.
  if not Month: Month = 1.
  if not Day: Day = 1.
  if not Hour: Hour = 0.
  if not Minute: Minute = 0.
  if not Second: Second = 0.

  DSEC = 24.*3600.
  YDAYS = 365.

  if LeapCheck(Year):
    MDAYS = [0.,31.,60.,91.,121.,152.,182.,213.,244.,274.,305.,335.]
  else:
    MDAYS = [0.,31.,59.,90.,120.,151.,181.,212.,243.,273.,304.,334.]

  YSec = (Year-1)*YDAYS*DSEC
  YSec += LeapNum(Year)*DSEC

  MSec = MDAYS[int(Month)-1]*DSEC

  DSec = (Day-1)*DSEC

  Sec = YSec + MSec + DSec + Hour*3600.+ Minute*60. + Second*1.

  return Sec

#-----------------------------------------------------------------------------------------

class Polygon():

  def __init__(self):

    self.x = []
    self.y = []

  #---------------------------------------------------------------------------------------

  def Load(self, XY):
    """
    Input polygon can be defined in two possible ways:
    1) list of x-y float pairs, e.g.
        [[22.0, -15.0],[24.0, -15.0],[24.0, -10.0],[22.0, -15.0]]
    2) wkt formatted string, e.g.
        'POLYGON((22. -15.,24. -15.,24. -10.,22. -15.))'
    """

    if type(XY) == list:
      self.x = [N[0] for N in XY]
      self.y = [N[1] for N in XY]

    else:
      # WKT String
      XY = XY.split('((')[1]
      XY = XY.split('))')[0]
      XY = XY.split('),(')

      self.x = []
      self.y = []

      for WktGroup in XY:
        WktArray = WktGroup.split(',')

        for WktPoint in WktArray[:-1]:
          point = re.split(' +', WktPoint)
          self.x.append(float(point[0]))
          self.y.append(float(point[1]))

  #---------------------------------------------------------------------------------------

  def IsInside(self, x, y):

    x0 = self.x[0]
    y0 = self.y[0]

    inside = False
    n = len(self.x)

    for i in range(n+1):
      x1 = self.x[i % n]
      y1 = self.y[i % n]

      if min(y0,y1) < y <= max(y0,y1):
        if x <= max(x0,x1):
          if y0 != y1:
            xints = (y-y0)*(x1-x0)/(y1-y0)+x0
          if x0 == x1 or x <= xints:
            inside = not inside
      x0,y0 = x1,y1

    return inside

  #---------------------------------------------------------------------------------------

  def Import (self, FileName, Type='xy'):

    with open(FileName, 'r') as f:

      XY = []
      if Type == 'wkt':
        XY = f.readline().strip()

      if Type == 'xy':
        for xy in f:
          xy = xy.strip()
          if xy:
            xy = re.split(',|;| ',xy)
            XY.append([float(xy[0]), float(xy[1])])

      self.Load(XY)
      f.close()
      return

    # Warn user if model file does not exist
    print 'File not found.'

  #---------------------------------------------------------------------------------------

  def WgsCart (self):
    """
    Approximate conversion using sinusoidal projection.
    """

    earth_radius = 6371009. # in meters
    y_dist = np.pi * earth_radius / 180.0

    y = self.y * y_dist
    x = self.x * y_dist * np.cos(np.radians(self.y))

    # Convert to Km
    self.y = y/1000.
    self.x = x/1000.

  #---------------------------------------------------------------------------------------

  def Area (self):
    """
    Using Shoelace formula to compute area.
    """

    A = np.dot(self.x, np.roll(self.y, 1))
    B = np.dot(self.y, np.roll(self.x, 1))

    return 0.5*np.abs(A-B)