#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
import sqlite3
from math import radians, cos, sin, asin, sqrt

os.system('clear')

print
print '   --------------------------------------------------------------------------------------------'
print '  | GPS LOG'
print '   --------------------------------------------------------------------------------------------'

#Get gps log
sqlite_file='/home/laserwolf/db/gps.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM GPS")
while True:
  row=c.fetchone()
  if row == None:
    break
  gpsnum=int(row[0])
  gpstime=str(row[1])
  gpslat=float(row[2])
  gpslon=float(row[3])
  gpsspd=float(row[4])
  gpscog=float(row[5])
  gpshdg=float(row[6])
  gpsclino=float(row[7])
  #Format Entry number
  gpsnumformatfull='%05d' %(gpsnum)
  #Format time
  gpstimeformatfull=datetime.fromtimestamp(float(gpstime)).strftime('%d.%m.%Y %H:%M')
  #Format Latitude
  if str(gpslat)[0] == "-":
    gpslatformat=float(str(gpslat)[1:])
    gpslatdir='S'
  else:
    gpslatformat=float(gpslat)
    gpslatdir='N'
  gpslatsplit=str(gpslatformat).split('.')
  gpslatdeg=int(gpslatsplit[0])
  gpslatmin='{0:.3f}'.format((float('0.%s' % gpslatsplit[1])*60))
  gpslatformatfull='{0}° {1}\'{2}'.format(gpslatdeg,gpslatmin,gpslatdir)
  #Format Longitude
  if str(gpslon)[0] == "-":
    gpslonformat=float(str(gpslon)[1:])
    gpslondir='W'
  else:
    gpslonformat=float(gpslon)
    gpslondir='E'
  gpslonsplit=str(gpslonformat).split('.')
  gpslondeg=int(gpslonsplit[0])
  gpslonmin='{0:.3f}'.format((float('0.%s' % gpslonsplit[1])*60))
  gpslonformatfull='{0}° {1}\'{2}'.format(gpslondeg,gpslonmin,gpslondir)
  #Format Speed
  gpsspdformat='{0:.1f}'.format((float(gpsspd) * 1.9438444924574))
  gpsspdformatfull='{0} KN'.format(gpsspdformat)
  #Format Course Over Ground
  gpscogformat='{0:03d}'.format(int(gpscog))
  gpscogformatfull='{0}°'.format(gpscogformat)
  #Print data
  print '  |   NO           //   ',gpsnumformatfull
  print '  |   TIME         //   ',gpstimeformatfull
  print '  |   LAT          //   ',gpslatformatfull
  print '  |   LON          //   ',gpslonformatfull
  print '  |   SPD          //   ',gpsspdformatfull
  print '  |   COG          //   ',gpscogformatfull
  print '  |   HDG          //   ',gpshdg
  print '  |   CLINO        //   ',gpsclino
  print '   --------------------------------------------------------------------------------------------'
conn.close()

while 1==1:
  time.sleep(24*60*60)
