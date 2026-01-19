'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

dev = 'Attenuator_1'
param = 'Position'

## Get the current value of the device parameter
val = pqd.get_value(dev, param)

## Change the value of the device parameter and print it
# for this demo: increment the value by 10 and take the modulo 100 to ensure that the value is between 0 and 99
val = val + 10
val = val % 100
pqd.set_value(dev, param, val)
# get the changed value of the device parameter and print it
val = pqd.get_value(dev, param)
print(f'Current value of parameter {param} on device {dev}: {val}')

