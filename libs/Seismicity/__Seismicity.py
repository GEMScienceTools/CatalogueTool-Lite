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

import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------------------

def MfdCum(a, b, Mbin, Mmax):
  """
  Cumulative MFD (Truncated Gutenberg-Richter)
  """

  Mbin = np.array(Mbin)

  Enum = (10.**a)*(10.**(-b*Mbin)-10.**(-b*Mmax))

  # If M > Mmax, remove negative rates
  Enum[Enum < 0] = 0

  return Enum

#-----------------------------------------------------------------------------------------

def MfdInc(a, b, Mbin, Minc, Mmax):
  """
  Incremental MFD (for discrete magnitude intervals).
  """

  Mbin = np.array(Mbin)
  Minc = np.array(Minc)

  Enum0 = MfdCum(a, b, Mbin, Mmax)
  Enum1 = MfdCum(a, b, Mbin+Minc, Mmax)

  return (Enum0-Enum1)

#-----------------------------------------------------------------------------------------

def MfdFit(ab, Enum, Mbin, Minc, Mmax, Merr, bfix=[]):
  """
  Misfit function (log normal)
  """

  # Target coefficients
  a = ab[0]

  if not bfix:
    b = ab[1]
  else:
    b = bfix

  # Analytical distribution
  Esyn = MfdInc(a, b, Mbin, Minc, Mmax)

  # Avoid log of 0
  Esyn[Esyn <= 0] = 1e-300

  Eres = np.log10(Enum/Esyn)

  # L2-norm
  Mfit = np.sum((Eres/Merr)**2.)

  return Mfit

#-----------------------------------------------------------------------------------------

def MfdOptimFun(Enum, Mbin, Minc, Mmax, Merr=[], a0=[], b0=[], bfix=[]):
  """
  Optimisation function
  Note: Minc and Merr can be single (constant) values or array
  """

  # Convert to numpy array
  Enum = np.array(Enum)
  Mbin = np.array(Mbin)
  Minc = np.array(Minc)
  Merr = np.array(Merr)

  # Setting initial values for the search
  if not a0: a0 = 10.
  if not b0: b0 = 1.

  if Merr.size == 0:
    Merr = np.ones_like(Enum)
  if Merr.size == 1:
    Merr = Merr * np.ones_like(Enum)
  if Minc.size == 1:
    Minc = Minc * np.ones_like(Enum)

  # Remove zero rate bins
  idx = (Enum > 0.0)
  Enum = Enum[idx]
  Mbin = Mbin[idx]
  Minc = Minc[idx]
  Merr = Merr[idx]

  # Optimization of GR coefficients
  Out = spo.minimize(MfdFit, [a0, b0], args=(Enum, Mbin, Minc, Mmax, Merr, bfix))

  a = Out.x[0]
  b = Out.x[1]

  if bfix:
    b = bfix

  return a, b

#-------------------------------------------
# Plot results

def mfd_plot(R, M, dM, Mmax, a, b, fig_file=[]):

  # Settings
  from matplotlib import rcParams
  rcParams['font.family'] = 'Times New Roman'
  rcParams['font.size'] = 16
  rcParams['axes.linewidth'] = 1.5

  # Variable Init.
  M = np.array(M)
  dM = np.array(dM)

  Mc = np.arange(0., Mmax, 0.01)

  Nc = mfd_cum(a, b, Mc, Mmax)
  Ni = mfd_inc(a, b, M, dM, Mmax)

  # Plot
  plt.figure(figsize=(5.5,4.5))
  ax = plt.gcf().add_subplot(111)

  # MFD Bounds
  plt.semilogy([Mmax, Mmax],[1.e-4, 1.e+3],'r--',
                                           linewidth=1,
                                           zorder=1)

  plt.semilogy([4.5, 4.5],[1.e-4, 1.e+3],'r--',
                                         linewidth=1,
                                         zorder=1)


  # Cumulative MFD
  plt.semilogy(Mc, Nc, 'r',
                       linewidth=2,
                       zorder=2)

  plt.semilogy(M, R[1], 'ro',
                        markeredgewidth=1,
                        markersize=8,
                        label='Cumulative MFD',
                        zorder=3)

  # Incremental MFD
  plt.semilogy(M+dM/2., R[0], 'ws',
                               markeredgewidth=1,
                               markersize=8,
                               label='Incremental MFD',
                               zorder=3)

  ax.bar(M, Ni, dM, color=[0.9,0.9,0.9],
                    log=True,
                    linewidth=1,
                    zorder=1)

  plt.xlim((4., 8.))
  plt.ylim((1.e-4, 1.e+3))

  plt.text(6.25, 5e+0, 'a-value: '+'{:.2f}'.format(a),
                    weight='bold',
                    color='k',
                    fontsize=14)
  plt.text(6.25, 2e+0, 'b-value: '+'{:.2f}'.format(b),
                    weight='bold',
                    color='k',
                    fontsize=14)
  plt.text(6.25, 8e-1, 'M-max: '+'{:.2f}'.format(Mmax),
                    weight='bold',
                    color='k',
                    fontsize=14)

  plt.title('Gutenberg-Richter Distribution')
  plt.legend(loc=1, borderaxespad=0., numpoints=1)

  plt.xlabel('Magnitude')
  plt.ylabel('Occurrence Rate (Event/Year)')

  plt.gca().yaxis.grid(color='0.65',linestyle='--')
  plt.tight_layout()

  plt.draw()
  plt.show(block=False)

  if fig_file:
    plt.savefig(fig_file, dpi=600)