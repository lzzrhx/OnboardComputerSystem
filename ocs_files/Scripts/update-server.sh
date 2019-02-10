#!/bin/bash

echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING SERVER UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && echo 'copying databases' && rsync -u -r ~/.OnboardComputerSystem/databases/ username@website.com:folder/db/ --delete && echo '- DONE'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
