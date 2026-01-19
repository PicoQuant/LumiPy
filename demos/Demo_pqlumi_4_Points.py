'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Dealing with points
print('Points:')
print('  Current points defined: ', pql.measurement.point_conf.point_list)
left = pql.measurement.scan_range_left
top = pql.measurement.scan_range_top
MY_POINTS = [(left + 5E-6, top + 5E-6),
             (left + 20E-6, top + 20E-6),
             (left + 40E-6, top + 40E-6)]
pql.measurement.point_conf.point_list = MY_POINTS
print('  New points defined: ', pql.measurement.point_conf.point_list)
