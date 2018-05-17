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
                           Delta=0.1, SphereGrid=False,
                           Box=[], Buffer=[], Grid=[],
                           Threshold=-100, Unwrap=False,
                           ZeroRates=False):

  if Par <= 0:
    Par = np.inf

  # Catalogue selection
  DbS = Sel.AreaSelect(Db, Wkt, Owrite=0, Buffer=Buffer, Unwrap=Unwrap)
  x,y,z = Exp.GetHypocenter(DbS)

  # Creating the mesh grid
  P = CU.Polygon()
  P.Load(Wkt)

  # Unwrapping coordinates
  if Unwrap:
    x = [i if i > 0. else i+360. for i in x]
    P.Unwrap()

  if Grid:
    XY = [G for G in Grid if P.IsInside(G[0], G[1])]
  else:
    if SphereGrid:
      XY = P.SphereGrid(Delta=Delta, Unwrap=Unwrap)
    else:
      XY = P.CartGrid(Dx=Delta, Dy=Delta, Bounds=Box)

  Win = []
  for xyP in XY:
    Win.append(0)
    for xyE in zip(x,y):
      Dis = CU.WgsDistance(xyP[1], xyP[0], xyE[1], xyE[0])
      Win[-1] += Window(Dis, Par)

  # Scaling and normalising the rates
  Norm = np.sum(Win)

  A = []; X = []; Y = []
  for I,W in enumerate(Win):

    aT = -np.inf
    if Norm > 0. and W > 0.:
      aT = a + np.log10(W/Norm)
      if aT < Threshold:
        # Filter below threshold
        aT = -np.inf

    if ZeroRates:
      A.append(aT)
      X.append(XY[I][0])
      Y.append(XY[I][1])
    else:
      if aT > -np.inf:
        A.append(aT)
        X.append(XY[I][0])
        Y.append(XY[I][1])

  if Unwrap:
    # Wrap back longitudes
    X = [x if x < 180. else x-360. for x in X]

  return X, Y, A