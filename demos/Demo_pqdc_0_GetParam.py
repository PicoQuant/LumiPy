'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

print('Module version: ', pqd.get_version())

# Assume that the devices database (*.db) has an entry for a device with name 'Attenuator_1'.
# Then this device should have a parameter called 'Position'
dev = 'Attenuator_1'
param = 'Position'

## To check if dev is present in the database and connected to the system, one can use the following code:
devs = pqd.get_device_names()
print('Available devices: ', devs)
if not dev in devs:
    print('Device ', dev, ' not present in database.')
    exit()

## To check if param is available on dev, one can use the following code:
params = pqd.get_param_names(dev)
print('Available parameter for device ', dev, ': ', params)
if not param in params:
    print('Parameter ', param, ' not present on device ', dev)
    exit()

## Get the current value of the device parameter and print it
val = pqd.get_value(dev, param)
print(f'Current value of parameter {param} on device {dev}: {val}')
