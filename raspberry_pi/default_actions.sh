#!/bin/bash

# Setting audio output to headset port. 1- headset port, 2- HDMI
amixer cset numid=3 1

#Installing required alsa tools
sudo apt-get install libasound-dev
sudo apt-get install alsa-tools alsa-utils