#!/bin/bash

scp ~/db/ocs.db user@perpetual.voyage:perpetual.voyage/db &&
rsync -u ~/db/gps.db user@perpetual.voyage:perpetual.voyage/db &&
rsync -u ~/db/weather.db user@perpetual.voyage:perpetual.voyage/db &&
scp ~/pictures/cam01.jpg user@perpetual.voyage:perpetual.voyage/img
