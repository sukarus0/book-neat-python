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

mysql -uroot -p1111 -Dmysql -e 'UPDATE user SET plugin="mysql_native_password" WHERE user="root"; FLUSH PRIVILEGES;'
mysql -uroot -p1111 -Dmysql -e 'SELECT user, plugin, host FROM user;'
