#! /usr/bin/python
# -*- coding: utf-8 -*-

#Import stuff
from gps import *
from time import *
from time import sleep
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import os
import logging
import time
import threading
import math
import sqlite3

#Set directories
home_dir = '/home/laserwolf/'  #Home directory
db_dir = home_dir + 'db/'      #Database directory

#Set database names
ocsdbname='ocs'                #OCS database
gpsdbname='gps'                #GPS log database
weatherdbname='weather'        #Weather log database

#Set temp sensor id
temp1name='28-0115905a2fff'    #Inside temp
temp2name='28-0415901b95ff'    #Outside temp
temp3name='28-01159066d4ff'    #Water temp

#Set time values (in seconds)
setrefreshtime=1               #Refresh data
setgpswaittime=2*60            #Wait for gps at boot
setdisttime=5*60               #Update distance travelled
settemptime=15*60              #Update temperature
setbarotime=15*60              #Update barometer

#Set distance values (in meters)
setlogdistmin=50               #Distance required for adding new entry to GPS log database
setdistprevmin=15              #Distance required for updating distance travelled

#Set clinometer calibration values
clinoxzero=(0)                 #X axis
clinoyzero=(0)                 #Y Axis

#Database stuff
ocsdb_file = db_dir + ocsdbname + '.db'
gpsdb_file = db_dir + gpsdbname + '.db'
weatherdb_file = db_dir + weatherdbname + '.db'
ocsdbonline=os.path.isfile(ocsdb_file)
gpsdbonline=os.path.isfile(gpsdb_file)
weatherdbonline=os.path.isfile(weatherdb_file)

#Create OCS database
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
    CLINOX         TEXT   NOT NULL,
    CLINOX_MIN     TEXT   NOT NULL,
    CLINOX_MAX     TEXT   NOT NULL,
    CLINOY         TEXT   NOT NULL,
    CLINOY_MIN     TEXT   NOT NULL,
    CLINOY_MAX     TEXT   NOT NULL,
    WINDDIR        TEXT   NOT NULL,
    WINDSPD        TEXT   NOT NULL,
    WINDSPD_MAX    TEXT   NOT NULL
    );""")
  c.execute("INSERT INTO OCS (ID, TIME, LAT, LON, SPD, SPD_MAX, COG, HEADING, UPTIME, UPTIME_MAX, DIST, DIST_START, BARO, BARO_MIN, BARO_MAX, TEMP1, TEMP1_MIN, TEMP1_MAX, TEMP2, TEMP2_MIN, TEMP2_MAX, TEMP3, TEMP3_MIN, TEMP3_MAX, CLINOX, CLINOX_MIN, CLINOX_MAX, CLINOY, CLINOY_MIN, CLINOY_MAX, WINDDIR, WINDSPD, WINDSPD_MAX) VALUES (1, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1481600', '0', '999999', '-999999', '0', '999', '-999', '0', '999', '-999', '0', '999', '-999', '0', '0', '0', '0', '0', '0', '0', '0', '0')")
  conn.commit()
  conn.close()

#Create GPS log database
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
    CLINOX         TEXT   NOT NULL,
    CLINOY         TEXT   NOT NULL
    );""")
  conn.commit()
  conn.close()
  
#Create weather log database
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

#Setup temperature sensors
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

#Setup LCD (from https://github.com/adafruit/Adafruit_Python_CharLCD)
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCD(25, 24, 23, 17, 27, 22, 20, 4)

#Setup BMP180 barometric pressure sensor (from https://github.com/adafruit/Adafruit_Python_BMP)
import Adafruit_BMP.BMP085 as BMP085
baro_sensor = BMP085.BMP085()

#Setup LSM303D compass+accelerometer sensor (from http://davekopp.weebly.com/minimu-inertial-measurement-unit-driver-for-raspberry-pi-lsm303d-and-l3gd20h.html)
def LSM_COMBINE(msb, lsb):
  comb = 256*msb + lsb
  if comb >= 32768:
    return comb - 65536
  else:
    return comb
from smbus import SMBus
LSM_BUS = SMBus(1)
LSM = 0x1d #Device I2C slave address
LSM_WHOAMI_ADDRESS = 0x0F
LSM_WHOAMI_CONTENTS = 0b1001001 #Device self-id
LSM_CTRL_0 = 0x1F #General settings
LSM_CTRL_1 = 0x20 #Turns on accelerometer and configures data rate
LSM_CTRL_2 = 0x21 #Self test accelerometer, anti-aliasing accel filter
LSM_CTRL_3 = 0x22 #Interrupts
LSM_CTRL_4 = 0x23 #Interrupts
LSM_CTRL_5 = 0x24 #Turns on temperature sensor
LSM_CTRL_6 = 0x25 #Magnetic resolution selection, data rate config
LSM_CTRL_7 = 0x26 #Turns on magnetometer and adjusts mode
LSM_MAG_X_LSB = 0x08 # x
LSM_MAG_X_MSB = 0x09
LSM_MAG_Y_LSB = 0x0A # y
LSM_MAG_Y_MSB = 0x0B
LSM_MAG_Z_LSB = 0x0C # z
LSM_MAG_Z_MSB = 0x0D
LSM_ACC_X_LSB = 0x28 # x
LSM_ACC_X_MSB = 0x29
LSM_ACC_Y_LSB = 0x2A # y
LSM_ACC_Y_MSB = 0x2B
LSM_ACC_Z_LSB = 0x2C # z
LSM_ACC_Z_MSB = 0x2D
LSM_TEMP_MSB = 0x05
LSM_TEMP_LSB = 0x06
#Ensure chip is detected properly on the bus
if LSM_BUS.read_byte_data(LSM, LSM_WHOAMI_ADDRESS) == LSM_WHOAMI_CONTENTS:
  lsmonline=True
  LSM_BUS.write_byte_data(LSM, LSM_CTRL_1, 0b1010111) # enable accelerometer, 50 hz sampling
  LSM_BUS.write_byte_data(LSM, LSM_CTRL_2, 0x00) #set +/- 2g full scale
  LSM_BUS.write_byte_data(LSM, LSM_CTRL_5, 0b01100100) #high resolution mode, thermometer off, 6.25hz ODR
  LSM_BUS.write_byte_data(LSM, LSM_CTRL_6, 0b00100000) # set +/- 4 gauss full scale
  LSM_BUS.write_byte_data(LSM, LSM_CTRL_7, 0x00) #get magnetometer out of low power mode
else:
  lsmonline=False

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
clinoxmin=float(row[25])
clinoxmax=str(row[26])
clinoymin=float(row[28])
clinoymax=str(row[29])
windspdmax=float(row[32])
conn.commit()
conn.close()
dist=olddist
spdmax=oldspdmax
uptimemax=olduptimemax

#Set default values
gpsd = None
uptime=0
refreshtime=setrefreshtime
gpsfixtime=0
disttime=0
barotime=setbarotime
temptime=settemptime
distfirst=1
logfirst=1
lcdnum=0
lcd_update=0
conky_update=0
ocsdb_update=0
gpsdb_update=0
weatherdb_update=0
gpsmod=0
gpslat=0
gpslon=0
gpsspd=0
gpscog=0
heading=0
clinox=0
clinoy=0
baro=0
temp1=0
temp2=0
temp3=0
windspd=0
winddir=0

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

      #Refresh
      if (refreshtime>=setrefreshtime):

        #Set update values
        if (uptime==0 or (datetime.now().strftime('%S')=='00' or datetime.now().strftime('%S')=='30')):
          lcd_update=1
        if (uptime==0 or (datetime.now().strftime('%S')=='00' or datetime.now().strftime('%S')=='30')):
          conky_update=1
        if (uptime>=setgpswaittime and datetime.now().strftime('%S')=='00'):
          ocsdb_update=1
        if (uptime>=setgpswaittime and (logfirst==1 or (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'))):
          gpsdb_update=1
        if (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'):
          weatherdb_update=1

        #Uptime
        if uptime > uptimemax:
          uptimemax=uptime
        uptimemin, uptimesec = divmod(uptime, 60)
        uptimehour, uptimemin = divmod(uptimemin, 60)
        uptimeday, uptimehour = divmod(uptimehour, 24)
      
        #Read GPS data
        if math.isnan(gpsd.fix.mode) is False:
          if gpsd.fix.mode == 3:
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
          else:
            gpsfix=0

        #Read heading & clinometer
        if lsmonline is True:
          magx = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_MAG_X_MSB), LSM_BUS.read_byte_data(LSM, LSM_MAG_X_LSB))
          magy = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_MAG_Y_MSB), LSM_BUS.read_byte_data(LSM, LSM_MAG_Y_LSB))
          magz = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_MAG_Z_MSB), LSM_BUS.read_byte_data(LSM, LSM_MAG_Z_LSB))
          accx = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_ACC_X_MSB), LSM_BUS.read_byte_data(LSM, LSM_ACC_X_LSB))
          accy = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_ACC_Y_MSB), LSM_BUS.read_byte_data(LSM, LSM_ACC_Y_LSB))
          accz = LSM_COMBINE(LSM_BUS.read_byte_data(LSM, LSM_ACC_Z_MSB), LSM_BUS.read_byte_data(LSM, LSM_ACC_Z_LSB))
          #Normalize accelerometer raw values
          accxnorm = accx/math.sqrt(accx * accx + accy * accy + accz * accz)
          accynorm = accy/math.sqrt(accx * accx + accy * accy + accz * accz)
          #Calculate pitch & roll
          accpitch = math.asin(-accxnorm)
          accroll = math.asin(accynorm/math.cos(accpitch))
          #Calculate tilt compensated heading
          magxcomp = magx*math.cos(accpitch)+magz*math.sin(accpitch)
          magycomp = magx*math.sin(accroll)*math.sin(accpitch)+magy*math.cos(accroll)-magz*math.sin(accroll)*math.cos(accpitch)
          heading = 180 * math.atan2(magycomp,magxcomp)/math.pi
          #heading = 180 * math.atan2(magy,magx)/math.pi
          if heading < 0:
            heading += 360
          #convert accelerometer values to degrees
          accxdeg =  (math.atan2(accy,accz)+math.pi)*57.29578
          accydeg =  (math.atan2(accz,accx)+math.pi)*57.29578
          accxdeg -= 180.0
          if accydeg > 90:
            accydeg -= 270.0
          else:
            accydeg += 90.0
          clinox=accxdeg+clinoxzero
          clinoy=accydeg+clinoyzero
          if clinox < clinoxmin:
            clinoxmin=clinox
          if clinox > clinoxmax:
            clinoxmax=clinox
          if clinoy < clinoymin:
            clinoymin=clinoy
          if clinoy > clinoymax:
            clinoymax=clinoy

        #Read barometric pressure
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
          #Temperature sensor #1
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
          #Temperature sensor #2
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
          #Temperature sensor #3
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

        #Calculate distance travelled
        if (gpsfix==1 and uptime>=setgpswaittime):
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

        #Format latitude
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

        #Format longitude
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

        #Format speed
        gpsspdformat='{0:.1f}'.format((float(gpsspd) * 1.9438444924574))
        gpsspdformatfull='{0} KN'.format(gpsspdformat)

        #Format course over ground
        gpscogformat='{0:03d}'.format(int(gpscog))
        gpscogformatfull='{0}°'.format(gpscogformat)

        #Format GPS fix
        if gpsfix==1:
          gpsfixformat='%{F#638057}[ FX ]%{F-}'
        else:
          gpsfixformat="%{F#805A57}[ NO ]%{F-}"

        #Format heading
        headingformat='{0:03d}'.format(int(heading))
        headingformatfull='{0}°'.format(headingformat)

        #Format clinometer (X axis)
        if str(clinox)[0] == "-":
          clinoxformat=int(float(str(clinox)[1:]))
          clinoxdir='starboard'
        else:
          clinoxformat=int(clinox)
          clinoxdir='port'
        if int(clinox) == 0:
          clinoxdir='none'
        clinoxformatfull='{0}°'.format(clinoxformat)

        #Format clinometer (Y axis)
        if str(clinoy)[0] == "-":
          clinoyformat=int(float(str(clinoy)[1:]))
          clinoydir='forward'
        else:
          clinoyformat=int(clinoy)
          clinoydir='backward'
        if int(clinoy) == 0:
          clinoydir='none'
        clinoyformatfull='{0}°'.format(clinoyformat)

        #Format barometric pressure
        baroformat='{0}'.format(int(baro/100))
        baroformatfull='{0} MBAR'.format(baroformat)

        #Format temperature
        temp1format='{0:.1f}'.format(float(temp1))
        temp1formatfull='{0}°C'.format(temp1format)
        temp2format='{0:.1f}'.format(float(temp2))
        temp2formatfull='{0}°C'.format(temp2format)
        temp3format='{0:.1f}'.format(float(temp3))
        temp3formatfull='{0}°C'.format(temp3format)

        #Format wind data
        windspdformat='{0:.1f}'.format(windspd)
        windspdformatfull='{0} MS'.format(windspdformat)
        winddirformat='{0:03d}'.format(int(winddir))
        winddirformatfull='{0}°'.format(winddirformat)
        windformatfull='{0} {1}'.format(winddirformatfull,windspdformatfull)

        #Format distance travelled
        distformat='{0:.1f}'.format((float(dist)+float(diststart)) * 0.000539956803)
        distformatfull='{0} NM'.format(distformat)

        #Format uptime
        uptimeformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptimeday, uptimehour, uptimemin)

        #Update LCD
        if (lcd_update==1):
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
          clino_lcd=('CLINO:')+('{0}'.format(clinoxformat)+chr(223)).rjust(14)
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
          lcd_update=0
        
        #Output data to conky
        if (conky_update==1):
          conkytext='$alignc CLINO: {CLINO} // HDG: {HDG} // LOG: {LOG} // WIND: {WIND} \n$alignc BARO: {BARO} // INSIDE: {INSIDE} // OUTSIDE: {OUTSIDE} // WATER: {WATER} '.format(HDG=headingformatfull,CLINO=clinoxformatfull,LOG=distformatfull,UPTIME=uptimeformatfull,INSIDE=temp1formatfull,OUTSIDE=temp2formatfull,WATER=temp3formatfull,BARO=baroformatfull,WIND=windformatfull)
          conkyfile = open(home_dir+'.conkytext.txt', 'w')
          conkyfile.writelines(conkytext)
          conkyfile.close()
          conky_update=0

        #Update ocs database
        if (gpsfix==1 and ocsdb_update==1):
          sqlite_file=ocsdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("UPDATE OCS SET TIME='{TIME}', LAT='{LAT}', LON='{LON}', SPD='{SPD}', SPD_MAX='{SPD_MAX}', COG='{COG}', HEADING='{HEADING}', UPTIME='{UPTIME}', UPTIME_MAX='{UPTIME_MAX}', DIST='{DIST}', BARO='{BARO}', BARO_MIN='{BARO_MIN}', BARO_MAX='{BARO_MAX}', TEMP1='{TEMP1}', TEMP1_MIN='{TEMP1_MIN}', TEMP1_MAX='{TEMP1_MAX}', TEMP2='{TEMP2}', TEMP2_MIN='{TEMP2_MIN}', TEMP2_MAX='{TEMP2_MAX}', TEMP3='{TEMP3}', TEMP3_MIN='{TEMP3_MIN}', TEMP3_MAX='{TEMP3_MAX}', CLINOX='{CLINOX}', CLINOX_MIN='{CLINOX_MIN}', CLINOX_MAX='{CLINOX_MAX}', CLINOY='{CLINOY}', CLINOY_MIN='{CLINOY_MIN}', CLINOY_MAX='{CLINOY_MAX}'".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,SPD_MAX=spdmax,COG=gpscog,HEADING=heading,UPTIME=int(uptime),UPTIME_MAX=int(uptimemax),DIST=dist,BARO=baro,BARO_MIN=baromin,BARO_MAX=baromax,TEMP1=temp1,TEMP1_MIN=temp1min,TEMP1_MAX=temp1max,TEMP2=temp2,TEMP2_MIN=temp2min,TEMP2_MAX=temp2max,TEMP3=temp3,TEMP3_MIN=temp3min,TEMP3_MAX=temp3max,CLINOX=clinox,CLINOX_MIN=clinoxmin,CLINOX_MAX=clinoxmax,CLINOY=clinoy,CLINOY_MIN=clinoymin,CLINOY_MAX=clinoymax))
          conn.commit()
          conn.close()
          ocsdb_update=0

        #Update GPS database
        if (gpsfix==1 and gpsdb_update==1):
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
            c.execute("INSERT INTO GPS ( TIME, LAT, LON, SPD, COG, HDG, CLINOX, CLINOY ) VALUES ( '{TIME}', '{LAT}', '{LON}', '{SPD}', '{COG}', '{HDG}', '{CLINOX}', '{CLINOY}')".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,COG=gpscog,HDG=heading,CLINOX=clinox,CLINOY=clinoy))
            conn.commit()
            conn.close()
            loglat=gpslat
            loglon=gpslon
            lognumfirst=0
          gpsdb_update=0

        #Update weather database
        if (weatherdb_update==1):
          sqlite_file=weatherdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("INSERT INTO WEATHER ( TIME, BARO, TEMP1, TEMP2, TEMP3, WINDDIR, WINDSPD ) VALUES ( '{TIME}', '{BARO}', '{TEMP1}', '{TEMP2}', '{TEMP3}', '{WINDDIR}', '{WINDSPD}')".format(TIME=currenttimestamp,BARO=baro,TEMP1=temp1,TEMP2=temp2,TEMP3=temp3,WINDDIR=winddir,WINDSPD=windspd))
          conn.commit()
          conn.close()
          weatherdb_update=0
        refreshtime=0
        
      #Print data
      print'%{c}',gpsfixformat,' TIME:',currenttime,' // LAT:',gpslatformatfull,' // LON:',gpslonformatfull,' // SPD:',gpsspdformatfull,' // COG:',gpscogformatfull,' ',gpsfixformat
      #print'time',currenttime,' - hdg:',headingformatfull,' - clinox:',clinoxformatfull,' - clinoy:',clinoyformatfull,' - x:',magx,' - y:',magy,' - z:',magz
      
      #Update time
      refreshtime+=0.5
      uptime+=0.5
      disttime+=0.5
      barotime+=0.5
      temptime+=0.5
      if gpsfix == 0:
        gpsfixtime+=0.5

      #Sleep
      time.sleep(0.5)

  except (SystemExit):
    gpsp.running = False
    gpsp.join()
    print'%{c}ERROR'
