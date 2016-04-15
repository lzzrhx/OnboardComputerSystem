#!/bin/sh

menu="%{c}"
menu="${menu}%{A:urxvt -cd ~ -name location-history -e ~/.OnboardComputerSystem/location-history-curses.py &:}[ LOG ]%{A}  "
menu="${menu}%{A:urxvt -cd ~ -name weather-history -e ~/.OnboardComputerSystem/weather-history-curses.py &:}[ WTHR ]%{A}  "
menu="${menu}%{A:opencpn &:}[ OCPN ]%{A}  "
menu="${menu}%{A:~/Apps/zyGrib/zyGrib &:}[ GRIB ]%{A}  "
menu="${menu}%{A:pcmanfm ~/ &:}[ HDD ]%{A}  "
menu="${menu}%{A:florence show &:}%{A3:florence hide &:}[ KEYB ]%{A}%{A}  "
menu="${menu}%{A:~/.OnboardComputerSystem/shutdown.sh:}%{A3:~/.OnboardComputerSystem/reboot.sh:}%{F#976B67}[ OFF ]%{F-}%{A}%{A}"
echo $menu
