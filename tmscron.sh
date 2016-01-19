#!/bin/sh
TMSPATH=$PWD
mkdir -p $TMSPATH/tmsApp/crontasks
#TODO: delete tmp file
CRONPATH=$TMSPATH/tmsApp/crontasks
touch $CRONPATH/getStatus
echo "*/5 * * * * python $TMSPATH/manage.py getAllStatus" > $CRONPATH/getStatus
crontab $CRONPATH/getStatus

