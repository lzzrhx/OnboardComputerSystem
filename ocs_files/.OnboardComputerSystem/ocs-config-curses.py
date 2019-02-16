#! /usr/bin/python3
# -*- coding: utf-8 -*-

#Import stuff
from datetime import datetime
from os import path, system
import time
import sqlite3
import curses
import sys
import locale
from configparser import SafeConfigParser
import datetime

locale.setlocale(locale.LC_ALL,"")

#Set values
main_title='SYSTEM SETTINGS'
margin=2
data_margin=5
scroll_offset=2
scroll_continuous=0
scroll_continuous2=0
title_width=100

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

#Set directories
home_dir = path.expanduser('~') + '/'           #Home directory
ocs_dir = home_dir + '.OnboardComputerSystem/'  #Onboard Computer System directory

#config parser
config_filename='OnboardComputerSystem.conf'
config = SafeConfigParser()
config.optionxform = lambda option: option
config.read(ocs_dir+config_filename)

#Create the list
list_entries = []
item_count=0
entry_width=100


def item_options(title,item_name):
  global item_title
  global item_content
  global option_count
  item_title=title.upper()
  item_content=str(config.get('Config', item_name))        
  option_count=0;list_entries.extend ([{'item_title': title, 'item_name': item_name, 'selected_option': 0, 'item_type': 'options', 'item_options':[]}]);

def option(option_title,option_value):
  global option_count
  option_title=option_title.upper()
  if item_content==option_value:
    list_entries[item_count]['selected_option']=option_count;
  list_entries[item_count]['item_options'].extend ([{'option_title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'option_value': option_value}])
  option_count+=1



#Disclaimer
item_options('Disable disclaimer','DisclaimerActivate')
option('No','True');
option('Yes','False');
item_count+=1



#Callsign



#MMSI



#UTC offset
item_options('Time offset','UtcOffset')
option_loop_value = -12
while option_loop_value <= 12:
  option_loop_value_new=option_loop_value
  option_loop_value_neg=str(option_loop_value)[0:1]
  if option_loop_value_neg == '-': option_loop_value_new=str(option_loop_value)[1:]
  option_loop_value_new='{0:02.0f}:{1:02.0f}'.format(*divmod(float(option_loop_value_new) * 60, 60))
  if option_loop_value_neg == '-': option_loop_value_new='-'+str(option_loop_value_new)
  else: option_loop_value_new='+'+str(option_loop_value_new)
  option_loop_title='UTC'+option_loop_value_new
  option(option_loop_title,option_loop_value_new);
  option_loop_value+=0.5
item_count+=1



#Use nautical timezone
item_options('Use nautical timezone (overrides time offset)','UseNauticalTimezone')
option('No','False');
option('Yes','True');
item_count+=1



#DistanceStart
item_options('Starting distance for log','DistanceStart')
option_loop_value = 0
while option_loop_value <= 100000:
  option(str(option_loop_value)+' NM',str(option_loop_value));
  option_loop_value+=100
item_count+=1



#TempInside



#TempOutside



#Barometric pressure usit: mmHg
item_options('Barometric pressure unit','BaroUnitMmhg')
option('Mbar','False');
option('mmHg','True');
item_count+=1



#Temperature unit
item_options('Temperature unit','TempUnitFahrenheit')
option('Celsius','False');
option('Fahrenheit','True');
item_count+=1



#Date format
item_options('Date format','DateMonthDayYear')
option('DD.MM.YYYY','False');
option('MM.DD.YYYY','True');
item_count+=1



#Datalines
def dataline(number):
  global item_count
  item_options('Data line '+number,'DataLine'+number)
  option('(Empty)','0');
  option('Uptime','1');
  option('Sunrise / Sunset','2');
  option('Barometric pressure / temperatures','3');
  option('Time offset / timezone','4');
  option('Latitude / longitude','5');
  option('Average / max speed','6');
  option('Alarm system status','7');
  option('Callsign / MMSI','8');
  item_count+=1
dataline('1')
dataline('2')
dataline('3')
dataline('4')
dataline('5')
dataline('6')
dataline('7')
dataline('8')



#Required distance for new entry in location history
item_options('Required distance for new entry in location history','LogEntryMinDistance')
option_loop_value = 10
while option_loop_value <= 10000:
  option(str(option_loop_value)+' meters',str(option_loop_value));
  option_loop_value+=10
item_count+=1



#SpdAvgReqMin
item_options('Required speed before calculating average speed','SpdAvgReqMin')
option_loop_value = float(0.25)
while option_loop_value <= 5:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1



#Show max speed
item_options('Show max speed','ShowMaxSpd')
option('No','False');
option('Yes','True');
item_count+=1



#Reset average speed
item_options('Reset average speed','SpdAvgReset')
option('No','False');
option('Yes','True');
item_count+=1



#Reset max speed
item_options('Reset max speed','SpdMaxReset')
option('No','False');
option('Yes','True');
item_count+=1



#Reset distance travelled
item_options('Reset distance travelled','DistanceReset')
option('No','False');
option('Yes','True');
item_count+=1


show_distupdatedistance=False
show_distupdateinterval=False
show_tempupdateinterval=False
show_baroupdateinterval=False
show_baroconnected=False

#Required distance travelled before updating distance travelled
if show_distupdatedistance is True:
  item_options('Required distance for updating distance travelled','DistUpdateDistance')
  option_loop_value = 1
  while option_loop_value <= 100:
    option(str(option_loop_value)+' meters',str(option_loop_value));
    option_loop_value+=1
  item_count+=1



#Interval for updating distance travelled
if show_distupdateinterval is True:
  item_options('Interval for updating distance travelled','DistUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' sec',str(option_loop_value));
    option_loop_value+=1
  item_count+=1



#Interval for updating temperature data
if show_tempupdateinterval is True:
  item_options('Interval for updating temperature data','TempUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' min',str(option_loop_value));
    option_loop_value+=1
  item_count+=1



#Interval for updating barometric pressure data
if show_baroupdateinterval is True:
  item_options('Interval for updating barometric pressure data','BaroUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' min',str(option_loop_value));
    option_loop_value+=1
  item_count+=1


#Enable barometric pressure sensor
if show_baroconnected is True:
  item_options('Enable barometric pressure sensor','BaroConnected')
  option('Yes','True');
  option('No','False');
  item_count+=1



#Save settings
#option_count=0;selected_option=0;list_entries.extend ([{'item_title': item_title, 'item_name': 0, 'selected_option': 0, 'item_type': 2, 'item_options':[]}]);
#option_title='SAVE SETTINGS';option_content='SAVE';
#list_entries[item_count]['item_options'].extend ([{'option_title': '  '+option_title+'  ','option_value': option_content}]);
#item_count+=1





#Display data
entrycount = len(list_entries)
data_line=''.rjust(entry_width,'-')
lastentry=entrycount-1
needed_space=entrycount
if needed_space>data_space:
  entry_range_first=needed_space-data_space
else:
  entry_range_first=0
entry_range_last=entrycount
pos=0
oldpos=None
x = None
pos2=None
oldpos2=None
lastentry2=0

while x!=ord('q') and x!=27 and x!=10:
  if pos != oldpos or pos2 != oldpos2:
    oldpos = pos
    dataspace=0
    entry_num=0
    if needed_space>data_space:
      if pos-scroll_offset<entry_range_first:
        new_scroll_offset=scroll_offset
        if pos<scroll_offset:
          new_scroll_offset=pos
        entry_range_first=pos-new_scroll_offset
        entry_range_last=pos-new_scroll_offset+data_space
      elif pos+1+scroll_offset>entry_range_last:
        new_scroll_offset=scroll_offset
        if pos+1>entrycount-scroll_offset:
          new_scroll_offset=entrycount-pos-1
        entry_range_first=pos+1+new_scroll_offset-data_space
        entry_range_last=pos+1+new_scroll_offset
    entry_range=range(entry_range_first,entry_range_last)
    for index in entry_range:
      if pos2!=oldpos2:
        list_entries[pos]['selected_option']=pos2
      selected_option=list_entries[index]['selected_option']
      entry_text=list_entries[index]['item_options'][selected_option]['option_title']
      if pos==index:
        screen.addstr(title_line3_pos+margin+entry_num+dataspace,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_selected)
        pos2=list_entries[index]['selected_option']
        oldpos2=pos2
        lastentry2=len(list_entries[index]['item_options'])-1
      else:
        screen.addstr(title_line3_pos+margin+entry_num+dataspace,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu)
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

  if x == 261: #right
    if pos2 < lastentry2:
      pos2 += 1
    elif scroll_continuous2==1:
      pos2 = 0
  elif x == 260: #left
    if pos2 > 0:
      pos2 += -1
    elif scroll_continuous2==1:
      pos2 = lastentry2

#Exit
if x == 10:
  count=0
  for index in list_entries:
    name=str(list_entries[count]['item_name'])
    selected=list_entries[count]['selected_option']
    value=str(list_entries[count]['item_options'][selected]['option_value'])
    config.set('Config', name, value)
    count+=1

  with open(ocs_dir+config_filename, 'w') as configfile:
    config.write(configfile)
    configfile.close()

curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
system('clear')
sys.exit()

