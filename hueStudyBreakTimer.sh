#!/bin/sh

if [ "$1" = "stop" ]; then
    kill $(ps -A | grep "[h]ueStudyBreakTimer.py" | awk '{print $1}')
    osascript -e 'display notification "StudyTimer has been stopped" with title "StudyTimer stopped"'

    exit 0
fi

python3 ~/dev/python/hueStudyBreakTimer/hueStudyBreakTimer.py &
