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

import math as mt

#-----------------------------------------------------------------------------------------
# Generic (template)

def Mw_Mw_Generic(MagSize, MagError):
  """
  """

  return (MagSize, MagError)

#-----------------------------------------------------------------------------------------
# Scordilis (2006)
#
# MS >> Mw

def Ms_Mw_Scordilis2006(MagSize, MagError):
  """
  Linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.0 and MagSize <= 6.1:
    M = 0.67 * MagSize + 2.07
    E = mt.sqrt(0.17**2. + MagError**2.)

  elif MagSize > 6.1 and MagSize <= 8.2:
    M = 0.99 * MagSize + 0.08
    E = mt.sqrt(0.2**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

# mb >> Mw

def mb_Mw_Scordilis2006(MagSize, MagError):
  """
  Linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 6.2:
    M = 0.85 * MagSize + 1.03
    E = mt.sqrt(0.29**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

#-----------------------------------------------------------------------------------------
# Di Giacomo 2015
#
# Note:
#   No Error is provided from the paper.
#   Magnitude range is taken approximatively 
#   from the paper's pictures. To check...
#
# MS >> Mw

def Ms_Mw_Lin_DiGiacomo2015(MagSize, MagError):
  """
  Piecewise linear
  """

  if MagSize >= 3.5 and MagSize <= 6.47:
    M = 0.67 * MagSize + 2.13
    E = MagError

  elif MagSize > 6.47 and MagSize <= 8.0:
    M = 1.10 * MagSize - 0.67
    E = MagError

  else:
    M = None
    E = None

  return (M, E)

def Ms_Mw_Exp_DiGiacomo2015(MagSize, MagError):
  """
  Exponential
  """

  if MagSize >= 3.5 and MagSize <= 8.0:
    M = mt.exp(-0.222 + 0.233 * MagSize) + 2.863
    E = MagError

  else:
    M = None
    E = None

  return (M, E)

# mb >> Mw

def mb_Mw_Lin_DiGiacomo2015(MagSize, MagError):
  """
  Linear
  """

  if MagSize >= 4.0 and MagSize <= 6.5:
    M = 1.38 * MagSize - 1.79
    E = MagError

  else:
    M = None
    E = None

  return (M, E)

def mb_Mw_Exp_DiGiacomo2015(MagSize, MagError):
  """
  Exponential
  """

  if MagSize >= 4.0 and MagSize <= 6.5:
    M =  mt.exp(-4.664 + 0.859 * MagSize) + 4.555
    E = MagError

  else:
    M = None
    E = None

  return (M, E)

#-----------------------------------------------------------------------------------------
# Weatherill 2016
#
# Mwrun >> Mw
def Mw_Mw_NEIC_Weatherill2016(MagSize, MagError):
  """
  Linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 4.5 and MagSize <= 9.0:
    M = 1.021 * MagSize - 0.091
    E = mt.sqrt(0.105**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)


# MS >> Mw

def Ms_Mw_ISC_Weatherill2016(MagSize, MagError):
  """
  Piecewise linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 6.0:
    M = 0.616 * MagSize + 2.369
    E = mt.sqrt(0.147**2. + MagError**2.)

  elif MagSize > 6.0 and MagSize <= 8.0:
    M = 0.994 * MagSize + 0.1
    E = mt.sqrt(0.174**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

def Ms_Mw_NEIC_Weatherill2016(MagSize, MagError):
  """
  Piecewise linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 6.47:
    M = 0.723 * MagSize + 1.798
    E = mt.sqrt(0.159**2. + MagError**2.)

  elif MagSize > 6.47 and MagSize <= 8.0:
    M = 1.005 * MagSize - 0.026
    E = mt.sqrt(0.187**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

def Msz_Mw_NEIC_Weatherill2016(MagSize, MagError):
  """
  Piecewise linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 6.47:
    M = 0.707 * MagSize + 1.933
    E = mt.sqrt(0.179**2. + MagError**2.)

  elif MagSize > 6.47 and MagSize <= 8.0:
    M = 0.950 * MagSize + 0.359
    E = mt.sqrt(0.204**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

# mb >> Mw

def mb_Mw_ISC_Weatherill2016(MagSize, MagError):
  """
  Linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 7.0:
    M = 1.048 * MagSize - 0.142
    E = mt.sqrt(0.317**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)

def mb_Mw_NEIC_Weatherill2016(MagSize, MagError):
  """
  Linear
  """
  M=None
  E=None
  Mo=None
  Eo=None

  if MagSize >= 3.5 and MagSize <= 7.0:
    M = 1.159 * MagSize - 0.659
    E = mt.sqrt(0.283**2. + MagError**2.)
  else:
    Mo = MagSize
    Eo = MagError

  return (M, E, Mo, Eo)


#-----------------------------------------------------------------------------------------
# Edwards 2010
#
# Ml >> Mw

def Ml_Mw_Edwards2010(MagSize, MagError):
  """
  Polynomial
  """

  if MagSize <= 6.0:
    M = 0.0491 * MagSize**2 + 0.472 * MagSize + 1.02
    E = mt.sqrt(0.15**2. + MagError**2.)

  else:
    M = None
    E = None

  return (M, E)

#-----------------------------------------------------------------------------------------
# CCARA - Mexico - 2017
#

def mb_Mw_NEIC_Weatherill2016_SSNM(MagSize, MagError):
  """
  Linear
  NOTA: cambie el rango de uso [3.75 - 5.0]
  """
  if MagSize >= 3.5 and MagSize < 6.0:
    M = 1.159 * MagSize - 0.659
    E = mt.sqrt(0.283**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def mb_Mw_NEIC_Weatherill2016_CDSA(MagSize, MagError):
  """
  Linear
  NOTA: cambie el rango de uso [3.75 - 5.0]
  """

  if MagSize >= 3.0 and MagSize < 7.0:
    M = 1.159 * MagSize - 0.659
    E = mt.sqrt(0.283**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def M_Mw_SSNM_GCMT_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 4.5 and MagSize <= 7.0:
    M = 0.876 * MagSize + 0.815
    E = mt.sqrt(0.169**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def M_Mw_RESNOM_GCMT_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 4.75 and MagSize <= 7.1:
    M = 0.990 * MagSize + 0.168
    E = mt.sqrt(0.213**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def M_mb_RESNOM_NEIC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.5 and MagSize <= 5.75:
    M = 0.965 * MagSize + 0.004
    E = mt.sqrt(0.279**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def M_mb_CDSA_NEIC_P(MagSize, MagError):
  """
  Polynomial D1
  """
 if MagSize >= 3.2 and MagSize <= 5.5:
    M = 0.995 * MagSize + 0.199
    E = mt.sqrt(0.204**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def ml_mb_PRSN_NEIC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.5 and MagSize <= 5.5:
    M = 1.069 * MagSize - 0.311
    E = mt.sqrt(0.279**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def MD_mb_ECX_NEIC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.75 and MagSize <= 6.0:
    M = 0.969 * MagSize + 0.041
    E = mt.sqrt(0.297**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def ML_mb_ECX_NEIC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.75 and MagSize <= 6.0:
    M = 0.982 * MagSize - 0.153
    E = mt.sqrt(0.305**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def MD_Mw_MEX_GCMT_E(MagSize, MagError):
  """
  Exponential
  """
  if MagSize >= 4.0 and MagSize <= 6.75:
    M =  mt.exp(-3.202 + 0.629 * MagSize) + 4.258
    E = mt.sqrt(0.208**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def ML_Mw_CASC_CASC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.5 and MagSize <= 5.5:
    M = 0.843 * MagSize + 0.954
    E = mt.sqrt(0.446**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def MD_Mw_CASC_CASC_P(MagSize, MagError):
  """
  Polynomial D1
  """
  if MagSize >= 3.5 and MagSize <= 5.5:
    M = 1.478 * MagSize - 1.807
    E = mt.sqrt(0.505**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)

def MD_mb_Mw_NEIC_Weatherill2016(MagSize, MagError):
  """
  Linear
  modified to convert the TRN[MD] magnitudes
  """
 
  if MagSize >= 3.5 and MagSize <= 6.5:
    M = 1.159 * (MagSize+0.248) - 0.659
    E = mt.sqrt(0.283**2. + MagError**2.)
  else:
    M = MagSize
    E = MagError

  return (M, E)




