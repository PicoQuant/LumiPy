'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Image scan parameter
print('Get image scan parameter:')
print('  Scan speed: ' , pql.measurement.img_conf.scan_speed)
print('  NumFrames: '  , pql.measurement.img_conf.num_frames)
print('  StopOnNumFrames: '           , pql.measurement.img_conf.stop_on_num_frames)
print('  StopOnPhotonsInBrightestPx: ', pql.measurement.img_conf.stop_on_photons_in_brightest_px)
print('  PhotonsInBrightestPx: '      , pql.measurement.img_conf.photons_in_brightest_px)
print('  StopOnMeasTime: '            , pql.measurement.img_conf.stop_on_meas_time)
print('  MeasTime: '                  , pql.measurement.img_conf.meas_time)

## Scan parameter (Overview)
print('\nGet scan parameter:')
scan_width = pql.measurement.scan_range_width # in SI units (m)
scan_width = round(scan_width * 1E6, 3)       # convert to um
print(f'  ScanRangeWidth: {scan_width} um')
print('  ScanRangeLeft: ' , pql.measurement.scan_range_left)
print('  ScanRangeTop: '  , pql.measurement.scan_range_top)
print('  ScanRangeMinX: ' , pql.measurement.scan_range_min_x)
print('  ScanRangeMaxX: ' , pql.measurement.scan_range_max_x)

## Point meas parameter
print('\nPoint meas parameter:')
print('  StopOnPhotons: '  , pql.measurement.point_conf.stop_on_photons)
print('  NumPhotons: '     , pql.measurement.point_conf.num_photons)
print('  StopOnMeasTime: ' , pql.measurement.point_conf.stop_on_meas_time)
print('  MeasTime: '       , pql.measurement.point_conf.meas_time)
print()
