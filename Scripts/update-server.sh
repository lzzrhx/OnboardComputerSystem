#!/bin/bash

camera_file=$(cd ~/Camera; ls | sort -n | tail -n 1);
#rsync -u -r ~/Databases/ laser_wolf@perpetual.voyage:perpetual.voyage/db/ &&
#rsync -u $camera_file laser_wolf@perpetual.voyage:perpetual.voyage/img/cam01.jpg
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING SERVER UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && echo 'updating databases' && rsync -u -r ~/Databases/ laser_wolf@perpetual.voyage:perpetual.voyage/db/ && echo ' -done'
echo '' && echo '' && echo 'updating webcam' && rsync -u ~/Camera/$camera_file laser_wolf@perpetual.voyage:perpetual.voyage/img/cam01.jpg && echo ' -done'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
