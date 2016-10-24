"""
EXAMPLE 7 - Prime analysis
"""

import Parsers as Par
import Exploration as Exp
import MapTools as Map

Db = Par.Database('ISC-HOM')
Db.ImportIsf('data/isc-rev-africa.isf')

DbP, DbN = Exp.SplitPrime(Db)

xn = DbN.Extract('Location','Longitude')
yn = DbN.Extract('Location','Latitude')

xp = DbP.Extract('Location','Longitude')
yp = DbP.Extract('Location','Latitude')


# Plot map
cfg = {'Bounds': [10., -40., 60., 20.],
       'FigSize': [8., 6.],
       'Background': ['none',[0.9,0.8,0.6],[0.5,0.8,1.]],
       'Grid': [10., 10.]}

M = Map.GeoMap(cfg)

M.BasePlot()
M.DrawBounds()
M.DrawGrid()

M.PointPlot(xp, yp, Set=['o','b',5,1], Label='Primes')
M.PointPlot(xn, yn, Set=['o','r',5,1], Label='Not Primes')

M.Legend()
M.Title('Example 7')
M.Show()

M.SaveFig('pictures/example7.png')