#! /usr/bin/python3
# -*- coding: utf-8 -*-

#Import stuff
from os import path, environ, system
from configparser import SafeConfigParser
import sys
import locale
import curses

#Setup
locale.setlocale(locale.LC_ALL,"")
environ.setdefault('ESCDELAY', '25')

#Setup ncurses
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.curs_set(0)
screen.border(0)
curses_size=screen.getmaxyx();

#Set values
set_width=100
margin=2
data_margin=5
scroll_offset=2
scroll_continuous1=1
scroll_continuous2=1

#Set text
main_title='SYSTEM SETTINGS'
quit_text='Press "Y" to quit or "N" to cancel'.upper()
button_save_text='Save settings'

#Set colors
curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3,curses.COLOR_BLACK, curses.COLOR_CYAN)
screen.bkgd(curses.color_pair(1))
style_title = curses.color_pair(1)
style_menu = curses.color_pair(1)
style_menu_selected = curses.color_pair(2)
style_menu_edit = curses.color_pair(3)
style_button = curses.color_pair(3)
style_button_selected = curses.color_pair(2)

#Set terminal title
print('\33]0;'+main_title+'\a', end='')
sys.stdout.flush()

#Set directories
home_dir = path.expanduser('~') + '/'           #Home directory
ocs_dir = home_dir + '.OnboardComputerSystem/'  #Onboard Computer System directory

#Config parser
config_filename='OnboardComputerSystem.conf'
config = SafeConfigParser()
config.optionxform = lambda option: option
config.read(ocs_dir+config_filename)

#Item with selectable options
def item_options(title,item_name):
  global item_title
  global item_content
  global option_count
  item_title=title.upper()
  item_content=str(config.get('Config', item_name))        
  option_count=0;list_entries.extend ([{'item_title': title, 'item_name': item_name, 'selected_option': 0, 'item_type': 'options', 'item_options':[]}]);
#Option
def option(option_title,option_value):
  global option_count
  option_title=option_title.upper()
  if item_content==option_value:
    list_entries[item_count]['selected_option']=option_count;
  list_entries[item_count]['item_options'].extend ([{'option_title': data_margin+item_title+':'+(option_title+data_margin).rjust(entry_width-len(item_title)-2),'option_value': option_value}])
  option_count+=1

#Create the list of items
data_margin=''.rjust(data_margin)
entry_width=set_width
list_entries = []
item_count=0



############################################################################################################



#Enable/disable items
show_distupdatedistance=False
show_distupdateinterval=False
show_tempupdateinterval=False
show_baroupdateinterval=False
show_baroconnected=False

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



############################################################################################################



#Title
title_width=set_width
title_text='* '+main_title+' *'
title_line=''.rjust(title_width,'-')
title_start_pos=margin
title_text_pos=title_start_pos+1
title_end_pos=title_text_pos+1

#Buttons
num_buttons=1
button_save='[ '+button_save_text.upper()+' ]'

#Calculate space
data_top = title_end_pos+margin
data_bottom = curses_size[0]-margin-1
data_space=data_bottom-data_top
entrycount = len(list_entries)
lastentry=entrycount-1+num_buttons
lastentry2=None
needed_space=entrycount
if needed_space>data_space:
  entry_range_first=needed_space-data_space
else:
  entry_range_first=0
entry_range_last=entrycount

#Start output
entry_pos=0
curses_button = None
curses_action=None
curses_mode=None
curses_first=True
curses_action_valid=None
while curses_action!='exit' and curses_action!='save':
  
  #Refresh screen and show stuff
  if curses_first is True or curses_action in curses_action_valid:
    screen.clear()
    
    #Title
    screen.addstr(title_start_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    screen.addstr(title_text_pos,int((curses_size[1]-len(title_text))/2), title_text, style_title)
    screen.addstr(title_end_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    
    #Quit dialog
    if curses_mode==None and (curses_action=='quit' or curses_action=='esc'): curses_mode='quit'
    if curses_mode=='quit':
      curses_action_valid=['yes','no']
      screen.addstr(title_end_pos+margin,int((curses_size[1]-len(quit_text))/2), quit_text, style_title)
      if curses_action=='yes':
        curses_action='exit'
      elif curses_action=='no':
        curses_mode=None
    
    #List of items
    if curses_mode!='quit':

      #Navigate up/down
      if curses_mode==None:
        curses_action_valid_default=['up','down','quit','esc']
        curses_action_valid=curses_action_valid_default
        #Go up
        if curses_action=='up':
          if entry_pos > 0:
            entry_pos += -1
          elif scroll_continuous1==1:
            entry_pos = lastentry
        #Go down
        if curses_action=='down':
          if entry_pos < lastentry:
            entry_pos += 1
          elif scroll_continuous1==1:
            entry_pos = 0
          
      #Calculate number of entries to show
      if needed_space>data_space:
        if entry_pos-scroll_offset<entry_range_first:
          new_scroll_offset=scroll_offset
          if entry_pos<scroll_offset:
            new_scroll_offset=entry_pos
          entry_range_first=entry_pos-new_scroll_offset
          entry_range_last=entry_pos-new_scroll_offset+data_space
        elif entry_pos+1+scroll_offset>entry_range_last:
          new_scroll_offset=scroll_offset
          if entry_pos+1>entrycount-scroll_offset:
            new_scroll_offset=entrycount-entry_pos-1
          entry_range_first=entry_pos+1+new_scroll_offset-data_space
          entry_range_last=entry_pos+1+new_scroll_offset
      entry_range=range(entry_range_first,entry_range_last)
      
      #Show entries
      entry_num=0
      for entry_num_current in entry_range:
        
        #Entry type "options"
        style_menu_current=style_menu
        if list_entries[entry_num_current]['item_type']=='options':
          #currently selected entry
          if entry_pos==entry_num_current:
            entry_pos2=list_entries[entry_num_current]['selected_option']
            lastentry2=len(list_entries[entry_num_current]['item_options'])-1
            #Go in/out of "change option" mode
            if curses_mode==None and curses_action=='enter': curses_mode='change_option';curses_action_valid=['left','right','esc']
            elif curses_mode=='change_option' and (curses_action=='enter' or curses_action=='esc'): curses_mode=None;curses_action_valid=curses_action_valid_default
            curses_action_valid.append('enter')
            if curses_mode=='change_option':
              #Select previous
              if curses_action=='left':
                if entry_pos2 > 0:
                  entry_pos2 += -1
                elif scroll_continuous2==1:
                  entry_pos2 = lastentry2
              #Select next
              if curses_action=='right':
                if entry_pos2 < lastentry2:
                  entry_pos2 += 1
                elif scroll_continuous2==1:
                  entry_pos2 = 0
              #Change selected option
              list_entries[entry_pos]['selected_option']=entry_pos2
              style_menu_current=style_menu_edit
            #If not in "change option" mode
            else:
              style_menu_current=style_menu_selected
          #Show the entries
          selected_option=list_entries[entry_num_current]['selected_option']
          entry_text=list_entries[entry_num_current]['item_options'][selected_option]['option_title']
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
        
        entry_num+=1

      #Save button 
      if entry_pos==lastentry:
        screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(button_save))/2), button_save, style_menu_selected)
        if curses_action=='enter':
          curses_action='save'
        curses_action_valid.append('enter')
      else:
        screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(button_save))/2), button_save, style_menu)
      
  #Keyboard input
  if curses_action!='exit' and curses_action!='save':
    curses_button = screen.getch()
    if curses_button==ord('q') or curses_button==ord('Q'):
      curses_action='quit'
    elif curses_button==27:
      curses_action='esc'
    elif curses_button==10:
      curses_action='enter'
    elif curses_button==259:
      curses_action='up'
    elif curses_button==258:
      curses_action='down'
    elif curses_button==261:
      curses_action='right'
    elif curses_button==260:
      curses_action='left'
    elif curses_button==ord('y') or curses_button==ord('Y'):
      curses_action='yes'
    elif curses_button==ord('n') or curses_button==ord('N'):
      curses_action='no'
  if curses_first is True: curses_first=False

#Save changes
if curses_action=='save':
  count=0
  #Get config values
  for index in list_entries:
    name=str(list_entries[count]['item_name'])
    selected=list_entries[count]['selected_option']
    value=str(list_entries[count]['item_options'][selected]['option_value'])
    config.set('Config', name, value)
    count+=1
  #Save to config file
  with open(ocs_dir+config_filename, 'w') as configfile:
    config.write(configfile)
    configfile.close()

#Exit
curses.nocbreak()
screen.keypad(0)
curses.echo()
curses.endwin()
system('clear')
sys.exit()