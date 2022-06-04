#!/bin/bash

mysql -uroot -p1111 -e 'create database miniter'
mysql -uroot -p1111 -Dminiter < ./sql/create_table.sql
mysql -uroot -p1111 -Dminiter -e 'show tables;'
