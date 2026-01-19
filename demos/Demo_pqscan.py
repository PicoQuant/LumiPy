'''
This script provides some code snippets demonstrating the use of the pqscan module.
'''
## Basic PQ imports
import pqscan as pqs
import pqtool as pqt

## Help for PQ imports
#help(pqs)
#help(pqt)

## Additional imports
import time


print('Module version: ', pqs.get_version())

dev = 'MainScanner'

## Get and print position
print('\nScanner position:')
print('  X: ', pqs.get_value(dev, 'spXPos'))
print('  Y: ', pqs.get_value(dev, 'spYPos'))
print('  Z: ', pqs.get_value(dev, 'spZPos'))

## Get and print all scan parameter
print('\nScanner parameter:')
params = pqs.get_param_names(dev)
for param in params:
    print('  ', param, ': ', pqs.get_value(dev, param))

# Start a scan for one 3 seconds
var = pqs.get_value(dev, 'spNumberOfFrames') # save number of frames
try:
    pqs.set_value(dev, 'spNumberOfFrames', -1)
    pqs.scan_stop(dev)
    pqs.scan_start(dev)
    start_time = time.time()
    print('\nScan started for 3 sec....')
    while True:
        if not pqs.is_scanning(dev):
            break
        pqt.gui_sleep(100)
        if time.time() - start_time > 3:
            pqs.scan_stop(dev)
            break 
    print('Scan stopped')
finally:
    pqs.set_value(dev, 'spNumberOfFrames', var) # restore number of frames


