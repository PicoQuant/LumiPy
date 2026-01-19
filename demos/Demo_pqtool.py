'''
This script provides some code snippets demonstrating the use of the pqtool module.
'''
## Basic PQ imports
import pqtool as pqt

## Help for PQ imports
#help(pqt)

## External imports
import numpy as np


print('Module version: ', pqt.get_version())

## Plot some curves to PlotView 1 to 4
x = np.linspace(0, 10, 1000)
y = 100 * np.sin(x) + np.random.randn(1000)
 
pqt.plot(None, y, 'MyCurve (no X)')

pqt.plot(x, y, 'MyCurve', 2)
y = 80 * np.sin(2*x) + np.random.randn(1000) 
pqt.plot(x, y, 'MyCurve 2', 2)

y = 10 * np.sin(x) + np.random.randn(1000)
x_ = 10 * np.cos(x) + np.random.randn(1000)  
pqt.plot(x_, y, 'MyCurve (scatter)', 3)

for i in range(20):
    y = np.sin(2*x + i)
    print('Plot curve ', i, '/20')
    pqt.plot(x, y, 'MyCurve (with gui sleep)', 4)
    pqt.gui_sleep(100)

## Plot some images to ImageView 1 to 2
img = []
allZeroes = []
allOnes = []
for i in range(0,800):
    allZeroes.append(0)
    allOnes.append(1)
allZeroes += 0.1 * np.random.randn(800)    
allOnes += 0.1 * np.random.randn(800)
 
for i in range(0, 400):
    img.append(allZeroes)
for i in range(0,400):
    img.append(allOnes)
img = np.array(img)

pqt.show_image(img, 'MyImage 1', 1)
img = np.flipud(img)
pqt.show_image(img, 'MyImage 2', 2)
