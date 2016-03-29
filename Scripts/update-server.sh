#!/bin/bash

camera_file=$(cd ~/Camera; ls | sort -n | tail -n 1);
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING SERVER UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && echo 'updating databases' && rsync -u -r ~/Databases/ username@website.com:folder/db/ && echo '- DONE'
echo '' && echo '' && echo 'updating webcam' && rsync -u ~/Camera/$camera_file username@website.com:folder/img/cam01.jpg && echo '- DONE'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
