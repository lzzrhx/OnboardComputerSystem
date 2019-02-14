#! /usr/bin/python3
# -*- coding: utf-8 -*-





#Import shit
from gps import *
from time import time, sleep
from datetime import datetime, timedelta
from math import isnan
from os import path, system
from configparser import SafeConfigParser
import threading
import sqlite3
import ephem
import signal
import geopy.distance
import Adafruit_BMP.BMP085 as BMP085
import traceback





#Killer
class killer:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)
  def exit_gracefully(self,signum, frame):
    self.kill_now = True
killer = killer()





#Boot animation
boot_animation_stop=0
class boot_animation(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global boot_animation_stop
    boot_message='[  I N I T I A L I Z I N G   S Y S T E M  ]'
    while True:
      if killer.kill_now or error_raised is True or boot_animation_stop==1:
        boot_animation_stop=2
        break
      sys.stdout.write('%{c}'+boot_message+'\n')
      sleep(0.8)
      sys.stdout.write('\n')
      sleep(0.8)





#Error animation
error_animation_running=0
class error_animation(threading.Thread):
  def __init__(self,error_type=None):
    global error_message
    global default_error_message
    
    #Error messages
    default_error_message='[  S Y S T E M   F A I L U R E  ]'
    if error_type=='initialization': error_message='[  I N I T I A L I Z A T I O N   E R R O R  ]'
    elif error_type=='config': error_message='[  C O N F I G   F I L E   E R R O R  ]'
    elif error_type=='time values': error_message='[  T I M E   V A L U E S   E R R O R  ]'
    elif error_type=='gps': error_message='[  G P S   E R R O R  ]'
    elif error_type=='read data': error_message='[  R E A D   D A T A   E R R O R  ]'
    elif error_type=='baro': error_message='[  B A R O   S E N S O R   E R R O R  ]'
    elif error_type=='conky': error_message='[  C O N K Y   O U T P U T   E R R O R  ]'
    elif error_type=='statusbar': error_message='[  S T A T U S B A R   O U T P U T   E R R O R  ]'
    elif error_type=='update databases': error_message='[   D A T A B A S E   U P D A T E   E R R O R  ]'
    elif error_type=='alarm': error_message='[   A L A R M   S Y S T E M   E R R O R  ]'
    else: error_message='[  U N K N O W N   E R R O R  ]'
    
    threading.Thread.__init__(self)
  def run(self):
    global error_raised
    global error_animation_running
    error_raised=True
    error_animation_running=1
    while True:
      if killer.kill_now:
        break
      if boot_animation_stop==2:
        sys.stdout.write('%{c}'+default_error_message+'\n')
        sleep(0.8)
        sys.stdout.write('\n')
        sleep(0.8)
        sys.stdout.write('%{c}'+error_message+'\n')
        sleep(0.8)
        sys.stdout.write('\n')
      sleep(0.8)





#Alarm animation
start_alarm_animation=0
alarm_animation_running=False
class alarm_animation(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    global alarm_animation_running
    
    #Alarm messages
    default_alarm_message='[  M A S T E R   C A U T I O N  ]'
    alarm_message_anchor='[  A N C H O R   A L A R M  ]'
    alarm_message_cog='[  C O U R S E   A L A R M  ]'
    alarm_message_timezone='[  N E W   T I M E Z O N E   A L A R M  ]'
    alarm_message_time='[  T I M E   A L A R M  ]'
    alarm_message_dist='[  D I S T A N C E   T R A V E L L E D   A L A R M  ]'
    alarm_message_spdlow='[  L O W   S P E E D   A L A R M  ]'
    alarm_message_spdhigh='[ H I G H   S P E E D   A L A R M  ]'
    
    while True:
      if killer.kill_now or error_raised:
        break
      if start_alarm_animation==1:
        if alarm_system_activate is True and (alarm_anchor_raised is True or alarm_cog_raised is True or alarm_timezone_raised is True or alarm_time_raised is True or alarm_dist_raised is True or alarm_spdlow_raised is True or alarm_spdhigh_raised is True):
          if alarm_animation_running is False: alarm_animation_running=True
          sys.stdout.write('%{c}'+default_alarm_message+'\n')
          sleep(0.8)
          sys.stdout.write('\n')
          if alarm_anchor_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_anchor+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_anchor+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_cog_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_cog+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_cog+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_timezone_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_timezone+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_timezone+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_time_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_time+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_time+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_dist_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_dist+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_dist+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_spdlow_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_spdlow+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_spdlow+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
          if alarm_spdhigh_raised is True:
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_spdhigh+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
            sleep(0.8)
            sys.stdout.write('%{c}'+alarm_message_spdhigh+'\n')
            sleep(0.8)
            sys.stdout.write('\n')
        else:
          if alarm_animation_running is True: alarm_animation_running=False
      sleep(0.8)





#Initialization
error_raised=False
boot_animation().start()
try:

  #Set directories
  home_dir = path.expanduser('~') + '/'
  ocs_dir = home_dir + '.OnboardComputerSystem/'
  db_dir = ocs_dir + 'databases/'

  #Set time values (in seconds)
  set_waittime=5             #Wait before starting
  set_configtime=5          #Update data from config file
  set_conkytime=3            #Update Conky
  set_gpswaittime=30         #Wait for gps at boot

  #Set database names
  ocsdb_name='ocs-main'
  locationdb_name='ocs-location'
  weatherdb_name='ocs-weather'

  #Database stuff
  ocsdb_file = db_dir + ocsdb_name + '.db'
  locationdb_file = db_dir + locationdb_name + '.db'
  weatherdb_file = db_dir + weatherdb_name + '.db'
  ocsdb_online=path.isfile(ocsdb_file)
  locationdb_online=path.isfile(locationdb_file)
  weatherdb_online=path.isfile(weatherdb_file)

  #Create OCS database
  if ocsdb_online is False:
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
      SPD_AVG        TEXT   NOT NULL,
      SPD_AVG_COUNT  TEXT   NOT NULL,
      COG            TEXT   NOT NULL,
      UPTIME         TEXT   NOT NULL,
      UPTIME_MAX     TEXT   NOT NULL,
      DIST           TEXT   NOT NULL,
      DIST_START     TEXT   NOT NULL,
      BARO           TEXT   NOT NULL,
      TEMP1          TEXT   NOT NULL,
      TEMP2          TEXT   NOT NULL,
      SUNRISE        TEXT   NOT NULL,
      SUNSET         TEXT   NOT NULL,
      TZ             TEXT   NOT NULL,
      TZ_OFFSET      TEXT   NOT NULL
      );""")
    c.execute("INSERT INTO OCS (ID, TIME, LAT, LON, SPD, SPD_MAX, SPD_AVG, SPD_AVG_COUNT, COG, UPTIME, UPTIME_MAX, DIST, DIST_START, BARO, TEMP1, TEMP2, SUNSET, SUNRISE, TZ, TZ_OFFSET) VALUES (1, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '00:00', '00:00', 'Z', '0')")
    conn.commit()
    conn.close()

  #Create location database
  if locationdb_online is False:
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
      DIST           TEXT   NOT NULL
      );""")
    conn.commit()
    conn.close()
    
  #Create weather database
  if weatherdb_online is False:
    sqlite_file=weatherdb_file
    conn=sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute("""CREATE TABLE WEATHER(
      ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
      TIME           TEXT   NOT NULL,
      BARO           TEXT   NOT NULL,
      TEMP1          TEXT   NOT NULL,
      TEMP2          TEXT   NOT NULL
      );""")
    conn.commit()
    conn.close()

  #Wait
  sleep(set_waittime)

  #Prepare for temperature sensors
  system('sudo modprobe w1-gpio')
  system('sudo modprobe w1-therm')
  temp_base_dir = '/sys/bus/w1/devices/'

  #Get old data
  sqlite_file=ocsdb_file
  conn=sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("SELECT * FROM OCS")
  row=c.fetchone()
  spdmax=float(row[5])
  spdavg=float(row[6])
  spdavgcount=float(row[7])
  uptimemax=float(row[10])
  dist=float(row[11])
  sunriseformat=str(row[16])
  sunsetformat=str(row[17])
  nauticaltimezone=str(row[18])
  nauticaltimeoffset=int(row[19])
  conn.commit()
  conn.close()

#Error handling
except:
  traceback.print_exc()
  if error_animation_running==0: error_animation('initialization').start()





#Read config file
start_read_config=1
start_time_values=0
class read_config(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      configtime=set_configtime
      global start_time_values
      global utcoffset_nauticaltimezone
      global utcoffset
      global dist_start
      global set_logdistmin
      global set_disttime
      global set_distmin
      global set_temptime
      global set_barotime
      global temp1device_file
      global temp2device_file
      global temp1_online
      global temp2_online
      global baro_online
      global baro_sensor
      global spdavg_min
      global conklyline1_selected
      global conklyline2_selected
      global conklyline3_selected
      global conklyline4_selected
      global conklyline5_selected
      global conklyline6_selected
      global barounit_mmhg
      global tempunit_fahrenheit
      global dateformat_mmddyyy
      global spdmax_show
      global spdavg_reset
      global spdmax_reset
      global dist_reset
      global alarm_system_activate
      global alarm_anchor_active
      global set_alarm_anchor_updatetime
      global set_alarm_anchor_distance
      global alarm_cog_active
      global alarm_cog_speed
      global alarm_cog_min
      global alarm_cog_max
      global alarm_timezone_active
      global alarm_time_active
      global alarm_time_value
      global alarm_dist_active
      global alarm_dist_value
      global alarm_spdlow_active
      global alarm_spdlow_req
      global alarm_spdlow_value
      global alarm_spdhigh_active
      global alarm_spdhigh_value
      spdavg_reset=False
      spdmax_reset=False
      dist_reset=False
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_read_config==1:
          if (configtime >= set_configtime):
          
            #Read config file
            config = SafeConfigParser()
            config.optionxform = lambda option: option
            config.read(ocs_dir+'OnboardComputerSystem.conf')
            
            #UTC offset
            utcoffset_nauticaltimezone=config.getboolean('Config', 'UseNauticalTimezone')
            utcoffset=str(config.get('Config', 'UtcOffset'))
            
            #Set starting number for total distance travelled (in nautical miles)
            set_dist_start=int(config.get('Config', 'DistanceStart'))
            dist_start=float(set_dist_start*1852)
            
            #Set minimum distance (in meters) for adding new entry to the location database
            set_logdistmin=int(config.get('Config', 'LogEntryMinDistance'))
            
            #Set values for calculating distance travelled
            set_disttime=int(config.get('Config', 'DistUpdateInterval'))
            set_distmin=float(config.get('Config', 'DistUpdateDistance'))
            
            #Set time values (in seconds)
            set_temptime=int(config.get('Config', 'TempUpdateInterval'))*60        #Update temperature
            set_barotime=int(config.get('Config', 'BaroUpdateInterval'))*60        #Update barometer
            
            #Set id & setup temp sensors
            temp1name=config.get('Config', 'TempInside')                           #Inside temp
            temp2name=config.get('Config', 'TempOutside')                          #Outside temp
            temp1device_folder = temp_base_dir + temp1name
            temp2device_folder = temp_base_dir + temp2name
            temp1device_file = temp1device_folder + '/w1_slave'
            temp2device_file = temp2device_folder + '/w1_slave'
            temp1_online=path.isfile(temp1device_file)
            temp2_online=path.isfile(temp2device_file)
            
            #Enable/disable barometer
            baro_online=config.getboolean('Config', 'BaroConnected')
            try:
              if baro_online is True: baro_sensor = BMP085.BMP085()
            #Error handling
            except:
              traceback.print_exc()
              if error_animation_running==0: error_animation('baro').start()
            
            #Minimum speed required for recording average speed
            spdavg_min=float(config.get('Config', 'SpdAvgReqMin'))
            
            #Set conky content
            conklyline1_selected=int(config.get('Config', 'ConkyLine1'))
            conklyline2_selected=int(config.get('Config', 'ConkyLine2'))
            conklyline3_selected=int(config.get('Config', 'ConkyLine3'))
            conklyline4_selected=int(config.get('Config', 'ConkyLine4'))
            conklyline5_selected=int(config.get('Config', 'ConkyLine5'))
            conklyline6_selected=int(config.get('Config', 'ConkyLine6'))
            
            #Set units
            dateformat_mmddyyy=config.getboolean('Config', 'DateMonthDayYear')
            barounit_mmhg=config.getboolean('Config', 'BaroUnitMmhg')
            tempunit_fahrenheit=config.getboolean('Config', 'TempUnitFahrenheit')
            
            #Show/hide max speed
            spdmax_show=config.getboolean('Config', 'ShowMaxSpd')
            
            #Alarm system
            alarm_system_activate=config.getboolean('Config', 'AlarmSystemActivate')
            alarm_anchor_active=config.getboolean('Config', 'AlarmAnchorActivate')
            set_alarm_anchor_updatetime=int(config.get('Config', 'AlarmAnchorInterval'))
            set_alarm_anchor_distance=float(config.get('Config', 'AlarmAnchorDistance'))
            alarm_cog_active=config.getboolean('Config', 'AlarmCourseActivate')
            alarm_cog_speed=float(config.get('Config', 'AlarmCourseSpeed'))
            alarm_cog_min=float(config.get('Config', 'AlarmCourseMin'))
            alarm_cog_max=float(config.get('Config', 'AlarmCourseMax'))
            if alarm_cog_max < alarm_cog_min: alarm_cog_max+=360
            alarm_timezone_active=config.getboolean('Config', 'AlarmTimezoneActivate')
            alarm_time_active=config.getboolean('Config', 'AlarmTimeActivate')
            alarm_time_value=str(config.get('Config', 'AlarmTimeValue'))
            alarm_dist_active=config.getboolean('Config', 'AlarmDistanceActivate')
            alarm_dist_value=int(config.get('Config', 'AlarmDistanceValue'))
            alarm_spdlow_active=config.getboolean('Config', 'AlarmSpeedLowActivate')
            alarm_spdlow_req=int(config.get('Config', 'AlarmSpeedLowRequired'))
            alarm_spdlow_value=int(config.get('Config', 'AlarmSpeedLowValue'))
            alarm_spdhigh_active=config.getboolean('Config', 'AlarmSpeedHighActivate')
            alarm_spdhigh_value=int(config.get('Config', 'AlarmSpeedHighValue'))
            
            #Reset average speed
            if config.getboolean('Config', 'SpdAvgReset') is True:
              config.set('Config', 'SpdAvgReset', 'False')
              with open(ocs_dir+'OnboardComputerSystem.conf', 'w') as configfile:
                config.write(configfile)
              spdavg_reset=True
            
            #Reset max speed
            if config.getboolean('Config', 'SpdMaxReset') is True:
              config.set('Config', 'SpdMaxReset', 'False')
              with open(ocs_dir+'OnboardComputerSystem.conf', 'w') as configfile:
                config.write(configfile)
              spdmax_reset=True
            
            #Reset distance travelled
            if config.getboolean('Config', 'DistanceReset') is True:
              config.set('Config', 'DistanceReset', 'False')
              with open(ocs_dir+'OnboardComputerSystem.conf', 'w') as configfile:
                config.write(configfile)
              dist_reset=True
              
            configtime=0
          if start_time_values==0:
            start_time_values=1
          configtime+=1
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('config').start()





#Set time values
start_gpsp=0
uptime=0
logfirst=1
astronomyfirst=1
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
    try:
      global start_gpsp
      global uptime
      global ocsdb_update
      global locationdb_update
      global weatherdb_update
      global astronomy_update
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_time_values==1:
          
          #Update OCS database
          if (uptime>=set_gpswaittime and datetime.now().strftime('%S')=='00'):
            ocsdb_update_lock.acquire()
            ocsdb_update=1
            ocsdb_update_lock.release()
          
          #Update location database
          if (uptime>=set_gpswaittime and datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'):
            locationdb_update_lock.acquire()
            locationdb_update=1
            locationdb_update_lock.release()
          
          #Update weather database
          if (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00'):
            weatherdb_update_lock.acquire()
            weatherdb_update=1
            weatherdb_update_lock.release()
          
          #Update astronomy
          if (uptime==0 or (datetime.now().strftime('%M')=='00' and datetime.now().strftime('%S')=='00')):
            astronomy_update_lock.acquire()
            astronomy_update=1
            astronomy_update_lock.release()
          
          uptime+=1
          if start_gpsp==0:
            start_gpsp=1
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('time values').start()





#GPS
start_read_data=0
gpsd = None
class gpsp(threading.Thread):
  def __init__(self):
    try:
      threading.Thread.__init__(self)
      global gpsd #bring it in scope
      gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
      self.current_value = None
      self.running = True #setting the thread running to true
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('gps').start()
  def run(self):
    try:
      global gpsd
      global start_read_data
      while self.running:
        if killer.kill_now or error_raised is True:
          break
        if start_gpsp==1:
          gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
          if start_read_data==0:
            start_read_data=1
        sleep(0.1)
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('gps').start()





#Read & format all data
gpstime=float(0)
gpslat=float(0)
gpslon=float(0)
gpsspd=float(0)
gpscog=float(0)
baro=float(0)
temp1=float(0)
temp2=float(0)
class read_data(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      disttime=0
      barotime=set_barotime
      temptime=set_temptime
      gpsspd1=0
      gpsspd2=0
      gpsspd3=0
      gpscog1=0
      gpscog2=0
      gpscog3=0
      distfirst=1
      global start_update_databases
      global start_alarm_system
      global uptimemax
      global utcoffsethours
      global utcoffsetminutes
      global utcoffsetformat
      global gpsfix
      global gpstime
      global gpslat
      global gpslon
      global gpsspd
      global spdmax
      global spdavg
      global spdavgcount
      global gpscog
      global baro
      global temp1
      global temp2
      global dist
      global disttotal
      global sunriseformat
      global sunsetformat
      global nauticaltimezone
      global nauticaltimeoffset
      global nauticaltimezoneformat
      global astronomy_update
      global astronomyfirst
      global gpsdatetimeformat
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
      global spdavgformatfull
      global spdmaxformatfull
      global gpscogformat
      global gpscogformatfull
      global gpsfixformat
      global baroformat
      global baroformatfull
      global temp1format
      global temp1formatfull
      global temp2format
      global temp2formatfull
      global distformat
      global distformatfull
      global uptimeformatfull
      global spdavg_reset
      global spdmax_reset
      global dist_reset
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_read_data==1:
          
          #Uptime
          if uptime > uptimemax:
            uptimemax=uptime
          
          #Reset average speed
          if spdavg_reset is True:
            spdavg=0
            spdavgcount=0
            spdavg_reset=False
          
          #Reset max speed
          if spdmax_reset is True:
            spdmax=0
            spdmax_reset=False
          
          #Reset distance
          if dist_reset is True:
            dist=0
            dist_reset=False
          
          #Read GPS data
          if isnan(gpsd.fix.mode) is False:
            if gpsd.fix.mode == 3:
              gpsfix=1
              if gpsd.utc is not None:
                  gpstime=gpsd.utc
              if isnan(gpsd.fix.latitude) is False:
                  gpslat=gpsd.fix.latitude
              if isnan(gpsd.fix.longitude) is False:
                  gpslon=gpsd.fix.longitude
              if isnan(gpsd.fix.speed) is False:
                  gpsspd3=gpsspd2
                  gpsspd2=gpsspd1
                  gpsspd1=gpsd.fix.speed
                  gpsspd=float((gpsspd1+gpsspd2+gpsspd3)/3)
                  if gpsspd>= (spdavg_min*1.9438444924574):
                    spdavg=((spdavg*spdavgcount)+gpsspd)/(spdavgcount+1)
                    spdavgcount+=1
                  if (uptime >= set_gpswaittime and gpsspd > spdmax):
                    spdmax=gpsspd
              if isnan(gpsd.fix.track) is False:
                  gpscog3=gpscog2
                  gpscog2=gpscog1
                  gpscog1=gpsd.fix.track
                  gpscog=float((gpscog1+gpscog2+gpscog3)/3)
            else:
              gpsfix=0
          
          #Read barometric pressure
          if (baro_online is True and barotime >= set_barotime):
            #baro_temp=baro_sensor.read_temperature()
            baro=float(baro_sensor.read_pressure())
            barotime=0
          barotime+=1
          
          #Read temperature
          if (temptime >= set_temptime):
            #Temperature sensor #1
            if temp1_online is True:
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
            if temp2_online is True:
              temp2f = open(temp2device_file, 'r')
              temp2flines = temp2f.readlines()
              temp2f.close()
              if temp2flines[0].strip()[-3:] == 'YES':
                  temp2equals_pos = temp2flines[1].find('t=')
                  if temp2equals_pos != -1:
                    temp2_string = temp2flines[1][temp2equals_pos+2:]
                    if (int(float(temp2_string)/1000.0)) != 85:
                      temp2 = float(temp2_string) / 1000.0
            temptime=0
          temptime+=1
          
          #Calculate distance travelled
          if (gpsfix==1 and uptime>=set_gpswaittime):
            if (distfirst==1):
              distlat=gpslat
              distlon=gpslon
              distfirst=0
            if (disttime >= set_disttime):
              distprev=geopy.distance.geodesic((distlat, distlon), (gpslat, gpslon)).m
              if distprev > set_distmin:
                  distlat=gpslat
                  distlon=gpslon
                  dist=dist+distprev
              disttime=0
            disttime+=1
          disttotal=dist+dist_start
          
          #Format GPS time
          gpsdatetimeformat='00.00.0000 00:00:00'
          if (gpsfix==1):
            gpstimesplit=str(gpstime).split('T')
            gpsdatetime=datetime.strptime(str(gpstimesplit[0])+' '+str(gpstimesplit[1])[:8], '%Y-%m-%d %H:%M:%S')
            gpsdatetimeformat=gpsdatetime.strftime('%d.%m.%Y %H:%M:%S')
          
          #UTC offset
          if utcoffset_nauticaltimezone is False:
            utcoffsetposneg=str(utcoffset[0:1])
            utcoffsethours=int(utcoffset[1:3])
            utcoffsetminutes=int(utcoffset[-2:])
            if utcoffsetposneg == '-':
              utcoffsethours=int('-'+str(utcoffsethours))
              utcoffsetminutes=int('-'+str(utcoffsetminutes))
            utcoffsetformat='UTC{0}'.format(utcoffset)
          
          #Nautical timezones (without accurate date line)
          if (gpsfix==1 and uptime>=set_gpswaittime):
            if -7.5 <= gpslon <= 7.5:
              nauticaltimezone='Z'
              nauticaltimeoffset=0
            elif 7.5 <= gpslon <= 22.5:
              nauticaltimezone='A'
              nauticaltimeoffset=int(-1)
            elif 22.5 <= gpslon <= 37.5:
              nauticaltimezone='B'
              nauticaltimeoffset=int(-2)
            elif 37.5 <= gpslon <= 52.5:
              nauticaltimezone='C'
              nauticaltimeoffset=int(-3)
            elif 52.5 <= gpslon <= 67.5:
              nauticaltimezone='D'
              nauticaltimeoffset=int(-4)
            elif 67.5 <= gpslon <= 82.5:
              nauticaltimezone='E'
              nauticaltimeoffset=int(-5)
            elif 82.5 <= gpslon <= 97.5:
              nauticaltimezone='F'
              nauticaltimeoffset=int(-6)
            elif 97.5 <= gpslon <= 112.5:
              nauticaltimezone='G'
              nauticaltimeoffset=int(-7)
            elif 112.5 <= gpslon <= 127.5:
              nauticaltimezone='H'
              nauticaltimeoffset=int(-8)
            elif 127.5 <= gpslon <= 142.5:
              nauticaltimezone='I'
              nauticaltimeoffset=int(-9)
            elif 142.5 <= gpslon <= 157.5:
              nauticaltimezone='K'
              nauticaltimeoffset=int(-10)
            elif 157.5 <= gpslon <= 172.5:
              nauticaltimezone='L'
              nauticaltimeoffset=int(-11)
            elif 172.5 <= gpslon <= 180.0:
              nauticaltimezone='M'
              nauticaltimeoffset=int(-12)
            elif -22.5 <= gpslon <= -7.5:
              nauticaltimezone='N'
              nauticaltimeoffset=int(1)
            elif -37.5 <= gpslon <= -22.5:
              nauticaltimezone='O'
              nauticaltimeoffset=int(2)
            elif -52.5 <= gpslon <= -37.5:
              nauticaltimezone='P'
              nauticaltimeoffset=int(3)
            elif -67.5 <= gpslon <= -52.5:
              nauticaltimezone='Q'
              nauticaltimeoffset=int(4)
            elif -82.5 <= gpslon <= -67.5:
              nauticaltimezone='R'
              nauticaltimeoffset=int(5)
            elif -97.5 <= gpslon <= -82.5:
              nauticaltimezone='S'
              nauticaltimeoffset=int(6)
            elif -112.5 <= gpslon <= -97.5:
              nauticaltimezone='T'
              nauticaltimeoffset=int(7)
            elif -127.5 <= gpslon <= -112.5:
              nauticaltimezone='U'
              nauticaltimeoffset=int(8)
            elif -142.5 <= gpslon <= -127.5:
              nauticaltimezone='V'
              nauticaltimeoffset=int(9)
            elif -157.5 <= gpslon <= -142.5:
              nauticaltimezone='W'
              nauticaltimeoffset=int(10)
            elif -172.5 <= gpslon <= -157.5:
              nauticaltimezone='X'
              nauticaltimeoffset=int(11)
            elif -180.0 <= gpslon <= -172.5:
              nauticaltimezone='Y'
              nauticaltimeoffset=int(12)
          nauticaltimezoneformat='{0} (UT'.format(nauticaltimezone)
          nauticaltimezoneformat+='{0:+03d}'.format(nauticaltimeoffset)
          nauticaltimezoneformat+=')'
          if utcoffset_nauticaltimezone is True:
            utcoffsethours=nauticaltimeoffset*-1
            utcoffsetminutes=0
            utcoffsetformat='UTC{0:+03d}:{1:02d}'.format(utcoffsethours,utcoffsetminutes)
          
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
          gpslatformatfull='{0}° {1:06.3f}\'{2}'.format(gpslatdeg,float(gpslatmin),gpslatdir)
          
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
          gpslonformatfull='{0}° {1:06.3f}\'{2}'.format(gpslondeg,float(gpslonmin),gpslondir)
          
          #Format speed
          gpsspdformat='{0:.1f}'.format((gpsspd * 1.9438444924574))
          gpsspdformatfull='{0} KN'.format(gpsspdformat)
          
          #Format average speed
          spdavgformat='{0:.1f}'.format((spdavg * 1.9438444924574))
          spdavgformatfull='{0} KN'.format(spdavgformat)
          
          #Format max speed
          spdmaxformat='{0:.1f}'.format((spdmax * 1.9438444924574))
          spdmaxformatfull='{0} KN'.format(spdmaxformat)
          
          #Format course over ground
          gpscogformat=int(gpscog)
          gpscogformatfull='{0:03d}°'.format(gpscogformat)
          
          #Format GPS fix
          if gpsfix==1:
            gpsfixformat='%{F#638057}[ FX ]%{F-}'
          else:
            gpsfixformat="%{F#805A57}[ NO ]%{F-}"
          
          #Format barometric pressure
          if barounit_mmhg is True:
            baroformat='{0}'.format(int((baro/100)*0.750061683))
            baroformatfull='{0} mmHg'.format(baroformat)
          else:
            baroformat='{0}'.format(int(baro/100))
            baroformatfull='{0} MBAR'.format(baroformat)
          if baro_online is False:
            baroformatfull='-'
          
          #Format temperature
          if tempunit_fahrenheit is True:
            temp1format='{0:.1f}'.format((float(temp1)*1.8)+32)
            temp1formatfull='{0}°F'.format(temp1format)
            temp2format='{0:.1f}'.format((float(temp2)*1.8)+32)
            temp2formatfull='{0}°F'.format(temp2format)
          else:
            temp1format='{0:.1f}'.format(float(temp1))
            temp1formatfull='{0}°C'.format(temp1format)
            temp2format='{0:.1f}'.format(float(temp2))
            temp2formatfull='{0}°C'.format(temp2format)
          if temp1_online is False:
            temp1formatfull='-'
          if temp2_online is False:
            temp2formatfull='-'
          
          #Format distance travelled
          distformat='{0:.2f}'.format(disttotal*0.000539956803)
          distformatfull='{0} NM'.format(distformat)
          
          #Format uptime
          uptimemin, uptimesec = divmod(uptime, 60)
          uptimehour, uptimemin = divmod(uptimemin, 60)
          uptimeday, uptimehour = divmod(uptimehour, 24)
          uptimeformatfull='{0:02d}D {1:02d}H {2:02d}M'.format(uptimeday,uptimehour,uptimemin)
          
          #Calculate sunset/sunrise
          if (gpsfix==1 and astronomy_update==1):
            astronomy=ephem.Observer()
            astronomy.lat=str(gpslatdeg)
            astronomy.long=str(gpslondeg)
            astronomy.date=datetime.utcnow().strftime("%Y/%m/%d 00:00:00")
            astronomy.elev=0
            astronomy.pressure=0
            astronomy.horizon='-0:34'       
            sunrise=astronomy.next_rising(ephem.Sun())
            sunset=astronomy.next_setting(ephem.Sun())
            astronomy_update_lock.acquire()
            astronomy_update=0
            astronomy_update_lock.release()
            if astronomyfirst==1:
              astronomyfirst=0
          if astronomyfirst==0:
            sunriseformat=(sunrise.datetime()+timedelta(hours=utcoffsethours,minutes=utcoffsetminutes)).strftime('%H:%M')
            sunsetformat=(sunset.datetime()+timedelta(hours=utcoffsethours,minutes=utcoffsetminutes)).strftime('%H:%M')
          if start_update_databases==0:
            start_update_databases=1
          if start_alarm_system==0:
            start_alarm_system=1
          
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('read data').start()





#Update databases
start_update_databases=0
class update_databases(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      global logfirst
      global ocsdb_update
      global locationdb_update
      global weatherdb_update
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_update_databases==1:
          currenttimestamp=time()
          
          #Update OCS database
          if (gpsfix==1 and ocsdb_update==1):
            sqlite_file=ocsdb_file
            conn=sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("UPDATE OCS SET TIME='{TIME}', LAT='{LAT}', LON='{LON}', SPD='{SPD}', SPD_MAX='{SPD_MAX}', SPD_AVG='{SPD_AVG}', SPD_AVG_COUNT='{SPD_AVG_COUNT}', COG='{COG}', UPTIME='{UPTIME}', UPTIME_MAX='{UPTIME_MAX}', DIST_START='{DIST_START}', DIST='{DIST}', BARO='{BARO}', TEMP1='{TEMP1}', TEMP2='{TEMP2}', SUNRISE='{SUNRISE}', SUNSET='{SUNSET}', TZ='{TZ}', TZ_OFFSET='{TZ_OFFSET}'".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,SPD_MAX=spdmax,SPD_AVG=spdavg,SPD_AVG_COUNT=spdavgcount,COG=gpscog,UPTIME=int(uptime),UPTIME_MAX=int(uptimemax),DIST_START=dist_start,DIST=dist,BARO=baro,TEMP1=temp1,TEMP2=temp2,SUNRISE=sunriseformat,SUNSET=sunsetformat,TZ=nauticaltimezone,TZ_OFFSET=nauticaltimeoffset))
            conn.commit()
            conn.close()
            ocsdb_update_lock.acquire()
            ocsdb_update=0
            ocsdb_update_lock.release()
          
          #Update GPS database
          if (gpsfix==1 and locationdb_update==1):
            if (logfirst==1):
              logdistprev=float(0)
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
              logdistprev=geopy.distance.geodesic((loglat, loglon), (gpslat, gpslon)).m            
            if (lognumfirst == 1) or (logdistprev > set_logdistmin):
              sqlite_file=locationdb_file
              conn=sqlite3.connect(sqlite_file)
              c = conn.cursor()
              c.execute("INSERT INTO LOCATION ( TIME, LAT, LON, SPD, COG, DIST ) VALUES ( '{TIME}', '{LAT}', '{LON}', '{SPD}', '{COG}', '{DIST}')".format(TIME=currenttimestamp,LAT=gpslat,LON=gpslon,SPD=gpsspd,COG=gpscog,DIST=disttotal))
              conn.commit()
              conn.close()
              loglat=gpslat
              loglon=gpslon
              lognumfirst=0
            locationdb_update_lock.acquire()
            locationdb_update=0
            locationdb_update_lock.release()
          
          #Update weather database
          if (baro_online is True and temp1_online is True and temp2_online is True and weatherdb_update==1):
            sqlite_file=weatherdb_file
            conn=sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("INSERT INTO WEATHER ( TIME, BARO, TEMP1, TEMP2 ) VALUES ( '{TIME}', '{BARO}', '{TEMP1}', '{TEMP2}')".format(TIME=currenttimestamp,BARO=baro,TEMP1=temp1,TEMP2=temp2))
            conn.commit()
            conn.close()
            weatherdb_update_lock.acquire()
            weatherdb_update=0
            weatherdb_update_lock.release()
          
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('update databases').start()





#Alarm system
alarm_anchor_raised=False
alarm_cog_raised=False
alarm_timezone_raised=False
alarm_time_raised=False
alarm_dist_raised=False
alarm_spdlow_raised=False
alarm_spdhigh_raised=False
start_alarm_system=0
class alarm_system(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      global alarm_anchor_raised
      global alarm_cog_raised
      global alarm_timezone_raised
      global alarm_time_raised
      global alarm_dist_raised
      global alarm_spdlow_raised
      global alarm_spdhigh_raised
      global alarmformat
      global start_output_conky
      global start_output_data
      global start_alarm_animation
      alarm_anchor_first=True
      alarm_timezone_first=True
      alarm_anchor_time=0
      while True:
        if killer.kill_now or error_raised is True:
          break
        
        #Active alarm system
        if start_alarm_system==1:
          if alarm_system_activate is True:
            alarmformat='[ALARM SYSTEM ACTIVE]'
            
            #Anchor alarm
            if alarm_anchor_active is True:
              if gpsfix==1:
                if alarm_anchor_first is True:
                  alarm_anchor_lat=gpslat
                  alarm_anchor_lon=gpslon
                  alarm_anchor_first=False
                if alarm_anchor_time>=set_alarm_anchor_updatetime:
                  alarm_anchor_prev_dist=geopy.distance.geodesic((alarm_anchor_lat, alarm_anchor_lon), (gpslat, gpslon)).m
                  if alarm_anchor_prev_dist > set_alarm_anchor_distance:
                    alarm_anchor_raised=True
                  elif alarm_anchor_raised is True: alarm_anchor_raised=False
                  alarm_anchor_time=0
                alarm_anchor_time+=1
            else:
              if alarm_anchor_raised is True: alarm_anchor_raised=False
              if alarm_anchor_first is False: alarm_anchor_first=True
              
            #Course alarm
            if alarm_cog_active is True:
              if gpsfix==1 and gpsspd>=(alarm_cog_speed*1.9438444924574):
                alarm_cog_value=int(gpscog)
                if alarm_cog_value < alarm_cog_min: alarm_cog_value += 360
                if alarm_cog_min!=alarm_cog_max and (alarm_cog_value<alarm_cog_min or alarm_cog_value>alarm_cog_max):
                  alarm_cog_raised=True
                elif alarm_cog_raised is True: alarm_cog_raised=False
            elif alarm_cog_raised is True: alarm_cog_raised=False
            
            #Distance alarm
            if alarm_dist_active is True:
              if gpsfix==1:
                if int(disttotal*0.000539956803)>=alarm_dist_value:
                  alarm_dist_raised=True
                elif alarm_dist_raised is True: alarm_dist_raised=False
            elif alarm_dist_raised is True: alarm_dist_raised=False
            
            #Low speed alarm
            if alarm_spdlow_active is True:
              if gpsfix==1:
                if int(gpsspd*1.9438444924574)>=alarm_spdlow_req and int(gpsspd*1.9438444924574)<=alarm_spdlow_value:
                  alarm_spdlow_raised=True
                elif alarm_spdlow_raised is True: alarm_spdlow_raised=False
            elif alarm_spdlow_raised is True: alarm_spdlow_raised=False
            
            #High speed alarm
            if alarm_spdhigh_active is True:
              if gpsfix==1:
                if int(gpsspd*1.9438444924574)>=alarm_spdhigh_value:
                  alarm_spdhigh_raised=True
                elif alarm_spdhigh_raised is True: alarm_spdhigh_raised=False
            elif alarm_spdhigh_raised is True: alarm_spdhigh_raised=False
            
            #Time alarm
            if alarm_time_active is True:
              if gpsfix==1 and alarm_time_raised is False:
                if alarm_time_value==str((datetime.utcnow()+timedelta(hours=utcoffsethours,minutes=utcoffsetminutes)).strftime('%H:%M')):
                  alarm_time_raised=True
            elif alarm_time_raised is True: alarm_time_raised=False
            
            #Timezone alarm
            if alarm_timezone_active is True:
              if gpsfix==1 and alarm_timezone_raised is False:
                if alarm_timezone_first is True:
                  alarm_timezone_old=nauticaltimezone
                  alarm_timezone_first=False
                if alarm_timezone_old!=nauticaltimezone:
                  alarm_timezone_raised=True
            elif alarm_timezone_raised is True: alarm_timezone_raised=False
          
          #Inactive alarm system
          else:
            alarmformat='[ALARM SYSTEM INACTIVE]'
          
          if start_alarm_animation==0:
            start_alarm_animation=1
          if start_output_conky==0:
            start_output_conky=1
          if start_output_data==0:
            start_output_data=1
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('alarm').start()





#Output data to Conky
start_output_conky=0
class output_conky(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      conkytime=0
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_output_conky==1:
          if (conkytime >= set_conkytime):
            
            #Conky lines
            conkyline_uptime='UPTIME: '+uptimeformatfull
            conkyline_astronomy='SUNRISE: '+sunriseformat+'  //  SUNSET: '+sunsetformat
            conkyline_weather='BARO: '+baroformatfull+'  //  INSIDE: '+temp1formatfull+'  //  OUTSIDE: '+temp2formatfull
            conkyline_timezone='TIME OFFSET: '+utcoffsetformat+'  //  NAUTICAL TIMEZONE: '+nauticaltimezoneformat
            conkyline_coordinates='LAT: '+gpslatformatfull+'  //  LON: '+gpslonformatfull
            conkyline_spd='AVG SPD: '+spdavgformatfull
            conkyline_alarm=alarmformat
            if spdmax_show is True: conkyline_spd+='  //  MAX SPD: '+spdmaxformatfull
            conkyline_options=['',conkyline_uptime,conkyline_astronomy,conkyline_weather,conkyline_timezone,conkyline_coordinates,conkyline_spd,conkyline_alarm]
            
            #Write text to file
            conkyline1=conkyline_options[conklyline1_selected]
            conkyline2=conkyline_options[conklyline2_selected]
            conkyline3=conkyline_options[conklyline3_selected]
            conkyline4=conkyline_options[conklyline4_selected]
            conkyline5=conkyline_options[conklyline5_selected]
            conkyline6=conkyline_options[conklyline6_selected]
            conkytext=conkyline1
            conkytext+='\n'
            conkytext+=conkyline2
            conkytext+='\n'
            conkytext+=conkyline3
            conkytext+='\n'
            conkytext+=conkyline4
            conkytext+='\n'
            conkytext+=conkyline5
            conkytext+='\n'
            conkytext+=conkyline6
            conkyfile = open(home_dir+'.conkytext', 'w')
            conkyfile.writelines(conkytext)
            conkyfile.close()
            
            conkytime=0
          conkytime+=1
        sleep(1)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('conky').start()





#Output data to statusbar
start_output_data=0
class output_data(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    try:
      global boot_animation_stop
      while True:
        if killer.kill_now or error_raised is True:
          break
        if start_output_data==1:
          if boot_animation_stop==0: boot_animation_stop=1
          
          #Format date/time
          if dateformat_mmddyyy is True: currenttime=(datetime.utcnow()+timedelta(hours=utcoffsethours,minutes=utcoffsetminutes)).strftime('%m.%d.%Y %H:%M:%S')
          else: currenttime=(datetime.utcnow()+timedelta(hours=utcoffsethours,minutes=utcoffsetminutes)).strftime('%d.%m.%Y %H:%M:%S')
          
          #Output data
          if boot_animation_stop==2 and alarm_animation_running is False: sys.stdout.write('%{c}'+gpsfixformat+'  TIME: '+currenttime+'  //  SPD: '+gpsspdformatfull+'  //  COG: '+gpscogformatfull+'  //  LOG: '+distformatfull+'  '+gpsfixformat+'\n')
          
        sleep(0.2)
    
    #Error handling
    except:
      traceback.print_exc()
      if error_animation_running==0: error_animation('statusbar').start()





#Start everything
if __name__ == '__main__' and error_raised is not True:
  read_config().start()
  time_values().start()
  gpsp().start()
  read_data().start()
  output_conky().start()
  output_data().start()
  update_databases().start()
  alarm_system().start()
  alarm_animation().start()
  while True:
    sleep(1)
    if killer.kill_now:
      break
