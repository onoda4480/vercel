#!/usr/bin/env python3
import subprocess

cmd = "ls -l"
runcmd = subprocess.call(cmd.split())
print (runcmd)