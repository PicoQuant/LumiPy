'''
This script demonstrates the use of a helper function to retrieves the device and parameter names for a laser assembly of the given wavelength.
A laser assembly is made up of a laser head, attenuator, main attenuator and shutter.
The device and parameter names are ment to be used with the pqdc module to access these devices.
'''
import pqlumi as pql

las, att, att_main, shut = pql.get_pqdc_laser_assembly(640)
print(att)
print(att_main)
print(shut)
print(las)
