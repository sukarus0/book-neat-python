#!/bin/bash

mysql -uroot -p1111 -Dmysql -e 'UPDATE user SET plugin="unix_socket" WHERE user="root"; FLUSH PRIVILEGES;'

service mysql stop

apt remove --purge mysql*
