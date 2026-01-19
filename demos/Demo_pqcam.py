'''
This script provides some code snippets demonstrating the use of the pqcam module.
'''
## Basic PQ imports
import pqcam as pqc
import pqtool as pqt

## Help for PQ imports
#help(pqcam)
#help(pqt)


print('Module version: ', pqc.get_version())

## Get and print all available camera device names
devs = pqc.get_device_names()
print('\nAvailable camera names:')
for dev in devs:
    print('  ', dev)

## Take first device and get all available parameters and print their names and values
dev = devs[0]
print('\nDeviceName: ', dev)
params = pqc.get_param_names(dev)
for param in params:
    print('  ', param, ': ', pqc.get_value(dev, param))


## Get an image from device and show it on ImageView 1
img = pqc.get_image(dev)
print('\nImage shape: ', img.shape)
pqt.show_image(img, dev, 1)

## Change the gain and get another image and show it on ImageView 2
var = pqc.get_value(dev, 'cpGain') # save current value
try:
    pqc.set_value(dev, 'cpGain', 50)
    print('\nGain was set to: ', pqc.get_value(dev, 'cpGain'), '%')
    pqt.gui_sleep(200) # wait to make sure a new image has been queued by the camera
    img = pqc.get_image(dev)
    pqt.show_image(img, dev + '(Gain 50%)', 2)
finally:
    pqc.set_value(dev, 'cpGain', var) # restore value
    print('\nGain was set back to: ', pqc.get_value(dev, 'cpGain'), '%')
