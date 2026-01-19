'''
This script demonstrates how to use the pqharp module to plot a simple countrate chart for all MultiHarp channels.
Every time the script is run the new countrates will be added to a global list and ploted.
'''
## Basic PQ imports
import pqharp as pqh
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

def add_global_count_rates() -> list:
    # check if global_count_rates already exists
    if not 'global_count_rates' in globals():
        global global_count_rates
        global_count_rates = []
    else:
        if not type(global_count_rates) == list:
            print('global_count_rates is not a list.')
            return

    cnts = pqh.get_all_countrates('MultiHarp')
    global_count_rates.append(cnts)
    return global_count_rates

if __name__ == '__main__':
    count_rates = add_global_count_rates()
    for i in range(1, len(count_rates[0])):
        y = [cnt[i] for cnt in count_rates]
        pqt.plot(y = y, name = 'Channel ' + str(i))