"""
EXAMPLE 4 - READING CSV CATALOGUE
"""

import Catalogue as Cat

#-----------------------------------------------------------------------------------------
# 1) STANDARD FORMAT

Db = Cat.Database('ISC-Africa')
Db.Import('data/isc-rev-africa-select.csv')

Db.Dump('data/isc-rev-africa-select.bin')

#-----------------------------------------------------------------------------------------
# 2) ARBITRARY FORMAT (USER DEFINED)

H = ['Id','','Year','Month','Day','Hour','Minute','Second',
     'Longitude','Latitude','','','','Depth','DepError',
     'MagSize','MagError','','','','','','','','','']

Db = Cat.Database('ISC-GEM')
Db.Import('data/isc-gem-v3.csv',Header=H,
                                SkipLine=1,
                                Delimiter=',')

Db.SetKey('Prime',True)
Db.SetKey('LocCode','ISC-GEM')
Db.SetKey('MagCode','ISC-GEM')
Db.SetKey('MagType','MW')

#-----------------------------------------------------------------------------------------
# Search Area (Africa) using internal filter

lon = [-20, 60]
lat = [-40, 40]

Db.Filter('Latitude',lat[0],Opr='>=')
Db.Filter('Latitude',lat[1],Opr='<=')
Db.Filter('Longitude',lon[0],Opr='>=')
Db.Filter('Longitude',lon[1],Opr='<=')

Db.Dump('data/isc-gem-v3.bin')