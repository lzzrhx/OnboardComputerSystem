#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import sqlite3
from math import radians, cos, sin, asin, sqrt

os.system('clear')

#Get stats
spdmax=0
uptime=0
uptimemax=0
sqlite_file='/home/laserwolf/Databases/ocs.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM ocs")
row=c.fetchone()
spdmax=float(row[5])
uptime=float(row[8])
uptimemax=float(row[9])
conn.commit()
conn.close()

#Format max speed
spdmaxformat='{0:.1f}'.format((float(spdmax) * 1.9438444924574))
spdmaxformatfull='{0} KN'.format(spdmaxformat)

#Format uptime
uptmin, uptsec = divmod(uptime, 60)
upthour, uptmin = divmod(uptmin, 60)
uptday, upthour = divmod(upthour, 24)
uptimeformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptday, upthour, uptmin)

#Format max uptime
uptmaxmin, uptmaxsec = divmod(uptimemax, 60)
uptmaxhour, uptmaxmin = divmod(uptmaxmin, 60)
uptmaxday, uptmaxhour = divmod(uptmaxhour, 24)
uptimemaxformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptmaxday, uptmaxhour, uptmaxmin)

#Print data
print
print '   --------------------------------------------------------------------------------------------'
print '  | INFO'
print '   --------------------------------------------------------------------------------------------'
print '  |   UPTIME       //   ',uptimeformatfull
print '  |   MAX SPD      //   ',spdmaxformatfull
print '  |   MAX UPTIME   //   ',uptimemaxformatfull
print '   --------------------------------------------------------------------------------------------'
print

while 1==1:
  time.sleep(24*60*60)
