#!/bin/bash

cd opt
wget http://www.tildeslash.com/monit/dist/monit-4.8.2.tar.gz
tar -zxvf monit-4.8.2.tar.gz
cd monit-4.8.2
./configure
make
make install
cp monitrc /etc/monitrc

# Configuration for monitrc: 
# https://www.cyberciti.biz/tips/howto-monitor-and-restart-linux-unix-service.html