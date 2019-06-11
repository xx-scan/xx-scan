import os
import sys

from src import django_setup

def test():
    django_setup()
    from scan.api.mudules.scan_v2.upgrade.masscan import msjson2cache
    print(msjson2cache())


if __name__ == '__main__':
    test()
