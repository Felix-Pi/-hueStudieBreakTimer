# hueStudyBreakTimer
> blink hue lights and show desktop notification


I tend to forget making breaks, so I created this little script to remind me ever hour to make a break by blinking my lights and showing a desktop notification.

### Prerequisites
made for MacOS

## Configuration
Configuration is pretty easy. `config.py` contains `ip` and `api_key` of the philips hue bridge.

`hueStudyBreakTimer.py` contains the timers parameter 

`hueStudyBreakTimer.sh` contains path to `hueStudyBreakTimer.py`

Creation of api_key is not part of this script (More information: [Hue API](https://developers.meethue.com/develop/get-started-2/))

### hueStudyBreakTimer.sh
Change path

### config.py
```python
ip = '' #hue bridge ip address
api_key = '' #hue bridge api key

```


### hueStudyBreakTimer.py
```python
    hue = Hue(ip=ip, api_key=api_key, notification=True) #notification can be turned on/off

    hue.timer(room_id=1, planned_runtime_in_hours=10, learn_perioud_in_min=60, break_perioud_in_min=5)
```

## Usage

```
Usage: hueStudyBreakTimer.sh [OPTIONS]

  starts hueStudyBreakTimer

Options:
  stop     stops hueStudyBreakTimer
```




## Create desktop icon with automator
Action > execute shell script

### start
```
sh PATH/hueStudyBreakTimer.sh &>/dev/null &
```

## stop
```
sh PATH/hueStudyBreakTimer.sh stop
```
