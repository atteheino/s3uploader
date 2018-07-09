#!/bin/bash

nohup python3 ../src/main.py -d /var/ftp/videoftp/files -p <profile> -b <bucket> -i 60 start > /dev/null 2>&1 & disown