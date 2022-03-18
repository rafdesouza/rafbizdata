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

cycle_root = "/opt/cycle_server"
cs_cmd = cycle_root + "/cycle_server"

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

def add_slurm_fix():
#     #download slurm fix 
    _catch_sys_error(["wget","-q","-O","/tmp/cluster-init-slurm-2.5.1.txt","https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/cluster-init-slurm-2.5.1.txt"])
    _catch_sys_error(["mv", "/tmp/cluster-init-slurm-2.5.1.txt", "/opt/cycle_server/config/data/"])

def import_bizcluster():
#    _catch_sys_error(["wget", "-q", "-O", "/tmp/slurm-bizcustom.txt", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/slurm-bizcustom.txt"])
#    _catch_sys_error(["wget", "-q", "-O", "/tmp/params.json", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/params.json"])
    _catch_sys_error(["cyclecloud", "import_cluster","Slurm3", "c","Slurm", "- f", "/tmp/slurm-bizcustom.txt", "-p", "/tmp/params.json"])
    

import_bizcluster()