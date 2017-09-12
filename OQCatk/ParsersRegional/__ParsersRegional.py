#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 GEM Foundation
#
# The CATK (Lite) is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# CATK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Poggi Valerio, Garcia Julio

"""
Module for Specific Regional Catalogue Parsers
SSA/Africa Project
CCARA Project
"""
import datetime as dt
import OQCatk.Catalogue as Cat
import OQCatk.AsciiTools as AT
import OQCatk.CatUtils as CU
import OQCatk.MyTools as Mt



class Database(Cat.Database):
    """
    """
    def __init__(self, Name=[], Info=[]):
        super(Database, self).__init__(Name=Name, Info=Info)

    def ImportIgn(self, file_name):
        """
        TODO:description of the catalogue
        """

        def _GetId(EventStr):
            I = []
            if EventStr:
                I = EventStr[0:12].strip(' ')
            return I

        def _GetLocation(EventStr):
            L = {}
            if EventStr:
                L['Year'] = EventStr[23:27].strip(' ')
                L['Month'] = EventStr[20:22].strip(' ')
                L['Day'] = EventStr[17:19].strip(' ')
                L['Hour'] = EventStr[34:36].strip(' ')
                L['Minute'] = EventStr[37:39].strip(' ')
                L['Second'] = EventStr[40:42].strip(' ')
                L['Latitude'] = EventStr[42:57].strip(' ')
                L['Longitude'] = EventStr[57:72].strip(' ')
                L['Depth'] = EventStr[72:87].strip(' ')
                L['LocCode'] = 'IGN'
            return L

        def _GetMagnitude(EventStr):
            M = {}
            if EventStr:
                M['MagSize'] = EventStr[102:117].strip(' ')
                M['MagError'] = 0.
                M['MagCode'] = 'IGN'
                if EventStr[131] == '1':
                    M['MagType'] = 'MDs'
                if EventStr[131] == '2':
                    M['MagType'] = 'MbLg'
                if EventStr[131] == '3':
                    M['MagType'] = 'mb'
                if EventStr[131] == '4':
                    M['MagType'] = 'mbLg'
                if EventStr[131] == '5':
                    M['MagType'] = 'Mw'
                if EventStr[131] == '6':
                    M['MagType'] = 'MLv'
                if EventStr[131] == '7':
                    M['MagType'] = 'mb'
                if EventStr[131] == '8':
                    M['MagType'] = 'mB'
                if EventStr[131] == '9':
                    M['MagType'] = 'Mwp'
                if EventStr[131] == '10':
                    M['MagType'] = 'MwmB'
                if EventStr[131] == '11':
                    M['MagType'] = 'MwMwp'
            return M

        def _GetLog(EventStr):
            O = []
            if EventStr:
                O = 'INFO({0});'.format(EventStr[135:-1])
            return O

            # Open IGN file
            with open(file_name, 'r') as f:

                # Read header
                Header = f.readline().strip('\n')

                while True:

                    EventStr = f.readline().strip('\n')

                    I = _GetId(EventStr)
                    L = _GetLocation(EventStr)
                    M = _GetMagnitude(EventStr)
                    O = _GetLog(EventStr)

                    if I:
                        self.AddEvent(I, L, M, O)
                    else:
                        break

            f.close()
        return

        # Warn user if model file does not exist
        print 'File not found.'

    def ImportSeisan(self, file_name):
        """
        """
        def add_nulls(num, cnt=2):

            cnt = cnt - len(str(num))
            nulls = '0' * cnt

            return '%s%s' % (nulls, num)

        def _DoId(I, cnt=7):

            Id = []
            if I:
                Id = 'CUB' + add_nulls(I, cnt)
            return Id

        def _GetLocation(EventStr,D):
            L = {}
            if EventStr:
                L['Year'] = EventStr[1:5].strip(' ')
                if int(L['Year']) < 1400 or int(L['Year']) > 2016:
                    print D, L['Year']
                L['Month'] = EventStr[6:8].strip(' ')
                if (int(L['Month']) < 0 or int(L['Month']) > 12):
                    print "ID = %s, Month = %s"% (D, L['Month'])
                if (int(L['Month']) == 0 or L['Month']==None):
                    L['Month'] = '1'

                L['Day'] = EventStr[8:10].strip(' ')
                if (int(L['Day']) < 0 or int(L['Day']) > 31):
                    print "ID = %s, Day = %s"%(D, L['Day'])                              
                if (int(L['Day']) == 0 or L['Day']==None):
                    L['Day'] = '1'
 
                L['Hour'] = EventStr[11:13].strip(' ')
                if (int(L['Hour']) < 1):
                    if (int(L['Hour']) > 24):
                        print "ID = %s, 'Hour' = %s"%(D, L['Hour'])              
                if (int(L['Hour']) == None):
                    L['Hour'] = '0'

                L['Minute'] = EventStr[13:15].strip(' ')
                if (int(L['Minute']) < 0 or int(L['Minute']) > 60):
                    print "ID = %s, 'Minute' = %s"%(D, L['Minute'])              
                if (int(L['Minute']) == 0 or L['Minute']==None):
                    L['Minute'] = '0'
                elif (int(L['Minute']) >= 60):
                    L['Minute'] = '59.9'

                L['Second'] = EventStr[16:20].strip(' ')
                if (float(L['Second']) >= 60.):
                    L['Second'] = '59.9'
                if (L['Second'] == None):
                    L['Second'] = '0.0'
                if (float(L['Second']) < 0. or float(L['Second']) > 60.):
                    print "ID = %s, Second = %s"% (D, L['Second'])
                L['SecError'] = EventStr[51:55].strip(' ')
                L['Latitude'] = EventStr[23:30].strip(' ')
                L['Longitude'] = EventStr[30:38].strip(' ')
                L['Depth'] = EventStr[38:43].strip(' ')
                if L['Depth'] == None:
                    L['Depth'] = '0'
                L['LocCode'] = EventStr[45:48].strip(' ')
                L['LocId'] = D
                L['LocPrime'] = False
            return L

        def _GetMagnitude(EventStr, MagN,D):
            if MagN == 1:
                dI = 0
            if MagN == 2:
                dI = 8
            if MagN == 3:
                dI = 16
            M = {}
            if EventStr:
                M['MagSize'] = EventStr[55+dI:59+dI].strip(' ')
                M['MagType'] = EventStr[59+dI].strip(' ')
                M['MagCode'] = EventStr[60+dI:63+dI].strip(' ')
                if M['MagType'] == 'L':
                    M['MagType'] = 'ML'
                if M['MagType'] == 'b':
                    M['MagType'] = 'mb'
                if M['MagType'] == 'B':
                    M['MagType'] = 'mB'
                if M['MagType'] == 's':
                    M['MagType'] = 'Ms'
                if M['MagType'] == 'S':
                    M['MagType'] = 'MS'
                if M['MagType'] == 'W':
                    M['MagType'] = 'MW'
                if M['MagType'] == 'G':
                    M['MagType'] = 'MbLg'
                if M['MagType'] == 'C':
                    M['MagType'] = 'Mc'
                if M['MagType'] == 'D':
                    M['MagType'] = 'Md'

                M['MagId'] = D
                M['MagPrime'] = False

            return M

        def _GetMagBlock(EventStr,D):
            M = []
            for N in [1, 2, 3]:
                M0 = _GetMagnitude(EventStr, N,D)
                if M0['MagSize']:
                    M.append(M0)
            return M

        def _GetLog(EventStr):
            O = ''
            if EventStr:
                S = EventStr[10].strip(' ')
                if S:
                    O += 'FIXT({0});'.format(S)
                S = EventStr[20].strip(' ')
                if S:
                    O += 'LMI({0});'.format(S)
                S = EventStr[43].strip(' ')
                if S:
                    O += 'DIND({0});'.format(S)
                S = EventStr[45:48].strip(' ')
                if S:
                    O += 'HYPA({0});'.format(S)
                S = EventStr[48:51].strip(' ')
                if S:
                    O += 'STAN({0});'.format(S)
            return O

        # Open SEISAN file
        with open(file_name, 'r') as f:
            I = 0
            while True:
                EventStr = f.readline().strip('\n')

                if not EventStr:
                    break
                if EventStr[79] == '1':
                    I += 1
                    D = _DoId(I)
                    L = _GetLocation(EventStr,D)
                    M = _GetMagBlock(EventStr,D)
                    O = _GetLog(EventStr)

                    self.AddEvent(D, L, M, O)

            f.close()

        return
        # Warn user if model file does not exist
        print 'File not found.'

    def ImportSSNM(self, file_name):
        """
        TODO:description of the catalogue
        """

        # Defining the headers/estruture
        #Header = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second',
        #          'Latitude', 'Longitude', 'Depth', 'MagSize']

        Header = ['YYYY', 'MM', 'DD', 'HH', 'MI', 'SS',
                  'LATITUDE', 'LONGITUDE', 'DEPTH', 'MAGNITUDE']

        def add_nulls(num, cnt=2):

            cnt = cnt - len(str(num))
            nulls = '0' * cnt

            return '%s%s' % (nulls, num)

        def _DoId(I, cnt=7):
            Id = []
            # print'{0:06d}'.format(I)
            if I:
                Id = 'SSNM' + add_nulls(I, cnt)
            return Id

        def _Local2Utc(Year, Month, Day, Hour, Minute, Second):
            """
            to convert from local [Mexico city time] to UTC time
            See [TODO] for more information
            """
            ldate = []
            ldate =[Year, Month, Day, Hour, Minute, Second]
            ddate = []
            # creating the datatime object
            year = int(Year)
            month = int(Month)
            day = int(Day)
            hour = int(Hour)
            minute = int(Minute)
            second = int(float(Second))

            local_time = dt.datetime(year, month, day, hour, minute, second)

            if(month >= 4 and month <= 10):
                DD = dt.timedelta(hours=5)
                # print "Month = ", month
                # print "Day = ", day
            else:
                DD = dt.timedelta(hours=6)
                # print "Month = ", month
                # print "Day = ", day

            utc_time = local_time + DD

            yyyy = utc_time.year
            mm = utc_time.month
            dd = utc_time.day
            hh = utc_time.hour
            mi = utc_time.minute
            sec = utc_time.second

            ddate = [yyyy, mm, dd, hh, mi, sec]

            # print "ldate = ", ldate
            # print "ddate = ", ddate


            return ddate

        def _GetLocation(ddate, lat, lon, depth,X):
            """
            """
            L = {}
            if ddate:
                L['Year'] = ddate[0]
                L['Month'] = ddate[1]
                L['Day'] = ddate[2]
                L['Hour'] = ddate[3]
                L['Minute'] = ddate[4]
                L['Second'] = ddate[5]
            if lat:
                L['Latitude'] = float(lat.strip(' '))
            if lon:
                L['Longitude'] = float(lon.strip(' '))
            if depth:
                L['Depth'] = float(depth.strip(' '))
            L['LocCode'] = "SSNM"
            L['LocId'] = X
            L['LocPrime'] = False
            return L

        def _GetMagnitude(mag_str,X):
            """
            """
            M = {}
            if mag_str:
                M['MagType'] = "M"
                M['MagSize'] = float(mag_str)
                M['MagCode'] = "SSNM"
                M['MagId'] = X
                M['MagPrime'] = False
            return M


        # Open/importing SSNM csv file
        tab = AT.AsciiTable()
        tab.Import(file_name, header=Header, delimiter=',', skipline=1,
                   comment='#', dtype='s')

        for I, D in enumerate(tab.data):
            if 'eventid' in D.keys():
                X = D['eventid']
            else:
                I += 1
                X = _DoId(I)

                # Changing the time from Local to UTC
                ddate = _Local2Utc(D['YYYY'], D['MM'], D['DD'], D['HH'], D['MI'], D['SS'])

            L = _GetLocation(ddate, D['LATITUDE'], D['LONGITUDE'], D['DEPTH'], X)

            M = _GetMagnitude(D['MAGNITUDE'], X)

            for K in tab.header:
                if K in L:
                    L[K] = D[K]
                if K in M:
                    M[K] = D[K]
                if 'Log' in D.keys():
                    O = D['Log']
                else:
                    O = ''
            if X:
                self.AddEvent(X, L, M, O)
        return

    def ImportRESNOM(self, file_name):
        """
        TODO:description of the catalogue
        """

        def add_nulls(num, cnt=2):

            cnt = cnt - len(str(num))
            nulls = '0' * cnt

            return '%s%s' % (nulls, num)

        def _DoId(I, cnt=7):
            Id = []
            if I:
                Id = 'RESNOM' + add_nulls(I, cnt)
            return Id

        def _GetLocation(EventStr, X):
            L = {}
            if EventStr:
                L['Year'] = EventStr[0:4].strip(' ')
                L['Month'] = EventStr[5:7].strip(' ')
                L['Day'] = EventStr[8:10].strip(' ')
                L['Hour'] = EventStr[11:13].strip(' ')
                L['Minute'] = EventStr[14:16].strip(' ')
                L['Second'] = EventStr[17:19].strip(' ')
                L['Latitude'] = EventStr[20:26].strip(' ')
                L['Longitude'] = EventStr[27:36].strip(' ')
                L['Depth'] = EventStr[38:42].strip(' ')
                L['LocCode'] = 'RESNOM'
                L['LocId'] = X
                L['LocPrime'] = False

            return L

        def _GetMagBlock(EventStr, X):
            M = []
            for N in [1, 2, 3]:
                M0 = _GetMagnitude(EventStr, N, X)
                if M0['MagSize']:
                    M.append(M0)
            return M

        def _GetMagnitude(EventStr, N,X):
            M = {}
            if EventStr:
                if N == 1:
                    M['MagSize'] = EventStr[92:98].strip(' ')
                    if M['MagSize'] == '0.0':
                       M['MagSize'] = ''
                       pass
                    else:
                       M['MagType'] = 'ML'
                       M['MagCode'] = 'RESNOM'
                       M['MagId'] = X
                       M['MagPrime'] = False
                    
                if N == 2:                
                    M['MagSize'] = EventStr[99:105].strip(' ')
                    if M['MagSize'] == '0.0':
                       M['MagSize'] = ''
                       pass
                    else:                
                       M['MagType'] = 'MC'
                       M['MagCode'] = 'RESNOM'
                       M['MagId'] = X
                       M['MagPrime'] = False

                if N == 3:
                    M['MagSize'] = EventStr[106:112].strip(' ')
                    M['MagType'] = 'M'
                    M['MagCode'] = 'RESNOM'
                    M['MagId'] = X
                    M['MagPrime'] = False
            return M

        def _GetLog(EventStr):
            O = ''
            if EventStr:
                S = EventStr[43:49].strip(' ')
                if S:
                    O += 'STAN({0});'.format(S)
                S = EventStr[50:56].strip(' ')
                if S:
                    O += 'DMIN({0});'.format(S)
                S = EventStr[57:63].strip(' ')
                if S:
                    O += 'RMS({0});'.format(S)
                S = EventStr[64:70].strip(' ')
                if S:
                    O += 'GAP({0});'.format(S)
                S = EventStr[71:77].strip(' ')
                if S:
                    O += 'ERH({0});'.format(S)
                S = EventStr[78:84].strip(' ')
                if S:
                    O += 'ERZ({0});'.format(S)
                S = EventStr[85:91].strip(' ')
                if S:
                    O += 'ERX({0});'.format(S)

            return O

        # Open RESNOM file
        with open(file_name, 'r') as f:
            # Read header
            Header = f.readline().strip('\n')

            I = 0
            while True:
                EventStr = f.readline().strip('\n')

                if not EventStr:
                    print "terminamos..."
                    break
                else:
                    I += 1
                    X = _DoId(I)
                    L = _GetLocation(EventStr,X)
                    M = _GetMagBlock(EventStr,X)
                    O = _GetLog(EventStr)

                    self.AddEvent(X, L, M, O)

            f.close()
            return
        # Warn user if model file does not exist
        print 'File not found.'

    def ImportPRSN04(self, file_name):
        """
        TODO:description of the catalogue
        """

        def add_nulls(num, cnt=2):

            cnt = cnt - len(str(num))
            nulls = '0' * cnt

            return '%s%s' % (nulls, num)

        def _DoId(I, cnt=7):

            Id = []
            # print'{0:06d}'.format(I)
            if I:
                Id = 'PRSN' + add_nulls(I, cnt)
            return Id

        def _GetLocation(EventStr,D):
            L = {}
            if EventStr:
                L['Year'] = EventStr[0:4].strip(' ')
                L['Month'] = EventStr[5:7].strip(' ')
                L['Day'] = EventStr[8:10].strip(' ')
                L['Hour'] = EventStr[11:13].strip(' ')
                L['Minute'] = EventStr[14:16].strip(' ')
                L['Second'] = EventStr[17:22].strip(' ')
                L['Latitude'] = EventStr[24:31].strip(' ')
                L['Longitude'] = EventStr[32:40].strip(' ')
                L['Depth'] = EventStr[41:47].strip(' ')
                L['LocCode'] = EventStr[57:62].strip(' ')
                L['IdLoc'] = D

            return L

        def _GetMagnitude(EventStr,D):
            M = {}
            if EventStr:
                M['MagSize'] = EventStr[48:52].strip(' ')
                M['MagType'] = EventStr[52:56].strip(' ')
                M['MagCode'] = 'PSRN'
                M['IdMag'] = D

            return M

        def _GetLog(EventStr):
            O = ''
            if EventStr:
                S = EventStr[102:105].strip(' ')
                if S:
                    O += 'STAN({0});'.format(S)
                S = EventStr[92:94].strip(' ')
                if S:
                    O += 'QLT({0});'.format(S)
                S = EventStr[64:69].strip(' ')
                if S:
                    O += 'RMS({0});'.format(S)
                S = EventStr[85:89].strip(' ')
                if S:
                    O += 'GAP({0});'.format(S)
                S = EventStr[71:77].strip(' ')
                if S:
                    O += 'ERH({0});'.format(S)
                S = EventStr[78:84].strip(' ')
                if S:
                    O += 'ERZ({0});'.format(S)
                S = EventStr[95:99].strip(' ')
                if S:
                    O += 'INT({0});'.format(S)

            return O

        # Open PRSN file [after 2004 web format]
        with open(file_name, 'r') as f:

            # Read header
            Header = f.readline().strip('\n')

            I = 0

            while True:
                EventStr = f.readline().strip('\n')
                if not EventStr:
                    break
                else:
                    I += 1
                    D = _DoId(I)
                    L = _GetLocation(EventStr,D)
                    M = _GetMagnitude(EventStr,D)
                    O = _GetLog(EventStr)

                    self.AddEvent(D, L, M, O)

            f.close()
            return

        # Warn user if model file does not exist
        print 'File not found.'

    def ImportPRSN(self, file_name):
        """
        to import the PRSN catalogue, data came from:
        http://www.prsn.uprm.edu/Spanish/catalogue/index.php
        Last access : 18/04/2017
        """
        # Defining the headers/structure
        Header = ['UTC Time', 'Lat', 'Long', 'Depth', 'Mag', 'Network', 'RMS',
                  'ERH', 'ERZ', 'GAP', 'Q', 'Int', 'nStat']

        def add_nulls(num, cnt=2):

            cnt = cnt - len(str(num))
            nulls = '0' * cnt

            return '%s%s' % (nulls, num)

        def _DoId(I, cnt=7):

            Id = []
            # print'{0:06d}'.format(I)
            if I:
                Id = 'PRSN' + add_nulls(I, cnt)
            return Id

        def _SplitDate(date):
            Date = ''
            Time = ''
            string = []
            if date:
                string = date.split(' ')
                Date = string[0].strip(' ')
                Time = string[1].strip(' ')
            return Date, Time

        def _SplitMag(mag_str):
            Mag = ''
            MagType = ''
            string = []
            if mag_str:
                string = mag_str.split(' ')
                Mag = string[0].strip(' ')
                MagType = string[1].strip(' ')
            return Mag, MagType

        def _GetLocation(date, lat, lon, depth, network,X):
            """
            """
            Date = ''
            Time = ''
            strD = []
            strT = []
            L = {}
            Date, Time = _SplitDate(date)

            L['LocCode'] = network.strip(' ')

            # Splitting the Date
            if Date:
                strD = Date.split('-')
                L['Year'] = strD[0].strip(' ')
                L['Month'] = strD[1].strip(' ')
                L['Day'] = strD[2].strip(' ')

            # Splitting the Time
            if Time:
                strT = Time.split(':')
                L['Hour'] = strT[0].strip(' ')
                L['Minute'] = strT[1].strip(' ')
                L['Second'] = strT[2].strip(' ')

            # Get location
            if lat:
                L['Latitude'] = float(lat.strip(' '))
            if lon:
                L['Longitude'] = float(lon.strip(' '))
            if depth:
                L['Depth'] = float(depth.strip(' '))
            # IdLoc
            L['LocId'] = X
            L['LocPrime'] = False

            return L

        def _GetMagnitude(mag_str, network,X):
            """
            """
            M = {}
            Mag, MagType = _SplitMag(mag_str)
            if Mag:
                M['MagType'] = MagType
                M['MagSize'] = float(Mag)
                M['MagCode'] = network.strip(' ')
                M['MagId'] = X
                M['MagPrime'] = False


            return M

        def _GetLog(RMS, ERH, ERZ, GAP, Q, I, nStat):
            O = ''
            if RMS:
                S = RMS.strip(' ')
                if S:
                    O += 'RMS({0});'.format(S)
                S = ERH.strip(' ')
                if S:
                    O += 'ERH({0});'.format(S)
                S = ERZ.strip(' ')
                if S:
                    O += 'ERZ({0});'.format(S)
                S = GAP.strip(' ')
                if S:
                    O += 'GAP({0});'.format(S)
                S = GAP.strip(' ')
                if S:
                    O += 'GAP({0});'.format(S)
                S = Q.strip(' ')
                if S:
                    O += 'Q({0});'.format(S)
                S = I.strip(' ')
                if S:
                    O += 'INT({0});'.format(S)
                S = nStat.strip(' ')
                if S:
                    O += 'NSTA({0});'.format(S)
            return O

        # Open/importing PRSN txt[tab] file
        tab = AT.AsciiTable()
        tab.Import(file_name, header=Header, delimiter='\t', skipline=1,
                   comment='#', dtype='s')

        for I, D in enumerate(tab.data):
            if 'eventid' in D.keys():
                I = D['eventid']
            else:
                I += 1
                X = _DoId(I)


            L = _GetLocation(D['UTC Time'], D['Lat'], D['Long'], D['Depth'],
                             D['Network'],X)
            M = _GetMagnitude(D['Mag'], D['Network'],X)

            O = _GetLog(D['RMS'], D['ERH'], D['ERZ'], D['GAP'], D['Q'],
                        D['Int'], D['nStat'])

            for K in tab.header:
                if K in L:
                    L[K] = D[K]
                if K in M:
                    M[K] = D[K]
                # if K in O:
                #    O[K] = D[K]
            self.AddEvent(X, L, M, O)
        return

    def ImportResis2(self, file_name):
        # Defining the headers/estruture
        Header = ['ID', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND',
                    'LATITUDE', 'LONGITUDE', 'DEPTH', 'AGENCY',
                    'MAG1', 'TYPE_MAG1', 'MAG2', 'TYPE_MAG2','MAG3', 'TYPE_MAG3']


        def add_nulls(num, cnt=2):

                cnt = cnt - len(str(num))
                nulls = '0' * cnt

                return '%s%s' % (nulls, num)

        def _DoId(I, cnt=6):
                Id = []
                # print'{0:06d}'.format(I)
                if I:
                    Id = 'RES2' + add_nulls(I, cnt)
                return Id


        def _GetLocation(year, month, day, hour, minute, second, lat, lon, depth, agency,ID):
            """
            """

            L = {}

            # getting Date-Time
            if year:
                L['Year'] = year
            if month:
                L['Month'] = month
            if (int(L['Month']) == 0 or L['Month']==None):
                L['Month'] = '1'
            if (int(L['Month']) < 0 or int(L['Month']) > 12):
                print "ID = %s, Month = %s"% (D, L['Month'])
 
            if day:
                L['Day'] = day
            if (int(L['Day']) == 0 or L['Day']==None):
                L['Day'] = '1'
            if (int(L['Day']) < 0 or int(L['Day']) > 31):
                print "ID = %s, Day = %s"%(D, L['Day'])                              
             
            if hour:
                L['Hour'] = hour
            if (L['Hour']==None):
                L['Hour'] = '0'
            if (int(L['Hour']) < 0 or int(L['Hour']) > 24):
                print "ID = %s, Hour = %s"%(D, L['Hour'])                              

            if minute:
                L['Minute'] = minute
            if (L['Minute']==None):
                L['Minute'] = '0'
            if (int(L['Minute']) < 0 or int(L['Minute']) > 60):
                print "ID = %s, Minute = %s"%(D, L['Minute'])                              

            if second:
                L['Second'] = second
            if (float(L['Second']) >= 60.):
                L['Second'] = '59.9'
            if (float(L['Second']) ==  None):
                L['Second'] = '0.0'
            if (float(L['Second']) < 0. or float(L['Second']) > 60.):
                print "ID = %s, Second = %s"% (D, L['Second'])
 
            # get location
            if lat:
                L['Latitude'] = lat
            if lon:
                L['Longitude'] = lon
            if depth:
                L['Depth'] = depth
            if L['Depth'] == None:
                L['Depth'] = '0'
            if agency:
                L['LocCode'] = agency

            L['LocId'] = ID
            L['LocPrime'] = False


            return L

        def _GetMagnitude(m1, m1_tp, m2, m2_tp, m3, m3_tp,ID):

            M1 = {}
            M2 = {}
            M3 = {}
            MM = []

            if m1:
                M1['MagSize'] = float(m1.strip(' '))
                M1['MagType'] = m1_tp[:1]
                M1['MagCode'] = m1_tp[1:]
                M1['MagId'] = ID
                M1['MagPrime'] = False
                MM.append(M1)
                #print "MM en 1= ", MM
            if m2:
                M2['MagSize'] = float(m2.strip(' '))
                M2['MagType'] = m2_tp[:1]
                M2['MagCode'] = m2_tp[1:]
                M2['MagId'] = ID
                M2['MagPrime'] = False
                MM.append(M2)
                #print "MM en 2= ", MM

            if m3:
                M3['MagSize'] = float(m3.strip(' '))
                M3['MagCode'] = m3_tp[1:]
                M3['MagId'] = ID
                M3['MagPrime'] = False
                if (m3_tp.strip(' ')=="1"):
                    M3['MagType'] = "Mww"
                if (m3_tp.strip(' ')=="WCCMT1"):
                    M3['MagType'] = "Mwc"
                if (m3_tp.strip(' ')=="WGFZ1"):
                    M3['MagType'] = "Mwc"
                if (m3_tp.strip(' ')=="WGUA1"):
                    M3['MagType'] = "Mw" + m1_tp[:1]
                # ONE single case!
                if (m3_tp.strip(' ')=="WCAL1"):
                    M3['MagType'] = "Mw" + m2_tp[:1]

                if (m3_tp.strip(' ')=="WHRV1"):
                    M3['MagType'] = "Mw" + m1_tp[:1]
                # GUA used Rojas et al. 1993 conversions
                # mc = ml, Ms = 1.783 ml - 4.165
                # Ms = 2.08 mb - 5.74
                # Mw = 0.655 Ms + 2.251
                # If  "WCMT1" seems no satisfied any previous rules!
                if (m3_tp.strip(' ') == "WCMT1"):
                    M3['MagType'] = m3_tp.strip(' ')
                # The rules are not satisfied but is the unique possible case!
                if (m3_tp.strip(' ') == "WGUA1") and m1_tp[:1] == "C":
                    M3['MagType'] = "Mw" + m1_tp[:1]
                if (m3_tp.strip(' ') == "WGUA1") and m1_tp[:1] == "L":
                    M3['MagType'] = "Mw" + m1_tp[:1]

                # NIC used a two step conversion
                # ml = mc, mc, mb -> Ms, Ms -> Mw
                # Ms = (0.8ml - 0.01 mlˆˆ2 - 0.1)/0.63
                # Ms = 1.74 mb - 3.95
                # IF Ms > 6.6, then Ms == Mw
                # Otherwise Mw = (2/3)Ms + 2.43
                if (m3_tp.strip(' ')=="WNIC1") and m1_tp[:1] == 'B':
                    M3['MagType'] = "MwBS"
                if (m3_tp.strip(' ')=="WNIC1") and m1_tp[:1] == 'L' or m2_tp[:1] == 'L':
                    M3['MagType'] = "MwLS"
                # SAL (EL Salvador?) used  the following rules
                # If mw exits Mw = mw
                # Mw = 0.82 ml + 0.8975
                # Mw = 0.8162 mb + 1.2291
                # Mw = 0.7571 mc + 1.5408
                # Mw = 0.66 Ms + 2.25
                if (m3_tp.strip(' ') == "WHRV1") and m1_tp[:1] == "C":
                    M3['MagType'] = "MwHRV1"
                if (m3_tp.strip(' ') == "WSAL1") and m1_tp[:1] == "L":
                    M3['MagType'] = "MwL"
                if (m3_tp.strip(' ') == "WSAL1") and m1_tp[:1] == "C":
                    M3['MagType'] = "MwC"

                # RSN - Costa Rica used Rojas et al. 1993 conversions
                if (m3_tp.strip(' ') == "WRSN1" and m2_tp[:1] == ""):
                    M3['MagType'] = "Mw" + m1_tp[:1]
                if (m3_tp.strip(' ') == "WRSN1" and m2_tp[:1] != " "):
                    M3['MagType'] = "Mw" + m3_tp[:1]

                # PDE [Ask for rules, tentatively I take the mag_code from the type_mag1 or 2]
                if (m3_tp.strip(' ') == "WPDE1"):
                    if(m1_tp[1:] == "PDE"):
                      M3['MagType'] = "Mw" + m1_tp[:1]
                    else:
                      M3['MagType'] = "Mw" + m2_tp[:1]
                # For the surrogated magnitudes
                if (m3_tp.strip(' ') == "WXXX1"):
                    M3['MagType'] = "MwX"

                MM.append(M3)
                #print "MM en 3= ", MM
            return MM



        # Open/importing resis2 csv file
        tab = AT.AsciiTable()
        tab.Import(file_name, header=Header,
                         delimiter=',',
                         skipline=1,
                         comment='#',
                         dtype='s')
        for I, D in enumerate(tab.data):

            ID = _DoId(D['ID'])
            # print ID

            L = _GetLocation(D['YEAR'],D['MONTH'],D['DAY'],D['HOUR'], D['MINUTE'], D['SECOND'],
                                 D['LATITUDE'],D['LONGITUDE'],D['DEPTH'],D['AGENCY'],ID)
            M = _GetMagnitude(D['MAG1'],D['TYPE_MAG1'],D['MAG2'],D['TYPE_MAG2'],D['MAG3'],D['TYPE_MAG3'],ID)

            for K in tab.header:
                if K in L:
                   L[K] = D[K]
                if K in M:
                   M[K] = D[K]
                if 'Log' in D.keys():
                   O = D['Log']
                else:
                   O = ''
            self.AddEvent(ID, L, M, O)
        return

    def ImportINET(self, file_name):
        """
        INETER Catalogue [version 2016]
        read(1,100) scat,asol,tsol,iyr,mon,iday,ihr,minu,sec,glat,glon,dep,nreg,ntel,
        (xmag(k),msc(k),mdo(k),k=1,8),
        (xmag(k),msc(k),mdo(k),k=9,12)
        format(a6,a1,a5,i4,2i3,1x,2i3,f6.2,1x,2f8.3,f6.1,2i4,8(f4.1,1x,a2,1x,a5),4(f5.1,1x,a2,1x,a5))
        Description:
        scat - source catalog --> (a6) --> x(1:6)
        asol - open azimuth of teleseismic stations (delta > 28 deg) --> (a1) --> x(7:7)
        tsol - solution type --> (a5) --> x(8:12)
        ciyr - year --> (i4) --> x(14:17)
        cmon - month --> (i3) --> x(16:20)
        ciday - day --> (i3) --> x(21:23)
        aqui va un espacio en blanco --> x(24:24)=' '
        cihr - origin hour --> (i3) --> x(25:27)
        cminu - origin minute --> (i3) --> x(28:30)
        csec - origin second --> (6.2) --> x(31:36)
        epq - authority/quality indicator (&, *, % or ?) (EHDF) (a1) --> x(37:37)
        cglat - geographic latitude --> (f8.3) --> x(39:46)
        cglon - geographic longitude --> (f8.3) --> x(47:54)
        cdep - focal depth --> (f6.1) --> x(55:60)
        cnreg - Flinn-Engdahl geographic region number --> (i4) --> x(61:64)
        cntel -  number of teleseismic observations (delta>28 deg) used in
        Magnitudes (up to 12) - first listed is magnitude used for event selection
        cada bloque esta compuesto por:
        primeras 8 (son 104 espacios, llega al 172)
        cxmag - magnitude --> (f4.1)
        aquí va un espacio en blanco
        msc - scale - (a2)
        aquí va un espacio en blanco
        mdo - source - (a5)
        ------------------------------------------
         i   tipo de magnitud  cxmag(i)    bl        msc(i)     bl         mdo(i)
         1 - mb                x(69:72)   x(73:73)   x(74:75)   x(76:76)   x(77:81)
         2 - Ms                x(82:85)   x(86:86)   x(87:88)   x(89:89)   x(90:94)
         3 - Mw                x(95:98)   x(99:99)   x(100:101) x(102:102) x(103:107)
         4 - MD o Mt o reserva x(108:111) x(112:112) x(113:114) x(115:115) x(116:120)
         5 - ML o KR           x(121:124) x(125:125) x(126:127) x(128:128) x(129:133)
         6 - M (~ MS)-reserva  x(134:137) x(138:138) x(139:140) x(141:141) x(142:146)
         7 - RG o LG o ME o MG x(147:150) x(151:151) x(152:153) x(154:154) x(155:159)
             o reserva
         8 - MC o reserva      x(160:163) x(164:164) x(165:166) x(167:167) x(168:172)
         ultimas 4 (son 56 espacios, llega al 228)
         cxmag1 - magnitude --> (f5.2)  numeración a partir de j=1
         aquí va un espacio en blanco
         msc - scale - (a2) continua numeración del otro bloque
         aquí va un espacio en blanco
         mdo - source - (a5) continúa numeración del otro bloque
         ------------------------------------------
         j   tipo de magnitud    cxmag1(j)    bl        i    msc(i)     bl         mdo(i)
         1 - Gutenberg-Richter  x(173:177) x(178:178)   9  x(179:180) x(181:181) x(182:186)
             o reserva
         2 - MI                 x(187:191) x(192:192)  10  x(193:194) x(195:195) x(196:200)
         3 - MKr o MKd          x(201:205) x(206:206)  11  x(207:208) x(209:209) x(210:214)
         4 - MwPS               x(215:219) x(220:220)  12  x(221:222) x(223:223) x(224:228)
         Esta última se usa para magnitudes finales Mw, reales o convertidas, con fines de PS
         ---------------------------------------------------------
        De ahora en adelante son nuestros añadidos al formato "centennial"
          dimension smac(3)
          character*3 amac
          character*1 smac
          character*4 cint
          read(1,101) amac,(sma(i),i=1,2),cint,rmst,rmsp,rmsn,rmse,rmsd,iorden,id1,id2
        format(226x.....,1x,a3,2a1,a4,1x,5f5.2,1x,i8,2i16)
         amac - (a3) --> x(230:232)
         MAC = tiempo de origen e hipocentro determinados por datos macrosísmicos
         MSC = tiempo de origen instrumental pero hipocentro macrosísmico
         smac(2) - (2a1) --> x(233:233),x(234:234) (ver abajo)
        II) opciones de error
         crmst - (f6.2) error medio cuadrático en tiempo de origen --> x(243:248)
         crmsp - (f6.2) error medio cuadrático en profundidad      --> x(249:254)
         crmsn - (f6.2) error medio cuadrático en epicentro (N-S)  --> x(255:260)
         crmse - (f6.2) error medio cuadrático en epicentro (E-W)  --> x(261:264)
         crmsd - (f6.2) error medio cuadrático en epicentro (total)--> x(267:272)
        III) opciones de indicadores
         ciorden - (i8) número de orden del terremoto en este catálogo --> x(274:281)
         cid1 (a16) - indicador del evento --> x(282:297)
         cid2 (a16) - identificador del evento en la fuente original --> x(298:313)
        IV) Otra información  otra(a12) --> x(314:325)
        """

        def _GetId(EventStr):
            Id = []
            if EventStr:
                Id = EventStr[298:313].strip(' ')
            return Id

        def _GetLocation(EventStr,D):
            L = {}
            if EventStr:
                L['Year'] = int(EventStr[13:17].strip(' '))
                L['Month'] = int(EventStr[18:20].strip(' '))
                L['Day'] = int(EventStr[21:23].strip(' '))
                L['Hour'] = int(EventStr[25:27].strip(' '))
                L['Minute'] = int(EventStr[28:30].strip(' '))
                L['Second'] = EventStr[31:36].strip(' ')
                L['Latitude'] = EventStr[39:46].strip(' ')
                L['Longitude'] = EventStr[47:54].strip(' ')
                L['Depth'] = EventStr[55:60].strip(' ')
                L['LocCode'] = EventStr[0:6].strip(' ')
                L['LocId'] = D
                L['LocPrime'] = False

            return L

        def _GetMagnitude(EventStr,D):             

            M1 = {}
            M2 = {}
            M3 = {}
            M = []

            N = 12  # Number of Magnitude types
            dI = 13
            for i in range (0, N):
                if i==0:
                    m = EventStr[68:73].strip(' ')
                    if len(m)> 1:
                        M1['MagSize'] = m
                        M1['MagType'] = EventStr[73:76].strip(' ')
                        M1['MagCode'] = EventStr[76:82].strip(' ')
                        M1['MagId'] = D
                        M1['MagPrime'] = False
                        M.append(M1)
                        print M1
                        #print "MM en 0 = ", MM
                elif i > 0 and i < 8:
                        print "i = ",i
                        m2 = EventStr[68+dI*i:73+dI*i].strip(' ')
                        if len(m2)> 1:
                            M2['MagSize'] = m2
                            M2['MagType'] = EventStr[73+dI*i:76+dI*i].strip(' ')
                            M2['MagCode'] = EventStr[76+dI*i:82+dI*i].strip(' ')
                            M2['MagId'] = D
                            M2['MagPrime'] = False
                            M.append(M2)
                            print M2
                            #print "MM = ", MM
                else:
                        # x(173:177) x(178:178)   9  x(179:180) x(181:181) x(182:186)
                        dK =14
                        k = i-8
                        print "i = %s, k = %s"%(i,k)
                        m3 = EventStr[173+dK*k:177+dK*k].strip(' ')
                        if len(m3)> 1:
                                M3['MagSize'] = m
                                M3['MagType'] = EventStr[178+dK*k:180+dK*k].strip(' ')
                                M3['MagCode'] = EventStr[181+dK*k:186+dK*k].strip(' ')
                                M3['MagId'] = D
                                M3['MagPrime'] = False
                                M.append(M3)
                                print "M = ", M3
                                #print "MM = ", MM
            print "en el metodo", M                        
            return M



        def _GetLog(EventStr):
            O = 'prova'
            """
            if EventStr:
                S = EventStr[102:105].strip(' ')
                if S:
                    O += 'STAN({0});'.format(S)
                S = EventStr[92:94].strip(' ')
                if S:
                    O += 'QLT({0});'.format(S)
                S = EventStr[64:69].strip(' ')
                if S:
                    O += 'RMS({0});'.format(S)
                S = EventStr[85:89].strip(' ')
                if S:
                    O += 'GAP({0});'.format(S)
                S = EventStr[71:77].strip(' ')
                if S:
                    O += 'ERH({0});'.format(S)
                S = EventStr[78:84].strip(' ')
                if S:
                    O += 'ERZ({0});'.format(S)
                S = EventStr[95:99].strip(' ')
                if S:
                    O += 'INT({0});'.format(S)
            """
            return O

        # Open INET file
        with open(file_name, 'r') as f:

            # Read header
            Header = f.readline().strip('\n')
            #print Header

            I = 0

            while True:
                EventStr = f.readline().strip('\n')
                #print EventStr
                if not EventStr:
                    break
                else:
                    I += 1
                    D = _GetId(EventStr)
                    print D
                    L = _GetLocation(EventStr,D)
                    print L
                    M = _GetMagnitude(EventStr,D)
                    print "despues=", M
                    O = _GetLog(EventStr)
                    #print O
                    self.AddEvent(D, L, M, O)

            f.close()
            return

        # Warn user if model file does not exist
        print 'File not found.'





