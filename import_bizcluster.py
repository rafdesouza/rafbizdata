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

def get_vm_metadata():
    metadata_url = "http://169.254.169.254/metadata/instance?api-version=2017-08-01"
    metadata_req = Request(metadata_url, headers={"Metadata": True})

    for _ in range(30):
        print("Fetching metadata")
        metadata_response = urlopen(metadata_req, timeout=2)

        try:
            return json.load(metadata_response)
        except ValueError as e:
            print("Failed to get metadata %s" % e)
            print("    Retrying")
            sleep(2)
            continue
        except:
            print("Unable to obtain metadata after 30 tries")
            raise

def add_slurm_fix():
#     #download slurm fix 
    _catch_sys_error(["sudo", "wget","-q","-O","/tmp/cluster-init-slurm-2.5.1.txt","https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/cluster-init-slurm-2.5.1.txt"])
    _catch_sys_error(["sudo", "mv", "/tmp/cluster-init-slurm-2.5.1.txt", "/opt/cycle_server/config/data/"])

def import_bizcluster(vm_metadata):
    _catch_sys_error(["sudo", "wget", "-q", "-O", "/tmp/slurm-bizcustom.txt", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/slurm-bizcustom.txt"])
    _catch_sys_error(["sudo", "wget", "-q", "-O", "/tmp/params.json", "https://raw.githubusercontent.com/rafdesouza/rafbizdata/main/params.json"])

    # /subscriptions/<subscription-id>resourceGroups/<resource-group-name>/providers/Microsoft.Network/virtualNetworks/<virtual-network-name>/subnets/<subnet-name>
    subscription_id = vm_metadata["compute"]["subscriptionId"]
    resource_group = vm_metadata["compute"]["resourceGroupName"]
    vmName = vm_metadata["compute"]["name"]

    subnetId = "/subscriptions/" + subscription_id + "/resourceGroups/" + resource_group + "/providers/Microsoft.Network/virtualNetworks/" + "vnet" + vmName + "/virtual-network-name/subnets/compute"
    print(subnetId)

    _catch_sys_error(["/usr/local/bin/cyclecloud","import_cluster","-f", "/tmp/slurm-bizcustom.txt", "-p", "/tmp/params.json"])


def start_cluster():
    _catch_sys_error(["/usr/local/bin/cyclecloud", "start_cluster", "Slurm"])
    

# add_slurm_fix()

vm_metadata = get_vm_metadata()

import_bizcluster(vm_metadata)

# start_cluster()
