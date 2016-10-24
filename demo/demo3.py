"""
EXAMPLE 3 - ISF CATALOGUE HOMOGENEISATION
"""

import Parsers as Par
import Exploration as Exp

LocCode = ['ISC','NEIC','CSEM']
MagCode = ['GCMT','HRVD','NEIC','ISC','IDC']
MagType = ['MW','MS','ML']

Db = Par.Database('ISC-HOM')
Db.ImportIsf('data/isc-rev-africa.isf')

# Basic Exploration
Key, Freq = Db.Occurrence('Location','Code')
Key, Freq = Db.Occurrence('Magnitude','Code')
Key, Freq = Db.Occurrence('Magnitude','Type')
Db.Size()

Db.Filter('Location','Code',LocCode)
Db.Filter('Magnitude','Code',MagCode)
Db.Filter('Magnitude','Type',MagType)

# Full magnitude report
Exp.MagnitudeReport(Db)

def Ms2Mw(m):
  return 1.*m

def Ml2Mw(m):
  return 1.*m

Db.MagConvert(['Ms','MS'], 'MW', Ms2Mw)
Db.MagConvert(['Ml','ML'], 'MW', Ml2Mw)

Db.Filter('Location','Code',LocCode,First=1)
Db.Filter('Magnitude','Code',MagCode,First=1)
Db.Filter('Magnitude','Type',MagType,First=1)

Db.Export('data/isc-rev-africa-select.csv')
