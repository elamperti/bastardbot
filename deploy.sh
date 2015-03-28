#!/bin/bash
export PYENV_VERSION="3.3.4"
export PATH="$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH"
git checkout master
git reset --hard origin/master
git pull
screen -ls | grep botsession && screen -x botsession -X stuff "^C"
screen -ls | grep webserver && screen -x webserver -X stuff "^C"
pip install -r requirements.txt --upgrade
git submodule init
git submodule update
rm bastard.sqlite
screen -S botsession -d -m python bot.py
screen -S webserver -d -m python webserver.py
