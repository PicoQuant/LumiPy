'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Image scan parameter
print('Set image scan parameter:')
## set scan_speed
pql.measurement.img_conf.scan_speed = 10
print('  ScanSpeed: ', pql.measurement.img_conf.scan_speed)
## set num_frames
pql.measurement.img_conf.num_frames = 2
print('  NumFrames: ', pql.measurement.img_conf.num_frames)

## Scan parameter (Overview)
print('\nSet scan parameter:')
## set scan_range_width
pql.measurement.scan_range_width = 123.0E-6 # in SI units (m)
scan_width = round(pql.measurement.scan_range_width * 1E6, 3)
print(f'  ScanRangeWidth: {scan_width} um')
