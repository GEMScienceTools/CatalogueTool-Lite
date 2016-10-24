"""
EXAMPLE 4 - READING CSV CATALOGUE
"""

import Catalogue as Cat

# 1) STANDARD FORMAT
Db = Cat.Database('ISC-Africa')
Db.Import('data/isc-rev-africa-select.csv')

Db.Dump('data/isc-rev-africa-select.bin')


# 2) ARBITRARY FORMAT (USER DEFINED)
Db = Cat.Database('ISC-GEM')

H = ['Id','Code','Year','Month','Day','Hour','Minute','Second',
     'Longitude','Latitude','_','_','_','Depth','_',
     'Size','Error','_','_','_','_','_','_','_','_','_']

Db.Import('data/isc-gem-v3.csv',Header=H,SkipLine=1)

Db.SetKey('Location','Prime',True)
Db.SetKey('Magnitude','Type','MW')

# Search Area (Africa)
lon = [-20, 60]
lat = [-40, 40]

Db.Filter('Location','Latitude',lat[0],Is='>=')
Db.Filter('Location','Latitude',lat[1],Is='<=')
Db.Filter('Location','Longitude',lon[0],Is='>=')
Db.Filter('Location','Longitude',lon[1],Is='<=')

Db.Dump('data/isc-gem-v3.bin')