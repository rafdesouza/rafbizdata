import os
import sys
import argparse
import json
import re
import random
from string import ascii_uppercase, ascii_lowercase, digits
import subprocess
from subprocess import CalledProcessError, run
from os import path, listdir, chdir, fdopen, remove
from urllib.request import urlopen, Request
from shutil import rmtree, copy2, move
from tempfile import mkstemp, mkdtemp
from time import sleep

def _catch_sys_error(cmd_list):
    try:
        output = subprocess.run(cmd_list, capture_output=True, check=True, text=True).stdout
        print("Command list:", cmd_list)
        print("Command output:", output)
        return output
    except CalledProcessError as e:
        print("Error with cmd: %s" % e.cmd)
        print("Output: %s" % e.output)
        raise

def import_bizcluster():
#    _catch_sys_error(["wget", "-q", "-O", "/tmp/slurm-bizcustom.txt", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/slurm-bizcustom.txt"])
#    _catch_sys_error(["wget", "-q", "-O", "/tmp/params.json", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/params.json"])

    try: 
        cmd_list = ["cyclecloud", "import_cluster","- f", "/tmp/slurm-bizcustom.txt", "-p", "/tmp/params.json"]
        output = subprocess.run(cmd_list, capture_output=True).stdout
        print("Command list:", cmd_list)
        print("Command output:", output)
    
    except CalledProcessError as e:
        print("Error adding the customized slurm cluster")

import_bizcluster()