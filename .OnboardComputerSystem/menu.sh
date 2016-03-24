#!/bin/sh

menu="%{c}"
menu="${menu}%{A:urxvt -hold -cd ~ -name location-history -e ~/.OnboardComputerSystem/location-history.py &:}[ LOG ]%{A}  "
menu="${menu}%{A:urxvt -hold -cd ~ -name weather-history -e ~/.OnboardComputerSystem/weather-history.py &:}[ WTHR ]%{A}  "
menu="${menu}%{A:opencpn &:}[ OCPN ]%{A}  "
menu="${menu}%{A:foxtrotgps &:}[ FGPS ]%{A}  "
menu="${menu}%{A:~/Apps/zyGrib/zyGrib &:}[ GRIB ]%{A}  "
menu="${menu}%{A:pcmanfm ~/ &:}[ HDD ]%{A}  "
menu="${menu}%{A:florence show &:}%{A3:florence hide &:}[ KEYB ]%{A}%{A}  "
menu="${menu}%{A:~/.OnboardComputerSystem/lcd-clear.py && sudo poweroff:}%{A3:~/.OnboardComputerSystem/lcd-clear.py && sudo reboot:}%{F#976B67}[ OFF ]%{F-}%{A}%{A}"
echo $menu
