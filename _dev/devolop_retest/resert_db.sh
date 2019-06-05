#!/bin/bash

db_host=127.0.0.1
db_username=admin007
db_passwd=myadmin@816
db_name=xxscan
db_port=3306


mycli -h${db_host} -P${db_port} -u${db_username} -p${db_passwd} ${db_name} << EOF
drop database xxscan;
CREATE DATABASE blog DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
EOF