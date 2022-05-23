#!/bin/bash

apt install default-mysql-server

service mysql start

while [ ${status:-3} -ne 0 ]
do
	sleep 2
	service mysql status > /dev/null 
	status=$?
done	

echo "##### mysql started ####"

mysql_secure_installation
