#!/usr/bin/env python
# -*- coding: latin-1 -*-
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
# Author: Garcia Julio

def Print(Key):
  if Key in GehCode.keys():
    print 'GEH CODE: {0}'.format(Key)
    print 'GEH AGENCY: {0}'.format(GehCode[Key])
  else:
    print 'Warning: GEH Code not found'


def ChangeCode(Db):

  for E in Db.Events:
    for K in GehCode:
      if E['Location'][0]['LocCode'] == GehCode[K]:
         E['Location'][0]['LocCode'] = K
         E['Magnitude'][0]['MagCode'] = K


GehCode = {
        'ABENO983' :  'Abe and Noguchi, 1983',
        'ALVAL999' :  'Alvarez et al., 1999',
        'AMBAA986a' :  'Ambraseys and Adams, 1986a',
        'AMBAA986b' :  'Ambraseys and Adams, 1986b',
        'AMBAA991' :  'Ambraseys and Adams, 1991',
        'AMBAB003' :  'Ambraseys and Bilham, 2003',
        'AMBAD004' :  'Ambraseys and Douglas, 2004',
        'AMBAJ998' :  'Ambraseys and Jackson, 1998',
        'AMBAJ003' :  'Ambraseys and Jackson, 2003',
        'AMBAM982' :  'Ambraseys and Melville, 1982',
        'AMBAL994' :  'Ambraseys et al., 1994',
        'AMBA989'  :  'Ambraseys, 1989',
        'AMBA997a' :  'Ambraseys, 1997a',
        'AMBA997b' :  'Ambraseys, 1997b',
        'AMBA001b' :  'Ambraseys, 2001b',
        'AMBA006'  :  'Ambraseys, 2006',
        'AMBA009'  :  'Ambraseys, 2009',
        'BAKU999'  :  'Bakun, 1999',
        'BAKU000'  :  'Bakun, 2000',
        'BAKU006a' :  'Bakun, 2006a',
        'BAKU006b' :  'Bakun, 2006b',
        'BATAO000' :  'Bautista and Oike, 2000',
        'BEAAL010' :  'Beauval et al., 2010',
        'BEAAL013' :  'Beauval et al., 2013',
        'BENAL012' :  'Benito et al., 2012',
        'BILH005'  :  'Bilham et al., 2005',
        'BOZK007'  :  'Bozkurt et al., 2007',
        'CERES995' :  'CERESIS, 1995',
        'CEUS012'  :  'CEUS, 2012',
        'CSSB990'  :  'China State Seismo. Bureau and Fudan University, 1990a',
        'CHIAK004' :  'Chiu and Kim, 2004',
        'CHOAL010' :  'Choy et al., 2010',
        'CUMM007'  :  'Cummins, 2007',
        'DIMAL005' :  'Dimate et al., 2005',
        'DORAL990' :  'Dorbath et al., 1990',
        'DOREL981' :  'Dorel, 1981',
        'DOSE006'  :  'Doser, 2006',
        'ENGVI002' :  'Engdahl and Villasenor, 2002',
        'FELCA008' :  'Felzer and Cao, 2008',
        'FLOAL012' :  'Flores et al., 2012',
        'GARAL985' :  'Garcia et al., 1985',
        'GEON011'  :  'GeoNet, 2011',
        'GOIN979'  :  'Gouin, 1979',
        'GRUAS006' :  'Grunewald and Stein, 2006',
        'HAMAL010' :  'Hamdache et al., 2010',
        'INPRE012' :  'INPRES, 2012',
        'ISCG012'  :  'ISC-GEM, 2012',
        'LAMAL008' :  'Lamontagne et al., 2008',
        'LOMN004'  :  'Lomnitz, 2004',
        'MAKAL012' :  'Makropoulos et al., 2012',
        'MINZ995'  :  'Min Ziqun, 1995',
        'MOCQ007'  :  'Mocquet, 2007',
        'MUSS012'  :  'Musson, 2012',
        'MUSS012a' :  'Musson, 2012a',
        'MUSS012b' :  'Musson, 2012b',
        'MUSS012c' :  'Musson, 2012c',
        'ONCAL999' :  'Oncescu et al., 1999',
        'ORTAB003' :  'Ortiz and Bilham, 2003',
        'PALAL005' :  'Palme et al., 2005',
        'PALAL009' :  'Palme et al., 2009',
        'PALAL007' :  'Pelaez et al., 2007',
        'PERAM999' :  'Peraldo and Montero, 1999',
        'RICH958'  :  'Richter, 1958',
        'SBEAL005' :  'Sbeinati et al., 2005',
        'SCHAM005' :  'Schulte and Mooney, 2005',
        'SHEAL997' :  'Shebalin and Leydecker, 1997',
        'SHEAT997' :  'Shebalin and Tatevossian, 1997',
        'SHV011'   :  'Sismologia Historica de Venezuela, 2011',
        'STOAC993' :  'Stover and Coffman, 1993',
        'STUAL012' :  'Stucchi et al., 2012',
        'SUAAA009' :  'Suarez and Albini, 2009',
        'SZEAL010' :  'Szeliga et al., 2010',
        'TANAS997' :  'Tanner and Shepherd, 1997',
        'TATAL012' :  'Tatevossian et al., 2012',
        'TAVAL001' :  'Tavera et al., 2001',
        'TORRE010' :  'Torres-Vera, 2010',
        'USA979'   :  'Usami, 1979',
        'UTSol'    :  'UTSU online',
        'WHIAL004' :  'White et al., 2004',
        'WHI984'   :  'White, 1984',
        'WYSAK992' :  'Wyss and Koyanagi, 1992',
        'ZUNAL997' :  'Zuniga et al., 1997',
        'ZHAAL999' :  'Zhang et al., 1999'
        }