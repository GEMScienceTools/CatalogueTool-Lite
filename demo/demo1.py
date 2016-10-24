"""
EXAMPLE 1 - MANUAL BUILD OF A DATABASE
"""

import Catalogue as Cat

Db = Cat.Database('Test')

L = [{'Year': 1960},
     {'Year': 1961, 'Month': 12},
     {'Year': 1962, 'Month': 12, 'Day': 3}]
M = [{'Size':6, 'Error': 0.2},
     {'Size':7, 'Error': 0.2, 'Type':'ML'}]

Db.AddEvent('A')
Db.AddEvent('B', L)
Db.AddEvent('C', L, M)

Db.AddEvent('A', L, [], Append=True)
Db.AddEvent('B', Magnitude=M, Append=True)

Db.DelEvent('C')

Db.PrintEvent('B')

Db.SetKey('Location', 'Code', 'NEW')
Db.SetKey('Location', 'Prime', True, Match=['Code','NEW'])
