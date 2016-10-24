"""
EXAMPLE 9 - Parseing GCMT bulletin (Ndk format)
"""

import Parsers as Par
import Exploration as Exp
import MapTools as Map

Db = Par.Database('GCMT')
Db.ImportNdk('data/jan76_dec13.ndk')

# Search Area (Africa)
p = [(-20.,30.),(60.,30.),(60.,60.),(-20.,60.)]

Db2 = Exp.AreaSelect(Db,p)

# Plot map
cfg = {'Bounds': [-20., 30., 60., 60.],
       'FigSize': [8., 6.],
       'Background': ['none',[0.9,0.8,0.6],[0.5,0.8,1.]],
       'Grid': [10., 10.]}

M = Map.GeoMap(cfg)

M.BasePlot()
M.DrawBounds()
M.DrawGrid()

MagTab = [[3,4,['d','w',2,1]],
          [4,5,['^','y',4,1]],
          [5,6,['o','g',6,1]],
          [6,7,['s','r',8,1]],
          [7,8,['p','m',10,1]]]

def RangeSelect(Db, Min,Max):

  DbC = Db.Copy()
  DbC.Filter('Magnitude','Size',Min,Is='>=')
  DbC.Filter('Magnitude','Size',Max,Is='<')
  x = DbC.Extract('Location','Longitude')
  y = DbC.Extract('Location','Latitude')
  return x, y

for mt in MagTab:

  x, y = RangeSelect(Db2, mt[0], mt[1])
  M.PointPlot(x, y, Set=mt[2])


M.Title('Example 9 - GCMT')
M.Show()

M.SaveFig('pictures/example9.png')