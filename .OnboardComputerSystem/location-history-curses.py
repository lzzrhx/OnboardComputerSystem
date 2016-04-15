#! /usr/bin/python
# -*- coding: utf-8 -*-

#Import stuff
from datetime import datetime
import os
import time
import sqlite3
import curses
import sys

#Set values
main_title='LOCATION HISTORY'
margin=2
data_margin=5
scroll_offset=2
scroll_continuous=0
title_width=50

#Set terminal title
sys.stdout.write('\x1b]2;'+main_title+'\x07')

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
data_top = title_line3_pos+margin
data_bottom = curses_size[0]-margin
data_space=data_bottom-data_top
data_margin=''.rjust(data_margin)

#Set colors
curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
screen.bkgd(curses.color_pair(1))
style_title = curses.color_pair(1)
style_menu = curses.color_pair(1)
style_menu_selected = curses.color_pair(2)
style_data = curses.color_pair(1)

#Show title
title_text='* '+main_title+' *'
title_line=''.rjust(title_width,'-')
screen.addstr(title_line1_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
screen.addstr(title_line2_pos,int((curses_size[1]-len(title_text))/2), title_text, style_title)
screen.addstr(title_line3_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)

#Get data from database
list_entries = {'list':[]}
count=0
home_dir = os.path.expanduser('~') + '/'
sqlite_file=home_dir + 'Databases/location.db'
conn=sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute("SELECT * FROM LOCATION")
while True:
  row=c.fetchone()
  if row == None:
    break
  #Format Entry number
  itemnum=int(row[0])
  itemnumformatfull='%05d' %(itemnum)
  #Format time
  itemtime=str(row[1])
  itemtimeformatfull=datetime.fromtimestamp(float(itemtime)).strftime('%d.%m.%Y %H:%M')
  #Format item title
  item_title='ENTRY NO. '+itemnumformatfull+' - '+itemtimeformatfull
  entry_width=len(item_title)
  #Format Latitude
  gpslat=float(row[2])
  gpslatlabel='LAT'
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
  gpslonlabel='LON'
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
  gpsspdlabel='SPD'
  gpsspdformat='{0:.1f}'.format((float(gpsspd) * 1.9438444924574))
  gpsspdformatfull='{0} KN'.format(gpsspdformat)
  #Format Course Over Ground
  gpscog=float(row[5])
  gpscoglabel='COG'
  gpscogformat=int(gpscog)
  gpscogformatfull='{0}°'.format(gpscogformat)
  #Format heading
  hdg=float(row[6])
  hdglabel='HDG'
  hdgformat=int(hdg)
  hdgformatfull='{0}°'.format(hdgformat)
  #Format clinometer (X axis)
  clinox=float(row[7])
  clinoxlabel='CLINO'
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
  clinoy=float(row[8])
  clinoylabel='CLINO (Y)'
  if str(clinoy)[0] == "-":
    clinoyformat=int(float(str(clinoy)[1:]))
    clinoydir='forward'
  else:
    clinoyformat=int(clinoy)
    clinoydir='backward'
  if int(clinoy) == 0:
    clinoydir='none'
  clinoyformatfull='{0}°'.format(clinoyformat)
  #Format distance travelled
  dist=float(row[9])
  distlabel='LOG'
  distformat='{0:.1f}'.format(float(dist) * 0.000539956803)
  distformatfull='{0} NM'.format(distformat)
  #Output data
  num_data_entries=0
  list_entries['list'].extend ([{'title': item_title, 'data':[]}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpslatlabel+':'+(gpslatformatfull+data_margin).rjust(entry_width-len(gpslatlabel)-2)}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpslonlabel+':'+(gpslonformatfull+data_margin).rjust(entry_width-len(gpslonlabel)-2)}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpsspdlabel+':'+(gpsspdformatfull+data_margin).rjust(entry_width-len(gpsspdlabel)-2)}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpscoglabel+':'+(gpscogformatfull+data_margin).rjust(entry_width-len(gpscoglabel)-2)}]);
  #num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+hdglabel+':'+(hdgformatfull+data_margin).rjust(entry_width-len(hdglabel)-2)}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+clinoxlabel+':'+(clinoxformatfull+data_margin).rjust(entry_width-len(clinoxlabel)-2)}]);
  #num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+clinoylabel+':'+(clinoyformatfull+data_margin).rjust(entry_width-len(clinoylabel)-2)}]);
  num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+distlabel+':'+(distformatfull+data_margin).rjust(entry_width-len(distlabel)-2)}]);
  count+=1
conn.close()

#Display data
entrycount = len(list_entries['list'])
data_line=''.rjust(entry_width,'-')
lastentry=entrycount-1
num_data_entries+=1
needed_space=entrycount+num_data_entries
if needed_space>data_space:
  entry_range_first=needed_space-data_space
else:
  entry_range_first=0
entry_range_last=entrycount
pos=lastentry
oldpos=None
x = None
while x!=ord('q'):
  if pos != oldpos:
    oldpos = pos
    dataspace=0
    entry_num=0
    if needed_space>data_space:
      if pos-scroll_offset<entry_range_first:
        new_scroll_offset=scroll_offset
        if pos<scroll_offset:
          new_scroll_offset=pos
        entry_range_first=pos-new_scroll_offset
        entry_range_last=pos-new_scroll_offset+data_space-num_data_entries
      elif pos+1+scroll_offset>entry_range_last:
        new_scroll_offset=scroll_offset
        if pos+1>entrycount-scroll_offset:
          new_scroll_offset=entrycount-pos-1
        entry_range_first=pos+1+new_scroll_offset-data_space+num_data_entries
        entry_range_last=pos+1+new_scroll_offset
    entry_range=range(entry_range_first,entry_range_last)
    for index in entry_range:
      entry_text=list_entries['list'][index]['title']
      if pos==index:
        screen.addstr(6+entry_num+dataspace,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_selected)
        datacount = len(list_entries['list'][index]['data'])
        dataspace=datacount+1
        for index2 in range(datacount):
          data_text=list_entries['list'][index]['data'][index2]['title'].ljust(len(entry_text))
          screen.addstr(6+entry_num+index2+1,int((curses_size[1]-len(data_text))/2), data_text, style_data)
        screen.addstr(6+entry_num+index2+1+1,int((curses_size[1]-len(data_line))/2), data_line, style_data)
      else:
        screen.addstr(6+entry_num+dataspace,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu)
      entry_num+=1
    screen.refresh()
  x = screen.getch()
  if x == 258:
    if pos < lastentry:
      pos += 1
    elif scroll_continuous==1:
      pos = 0
  elif x == 259:
    if pos > 0:
      pos += -1
    elif scroll_continuous==1:
      pos = lastentry

#Exit
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
os.system('clear')
