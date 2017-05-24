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

import numpy as np

import OQCatk.Selection as Sel
import OQCatk.Exploration as Exp
import OQCatk.CatUtils as CU

#-----------------------------------------------------------------------------------------

def GaussWin (Dis, Sig):

  return np.exp(-(Dis**2)/(Sig**2.))

#-----------------------------------------------------------------------------------------

def SmoothMFD (Db, a, Wkt, Window=GaussWin, Par=50.,
                           Dx=0.1, Dy=0.1, Box=[],
                           Buffer=[]):

  # Catalogue selection
  DbS = Sel.AreaSelect(Db, Wkt, Owrite=0, Buffer=Buffer)
  x,y,z = Exp.GetHypocenter(DbS)

  # Creating the mesh grid
  P = CU.Polygon()
  P.Load(Wkt)
  XY = P.Grid(Dx=Dx, Dy=Dy, Bounds=Box)

  Win = []

  for xyP in XY:
    Win.append(0)

    for xyE in zip(x,y):
      Dis = CU.WgsDistance(xyP[0], xyP[1], xyE[0], xyE[1])
      Win[-1] += Window(Dis, Par)

  # Scaling and normalising the rates
  Norm = np.sum(Win)
  a = [a*g/Norm for g in Win]

  x = [i[0] for i in XY]
  y = [i[1] for i in XY]

  return x, y, a