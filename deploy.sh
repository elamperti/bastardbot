#!/bin/bash
echo $PWD
echo $CWD
pyenv local
screen -ls | grep botsession && screen -x botsession -X stuff "^C"
screen -ls | grep webserver && screen -x webserver -X stuff "^C"
pip install -r requirements.txt
git submodule init
git submodule update
rm bastard.sqlite
screen -S botsession -d -m python bot.py
screen -S webserver -d -m python webserver.py
