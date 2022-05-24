#!/bin/bash
echo "Cleaning downloads"
rm *.zip -f
echo "Checking for updates"
python3 main.py
echo "Unzipping"
unzip -o *.zip -d /mnt/REGIST
echo "Removing unnesessary files from SD"
rm /mnt/REGIST/*.doc -f
echo "Cleaning downloads"
rm *.zip -f
