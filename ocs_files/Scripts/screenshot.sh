#!/bin/bash

sleeptime=5;if [ ! -z $1 ];then sleeptime=$1;fi;

DATE=$(date +"%Y-%m-%d_%H%M%S")
echo '' && echo '' && echo '----------------------------------------' && echo '** TAKING SCREENSHOT **' && echo '----------------------------------------'
echo '' && echo '' && sleep $sleeptime && scrot /home/operator/screenshot_$DATE.png && echo 'saved as screenshot_'$DATE'.png'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
