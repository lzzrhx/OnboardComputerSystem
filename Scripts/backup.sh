#!/bin/bash

echo '' && echo '' && echo '----------------------------------------' && echo '** RUNNING BACKUP **' && echo '----------------------------------------'
echo '' && echo '' && sudo rm -f ~/OnboardComputerSystem_backup.tar.gz && tar --exclude='Charts' --exclude='Documents' --exclude='Music' --exclude='OnboardComputerSystem_backup.tar.gz' --exclude='OnboardComputerSystem_backup_full.tar.gz' -zcvf ~/OnboardComputerSystem_backup.tar.gz ~/
echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
