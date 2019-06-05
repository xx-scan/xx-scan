import os
import sys

from src import django_setup

def test():
    django_setup()
    from scan.models.http import ServicePort, inital_ports, ports_range
    inital_ports()

    ports_range()

def inital2():
    pass


if __name__ == '__main__':
    test()
