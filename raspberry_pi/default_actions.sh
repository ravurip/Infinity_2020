#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

#Installing required alsa tools
sudo apt-get install git
sudo apt-get install libasound-dev
sudo apt-get install alsa-tools alsa-utils

# Setting audio output to headset port. 1- headset port, 2- HDMI
amixer cset numid=3 1
