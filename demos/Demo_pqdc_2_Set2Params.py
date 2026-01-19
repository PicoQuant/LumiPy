'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

## Set parameter values on two devices simultaneously
devs = ['Attenuator_1', 'Attenuator_2']
params = ['Position', 'Position']

val = pqd.get_value(devs[0], params[0])
val = val + 10
val = val % 100
vals = [val, val]

hdl = pqd.create_transaction()
for dev, param, val in zip(devs, params, vals):
    pqd.set_value(dev, param, val, hdl)
req_id = pqd.start_transaction(hdl)
pqd.wait_until_done(req_id)
pqd.destroy_transaction(hdl)
