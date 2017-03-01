"""
EXAMPLE 8 - Sort catalogue
"""

import OQCatk.Catalogue as Cat
import OQCatk.Exploration as Exp

#-----------------------------------------------------------------------------------------
# Import catalogue

Db1 = Cat.Database()
Db1.Load('data/isc-rev-africa-select.bin')

#-----------------------------------------------------------------------------------------
# Randomly shuffling catalogue (for testing)

import numpy as np
Ind = np.random.randint(0,Db1.Size(),Db1.Size())

Db2 = Cat.Database('Unsorted')
for I in Ind:
  Db2.Events.append(Db1.Events[I])

#-----------------------------------------------------------------------------------------
# Sorting again

Db2.Sort()

