#!/bin/bash

yum -y install epel-release
yum -y install python36 python36-devel python36-pip
yum -y install docker-compose curl make gcc git unzip wget

cd /home/django && python3 -m venv /home/django/xs_venv/

cd /home/django/xx-scan && ../xs_venv/bin/python apps/manage.py collectstatic && \
../xs_venv/bin/python apps/manage.py makemigrations && \
../xs_venv/bin/python apps/manage.py migrate && \
../xs_venv/bin/python tests/2019_05_24_test_configparsecli.py && \
../xs_venv/bin/python tests/2019_06_03_test_workspace.py



