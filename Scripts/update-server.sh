#!/bin/bash

echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING SERVER UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && echo 'copying databases' && rsync -u -r ~/Databases/ username@website.com:folder/db/ && echo '- DONE'
echo '' && echo '' && echo 'copying camera files' && rsync -u -r ~/Camera/ username@website.com:folder/img/camera/ && echo '- DONE'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
