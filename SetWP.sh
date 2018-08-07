#!/bin/bash

./ImgCalc.py
gsettings set org.gnome.desktop.background picture-uri $(cat saveLocation.txt)
