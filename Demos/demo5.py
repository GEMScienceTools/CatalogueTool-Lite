"""
EXAMPLE 5 - CATALOGUE MERGING
"""

import OQCatk.Catalogue as Cat
import OQCatk.Selection as Sel
import OQCatk.MagRules as MR

#-----------------------------------------------------------------------------------------
# Import Catalogues

Db1 = Cat.Database()
Db1.Load('data/isc-rev-africa-select.bin')

Db2 = Cat.Database()
Db2.Load('data/isc-gem-v3.bin')

#-----------------------------------------------------------------------------------------
# Duplicate findings

# Between Catalogues
Db3, Log = Sel.MergeDuplicate(Db1,Db2,Twin=60.,Swin=50.,Log=1, Owrite=False)

# Within a catalogue
Log = Sel.MergeDuplicate(Db1,Twin=60.,Swin=50.,Log=1)

#-----------------------------------------------------------------------------------------
# Magnitude conversion

# Apply to all agency
Sel.MagConvert(Db1,'*',['Ms','MS'],'Mw',MR.MsMw_Scordillis2006)

# Apply to single agency
Sel.MagConvert(Db1,'ISC','Ms','Mw',MR.MsMw_Scordillis2006)
