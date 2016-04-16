#!/bin/bash

menu="%{c}"
menu="${menu}%{A:urxvt -cd ~ -name location-history -e ~/.OnboardComputerSystem/location-history-curses.py &:}[ LOG ]%{A}  "
menu="${menu}%{A:urxvt -cd ~ -name weather-history -e ~/.OnboardComputerSystem/weather-history-curses.py &:}[ WTHR ]%{A}  "
menu="${menu}%{A:opencpn &:}[ OCPN ]%{A}  "
menu="${menu}%{A:~/Apps/zyGrib/zyGrib &:}[ GRIB ]%{A}  "
menu="${menu}%{A:pcmanfm ~/ &:}[ HDD ]%{A}  "
menu="${menu}%{A:florence show &:}%{A3:florence hide &:}[ KEYB ]%{A}%{A}  "
menu="${menu}%{A:~/.OnboardComputerSystem/shutdown.sh:}%{A3:~/.OnboardComputerSystem/reboot.sh:}%{F#976B67}[ OFF ]%{F-}%{A}%{A}"

echo $menu | lemonbar -g "x40xx" -p -B "#303030" -F "#A9A28F" -f "ProggyCleanTT:size=30" -a 20 | sh &
python -u ~/.OnboardComputerSystem/OnboardComputerSystem.py | lemonbar -b -g "x40xx" -p -B "#303030" -F "#A9A28F" -f "ProggyCleanTT:size=30"
