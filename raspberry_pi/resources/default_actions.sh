#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

#Installing required alsa tools
sudo apt-get install git
sudo apt-get install libasound-dev
sudo apt-get install alsa-tools alsa-utils

#install portaudio
cd /usr/src/

sudo wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
sudo tar xvfz pa_stable_v190600_20161030.tgz

cd /usr/src/portaudio/
sudo ./configure
sudo make
sudo make install
sudo ldconfig

# Setting audio output to headset port. 1- headset port, 2- HDMI
amixer cset numid=3 1

export ARANYANI_HOME=/home/pi/aranyani

mkdir -p $ARANYANI_HOME/data/audio
mkdir -p $ARANYANI_HOME/logs
mkdir -p $ARANYANI_HOME/temp