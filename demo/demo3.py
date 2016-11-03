"""
EXAMPLE 3 - ISF CATALOGUE EXPLORATION
"""

import Parsers as Par

#-----------------------------------------------------------------------------------------
# Isf parsing

Db = Par.Database('ISC-HOM')
Db.ImportIsf('data/isc-rev-africa.isf')

#-----------------------------------------------------------------------------------------
# Basic Exploration and filtering

LocCode = ['ISC','NEIC','CSEM']
MagCode = ['GCMT','HRVD','NEIC','ISC','IDC']
MagType = ['MW','MS','ML']

Key, Freq = Db.Occurrence('LocCode')
Key, Freq = Db.Occurrence('MagCode')
Key, Freq = Db.Occurrence('MagType')

Db.Filter('LocCode',LocCode)
Db.Filter('MagCode',MagCode)
Db.Filter('MagType',MagType)

Db.Filter('LocCode',LocCode,Best=1)
Db.Filter('MagCode',MagCode,Best=1)
Db.Filter('MagType',MagType,Best=1)

Db.Export('data/isc-rev-africa-select.csv')
