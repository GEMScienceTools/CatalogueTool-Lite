def MergeDuplicate(DbA, DbB=[],
                        Twin=60.,
                        Swin=50.,
                        Unit='Second',
                        Owrite=True,
                        Log=False,
                        LogFile=[]):

  if Unit not in ['Second','Minute','Hour','Day','Month','Year']:
    print 'Warning: time unit not recognized'
    return

  # Converting current-units to seconds
  if Unit == 'Second':
    Twin *= 1
    Mask = (1,1,1,1,1,1)
  if Unit == 'Minute':
    Twin *= 60
    Mask = (1,1,1,1,1,0)
  if Unit == 'Hour':
    Twin *= 60*60
    Mask = (1,1,1,1,0,0)
  if Unit == 'Day':
    Twin *= 60*60*24
    Mask = (1,1,1,0,0,0)
  if Unit == 'Month':
    Twin *= 60*60*24*12
    Mask = (1,1,0,0,0,0)
  if Unit == 'Year':
    Twin *= 60*60*24*12*365
    Mask = (1,0,0,0,0,0)

  def GetDate(Event, Mask):

    L = Event['Location'][0]
    S = CU.DateToSec(L['Year'] or Mask[0],
                     L['Month'] or Mask[1],
                     L['Day'] or Mask[2],
                     L['Hour'] or Mask[3],
                     L['Minute'] or Mask[4],
                     L['Second'] or Mask[5])
    return S

  def GetCoor(Event):
    X = Event['Location'][0]['Longitude']
    Y = Event['Location'][0]['Latitude']
    return [X, Y]

  def DeltaSec(S0, S1):
    Sec = ma.fabs(S1-S0)
    return Sec

  def DeltaLen(C0, C1):
    Dis = CU.WgsDistance(C0[1],C0[0],C1[1],C1[0])
    return Dis

  #---------------------------------------------------------------------------------------

  Db0 = DbA.Copy()
  Db1 = DbB.Copy() if DbB else DbA.Copy()
  End = None if DbB else -1
  LogE = []
  Ind = []
  Name = Db1.Header['Name']

  for J, E0 in enumerate(Db0.Events[:End]):
    T0 = GetDate(E0, Mask)
    C0 = GetCoor(E0)

    Start = 0 if DbB else J+1

    for I, E1 in enumerate(Db1.Events[Start:]):
      C1 = GetCoor(E1)
      dC = DeltaLen(C0, C1)

      if (dC <= Swin):
        T1 = GetDate(E1, Mask)
        dT = DeltaSec(T0, T1)

        if (dT <= Twin):
          E0['Location'].extend(E1['Location'])
          E0['Magnitude'].extend(E1['Magnitude'])
          E0['Log'] += 'MERGED({0}:{1});'.format(Name,E1['Id'])
          LogE.append((J, E0['Id'], Start+I, E1['Id'], dT, dC))
          Ind.append(Start+I)

  if DbB:
    for I in range(0,Db1.Size()):
      if I not in Ind:
        Db0.Events.append(Db1.Events[I])
        Db0.Events[-1]['Log'] += 'ADDED({0});'.format(Name)

  else:
    for I in Ind:
      Db0.Events[I] = []
    Db0.Events = [e for e in Db0.Events if e]

  if Owrite:
    DbA.Events = Db0.Events
    if Log:
      return LogE

  else:
    if Log:
      return Db0, LogE
    else:
      return Db0

  if LogFile:
    # Open input ascii file
    with open(LogFile, 'w') as f:
      for L in LogE:
        f.write('{0},{1},'.format(L[0],L[1]))
        f.write('{0},{1},'.format(L[2],L[3]))
        f.write('{0},{1}\n'.format(L[4],L[5]))
      f.close()
      return
    # Warn user if model file does not exist
    print 'Cannot open file'