#!/bin/bash

echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING UPDATE **' && echo '----------------------------------------'
echo '' && echo '' && sudo apt-get update
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING UPGRADE **' && echo '----------------------------------------'
echo '' && echo '' && sudo apt-get upgrade
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING AUTOREMOVE **' && echo '----------------------------------------'
echo '' && echo '' && sudo apt-get autoremove
echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING CLEAN **' && echo '----------------------------------------'
echo '' && echo '' && sudo apt-get clean && echo 'clean finished'
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
