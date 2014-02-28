import json
import random
import subprocess
from internet_spaceships import firmware
import sys

sys.path.insert(0, 'internet_spaceships')

def test(ship):
    read_data = open('internet_spaceships/test_files/input.json').read()
    subprocess.call("python internet_spaceships/firmware.py '{}'".format(
        read_data),
                    shell=True)


if __name__ == '__main__':
    ship = firmware.Firmware()
    test(ship)
