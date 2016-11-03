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

import math as mt

#----------------------------------------------
# Scordilis (2006)

def MsMw_Scordillis2006(MagSize, MagError):
  """
  """

  if MagSize < 6.1:
    M = 0.67 * MagSize + 2.07
    E = mt.sqrt(0.17**2. + MagError**2.)

  else:
    M = 0.99 * MagSize + 0.08
    E = mt.sqrt(0.2**2. + MagError**2.)

  return (M, E)


def mbMw_Scordillis2006(MagSize, MagError):
  """
  """

  M = 0.85 * MagSize + 1.03
  E = mt.sqrt(0.29**2. + MagError**2.)

  return (M, E)