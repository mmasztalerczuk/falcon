import subprocess
import os
from time import sleep

from tracker.settings import Config


def print_function_name(method):

    def wrapped_method(*args, **kw):
        print('Executing: ' + method.__name__.replace("_", " "))
        result = method(*args, **kw)
        return result

    return wrapped_method


@print_function_name
def run_celery():
    kill_celery()
    with cd("../"):
        subprocess.Popen(['/bin/bash', 'celery_run.sh'])
        sleep(5)


@print_function_name
def kill_celery():
    subprocess.Popen(['killall', 'celery'])
    sleep(5)


@print_function_name
def create_config(user, host, dbname):
    delete_config()
    with cd("../"):
        cfgfile = open("test.ini", 'w')

        Config.add_section('Test')
        Config.set('Test', 'USER', user)
        Config.set('Test', 'HOST', host)
        Config.set('Test', 'DBNAME', dbname)
        Config.write(cfgfile)
        cfgfile.close()
        sleep(2)


def delete_config():
    with cd("../"):
        try:
            os.remove("test.ini")
        except OSError:
            pass


def run_gunicorn():
    kill_gunicorn()
    with cd("../"):
        subprocess.Popen(['gunicorn', 'main:main'])
        sleep(5)


def kill_gunicorn():
    subprocess.Popen(['killall', 'gunicorn'])


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
