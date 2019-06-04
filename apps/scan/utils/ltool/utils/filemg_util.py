import re

import filelock
def file_lock_read(file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        return open(file_path, "r+", encoding="utf-8").read()
    finally:
        _flock.release()


def file_lock_write(write_str, file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        open(file_path, "w+", encoding="utf-8").write(write_str)
    finally:
        _flock.release()


def file_lock_add(write_str, file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        open(file_path, "a", encoding="utf-8").write(write_str)
    finally:
        _flock.release()

def write_str2file(file, txtstr):
    try:
        # with open(file, "w+", encoding="utf-8") as f:
        #     f.write(txtstr)
        #     f.close()
        file_lock_write(file_path=file, write_str=txtstr)
        return True
    except:
        return False
