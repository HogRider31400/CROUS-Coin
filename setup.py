

import subprocess
import sys

def launch_cmd(cmd):

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode())
    process.wait()
    return process.returncode

def setup():
    launch_cmd("python -m ensurepip --default-pip")
    launch_cmd("python -m pip install --upgrade pip")
    launch_cmd("python -m pip install pycryptodome")
    launch_cmd("python -m pip install p2pd")