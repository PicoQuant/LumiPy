'''
This script provides some code snippets demonstrating the use of the pqharp module.
'''
## Basic PQ imports
import pqharp as pqh

## Help for PQ imports
#help(pqh)

print('Module version: ', pqh.get_version())

## Get and print all available parameter for a MultiHarp device
params = pqh.get_param_names('MultiHarp')
print('\nAvailable parameters for MultiHarp:')
for param in params:
    if param.startswith('pa'): # a channel parameter
        for chan in range(0, pqh.get_channel_count('MultiHarp')):
            print('  ', param, ' (' + str(chan) + '): ', pqh.get_value('MultiHarp', param, chan))
    else:
        print('  ', param, ': ', pqh.get_value('MultiHarp', param))

## Get and print additional infos
print('\nInfo:')
print('  ChannelCount: ', pqh.get_channel_count('MultiHarp'))
print('  Flags: ', pqh.get_flags('MultiHarp'))

## Get all available countrates
print('\nCountrates:')
cnts = pqh.get_all_countrates('MultiHarp')
for i, cnt in enumerate(cnts):
    print('  Channel ', i, ': ', cnt, ' cps')
