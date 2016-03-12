#!/bin/bash
##
echo'' && echo '' && echo '----------------------------------------' && echo '** RUNNING FULL BACKUP **' && echo '----------------------------------------' && echo '' && echo '' && sudo rm -f ~/OnboardComputerSystem_backup_full.tar.gz && tar --exclude='music' --exclude='OnboardComputerSystem_backup.tar.gz' --exclude='OnboardComputerSystem_backup_full.tar.gz' -zcvf ~/OnboardComputerSystem_backup_full.tar.gz ~/ && echo '' && echo '' && echo '----------------------------------------' && echo '** DONE **' && echo '----------------------------------------' && echo '' && echo ''
