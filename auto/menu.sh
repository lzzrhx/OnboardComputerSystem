#!/bin/sh

menu="%{c}"
menu="${menu}%{A:terminator --working-dir=~ --command='~/scripts/log.py' &:}[ LOG ]%{A} "
menu="${menu}%{A:terminator --working-dir=~ --command='~/scripts/weather.py' &:}[ WTHR ]%{A} "
menu="${menu}%{A:opencpn &:}[ OCPN ]%{A} "
menu="${menu}%{A:foxtrotgps &:}[ FGPS ]%{A} "
menu="${menu}%{A:~/apps/zyGrib/zyGrib &:}[ GRIB ]%{A} "
menu="${menu}%{A:pcmanfm ~/ &:}[ HDD ]%{A} "
menu="${menu}%{A:florence show &:}%{A3:florence hide &:}[ KEY ]%{A}%{A} "
menu="${menu}%{A:sudo poweroff:}%{A3:sudo reboot:}%{F#976B67}[ OFF ]%{F-}%{A}%{A}"
echo $menu
