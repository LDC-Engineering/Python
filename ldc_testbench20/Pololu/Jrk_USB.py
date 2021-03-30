# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:20:10 2020

@author: wadre
"""


# Uses jrk2cmd to send and receive data from the Jrk G2 over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Jrk's input mode must be "Serial / I2C / USB".
 
import subprocess
import yaml
 
def jrk2cmd(*args):
  return subprocess.check_output(['jrk2cmd'] + list(args))
 
status = yaml.safe_load(jrk2cmd('-s', '--full'))
 
feedback = status['Feedback']
print("Feedback is {}.".format(feedback))
 
target = status['Target']
print("Target is {}.".format(target))
 
new_target = 2248 if target < 2048 else 1848
print("Setting target to {}.".format(new_target))
 
jrk2cmd('--target', str(new_target))