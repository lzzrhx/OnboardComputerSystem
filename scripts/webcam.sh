#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")
fswebcam -r 1280x720 -S 99 --banner-colour "#FF303030" --line-colour "#FF303030" --text-colour "#00A9A28F" --font ProggyCleanTT:18 --shadow --timestamp "%d.%m.%Y %H:%M" ~/pictures/webcam/cam01_$DATE.jpg &&
cp ~/pictures/webcam/cam01_$DATE.jpg ~/pictures/cam01.jpg
