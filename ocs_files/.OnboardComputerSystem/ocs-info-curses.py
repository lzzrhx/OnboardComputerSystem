#! /usr/bin/python3
# -*- coding: utf-8 -*-

#Import stuff
from datetime import datetime
import os
import time
import sqlite3
import curses
import sys
import locale

locale.setlocale(locale.LC_ALL,"")

#Set values
main_title='INFO'
margin=2
data_margin=5
title_width=50
entry_width=50

#Set terminal title
print('\33]0;'+main_title+'\a', end='')
sys.stdout.flush()

#Setup ncurses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.curs_set(0)
screen.border(0)
curses_size=screen.getmaxyx();
title_line1_pos=margin
title_line2_pos=title_line1_pos+1
title_line3_pos=title_line2_pos+1
title_line4_pos=title_line3_pos+1
data_top = title_line4_pos+margin
data_bottom = curses_size[0]-margin
data_space=data_bottom-data_top
data_margin=''.rjust(data_margin)

#Set colors
curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
screen.bkgd(curses.color_pair(1))
style_title = curses.color_pair(1)
style_data = curses.color_pair(1)

#Get data from database
list_entries = {'data':[]}
count=0
home_dir = os.path.expanduser('~') + '/'
sqlite_file=home_dir + '.OnboardComputerSystem/databases/ocs-main.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM OCS")
while True:
  row=c.fetchone()
  if row == None:
    break
  #Format time
  itemtime=str(row[1])
  itemtimelabel='UPDATED'
  itemtimeformatfull=datetime.fromtimestamp(float(itemtime)).strftime('%d.%m.%Y %H:%M')
  #Format Latitude
  gpslat=float(row[2])
  gpslatlabel='LATITUDE'
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
  gpslon=float(row[3])
  gpslonlabel='LONGITUDE'
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
  gpsspd=float(row[4])
  gpsspdlabel='SPEED'
  gpsspdformat='{0:.1f}'.format((float(gpsspd) * 1.9438444924574))
  gpsspdformatfull='{0} KN'.format(gpsspdformat)
  #Format Max speed
  gpsspdmax=float(row[5])
  gpsspdmaxlabel='MAX SPEED'
  gpsspdmaxformat='{0:.1f}'.format((float(gpsspdmax) * 1.9438444924574))
  gpsspdmaxformatfull='{0} KN'.format(gpsspdmaxformat)
  #Format Course Over Ground
  gpscog=float(row[6])
  gpscoglabel='COURSE OVER GROUND'
  gpscogformat=int(gpscog)
  gpscogformatfull='{0}°'.format(gpscogformat)
  #Format uptime
  uptime=float(row[7])
  uptimelabel='UPTIME'
  uptimemin, uptimesec = divmod(uptime, 60)
  uptimehour, uptimemin = divmod(uptimemin, 60)
  uptimeday, uptimehour = divmod(uptimehour, 24)
  uptimeformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptimeday, uptimehour, uptimemin)
  #Format max uptime
  uptimemax=float(row[8])
  uptimemaxlabel='MAX UPTIME'
  uptimemaxmin, uptimemaxsec = divmod(uptimemax, 60)
  uptimemaxhour, uptimemaxmin = divmod(uptimemaxmin, 60)
  uptimemaxday, uptimemaxhour = divmod(uptimemaxhour, 24)
  uptimemaxformatfull="%02d DAYS - %02d HOURS - %02d MINUTES" % (uptimemaxday, uptimemaxhour, uptimemaxmin)
  #Format distance travelled
  dist=float(row[9])
  diststart=float(row[10])
  distlabel='TOTAL DISTANCE TRAVELLED'
  distformat='{0:.1f}'.format(float(dist+diststart) * 0.000539956803)
  distformatfull='{0} NM'.format(distformat)
  #Format barometric pressure
  baro=float(row[11])
  barolabel='BAROMETRIC PRESSURE'
  baroformat='{0}'.format(int(baro/100))
  baroformatfull='{0} MBAR'.format(baroformat)
  #Format temperature
  temp1=float(row[12])
  temp2=float(row[13])
  temp1label='TEMPERATURE INSIDE'
  temp2label='TEMPERATURE OUTSIDE'
  temp1format='{0:.1f}'.format(float(temp1))
  temp1formatfull='{0}°C'.format(temp1format)
  temp2format='{0:.1f}'.format(float(temp2))
  temp2formatfull='{0}°C'.format(temp2format)
  #Format sunrise
  sunrise=str(row[14])
  sunriselabel='SUNRISE'
  #Format sunset
  sunset=str(row[15])
  sunsetlabel='SUNSET'
  #Output data
  #list_entries['data'].extend ([{'title': data_margin+itemtimelabel+':'+(itemtimeformatfull+data_margin).rjust(entry_width-len(itemtimelabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+uptimelabel+':'+(uptimeformatfull+data_margin).rjust(entry_width-len(uptimelabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+gpslatlabel+':'+(gpslatformatfull+data_margin).rjust(entry_width-len(gpslatlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+gpslonlabel+':'+(gpslonformatfull+data_margin).rjust(entry_width-len(gpslonlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+gpsspdlabel+':'+(gpsspdformatfull+data_margin).rjust(entry_width-len(gpsspdlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+gpscoglabel+':'+(gpscogformatfull+data_margin).rjust(entry_width-len(gpscoglabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+distlabel+':'+(distformatfull+data_margin).rjust(entry_width-len(distlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+barolabel+':'+(baroformatfull+data_margin).rjust(entry_width-len(barolabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+temp1label+':'+(temp1formatfull+data_margin).rjust(entry_width-len(temp1label)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+temp2label+':'+(temp2formatfull+data_margin).rjust(entry_width-len(temp2label)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+sunriselabel+':'+(sunrise+data_margin).rjust(entry_width-len(sunriselabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+sunsetlabel+':'+(sunset+data_margin).rjust(entry_width-len(sunsetlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+gpsspdmaxlabel+':'+(gpsspdmaxformatfull+data_margin).rjust(entry_width-len(gpsspdmaxlabel)-2)}]);
  list_entries['data'].extend ([{'title': data_margin+uptimemaxlabel+':'+(uptimemaxformatfull+data_margin).rjust(entry_width-len(uptimemaxlabel)-2)}]);
conn.close()

updatetime='(UPDATED '+itemtimeformatfull+')'

#Show title
title_text='* '+main_title+' *'
title_line=''.rjust(title_width,'-')
screen.addstr(title_line1_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
screen.addstr(title_line2_pos,int((curses_size[1]-len(title_text))/2), title_text, style_title)
screen.addstr(title_line3_pos,int((curses_size[1]-len(updatetime))/2), updatetime, style_title)
screen.addstr(title_line4_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)

#Display data
entrycount = len(list_entries['data'])
data_line=''.rjust(entry_width,'-')
lastentry=entrycount-1
entry_range_first=0
entry_range_last=entrycount
refresh=1
x=None
while x!=ord('q'):
  if refresh == 1:
    entry_num=0
    entry_range=range(entry_range_first,entry_range_last)
    for index in entry_range:
      entry_text=list_entries['data'][index]['title']
      screen.addstr(title_line4_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_data)
      entry_num+=1
    screen.refresh()
    refresh=0
  x = screen.getch()

#Exit
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
os.system('clear')
sys.exit()

