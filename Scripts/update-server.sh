#!/bin/bash

camera_file=$(cd ~/Camera; ls | sort -n | tail -n 1);
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING SERVER UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && echo 'updating databases' && rsync -u -r ~/Databases/ username@perpetual.voyage:perpetual.voyage/db/ && echo ' -done'
echo '' && echo '' && echo 'updating webcam' && rsync -u ~/Camera/$camera_file username@perpetual.voyage:perpetual.voyage/img/cam01.jpg && echo ' -done'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
