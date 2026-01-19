'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql
import pqtool as pqt

## Start a point measurement
#USR_SET = 'MyFCSSettings' <- enter your user settings name here
#pql.measurement.load_user_setting(USR_SET)

pql.measurement.point_conf.stop_on_meas_time = True
pql.measurement.point_conf.meas_time = 10 # in SI units (s)
pql.measurement.start_meas('point')
print('Measurement started')
while True:
    if not pql.measurement.meas_status():
        break
    pqt.gui_sleep(100)
print('ElapsedMeasTime: ', pql.measurement.get_elapsed_meas_time(), ' s\n')

## Get available live analyses for point measurements configured in Luminosa SW
print('Live Analyses:')
anas = pql.measurement.get_analysis_names()
print('  ', anas)
plt_idx = 1
for ana in anas:
    print('\nAnalysis name: ', ana)

    # curves
    cts = pql.measurement.get_analysis_curve_types(ana)
    print('    Num curves: ', len(cts))
    for ct in cts:
        print('      Curve name: ', ct)
        curve = pql.measurement.get_analysis_curve(ana, ct)
        print('        Curve keys: ', curve.keys())
        pqt.plot(curve['data_x'], curve['data_y'], curve['name'], plt_idx)
        plt_idx += 1

    # params
    pts = pql.measurement.get_analysis_param_types(ana)
    print('    Num param types: ', len(pts))
    for pt in pts:
        print('      Param type: ', pt)
        params = pql.measurement.get_analysis_param(ana, pt)
        print('        Num params', len(params))
        for param in params:
            print('          Param keys: ', param.keys())
