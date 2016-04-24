#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")
echo '' && echo '' && echo '----------------------------------------' && echo '** TAKING WEBCAM PICTURE **' && echo '----------------------------------------'
echo '' && echo '' && fswebcam -r 1280x720 -S 99 --banner-colour "#FF303030" --line-colour "#FF303030" --text-colour "#00A9A28F" --font ProggyCleanTT:18 --shadow --timestamp "%d.%m.%Y %H:%M" ~/Camera/ocs-camera_$DATE.jpg &&
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
