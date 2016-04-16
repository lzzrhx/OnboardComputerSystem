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
import ephem

main_title='Onboard Computer System'

alarm=0

#Set starting number for total distance travelled (in meters)
setdiststart=925*1852

#Set temp sensor id
temp1name='28-0115905a2fff'                     #Inside temp
temp2name='28-0415901b95ff'                     #Outside temp
temp3name='28-01159066d4ff'                     #Water temp

#Set calibration values (in degrees)
headingcalibrate=(0)                            #Heading
clinoxcalibrate=(+3.0)                          #Clinometer X axis
clinoycalibrate=(-1.5)                          #Clinometer Y Axis

#Set minimum distance (in meters) for adding new entry to the location database
setlogdistmin=50

#Set values for calculating distance travelled
setdistmultiplier=1
setdisttime=setdistmultiplier*100
setdistprevmin=setdistmultiplier*5

#Set time values (in seconds)
setwaittime=5                                   #Wait before starting
setlcdtime_screen1=3*60                         #LCD screen 1
setlcdtime_screen2=30                           #LCD screen 2
setlcdtime_screen3=setlcdtime_screen2           #LCD screen 3
setconkytime=3                                  #Update Conky
setgpswaittime=2*60                             #Wait for gps at boot
settemptime=15*60                               #Update temperature
setbarotime=15*60                               #Update barometer

#Set directories
home_dir = os.path.expanduser('~') + '/'        #Home directory
ocs_dir = home_dir + '.OnboardComputerSystem/'  #Onboard Computer System directory
db_dir = home_dir + 'Databases/'                #Database directory

#Set database names
ocsdbname='ocs'                                 #OCS database
locationdbname='location'                       #Location log database
weatherdbname='weather'                         #Weather log database

#Set terminal title
sys.stdout.write('\x1b]2;'+main_title+'\x07')

#Database stuff
ocsdb_file = db_dir + ocsdbname + '.db'
locationdb_file = db_dir + locationdbname + '.db'
weatherdb_file = db_dir + weatherdbname + '.db'
ocsdbonline=os.path.isfile(ocsdb_file)
locationdbonline=os.path.isfile(locationdb_file)
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
    HDG            TEXT   NOT NULL,
    UPTIME         TEXT   NOT NULL,
    UPTIME_MAX     TEXT   NOT NULL,
    DIST           TEXT   NOT NULL,
    DIST_START     TEXT   NOT NULL,
    BARO           TEXT   NOT NULL,
    TEMP1          TEXT   NOT NULL,
    TEMP2          TEXT   NOT NULL,
    TEMP3          TEXT   NOT NULL,
    CLINOX         TEXT   NOT NULL,
    CLINOX_MIN     TEXT   NOT NULL,
    CLINOX_MAX     TEXT   NOT NULL,
    CLINOY         TEXT   NOT NULL,
    CLINOY_MIN     TEXT   NOT NULL,
    CLINOY_MAX     TEXT   NOT NULL,
    WINDDIR        TEXT   NOT NULL,
    WINDSPD        TEXT   NOT NULL,
    SUNRISE        TEXT   NOT NULL,
    SUNSET         TEXT   NOT NULL
    );""")
  c.execute("INSERT INTO OCS (ID, TIME, LAT, LON, SPD, SPD_MAX, COG, HDG, UPTIME, UPTIME_MAX, DIST, DIST_START, BARO, TEMP1, TEMP2, TEMP3, CLINOX, CLINOX_MIN, CLINOX_MAX, CLINOY, CLINOY_MIN, CLINOY_MAX, WINDDIR, WINDSPD, SUNSET, SUNRISE) VALUES (1, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00:00', '00:00')")
  conn.commit()
  conn.close()

#Create GPS log database
if locationdbonline is False:
  sqlite_file=locationdb_file
  conn=sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("""CREATE TABLE LOCATION(
    ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
    TIME           TEXT   NOT NULL,
    LAT            TEXT   NOT NULL,
    LON            TEXT   NOT NULL,
    SPD            TEXT   NOT NULL,
    COG            TEXT   NOT NULL,
    HDG            TEXT   NOT NULL,
    CLINOX         TEXT   NOT NULL,
    CLINOY         TEXT   NOT NULL,
    DIST           TEXT   NOT NULL
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
time.sleep(setwaittime)
temp1online=os.path.isfile(temp1device_file)
temp2online=os.path.isfile(temp2device_file)
temp3online=os.path.isfile(temp3device_file)

#Setup LCD (from https://github.com/adafruit/Adafruit_Python_CharLCD)
execfile(ocs_dir+'/lcd-boot.py')

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
spdmax=float(row[5])
uptimemax=float(row[9])
dist=float(row[10])
diststart=setdiststart
disttotal=dist+diststart
clinoxmin=float(row[17])
clinoxmax=str(row[18])
clinoymin=float(row[20])
clinoymax=str(row[21])
sunriseformat=str(row[24])
sunsetformat=str(row[25])
conn.commit()
conn.close()

#Set time values
start_time_values=1
start_gpsp=0
uptime=0
logfirst=1
ocsdb_update=0
ocsdb_update_lock = threading.Lock()
locationdb_update=0
locationdb_update_lock = threading.Lock()
weatherdb_update=0
weatherdb_update_lock = threading.Lock()
astronomy_update=0
astronomy_update_lock = threading.Lock()
class time_values(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global start_gpsp
    global uptime
    global ocsdb_update
    global locationdb_update
    global weatherdb_update
    global astronomy_update
    while True:
      if start_time_values==1:
        if (uptime>=setgpswaittime and datetime.now().strftime('%S')=='00'):
          ocsdb_update_lock.acquire()
          ocsdb_update=1
          ocsdb_update_lock.release()
        if (uptime>=setgpswaittime and (logfirst==1 or (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'))):
          locationdb_update_lock.acquire()
          locationdb_update=1
          locationdb_update_lock.release()
        if (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'):
          weatherdb_update_lock.acquire()
          weatherdb_update=1
          weatherdb_update_lock.release()
        if (uptime==0 or (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00')):
          astronomy_update_lock.acquire()
          astronomy_update=1
          astronomy_update_lock.release()
        uptime+=1
        if start_gpsp==0:
          start_gpsp=1
        sleep(1)

#Get GPS data
start_read_data=0
gpsd = None
class gpsp(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
  def run(self):
    global gpsd
    global start_read_data
    while gpsp.running:
      if start_gpsp==1:
        gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
        if start_read_data==0:
          start_read_data=1
        sleep(0.1)

#Read data
start_output_lcd=0
start_output_conky=0
start_output_data=0
start_update_databases=0
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
class read_data(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    disttime=0
    barotime=0
    temptime=0
    barotime=setbarotime
    temptime=settemptime
    gpsspd1=0
    gpsspd2=0
    gpsspd3=0
    distfirst=1
    global start_output_lcd
    global start_output_conky
    global start_output_data
    global start_update_databases
    global currenttimestamp
    global uptimemax
    global gpsfix
    global gpslat
    global gpslon
    global gpsspd
    global spdmax
    global gpscog
    global heading
    global clinox
    global clinoxmin
    global clinoxmax
    global clinoy
    global clinoymin
    global clinoymax
    global baro
    global temp1
    global temp2
    global temp3
    global dist
    global disttotal
    global sunriseformat
    global sunsetformat
    global astronomy_update
    global gpslatdir
    global gpslatdeg
    global gpslatdegformat
    global gpslatmin
    global gpslatminformat
    global gpslatformatfull
    global gpslondir
    global gpslondeg
    global gpslondegformat
    global gpslonmin
    global gpslonminformat
    global gpslonformatfull
    global gpsspdformat
    global gpsspdformatfull
    global gpscogformat
    global gpscogformatfull
    global gpsfixformat
    global headingformat
    global headingformatfull
    global clinoxformat
    global clinoxdir
    global clinoxformatfull
    global clinoyformat
    global clinoydir
    global clinoyformatfull
    global baroformat
    global baroformatfull
    global temp1format
    global temp1formatfull
    global temp2format
    global temp2formatfull
    global temp3format
    global temp3formatfull
    global windspdformat
    global windspdformatfull
    global winddirformat
    global winddirformatfull
    global windformatfull
    global distformat
    global distformatfull
    global uptimeformatfull
    while True:
      if start_read_data==1:
        #Time
        currenttimestamp=time.time()
        #Uptime
        if uptime > uptimemax:
          uptimemax=uptime
        #Read GPS data
        if math.isnan(gpsd.fix.mode) is False:
          if gpsd.fix.mode == 3:
            gpsfix=1
            if math.isnan(gpsd.fix.latitude) is False:
                gpslat=gpsd.fix.latitude
            if math.isnan(gpsd.fix.longitude) is False:
                gpslon=gpsd.fix.longitude
            if math.isnan(gpsd.fix.speed) is False:
                gpsspd3=gpsspd2
                gpsspd2=gpsspd1
                gpsspd1=gpsd.fix.speed
                gpsspd=(gpsspd1+gpsspd2+gpsspd3)/3
                if (uptime >= setgpswaittime and gpsspd > spdmax):
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
          heading = (180 * math.atan2(magycomp,magxcomp)/math.pi)+headingcalibrate
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
          clinox=accxdeg+clinoxcalibrate
          clinoy=accydeg+clinoycalibrate
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
          barotime=0
        barotime+=1
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
          temptime=0
        temptime+=1
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
            disttotal=dist+diststart
            disttime=0
          disttime+=1
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
        gpscogformat=int(gpscog)
        gpscogformatfull='{0}°'.format(gpscogformat)
        #Format GPS fix
        if gpsfix==1:
          gpsfixformat='%{F#638057}[ FX ]%{F-}'
        else:
          gpsfixformat="%{F#805A57}[ NO ]%{F-}"
        #Format heading
        headingformat=int(heading)
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
        winddirformat=int(winddir)
        winddirformatfull='{0}°'.format(winddirformat)
        windformatfull='{0} {1}'.format(winddirformatfull,windspdformatfull)
        #Format distance travelled
        distformat='{0:.1f}'.format((float(dist)+float(diststart)) * 0.000539956803)
        distformatfull='{0} NM'.format(distformat)
        #Format uptime
        uptimemin, uptimesec = divmod(uptime, 60)
        uptimehour, uptimemin = divmod(uptimemin, 60)
        uptimeday, uptimehour = divmod(uptimehour, 24)
        uptimeformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptimeday, uptimehour, uptimemin)
        #Calculate sunset/sunrise
        if (gpsfix==1 and astronomy_update==1):
          eph_observer=ephem.Observer()
          eph_observer.lat=str(gpslatdeg)
          eph_observer.long=str(gpslondeg)
          eph_sun=ephem.Sun()
          eph_sun.compute()
          sunrise=ephem.localtime(eph_observer.next_rising(eph_sun))
          sunset=ephem.localtime(eph_observer.next_setting(eph_sun))
          sunriseformat=sunrise.strftime('%H:%M')
          sunsetformat=sunset.strftime('%H:%M')
          astronomy_update_lock.acquire()
          astronomy_update=0
          astronomy_update_lock.release()
        if start_output_lcd==0:
          start_output_lcd=1
        if start_output_conky==0:
          start_output_conky=1
        if start_output_data==0:
          start_output_data=1
        if start_update_databases==0:
          start_update_databases=1
        sleep(1)

#Output data to LCD
class output_lcd(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    lcdtime=0
    while True:
      if start_output_lcd==1:
        sec_tenth=datetime.now().microsecond/100000
        if sec_tenth==0:
          if alarm==1:
            lcdscreen=0
          elif lcdtime <= setlcdtime_screen1:
            lcdscreen=1
          elif lcdtime <= setlcdtime_screen1+setlcdtime_screen2:
            lcdscreen=2
          elif lcdtime <= setlcdtime_screen1+setlcdtime_screen2+setlcdtime_screen3:
            lcdscreen=3
          else:
            lcdtime=0
          time_lcd='{TIME}'.format(TIME=datetime.now().strftime('%d.%m.%Y  %H:%M:%S'))
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
          #Alarm screen
          lcd_screen0_line1=' ------------------ '
          lcd_screen0_line2=' !!MASTER CAUTION!! '
          lcd_screen0_line3=' !!MASTER CAUTION!! '
          lcd_screen0_line4=' ------------------ '
          #LCD screen 1
          lcd_screen1_line1=time_lcd
          lcd_screen1_line2=lat_lcd
          lcd_screen1_line3=lon_lcd
          lcd_screen1_line4=spdcog_lcd
          #LCD screen 2
          lcd_screen2_line1=clino_lcd
          lcd_screen2_line2=heading_lcd
          lcd_screen2_line3=dist_lcd
          lcd_screen2_line4=wind_lcd
          #LCD screen 3
          lcd_screen3_line1=baro_lcd
          lcd_screen3_line2=temp1_lcd
          lcd_screen3_line3=temp2_lcd
          lcd_screen3_line4=temp3_lcd
          if lcdscreen == 0:
            lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen0_line1,line2=lcd_screen0_line2,line3=lcd_screen0_line3,line4=lcd_screen0_line4)
          elif lcdscreen == 1:
            lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen1_line1,line2=lcd_screen1_line2,line3=lcd_screen1_line3,line4=lcd_screen1_line4)
          elif lcdscreen == 2:
            lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen2_line1,line2=lcd_screen2_line2,line3=lcd_screen2_line3,line4=lcd_screen2_line4)
          elif lcdscreen == 3:          
            lcdtext='{line1}\n{line2}\n{line3}\n{line4}'.format(line1=lcd_screen3_line1,line2=lcd_screen3_line2,line3=lcd_screen3_line3,line4=lcd_screen3_line4)
          lcd.message(lcdtext)
          lcdtime+=1
          sleep(0.1)
        sleep(0.01)

#Output data to Conky
class output_conky(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    conkytime=0
    while True:
      if start_output_conky==1:
        if (conkytime >= setconkytime):
          conkytext='$alignc LAT: {LAT} // LON: {LON} '.format(LAT=gpslatformatfull,LON=gpslonformatfull)
          conkytext+='\n'
          conkytext+='$alignc CLINO: {CLINO} // HDG: {HDG} // LOG: {LOG} // WIND: {WIND} '.format(CLINO=clinoxformatfull,HDG=headingformatfull,LOG=distformatfull,WIND=windformatfull)
          conkytext+='\n'
          conkytext+='$alignc BARO: {BARO} // INSIDE: {INSIDE} // OUTSIDE: {OUTSIDE} // WATER: {WATER} '.format(BARO=baroformatfull,INSIDE=temp1formatfull,OUTSIDE=temp2formatfull,WATER=temp3formatfull)
          conkytext+='\n'
          conkytext+='$alignc SUNRISE: {SUNRISE} // SUNSET: {SUNSET} '.format(SUNRISE=sunriseformat,SUNSET=sunsetformat)
          conkyfile = open(home_dir+'.conkytext', 'w')
          conkyfile.writelines(conkytext)
          conkyfile.close()
          conkytime=0
        conkytime+=1
        sleep(1)

#Output data
class output_data(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global gpsfixformat
    while True:
      if start_output_data==1:
        currenttime=datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print'%{c}',gpsfixformat,' TIME:',currenttime,' // SPD:',gpsspdformatfull,' // COG:',gpscogformatfull,' ',gpsfixformat
        #print'TIME:',currenttime,' - HDG:',headingformatfull,' - CLINO(X):',clinox,' - CLINO(Y):',clinoy
        sleep(0.1)

#Update databases
class update_databases(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global logfirst
    global ocsdb_update
    global locationdb_update
    global weatherdb_update
    while True:
      if start_update_databases==1:
        #Update OCS database
        if (gpsfix==1 and ocsdb_update==1):
          sqlite_file=ocsdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("UPDATE OCS SET TIME='{TIME}', LAT='{LAT}', LON='{LON}', SPD='{SPD}', SPD_MAX='{SPD_MAX}', COG='{COG}', HDG='{HDG}', UPTIME='{UPTIME}', UPTIME_MAX='{UPTIME_MAX}', DIST_START='{DIST_START}', DIST='{DIST}', BARO='{BARO}', TEMP1='{TEMP1}', TEMP2='{TEMP2}', TEMP3='{TEMP3}', CLINOX='{CLINOX}', CLINOX_MIN='{CLINOX_MIN}', CLINOX_MAX='{CLINOX_MAX}', CLINOY='{CLINOY}', CLINOY_MIN='{CLINOY_MIN}', CLINOY_MAX='{CLINOY_MAX}', SUNRISE='{SUNRISE}', SUNSET='{SUNSET}'".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,SPD_MAX=spdmax,COG=gpscog,HDG=heading,UPTIME=int(uptime),UPTIME_MAX=int(uptimemax),DIST_START=diststart,DIST=dist,BARO=baro,TEMP1=temp1,TEMP2=temp2,TEMP3=temp3,CLINOX=clinox,CLINOX_MIN=clinoxmin,CLINOX_MAX=clinoxmax,CLINOY=clinoy,CLINOY_MIN=clinoymin,CLINOY_MAX=clinoymax,SUNRISE=sunriseformat,SUNSET=sunsetformat))
          conn.commit()
          conn.close()
          ocsdb_update_lock.acquire()
          ocsdb_update=0
          ocsdb_update_lock.release()
        #Update location database
        if (gpsfix==1 and locationdb_update==1):
          if (logfirst==1):
            logdistprev=0
            oldlognum=int(0)
            oldloglat=float(0)
            oldloglon=float(0)
            sqlite_file=locationdb_file
            conn=sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("SELECT count(*), LAT, LON FROM LOCATION ORDER BY ID DESC LIMIT 1")
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
            sqlite_file=locationdb_file
            conn=sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("INSERT INTO LOCATION ( TIME, LAT, LON, SPD, COG, HDG, CLINOX, CLINOY, DIST ) VALUES ( '{TIME}', '{LAT}', '{LON}', '{SPD}', '{COG}', '{HDG}', '{CLINOX}', '{CLINOY}', '{DIST}')".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,COG=gpscog,HDG=heading,CLINOX=clinox,CLINOY=clinoy,DIST=disttotal))
            conn.commit()
            conn.close()
            loglat=gpslat
            loglon=gpslon
            lognumfirst=0
          locationdb_update_lock.acquire()
          locationdb_update=0
          locationdb_update_lock.release()
        #Update weather database
        if (weatherdb_update==1):
          sqlite_file=weatherdb_file
          conn=sqlite3.connect(sqlite_file)
          c = conn.cursor()
          c.execute("INSERT INTO WEATHER ( TIME, BARO, TEMP1, TEMP2, TEMP3, WINDDIR, WINDSPD ) VALUES ( '{TIME}', '{BARO}', '{TEMP1}', '{TEMP2}', '{TEMP3}', '{WINDDIR}', '{WINDSPD}')".format(TIME=currenttimestamp,BARO=baro,TEMP1=temp1,TEMP2=temp2,TEMP3=temp3,WINDDIR=winddir,WINDSPD=windspd))
          conn.commit()
          conn.close()
          weatherdb_update_lock.acquire()
          weatherdb_update=0
          weatherdb_update_lock.release()
        sleep(1)

#Start everything
if __name__ == '__main__':
  time_values = time_values()
  time_values.start()
  gpsp = gpsp()
  gpsp.start()
  read_data = read_data()
  read_data.start()
  output_lcd = output_lcd()
  output_lcd.start()
  output_conky = output_conky()
  output_conky.start()
  output_data = output_data()
  output_data.start()
  update_databases = update_databases()
  update_databases.start()
