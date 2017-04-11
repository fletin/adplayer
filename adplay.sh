#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

sleep 10
export DISPLAY=:0.0
/usr/bin/unclutter -idle 15 &
sleep 5
echo "y1"
sudo DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority feh --quiet --preload --recursive --randomize --full-screen $DIR/black1920x1080.jpg &
sleep 5
echo "y2"
sudo DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 $DIR/adplay.py &

