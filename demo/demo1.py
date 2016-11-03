"""
EXAMPLE 1 - MANUAL BUILD OF A DATABASE
"""

import Catalogue as Cat

Db = Cat.Database('First Test','Just a test')

L = [{'Year': 1960},
     {'Year': 1961, 'Month': 12},
     {'Year': 1962, 'Month': 12, 'Day': 3, 'Hour': 5, 'Minute': 20, 'Second': 10}]

M = [{'MagCode': 'AAA', 'MagSize':5, 'MagError': 0.1, 'MagType':'Mw'},
     {'MagCode': 'XXX', 'MagSize':7, 'MagError': 0.2, 'MagType':'ML'}]

Db.AddEvent('E1')
Db.AddEvent('E2', L)
Db.AddEvent('E3', L, M)

Db.AddEvent('E1', L, [], Append=True)
Db.AddEvent('E2', Magnitude=M, Append=True)

Db.DelEvent('E3')

Db.SetKey('LocCode', 'ZZZ')
Db.SetKey('Prime', True, Match=['LocCode','ZZZ'])

Db.PrintEvent('E2')
Db.Size()

I = Db.GetIndex('E2')

print Db.Header
print Db.Events[I]