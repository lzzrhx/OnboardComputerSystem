#!/bin/bash

#rsync -u ~/db/ocs.db laser_wolf@perpetual.voyage:perpetual.voyage/db/ocs.db &&
#rsync -u ~/db/gps.db laser_wolf@perpetual.voyage:perpetual.voyage/db/gps.db &&
#rsync -u ~/db/weather.db laser_wolf@perpetual.voyage:perpetual.voyage/db/weather.db &&
rsync -u -r ~/db/ laser_wolf@perpetual.voyage:perpetual.voyage/db/ &&
rsync -u ~/pictures/cam01.jpg laser_wolf@perpetual.voyage:perpetual.voyage/img/cam01.jpg
