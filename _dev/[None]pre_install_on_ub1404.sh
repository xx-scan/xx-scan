#!/usr/bin/env bash

cat > /etc/apt/sources.list <<- EOF
deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
EOF

# 先安装一些常用工具
apt-get -y update && apt-get install -y wget curl git make gcc unzip

## 安装 redis 和 mysql
#apt-get -y install mysql-server redis-server

## 安装 docker-ce
apt-get update && apt-get -y install apt-transport-https \
ca-certificates curl software-properties-common && \
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add - && \
add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" && \
apt-get -y update && apt-get install -y docker-ce=17.12.1~ce-0~ubuntu

# /etc/init.d/mysql start && /etc/init.d/redis-server start
## 安装 python3.6
# apt-get install software-properties-common python-software-properties
add-apt-repository ppa:jonathonf/python-3.6 && \
apt-get -y update && apt-get -y install python3.6

apt-get install python3-pip && pip3 install virtualenv

## 放置编译出错相关的安装辅助工具包
apt-get install -y python-dev python3-dev python3.6-dev\
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev

venv_list=('/home/django/xs_venv' '/home/django/cso_venv')

{ mkdir -p /home/django/xs_venv } || {echo "文件夹已存在"}

virtualenv -p /usr/bin/python3.6 /home/django/xs_venv


cd /home/django && git clone https://github.com/xx-scan/xx-scan && \
cd xx-scan && ../xs_venv/bin/pip install -r requirements/requirements.txt


## 最终放弃; 除非所有的工具都在docker中。

