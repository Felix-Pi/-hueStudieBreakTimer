#!/bin/sh

if [ "$1" = "stop" ]; then
    kill $(ps -A | grep "[h]ueStudyBreakTimer.py" | awk '{print $1}')
    exit 0
fi

python /PATH/hueStudyBreakTimer/hueStudyBreakTimer.py &
