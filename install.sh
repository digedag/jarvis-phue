#!/bin/bash
# Use only if you need to perform changes on the user system such as installing software
sudo pip install phue
sudo -a $(pwd)/plugins_installed/jarvis-phue/config.ini.dist $(pwd)/plugins_installed/jarvis-phue/config.ini
