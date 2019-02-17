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
curses_size=screen.getmaxyx();
screen.border(0)

#Set values
callsign_length=20
set_width=100
margin=2
data_margin_num=5
scroll_offset=2
scroll_continuous1=1
scroll_continuous2=1

#Set text
main_title='System settings'.upper()
quit_text='Press "Y" to quit or "N" to cancel'
button_save_text='Save settings'

#Set registered key inputs (in groups)
list_numbers=['0','1','2','3','4','5','6','7','8','9']
list_alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
list_special_chars=['-','"']

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
config_category='Config'
config = SafeConfigParser()
config.optionxform = lambda option: option
config.read(ocs_dir+config_filename)

#Change single character
def change_char(s, p, r):
  return s[:p]+r+s[p+1:]

#Item with selectable options
def item_options(title,item_name):
  global item_content
  global option_count
  item_content=str(config.get(config_category, item_name))        
  option_count=0;list_entries.extend ([{'item_title': title, 'item_name': item_name, 'selected_option': 0, 'item_type': 'options', 'item_options':[]}]);
#Option
def option(option_title,option_value):
  global option_count
  if item_content==option_value:
    list_entries[item_count]['selected_option']=option_count;
  list_entries[item_count]['item_options'].extend ([{'option_title': option_title,'option_value': option_value}])
  option_count+=1

#Item with alphanumeric input
def item_input_alphanumeric(item_title,item_name,number,enable_numbers='true',enable_alphabet='false',enable_special_chars='false',enable_space='false'):
  global item_count
  item_content=str(config.get(config_category, item_name))
  list_entries.extend ([{'item_title': item_title, 'item_name': item_name, 'item_type': 'input_alphanumeric', 'item_subtype': number, 'enable_numbers': enable_numbers, 'enable_alphabet': enable_alphabet, 'enable_special_chars': enable_special_chars, 'enable_space': enable_space, 'item_content': item_content}]);
  item_count+=1

#Seperator
def item_seperator(subtype='space',content='-'):
  global item_count
  list_entries.extend ([{'item_type': 'seperator', 'item_subtype': subtype, 'item_content': content}]);
  item_count+=1

#Create the list of items
list_entries = []
item_count=0



############################################################################################################



#Enable/disable items
show_distupdatedistance=False
show_distupdateinterval=False
show_tempupdateinterval=False
show_baroupdateinterval=False
show_baroconnected=False

#DisclaimerActivate
item_options('Disclaimer','DisclaimerActivate')
option('Enable','True');
option('Disable','False');
item_count+=1

#Callsign
item_input_alphanumeric('Identification, callsign','Callsign',callsign_length,'true','true','true','true')

#MMSI
item_input_alphanumeric('Identification, MMSI','MMSI','9')

#UtcOffset
item_options('Time, Time offset','UtcOffset')
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

#UseNauticalTimezone
item_options('Time, use nautical timezone (overrides time offset)','UseNauticalTimezone')
option('Disable','False');
option('Enable','True');
item_count+=1

#DistanceStart
item_options('Log, start distance','DistanceStart')
option_loop_value = 0
while option_loop_value <= 100000:
  option(str(option_loop_value)+' NM',str(option_loop_value));
  option_loop_value+=100
item_count+=1

#TempInside
item_input_alphanumeric('Temperature sensor ID, inside','TempInside','15','true','true','true','false')

#TempOutside
item_input_alphanumeric('Temperature sensor ID, outside','TempOutside','15','true','true','true','false')

#BaroUnitMmhg
item_options('Units, pressure','BaroUnitMmhg')
option('Mbar','False');
option('mmHg','True');
item_count+=1

#TempUnitFahrenheit
item_options('Units, temperature','TempUnitFahrenheit')
option('Celsius','False');
option('Fahrenheit','True');
item_count+=1

#DateMonthDayYear
item_options('Units, date format','DateMonthDayYear')
option('DD.MM.YYYY','False');
option('MM.DD.YYYY','True');
item_count+=1

#Datalines
def dataline(number):
  global item_count
  item_options('Data line #'+number,'DataLine'+number)
  option('(Empty)','0');
  option('Uptime','1');
  option('Sunrise / Sunset','2');
  option('Pressure / temperature','3');
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

#LogEntryMinDistance
item_options('Location history, required distance for new entry','LogEntryMinDistance')
option_loop_value = 10
while option_loop_value <= 10000:
  option(str(option_loop_value)+' meters',str(option_loop_value));
  option_loop_value+=10
item_count+=1

#SpdAvgReqMin
item_options('Average speed, required speed before calculating','SpdAvgReqMin')
option_loop_value = float(0.25)
while option_loop_value <= 5:
  option_loop_value_new='{0:.02f}'.format(option_loop_value)
  option(option_loop_value_new+' KN',option_loop_value_new);
  option_loop_value+=0.25
item_count+=1

#ShowMaxSpd
item_options('Max speed, display','ShowMaxSpd')
option('Disable','False');
option('Enable','True');
item_count+=1

#SpdAvgReset
item_options('Average speed, reset','SpdAvgReset')
option('No','False');
option('Yes','True');
item_count+=1

#SpdMaxReset
item_options('Max speed, reset','SpdMaxReset')
option('No','False');
option('Yes','True');
item_count+=1

#DistanceReset
item_options('Log, reset','DistanceReset')
option('No','False');
option('Yes','True');
item_count+=1

#DistUpdateDistance
if show_distupdatedistance is True:
  item_options('Log, required distance for updating','DistUpdateDistance')
  option_loop_value = 1
  while option_loop_value <= 100:
    option(str(option_loop_value)+' meters',str(option_loop_value));
    option_loop_value+=1
  item_count+=1

#DistUpdateInterval
if show_distupdateinterval is True:
  item_options('Log, update interval','DistUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' sec',str(option_loop_value));
    option_loop_value+=1
  item_count+=1

#TempUpdateInterval
if show_tempupdateinterval is True:
  item_options('Temperature, update interval','TempUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' min',str(option_loop_value));
    option_loop_value+=1
  item_count+=1

#BaroUpdateInterval
if show_baroupdateinterval is True:
  item_options('Pressure, update interval','BaroUpdateInterval')
  option_loop_value = 1
  while option_loop_value <= 60:
    option(str(option_loop_value)+' min',str(option_loop_value));
    option_loop_value+=1
  item_count+=1

#BaroConnected
if show_baroconnected is True:
  item_options('Pressure, barometric pressure sensor','BaroConnected')
  option('Enable','True');
  option('Disable','False');
  item_count+=1



############################################################################################################



#Title
title_width=int(set_width/2)
title_text='* '+main_title+' *'
title_line=''.rjust(title_width,'-')
title_start_pos=margin
title_text_pos=title_start_pos+1
title_end_pos=title_text_pos+1

#Entries
entry_width=set_width
data_margin=''.rjust(data_margin_num)
fill_space=''.rjust(entry_width)

#Seperators
seperator_width1=int(entry_width)
seperator_width2=int(entry_width-(entry_width/4))
seperator_width3=int(entry_width/2)
seperator_width4=int(entry_width/4)

#Buttons
num_buttons=1
quit_dialog=' '+quit_text.upper()+' '
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
entry_pos_old=None
curses_button = None
curses_action=None
curses_mode=None
curses_first=True
curses_action_valid=None
while curses_action!='exit' and curses_action!='save':
  if curses_first is True or curses_action in curses_action_valid:

    #Title
    screen.addstr(title_start_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    screen.addstr(title_text_pos,int((curses_size[1]-len(title_text))/2), title_text, style_title)
    screen.addstr(title_end_pos,int((curses_size[1]-len(title_line))/2), title_line, style_title)
    
    #Quit dialog
    if curses_mode==None and (curses_action=='q' or curses_action=='esc'): curses_mode='quit'
    if curses_mode=='quit':
      curses_action_valid=['y','n']
      screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(quit_dialog))/2), quit_dialog, style_menu_selected)
      if curses_action=='y':
        curses_action='exit'
      elif curses_action=='n':
        screen.addstr(curses_size[0]-margin,int((curses_size[1]-len(fill_space))/2), fill_space, style_title)
        curses_mode=None
    
    #List of items
    if curses_mode!='quit':

      #Navigate up/down
      if curses_mode==None:
        curses_action_valid_default=['up','down','q','esc']
        curses_action_valid=curses_action_valid_default
        #Go up
        if curses_action=='up':
          if entry_pos_up_skip!=0: entry_pos=entry_pos-entry_pos_up_skip
          if entry_pos > 0:
            entry_pos += -1
          elif scroll_continuous1==1:
            entry_pos = lastentry
        #Go down
        elif curses_action=='down':
          if entry_pos_down_skip!=0: entry_pos=entry_pos+entry_pos_down_skip
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
      entry_pos_up_skip=0
      entry_pos_down_skip=0
      for entry_num_current in entry_range:
        style_menu_current=style_menu
        
        #Skip up if previous entry seperator
        if entry_pos>0:
          if list_entries[entry_pos-1]['item_type']=='seperator':
            entry_pos_up_skip=1
            if (entry_pos-1)>0:
              if list_entries[entry_pos-2]['item_type']=='seperator':
                entry_pos_up_skip=2
                if (entry_pos-2)>0:
                  if list_entries[entry_pos-3]['item_type']=='seperator':
                    entry_pos_up_skip=3
        #Skip down if next entry seperator
        if entry_pos<(lastentry-num_buttons):
          if list_entries[entry_pos+1]['item_type']=='seperator':
            entry_pos_down_skip=1
            if (entry_pos+1)<(lastentry-num_buttons):
              if list_entries[entry_pos+2]['item_type']=='seperator':
                entry_pos_down_skip=2
                if (entry_pos+2)<(lastentry-num_buttons):
                  if list_entries[entry_pos+3]['item_type']=='seperator':
                    entry_pos_down_skip=3
        
        #Entry type "seperator"
        if list_entries[entry_num_current]['item_type']=='seperator':
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(fill_space))/2), fill_space, style_title)
          if list_entries[entry_num_current]['item_subtype']!='space':
            if list_entries[entry_num_current]['item_subtype']=='custom':
              entry_text=(list_entries[entry_num_current]['item_content']).upper()
            elif list_entries[entry_num_current]['item_subtype']=='fill':
              entry_text=list_entries[entry_num_current]['item_content']
              entry_text=''.rjust(seperator_width2,entry_text)
            screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
        
        #Entry type "options"
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
              elif curses_action=='right':
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
          #Show entry
          selected_option=list_entries[entry_num_current]['selected_option']
          entry_text_item=list_entries[entry_num_current]['item_title']
          entry_text_option=list_entries[entry_num_current]['item_options'][selected_option]['option_title']
          entry_text=(data_margin+entry_text_item+':'+(entry_text_option+data_margin).rjust(entry_width-len(entry_text_item)-2)).upper()
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
              
        #Entry type "input_alphanumeric"
        elif list_entries[entry_num_current]['item_type']=='input_alphanumeric':
          #currently selected entry
          if entry_pos==entry_num_current:
            if entry_pos_old!=entry_pos: entry_pos2=0
            lastentry2=int(list_entries[entry_num_current]['item_subtype'])-1
            #Go in/out of "change option" mode
            enable_space=list_entries[entry_num_current]['enable_space']
            enable_numbers=list_entries[entry_num_current]['enable_numbers']
            enable_alphabet=list_entries[entry_num_current]['enable_alphabet']
            enable_special_chars=list_entries[entry_num_current]['enable_special_chars']
            if curses_mode==None and curses_action=='enter':
              curses_mode='input_alphanumeric';
              curses_action_valid=['up','down','left','right','esc'];
              if enable_space=='true': curses_action_valid.extend(['del','space','backspace']);
              if enable_numbers=='true': curses_action_valid.extend(list_numbers);
              if enable_alphabet=='true': curses_action_valid.extend(list_alphabet);
              if enable_special_chars=='true': curses_action_valid.extend(list_special_chars)
            elif curses_mode=='input_alphanumeric' and (curses_action=='enter' or curses_action=='esc'): curses_mode=None;curses_action_valid=curses_action_valid_default;entry_pos2=0
            curses_action_valid.append('enter')
            if curses_mode=='input_alphanumeric':
              entry_content=(list_entries[entry_num_current]['item_content']).rjust(lastentry2+1)
              #Select previous
              if curses_action=='left':
                if entry_pos2 > 0:
                  entry_pos2 += -1
                elif scroll_continuous2==1:
                  entry_pos2 = lastentry2
              #Select next
              elif curses_action=='right':
                if entry_pos2 < lastentry2:
                  entry_pos2 += 1
                elif scroll_continuous2==1:
                  entry_pos2 = 0
              #Input number
              elif curses_action=='del' or curses_action=='space' or curses_action=='backspace' or curses_action in list_numbers or curses_action in list_alphabet or curses_action in list_special_chars:
                if curses_action=='del' or curses_action=='space' or curses_action=='backspace':
                  entered_char=' '
                else:
                  entered_char=curses_action
                entry_content_new=change_char(entry_content,entry_pos2,entered_char)
                list_entries[entry_num_current]['item_content']=entry_content_new
                if curses_action=='backspace':
                  if entry_pos2 > 0:
                    entry_pos2 += -1
                  elif scroll_continuous2==1:
                    entry_pos2 = lastentry2
                else:
                  if entry_pos2 < lastentry2:
                    entry_pos2 += 1
                  elif scroll_continuous2==1:
                    entry_pos2 = 0
            #Style selected entry
            else:
              style_menu_current=style_menu_selected
          #Show entry
          entry_text_item=list_entries[entry_num_current]['item_title']
          entry_text_content=list_entries[entry_num_current]['item_content']
          entry_text=(data_margin+entry_text_item+':'+(entry_text_content+data_margin).rjust(entry_width-len(entry_text_item)-2)).upper()
          screen.addstr(title_end_pos+margin+entry_num,int((curses_size[1]-len(entry_text))/2), entry_text, style_menu_current)
          #Highlight selected char
          if entry_pos==entry_num_current and curses_mode=='input_alphanumeric':              
              style_menu_current=style_menu_edit
              entry_text_content=(list_entries[entry_num_current]['item_content']).rjust(lastentry2+1)
              entry_text_content_selected_char=entry_text_content[entry_pos2].upper()
              screen.addstr(title_end_pos+margin+entry_num,int(curses_size[1]/2)+50-data_margin_num-(lastentry2-entry_pos2)+1, entry_text_content_selected_char, style_menu_current)
          
        entry_num+=1
      entry_pos_old=entry_pos

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
    curses_button_found=False
    #Some special keys
    if curses_button==27:
      curses_action='esc'
      curses_button_found=True
    elif curses_button==10:
      curses_action='enter'
      curses_button_found=True
    elif curses_button==32:
      curses_action='space'
      curses_button_found=True
    elif curses_button==curses.KEY_BACKSPACE:
      curses_action='backspace'
      curses_button_found=True
    elif curses_button==curses.KEY_DC:
      curses_action='del'
      curses_button_found=True
    elif curses_button==259:
      curses_action='up'
      curses_button_found=True
    elif curses_button==258:
      curses_action='down'
      curses_button_found=True
    elif curses_button==261:
      curses_action='right'
      curses_button_found=True
    elif curses_button==260:
      curses_action='left'
      curses_button_found=True
    #Numbers
    if curses_button_found is False:
      for i in list_numbers:
        if curses_button_found is False:
          if curses_button==ord(i):
            curses_action=i
            curses_button_found=True
    #Alphabet
    if curses_button_found is False:
      for i in list_alphabet:
        if curses_button_found is False:
          if curses_button==ord(i) or curses_button==ord(i.upper()):
            curses_action=i
            curses_button_found=True
    #Special characters
    if curses_button_found is False:
      for i in list_special_chars:
        if curses_button_found is False:
          if curses_button==ord(i):
            curses_action=i
            curses_button_found=True
    #Set no action if button not found
    if curses_button_found is False:
      curses_action=None

  if curses_first is True: curses_first=False

#Save changes
if curses_action=='save':
  count=0
  #Get config values
  for index in list_entries:
    add_entry=False
    #Selectable option entries
    if list_entries[count]['item_type']=='options':
      name=str(list_entries[count]['item_name'])
      selected=list_entries[count]['selected_option']
      value=str(list_entries[count]['item_options'][selected]['option_value'])
      add_entry=True
    #Alphanumeric input entries
    elif list_entries[count]['item_type']=='input_alphanumeric':
      name=str(list_entries[count]['item_name'])
      value=list_entries[count]['item_content']
      add_entry=True
    if add_entry is True: config.set(config_category, name, value)
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