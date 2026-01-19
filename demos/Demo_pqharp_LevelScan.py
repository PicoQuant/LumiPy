'''
This script demonstrates how to use the pqharp module to perform a TriggerLevel scan on one channel.
'''
## Basic PQ imports
import pqharp as pqh
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

## External imports
import numpy as np

## Define channel to scan (Channel 0 = Sync channel) and range
CHANNEL = 1

## Triggel levels in mV.
## Use positive levels for SPADs and negative levels for HPDs.
LEVELS = np.arange(0, 301, 10)  

## Scan and plot on PlotView 1
counts = np.zeros(LEVELS.size)
curr_level = pqh.get_value('MultiHarp', 'paTriggerLevel', CHANNEL)
print('Current triggel level of channel ', CHANNEL, ': ', curr_level, 'mV')
try:
    for i, level in enumerate(LEVELS):
        pqh.set_value('MultiHarp', 'paTriggerLevel', level, CHANNEL)
        print('Set TriggerLevel to ', level, ' mV')
        pqt.gui_sleep(1000)
        cnts = pqh.get_all_countrates('MultiHarp')
        counts[i] = cnts[CHANNEL]
        print('Count rate: ', counts[i], ' cps')
        pqt.plot(LEVELS, counts, 'LevelScan Chan ' + str(CHANNEL), 1)
finally:
    pqh.set_value('MultiHarp', 'paTriggerLevel', curr_level, CHANNEL)
    
