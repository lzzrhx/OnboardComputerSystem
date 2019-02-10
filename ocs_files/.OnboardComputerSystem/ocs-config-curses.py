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
config = SafeConfigParser()
config.read(ocs_dir+'OnboardComputerSystem.conf')

#Create the list
list_entries = {'list':[]}
item_count=0
entry_width=100

#UTC offset
item_name='UtcOffset'
item_content=str(config.get('Config', item_name))
item_title='TIME OFFSET';

option_count=0;selected_option=0;list_entries['list'].extend ([{'title': item_title, 'selected':[0], 'data':[]}]);

option_title='UTC-01:00';option_content='-01:00';
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

option_title='UTC+00:00';option_content='+00:00';
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

option_title='UTC+01:00';option_content='+01:00';
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

item_count+=1



#Use nautical timezone
item_name='UseNauticalTimezone'
item_content=str(config.get('Config', item_name))
item_title='USE NAUTICAL TIMEZONE (OVERRIDES TIME OFFSET)';

option_count=0;selected_option=0;list_entries['list'].extend ([{'title': item_title, 'selected':[0], 'data':[]}]);

option_title='NO';option_content='False';
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

option_title='YES';option_content='True';
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

item_count+=1

#Starting distance
item_name='DistanceStart'
item_content=str(config.get('Config', item_name))
item_title='STARTING DISTANCE IN NAUTICAL MILES (FOR LOG)';

option_count=0;selected_option=0;list_entries['list'].extend ([{'title': item_title, 'selected':[0], 'data':[]}]);

option_title=str(item_content);option_content=str(item_content);
if item_content==option_content: selected_option=option_count
option_count+=1;list_entries['list'][item_count]['selected'][0]=selected_option;list_entries['list'][item_count]['data'].extend ([{'title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'value': option_content}]);

item_count+=1


#Starting distance
option_count=0;selected_option=0;list_entries['list'].extend ([{'title': item_title, 'selected':[0], 'data':[]}]);

option_title='SAVE SETTINGS';option_content='SAVE';
list_entries['list'][item_count]['data'].extend ([{'title': '  '+option_title+'  ','value': option_content}]);

item_count+=1

#item_title='TITLE2';item_content='TEXT2';list_entries['list'].extend ([{'title': data_margin+item_title+':'+(data_margin+item_content).rjust(entry_width-len(item_title)-2)}]);
#item_title='TITLE3';item_content='TEXT3';list_entries['list'].extend ([{'title': data_margin+item_title+':'+(data_margin+item_content).rjust(entry_width-len(item_title)-2)}]);
#item_title='TITLE4';item_content='TEXT4';list_entries['list'].extend ([{'title': data_margin+item_title+':'+(data_margin+item_content).rjust(entry_width-len(item_title)-2)}]);
#entry_width=len(item_title)
#Output data
#num_data_entries=0
#list_entries['list'].extend ([{'title': item_title, 'data':[]}]);
#num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+'123'+':'+('456'+data_margin).rjust(entry_width-len('123')-2)}]);
#list_entries['list'].extend ([{'title': data_margin+item_title+':'+(item_content+data_margin).rjust(entry_width-len(item_title)-2)}]);
#num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpsspdlabel+':'+(gpsspdformatfull+data_margin).rjust(entry_width-len(gpsspdlabel)-2)}]);
#num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+gpscoglabel+':'+(gpscogformatfull+data_margin).rjust(entry_width-len(gpscoglabel)-2)}]);
#num_data_entries+=1;list_entries['list'][count]['data'].extend ([{'title': data_margin+distlabel+':'+(distformatfull+data_margin).rjust(entry_width-len(distlabel)-2)}]);


pos2=None
oldpos2=None
lastentry2=1

#Display data
entrycount = len(list_entries['list'])
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
while x!=ord('q') and x!=27:
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
        list_entries['list'][pos]['selected'][0]=pos2
      selected_option=list_entries['list'][index]['selected'][0]
      entry_text=list_entries['list'][index]['data'][selected_option]['title']
      if pos==index:
        screen.addstr(title_line3_pos+margin+entry_num+dataspace,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_selected)
        pos2=list_entries['list'][index]['selected'][0]
        oldpos2=pos2
        lastentry2=len(list_entries['list'][index]['data'])-1
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
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
system('clear')
sys.exit()

