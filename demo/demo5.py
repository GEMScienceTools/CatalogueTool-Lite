"""
EXAMPLE 5 - CATALOGUE MERGING
"""

import Catalogue as Cat

Db1 = Cat.Database()
Db1.Load('data/isc-rev-africa-select.bin')

Db2 = Cat.Database()
Db2.Load('data/isc-gem-v3.bin')

Log = Db1.MergeDuplicate(Db2,Twin=60.,Swin=50.,Log=1)

CodeList = ['ISC-GEM','ISC-HOM']

Db1.Filter('Location','Code',CodeList,First=1)
Db1.Filter('Magnitude','Code',CodeList,First=1)

