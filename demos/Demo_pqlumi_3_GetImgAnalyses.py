'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql
import pqtool as pqt

import numpy as np

## Get available live analyses for image measurements configured in Luminosa SW
print('Live Analyses:')
anas = pql.measurement.get_analysis_names()
print('  ', anas)

for ana in anas:
    print('\nAnalysis name: ', ana)

    # images
    its = pql.measurement.get_analysis_image_types(ana)
    print('    Num images: ', len(its))
    for it in its:
        print('      Image name: ', it)
        img = pql.measurement.get_analysis_image(ana, it)
        print('        Image keys: ', img.keys())

        img_data = np.array(img['img_data'])
        if it == 'Intensity':
            pqt.show_image(img_data, 'FLIM Intensity', 1)
        elif it == 'Fast Lifetime':
            pqt.show_image(img_data, 'Fast Lifetime', 2)

    # curves
    cts = pql.measurement.get_analysis_curve_types(ana)
    print('    Num curves: ', len(cts))
    for ct in cts:
        print('      Curve name: ', ct)
        curve = pql.measurement.get_analysis_curve(ana, ct)
        print('        Curve keys: ', curve.keys())
        pqt.plot(curve['data_x'], curve['data_y'], curve['name'])

    # params
    pts = pql.measurement.get_analysis_param_types(ana)
    print('    Num param types: ', len(pts))
    for pt in pts:
        print('      Param type: ', pt)
        params = pql.measurement.get_analysis_param(ana, pt)
        print('        Num params', len(params))
        for param in params:
            print('          Param keys: ', param.keys())


