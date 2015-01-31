#!/bin/bash
cd $(dirname "$(readlink -fn "$0")")
screen -ls | grep botsession && screen -x botsession -X stuff "^C"
screen -ls | grep webserver && screen -x webserver -X stuff "^C"
pip install -r requirements.txt
git submodule init
git submodule update
rm bastard.sqlite
screen -S botsession python bot.py
screen -S webserver python webserver.py
