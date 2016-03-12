#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from gps import *
from time import *
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import time
import threading
import math
import sqlite3
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_CharLCD as LCD

#Set database directory
home_dir = '/home/laserwolf/'
db_dir = home_dir + 'db/'

#Set database names
ocsdbname='ocs'
gpsdbname='gps'
weatherdbname='weather'

#Set temp sensor id
temp1name='28-0115905a2fff' #Inside temp
temp2name='28-0415901b95ff' #Outside temp
temp3name='28-01159066d4ff' #Water temp

#Set time values (in seconds)
setrefreshtime=1            #Refresh data
setdisttime=5*60            #Update distance travelled
settemptime=15*60           #Update temperature
setbarotime=15*60           #Update barometer

#Set distance values (in meters)
setlogdistmin=50            #Distance required for adding new entry to gps database
setdistprevmin=15           #Distance required for updating distance travelled

#Database stuff
ocsdb_file = db_dir + ocsdbname + '.db'
gpsdb_file = db_dir + gpsdbname + '.db'
weatherdb_file = db_dir + weatherdbname + '.db'
ocsdbonline=os.path.isfile(ocsdb_file)
gpsdbonline=os.path.isfile(gpsdb_file)
weatherdbonline=os.path.isfile(weatherdb_file)

#Create ocs database
if ocsdbonline is False:
  sqlite_file=ocsdb_file
  conn=sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("""CREATE TABLE OCS(
    ID INT PRIMARY KEY   NOT NULL,
    TIME           TEXT   NOT NULL,
    LAT            TEXT   NOT NULL,
    LON            TEXT   NOT NULL,
    SPD            TEXT   NOT NULL,
    SPD_MAX        TEXT   NOT NULL,
    COG            TEXT   NOT NULL,
    HEADING        TEXT   NOT NULL,
    UPTIME         TEXT   NOT NULL,
    UPTIME_MAX     TEXT   NOT NULL,
    DIST           TEXT   NOT NULL,
    DIST_START     TEXT   NOT NULL,
    BARO           TEXT   NOT NULL,
    BARO_MIN       TEXT   NOT NULL,
    BARO_MAX       TEXT   NOT NULL,
    TEMP1          TEXT   NOT NULL,
    TEMP1_MIN      TEXT   NOT NULL,
    TEMP1_MAX      TEXT   NOT NULL,
    TEMP2          TEXT   NOT NULL,
    TEMP2_MIN      TEXT   NOT NULL,
    TEMP2_MAX      TEXT   NOT NULL,
    TEMP3          TEXT   NOT NULL,
    TEMP3_MIN      TEXT   NOT NULL,
    TEMP3_MAX      TEXT   NOT NULL,
    CLINO          TEXT   NOT NULL,
    CLINO_MAX      TEXT   NOT NULL,
    WINDDIR        TEXT   NOT NULL,
    WINDSPD        TEXT   NOT NULL,
    WINDSPD_MAX    TEXT   NOT NULL
    );""")
  c.execute("INSERT INTO OCS (ID, TIME, LAT, LON, SPD, SPD_MAX, COG, HEADING, UPTIME, UPTIME_MAX, DIST, DIST_START, BARO, BARO_MIN, BARO_MAX, TEMP1, TEMP1_MIN, TEMP1_MAX, TEMP2, TEMP2_MIN, TEMP2_MAX, TEMP3, TEMP3_MIN, TEMP3_MAX, CLINO, CLINO_MAX, WINDDIR, WINDSPD, WINDSPD_MAX) VALUES (1, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1481600', '0', '999999', '-999999', '0', '999', '-999', '0', '999', '-999', '0', '999', '-999', '0', '0', '0', '0', '0')")
  conn.commit()
  conn.close()

#Create gps database
if gpsdbonline is False:
  sqlite_file=gpsdb_file
  conn=sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("""CREATE TABLE GPS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
    TIME           TEXT   NOT NULL,
    LAT            TEXT   NOT NULL,
    LON            TEXT   NOT NULL,
    SPD            TEXT   NOT NULL,
    COG            TEXT   NOT NULL,
    HDG            TEXT   NOT NULL,
    CLINO          TEXT   NOT NULL
    );""")
  conn.commit()
  conn.close()
  
#Create weather database
if weatherdbonline is False:
  sqlite_file=weatherdb_file
  conn=sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("""CREATE TABLE WEATHER(
    ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
    TIME           TEXT   NOT NULL,
    BARO           TEXT   NOT NULL,
    TEMP1          TEXT   NOT NULL,
    TEMP2          TEXT   NOT NULL,
    TEMP3          TEXT   NOT NULL,
    WINDDIR        TEXT   NOT NULL,
    WINDSPD        TEXT   NOT NULL
    );""")
  conn.commit()
  conn.close()

#Temperature stuff
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
temp_base_dir = '/sys/bus/w1/devices/'
temp1device_folder = temp_base_dir + temp1name
temp2device_folder = temp_base_dir + temp2name
temp3device_folder = temp_base_dir + temp3name
temp1device_file = temp1device_folder + '/w1_slave'
temp2device_file = temp2device_folder + '/w1_slave'
temp3device_file = temp3device_folder + '/w1_slave'
time.sleep(1)
temp1online=os.path.isfile(temp1device_file)
temp2online=os.path.isfile(temp2device_file)
temp3online=os.path.isfile(temp3device_file)

#Setup LCD
lcd = LCD.Adafruit_CharLCD(25, 24, 23, 17, 27, 22, 20, 4)

#Setup barometric sensor
baro_sensor = BMP085.BMP085()

#Get old data
sqlite_file=ocsdb_file
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM OCS")
row=c.fetchone()
oldspdmax=float(row[5])
olduptimemax=float(row[9])
olddist=float(row[10])
diststart=float(row[11])
baromin=float(row[13])
baromax=float(row[14])
temp1min=float(row[16])
temp1max=float(row[17])
temp2min=float(row[19])
temp2max=float(row[20])
temp3min=float(row[22])
temp3max=float(row[23])
clinomax=float(row[25])
windspdmax=float(row[28])
conn.commit()
conn.close()
dist=olddist
spdmax=oldspdmax
uptimemax=olduptimemax

#Set default values
setlcdtime=15
setconkytime=15
setocstime=15
setweatherlogtime=30*60
setlogtime=30*60
uptime=0
uptimesec=0
uptimemin=0
uptimehour=0
uptimeday=0
refreshtime=0
gpsfixtime=0
disttime=0
lcdtime=setlcdtime
conkytime=setconkytime
ocstime=setocstime
logtime=setlogtime
barotime=setbarotime
temptime=settemptime
weatherlogtime=setweatherlogtime
distfirst=1
logfirst=1
gpsmod=0
gpslat=0
gpslon=0
gpsspd=0
gpscog=0
gpslatdir='N'
gpslondir='E'
baro=0
temp1=0
temp2=0
temp3=0
heading=0
clino=0
windspd=0
winddir=0
lcdnum=0
lcdscreen=1
gpsd = None

#Start realtime
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:

      #Time
      currenttime=datetime.now().strftime('%d.%m.%Y %H:%M:%S')
      currenttimestamp=time.time()
      
      #Refresh GPS data
      if (uptime == 0) or (refreshtime >= setrefreshtime):
        gpsfix=0
        if math.isnan(gpsd.fix.mode) is False:
          gpsmod=gpsd.fix.mode
          if gpsmod == 3:
            gpsfix=1
            gpsfixtime=0
            if math.isnan(gpsd.fix.latitude) is False:
              gpslat=gpsd.fix.latitude
            if math.isnan(gpsd.fix.longitude) is False:
              gpslon=gpsd.fix.longitude
            if math.isnan(gpsd.fix.speed) is False:
              gpsspd=gpsd.fix.speed
              if gpsspd > spdmax:
                spdmax=gpsspd
            if math.isnan(gpsd.fix.track) is False:
              gpscog=gpsd.fix.track
        refreshtime = 0
        #Format Latitude
        if str(gpslat)[0] == "-":
          gpslatformat=float(str(gpslat)[1:])
          gpslatdir='S'
        else:
          gpslatformat=float(gpslat)
          gpslatdir='N'
        gpslatsplit=str(gpslatformat).split('.')
        gpslatdeg=int(gpslatsplit[0])
        gpslatdegformat='0:03d'.format(gpslatdeg)
        gpslatmin='{0:.3f}'.format((float('0.%s' % gpslatsplit[1])*60))
        gpslatminformat='{0:06.3f}'.format(float(gpslatmin))
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
        gpslondegformat='0:03d'.format(gpslondeg)
        gpslonmin='{0:.3f}'.format((float('0.%s' % gpslonsplit[1])*60))
        gpslonminformat='{0:06.3f}'.format(float(gpslonmin))
        gpslonformatfull='{0}° {1}\'{2}'.format(gpslondeg,gpslonmin,gpslondir)
        #Format Speed
        gpsspdformat='{0:.1f}'.format((float(gpsspd) * 1.9438444924574))
        gpsspdformatfull='{0} KN'.format(gpsspdformat)
        #Format Course Over Ground
        gpscogformat='{0:03d}'.format(int(gpscog))
        gpscogformatfull='{0}°'.format(gpscogformat)
        #Format Fix
        if gpsfix==1:
          gpsfixformat='%{F#638057}[ FX ]%{F-}'
        else:
          gpsfixformat="%{F#805A57}[ NO ]%{F-}"

      #Calculate distance
      if (gpsfix==1):
        if (distfirst==1):
          distlat=gpslat
          distlon=gpslon
          distfirst=0
        if (disttime >= setdisttime):
          lat1=float(distlat)
          lon1=float(distlon)
          lat2=float(gpslat)
          lon2=float(gpslon)
          lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
          #haversine formula 
          dlon = lon2 - lon1 
          dlat = lat2 - lat1 
          haversine_a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
          haversine_c = 2 * asin(sqrt(haversine_a)) 
          haversine_r = 6371 # Radius of earth in kilometers. Use 3956 for miles
          distprev=int((haversine_c*haversine_r)*1000)
          if distprev > setdistprevmin:
            distprev=distprev
            distlat=gpslat
            distlon=gpslon
          else:
            distprev=0
          dist=int(dist)+int(distprev)
          disttime=0

      #Read barometer
      if (barotime >= setbarotime):
        #baro_temp=baro_sensor.read_temperature()
        baro=float(baro_sensor.read_pressure())
        if (baro > baromax) and (baro != 0):
          baromax=baro
        if (baro < baromin) and (baro != 0):
          baromin=baro
        barotime=0

      #Read temperature
      if (temptime >= settemptime):
        #temp1
        if temp1online is True:
          temp1f = open(temp1device_file, 'r')
          temp1flines = temp1f.readlines()
          temp1f.close()
          if temp1flines[0].strip()[-3:] == 'YES':
            temp1equals_pos = temp1flines[1].find('t=')
            if temp1equals_pos != -1:
              temp1_string = temp1flines[1][temp1equals_pos+2:]
              if (int(float(temp1_string)/1000.0)) != 85:
                temp1 = float(temp1_string) / 1000.0
                if temp1 > temp1max:
                  temp1max=temp1
                if temp1 < temp1min:
                  temp1min=temp1
        #temp2
        if temp2online is True:
          temp2f = open(temp2device_file, 'r')
          temp2flines = temp2f.readlines()
          temp2f.close()
          if temp2flines[0].strip()[-3:] == 'YES':
            temp2equals_pos = temp2flines[1].find('t=')
            if temp2equals_pos != -1:
              temp2_string = temp2flines[1][temp2equals_pos+2:]
              if (int(float(temp2_string)/1000.0)) != 85:
                temp2 = float(temp2_string) / 1000.0
                if temp2 > temp2max:
                  temp2max=temp2
                if temp2 < temp2min:
                  temp2min=temp2
        #temp3
        if temp3online is True:
          temp3f = open(temp3device_file, 'r')
          temp3flines = temp3f.readlines()
          temp3f.close()
          if temp3flines[0].strip()[-3:] == 'YES':
            temp3equals_pos = temp3flines[1].find('t=')
            if temp3equals_pos != -1:
              temp3_string = temp3flines[1][temp3equals_pos+2:]
              if (int(float(temp3_string)/1000.0)) != 85:
                temp3 = float(temp3_string) / 1000.0
                if temp3 > temp3max:
                  temp3max=temp3
                if temp3 < temp3min:
                  temp3min=temp3
        temptime=0

      #Format stuff
      windspdformat='{0:.1f}'.format(windspd)
      windspdformatfull='{0} MS'.format(windspdformat)
      winddirformat='{0:03d}'.format(int(winddir))
      winddirformatfull='{0}°'.format(winddirformat)
      windformatfull='{0} {1}'.format(winddirformatfull,windspdformatfull)
      headingformat='{0:03d}'.format(int(heading))
      headingformatfull='{0}°'.format(headingformat)
      clinoformat='{0}'.format(int(clino))
      clinoformatfull='{0}°'.format(clinoformat)
      distformat='{0:.1f}'.format((float(dist)+float(diststart)) * 0.000539956803)
      distformatfull='{0} NM'.format(distformat)
      baroformat='{0}'.format(int(baro/100))
      baroformatfull='{0} MBAR'.format(baroformat)
      temp1format='{0:.1f}'.format(float(temp1))
      temp1formatfull='{0}°C'.format(temp1format)
      temp2format='{0:.1f}'.format(float(temp2))
      temp2formatfull='{0}°C'.format(temp2format)
      temp3format='{0:.1f}'.format(float(temp3))
      temp3formatfull='{0}°C'.format(temp3format)
      uptimeformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptimeday, uptimehour, uptimemin)

      #Print data
      print'%{c}',gpsfixformat,' TIME:',currenttime,' // LAT:',gpslatformatfull,' // LON:',gpslonformatfull,' // SPD:',gpsspdformatfull,' // COG:',gpscogformatfull,' ',gpsfixformat
      
      #Update LCD
      if (uptime==0) or ((lcdtime >= setlcdtime) and (((datetime.now().strftime('%S')) == '00') or ((datetime.now().strftime('%S')) == '30'))):
        lcdnum+=1
        if lcdnum == 1:
          lcdscreen=1
        elif lcdnum == 3:
          lcdscreen=2
        elif lcdnum == 4:
          lcdscreen=3
        time_lcd='  {TIME}  '.format(TIME=datetime.now().strftime('%d.%m.%Y %H:%M'))
        lat_lcd=('LAT:')+('{0}'.format(gpslatdeg)+chr(223)).rjust(7)+('{0}\'{1}'.format(gpslatmin,gpslatdir)).rjust(9)
        lon_lcd=('LON:')+('{0}'.format(gpslondeg)+chr(223)).rjust(7)+('{0}\'{1}'.format(gpslonmin,gpslondir)).rjust(9)
        spdcog_lcd=('SPD:')+('{0}KN'.format(gpsspdformat)).rjust(6)+' '+'COG:'+('{0}'.format(gpscogformat)+chr(223)).rjust(5)
        wind_lcd=('WIND:')+('{0}'.format(winddirformat)+chr(223)+' {0}'.format(windspdformatfull)).rjust(15)
        dist_lcd=('LOG:')+('{0}'.format(distformatfull)).rjust(16)
        heading_lcd=('HDG:')+('{0}'.format(headingformat)+chr(223)).rjust(16)
        clino_lcd=('CLINO:')+('{0}'.format(clinoformat)+chr(223)).rjust(14)
        baro_lcd=('BARO:')+(baroformatfull).rjust(15)
        temp1_lcd=('INSIDE:')+('{0}'.format(temp1format)+chr(223)+'C').rjust(13)
        temp2_lcd=('OUTSIDE:')+('{0}'.format(temp2format)+chr(223)+'C').rjust(12)
        temp3_lcd=('WATER:')+('{0}'.format(temp3format)+chr(223)+'C').rjust(14)
        #screen1
        lcd_screen1_line1=time_lcd
        lcd_screen1_line2=lat_lcd
        lcd_screen1_line3=lon_lcd
        lcd_screen1_line4=spdcog_lcd
        #screen2
        lcd_screen2_line1=clino_lcd
        lcd_screen2_line2=heading_lcd
        lcd_screen2_line3=dist_lcd
        lcd_screen2_line4=wind_lcd
        #screen3
        lcd_screen3_line1=baro_lcd
        lcd_screen3_line2=temp1_lcd
        lcd_screen3_line3=temp2_lcd
        lcd_screen3_line4=temp3_lcd
        if lcdscreen == 1:
          lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen1_line1,line2=lcd_screen1_line2,line3=lcd_screen1_line3,line4=lcd_screen1_line4)
        elif lcdscreen == 2:
          lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen2_line1,line2=lcd_screen2_line2,line3=lcd_screen2_line3,line4=lcd_screen2_line4)
        elif lcdscreen == 3:        
          lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen3_line1,line2=lcd_screen3_line2,line3=lcd_screen3_line3,line4=lcd_screen3_line4)
          lcdnum=0
        lcd.clear()
        lcd.message(lcdtext)
        lcdtime=0
      
      #Output data to conky
      if (uptime==0) or ((conkytime >= setconkytime) and (((datetime.now().strftime('%S')) == '00') or ((datetime.now().strftime('%S')) == '30'))):
        conkytext='$alignc CLINO: {CLINO} // HDG: {HDG} // LOG: {LOG} // WIND: {WIND} \n$alignc BARO: {BARO} // INSIDE: {INSIDE} // OUTSIDE: {OUTSIDE} // WATER: {WATER} '.format(HDG=headingformatfull,CLINO=clinoformatfull,LOG=distformatfull,UPTIME=uptimeformatfull,INSIDE=temp1formatfull,OUTSIDE=temp2formatfull,WATER=temp3formatfull,BARO=baroformatfull,WIND=windformatfull)
        conkyfile = open(home_dir+'.conkytext.txt', 'w')
        conkyfile.writelines(conkytext)
        conkyfile.close()
        conkytime=0

      #Update ocs database
      if (gpsfix==1) and ((ocstime >= setocstime) and(datetime.now().strftime('%S')) == '00'):
        sqlite_file=ocsdb_file
        conn=sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("UPDATE OCS SET TIME='{TIME}', LAT='{LAT}', LON='{LON}', SPD='{SPD}', SPD_MAX='{SPD_MAX}', COG='{COG}', HEADING='{HEADING}', UPTIME='{UPTIME}', UPTIME_MAX='{UPTIME_MAX}', DIST='{DIST}', BARO='{BARO}', BARO_MIN='{BARO_MIN}', BARO_MAX='{BARO_MAX}', TEMP1='{TEMP1}', TEMP1_MIN='{TEMP1_MIN}', TEMP1_MAX='{TEMP1_MAX}', TEMP2='{TEMP2}', TEMP2_MIN='{TEMP2_MIN}', TEMP2_MAX='{TEMP2_MAX}', TEMP3='{TEMP3}', TEMP3_MIN='{TEMP3_MIN}', TEMP3_MAX='{TEMP3_MAX}'".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,SPD_MAX=spdmax,COG=gpscog,HEADING=heading,UPTIME=int(uptime),UPTIME_MAX=int(uptimemax),DIST=dist,BARO=baro,BARO_MIN=baromin,BARO_MAX=baromax,TEMP1=temp1,TEMP1_MIN=temp1min,TEMP1_MAX=temp1max,TEMP2=temp2,TEMP2_MIN=temp2min,TEMP2_MAX=temp2max,TEMP3=temp3,TEMP3_MIN=temp3min,TEMP3_MAX=temp3max))
        conn.commit()
        conn.close()
        ocstime = 0

      #Update log database
      if (gpsfix==1) and (logtime >= setlogtime) and ((logfirst==1) or ((datetime.now().strftime('%M')) == '00')):
        if (logfirst==1):
          logdistprev=0
          oldlognum=int(0)
          oldloglat=float(0)
          oldloglon=float(0)
          sqlite_file=gpsdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("SELECT count(*), LAT, LON FROM GPS ORDER BY ID DESC LIMIT 1")
          row=c.fetchone()
          oldlognum=int(row[0])
          if oldlognum == 0:
            lognumfirst=1
          else:
            lognumfirst=0
            oldloglat=float(row[1])
            oldloglon=float(row[2])
          conn.commit()
          conn.close()
          loglat=oldloglat
          loglon=oldloglon
          logfirst=0
        #calculate distance
        if lognumfirst == 0:
          lat1=float(loglat)
          lon1=float(loglon)
          lat2=float(gpslat)
          lon2=float(gpslon)
          lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
          #haversine formula 
          dlon = lon2 - lon1 
          dlat = lat2 - lat1 
          haversine_a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
          haversine_c = 2 * asin(sqrt(haversine_a)) 
          haversine_r = 6371 # Radius of earth in kilometers. Use 3956 for miles
          logdistprev=int((haversine_c*haversine_r)*1000)
        if (lognumfirst == 1) or (logdistprev > setlogdistmin):
          sqlite_file=gpsdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("INSERT INTO GPS ( TIME, LAT, LON, SPD, COG, HDG, CLINO ) VALUES ( '{TIME}', '{LAT}', '{LON}', '{SPD}', '{COG}', '{HDG}', '{CLINO}')".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,COG=gpscog,HDG=heading,CLINO=clino))
          conn.commit()
          conn.close()
          loglat=gpslat
          loglon=gpslon
          lognumfirst=0
        logtime = 0

      #Update weather database
      if (weatherlogtime >= setweatherlogtime) and ((datetime.now().strftime('%M')) == '00'):
        sqlite_file=weatherdb_file
        conn=sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("INSERT INTO WEATHER ( TIME, BARO, TEMP1, TEMP2, TEMP3, WINDDIR, WINDSPD ) VALUES ( '{TIME}', '{BARO}', '{TEMP1}', '{TEMP2}', '{TEMP3}', '{WINDDIR}', '{WINDSPD}')".format(TIME=currenttimestamp,BARO=baro,TEMP1=temp1,TEMP2=temp2,TEMP3=temp3,WINDDIR=winddir,WINDSPD=windspd))
        conn.commit()
        conn.close()
        weatherlogtime = 0

      #Update time
      uptime+=0.5
      if uptime > uptimemax:
        uptimemax=uptime
      uptimemin, uptimesec = divmod(uptime, 60)
      uptimehour, uptimemin = divmod(uptimemin, 60)
      uptimeday, uptimehour = divmod(uptimehour, 24)
      refreshtime+=0.5
      lcdtime+=0.5
      conkytime+=0.5
      disttime+=0.5
      barotime+=0.5
      temptime+=0.5
      ocstime+=0.5
      logtime+=0.5
      weatherlogtime+=0.5
      if gpsfix == 0:
        gpsfixtime+=0.5

      #Sleep
      time.sleep(0.5)

  except (SystemExit):
    gpsp.running = False
    gpsp.join()
    print'%{c}ERROR'
