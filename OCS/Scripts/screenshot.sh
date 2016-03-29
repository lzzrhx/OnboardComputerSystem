#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")
echo '' && echo '' && echo '----------------------------------------' && echo '** TAKING SCREENSHOT **' && echo '----------------------------------------'
echo '' && echo '' && scrot /home/laserwolf/screenshot_$DATE.png && echo 'saved as screenshot_'$DATE'.png'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
