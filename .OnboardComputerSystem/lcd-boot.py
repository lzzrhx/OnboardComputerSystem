#!/usr/bin/python
     
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCD(25, 24, 23, 17, 27, 22, 20, 4)
#lcd.clear()
lcd.message('  ----------------  \n  ONBOARD COMPUTER  \n       SYSTEM       \n  ----------------  ')
