#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
import sqlite3
import math

os.system('clear')

print
print '   --------------------------------------------------------------------------------------------'
print '  | WEATHER HISTORY'
print '   --------------------------------------------------------------------------------------------'

#Get weather log
home_dir = os.path.expanduser('~') + '/'
sqlite_file=home_dir + 'Databases/weather.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM WEATHER")
while True:
  row=c.fetchone()
  if row == None:
    break
  weather_num=int(row[0])
  weather_time=str(row[1])
  weather_baro=float(row[2])
  weather_temp1=float(row[3])
  weather_temp2=float(row[4])
  weather_temp3=float(row[5])
  weather_winddir=float(row[6])
  weather_windspd=float(row[7])
  #Format Entry number
  weather_numformatfull='%05d' %(weather_num)
  #Format time
  weather_timeformatfull=datetime.fromtimestamp(float(weather_time)).strftime('%d.%m.%Y %H:%M')
  #Format baro
  weather_baroformat=int(weather_baro/100)
  weather_baroformatfull='{0} mbar'.format(weather_baroformat)
  #Format temp1
  weather_temp1format='{0:.1f}'.format(float(weather_temp1))
  weather_temp1formatfull='{0}°C'.format(weather_temp1format)
  #Format temp2
  weather_temp2format='{0:.1f}'.format(float(weather_temp2))
  weather_temp2formatfull='{0}°C'.format(weather_temp2format)
  #Format temp3
  weather_temp3format='{0:.1f}'.format(float(weather_temp3))
  weather_temp3formatfull='{0}°C'.format(weather_temp3format)
  #Print data
  print '  |   NO             //   ',weather_numformatfull
  print '  |   TIME           //   ',weather_timeformatfull
  print '  |   BARO           //   ',weather_baroformatfull
  print '  |   INSIDE         //   ',weather_temp1formatfull
  print '  |   OUTSIDE        //   ',weather_temp2formatfull
  print '  |   WATER          //   ',weather_temp3formatfull
  print '  |   WINDDIR        //   ',weather_winddir
  print '  |   WINDSPD        //   ',weather_windspd
  print '   --------------------------------------------------------------------------------------------'
conn.close()

#Get stats
sqlite_file='/home/laserwolf/Databases/ocs.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM OCS")
row=c.fetchone()
baromin=float(row[13])
baromax=float(row[14])
temp1min=float(row[16])
temp1max=float(row[17])
temp2min=float(row[19])
temp2max=float(row[20])
temp3min=float(row[22])
temp3max=float(row[23])
conn.commit()
conn.close()
#Format baro
barominformat='{0:.1f}'.format(float(baromin/100))
barominformatfull='{0} mbar'.format(barominformat)
baromaxformat='{0:.1f}'.format(float(baromax/100))
baromaxformatfull='{0} mbar'.format(baromaxformat)
#Format temp1
temp1minformat='{0:.1f}'.format(float(temp1min))
temp1minformatfull='{0}°C'.format(temp1minformat)
temp1maxformat='{0:.1f}'.format(float(temp1max))
temp1maxformatfull='{0}°C'.format(temp1maxformat)
#Format temp2
temp2minformat='{0:.1f}'.format(float(temp2min))
temp2minformatfull='{0}°C'.format(temp2minformat)
temp2maxformat='{0:.1f}'.format(float(temp2max))
temp2maxformatfull='{0}°C'.format(temp2maxformat)
#Format temp3
temp3minformat='{0:.1f}'.format(float(temp3min))
temp3minformatfull='{0}°C'.format(temp3minformat)
temp3maxformat='{0:.1f}'.format(float(temp3max))
temp3maxformatfull='{0}°C'.format(temp3maxformat)
#Print data
print
print '   --------------------------------------------------------------------------------------------'
print '  | STATS'
print '   --------------------------------------------------------------------------------------------'
print '  |   MIN BAROMETRIC PRESSURE   //   ',barominformatfull
print '  |   MAX BAROMETRIC PRESSURE   //   ',baromaxformatfull
print '  |   MIN TEMP INSIDE           //   ',temp1minformatfull
print '  |   MAX TEMP INSIDE           //   ',temp1maxformatfull
print '  |   MIN TEMP OUTSIDE          //   ',temp2minformatfull
print '  |   MAX TEMP OUTSIDE          //   ',temp2maxformatfull
print '  |   MIN TEMP WATER            //   ',temp3minformatfull
print '  |   MAX TEMP WATER            //   ',temp3maxformatfull
print '   --------------------------------------------------------------------------------------------'
print

while 1==1:
  time.sleep(24*60*60)
