"""
USE CASE:  Multi-ROIs - Time Lapse
The user defines Multiple rectangular ROIs (e.g. 20 ROIs: #1 - #20)
In each ROI a 100-frames-image is acquired, for all ROIs.
Then the system waits for 1 hour and then again a 100-frames-image is acquired for all ROIs.
This cycle  is repeated for 5 iterations in total.
The same variant can be used while instead of Time-lapse a z-stack is acquired in each ROI.

To use this script see the 'User Input' section below.
"""

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

## External imports
import numpy as np

## User Input #######################################################################
USR_SET = '' #'LumiPy_UC_MultiRoi'
## parameters according to loaded/active USR_SET
ANA_NAME_FLIM = 'FLIM'
ANA_IMG_INT = 'Intensity'
ANA_IMG_FLT = 'Fast Lifetime'

ANA_NAME_HISTO = 'TCSPC histogram'
ANA_CRV = 'AutoR Detector 2'
ANA_PARAM = 'AutoR Detector 2'

##
NUM_FRAMES_PER_ROI = 2
NUM_REPEATS = 2
WAIT_BETWEEN_REPEATS = 1 # in sec.

## use global_rois defined elsewhere (e.g. add_global_rois.py)
USE_GLOBAL_ROIS = False
## or define rois manually
SCAN_LEFT = pql.measurement.scan_range_left
SCAN_TOP = pql.measurement.scan_range_top

MY_ROIS =  [
         {
            'name'  : 'Overview',
            'left'  : SCAN_LEFT,
            'top'   : SCAN_TOP,
            'width' : 100.0*1E-6,
            'height': 100.0*1E-6,
         },
         {
            'name'  : 'ROI 1',
            'left'  : SCAN_LEFT + 25.0*1E-6,
            'top'   : SCAN_TOP  + 25.0*1E-6,
            'width' : 50.0*1E-6,
            'height': 50.0*1E-6,
         },
         {
            'name'  : 'ROI 2',
            'left'  :  SCAN_LEFT + 50.0*1E-6,
            'top'   :  SCAN_TOP  + 50.0*1E-6,
            'width' : 10.0*1E-6,
            'height': 10.0*1E-6,
         },
        ]
## End User Input ###################################################################

def print_scan_range():
    print('Scan range:')
    print('  Left: ', pql.measurement.scan_range_left*1E6, ' um')
    print('  Top: ', pql.measurement.scan_range_top*1E6, ' um')
    print('  Width: ', pql.measurement.scan_range_width*1E6, ' um')
    print('  Height: ', pql.measurement.scan_range_height*1E6, ' um')

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## set meas duration to num frames
    pql.measurement.img_conf.stop_on_photons_in_brightest_px = False
    pql.measurement.img_conf.stop_on_meas_time = False
    pql.measurement.img_conf.stop_on_num_frames = True
    pql.measurement.img_conf.num_frames = NUM_FRAMES_PER_ROI

    ## assign roi list
    if USE_GLOBAL_ROIS and 'global_rois' in globals() and type(global_rois) == list:
        rois = global_rois
    else:
        rois = MY_ROIS

    ## start measurement loop
    for i in range(NUM_REPEATS):
        for roi in rois:
            ## set roi
            pql.measurement.scan_range_left = roi['left']
            pql.measurement.scan_range_top = roi['top']
            pql.measurement.scan_range_width = roi['width']
            pql.measurement.scan_range_height = roi['height']
            print_scan_range()

            ## start measurement
            pql.measurement.start_meas('image')
            print('Measurement started')
            while True:
                if not pql.measurement.meas_status():
                    break
                pqt.gui_sleep(100)

                ## get intensity image and show on ImgView1
                img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_INT)
                img = np.array(img['img_data'])
                pqt.show_image(img, 'Intensity ' + roi['name'], 1)

                ## get fast lifetime image and show on ImgView2
                img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_FLT)
                img = np.array(img['img_data'])
                pqt.show_image(img, 'Fast Lifetime ' + roi['name'], 2)

                ## get decay and show on P1
                decay = pql.measurement.get_analysis_curve(ANA_NAME_HISTO, ANA_CRV)
                pqt.plot(decay['data_x'], decay['data_y'], roi['name'], 1)

            print('Measurement stopped')
            print('-------------------------------------------------------------')

            ## get intensity image and show on Imgview1
            img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_INT)
            img = np.array(img['img_data'])
            pqt.show_image(img, 'Intensity ' + roi['name'], 1)

            ## get fast lifetime image and show on Imgview2
            img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_FLT)
            img = np.array(img['img_data'])
            pqt.show_image(img, 'Fast Lifetime ' + roi['name'], 2)

            ## get decay and show on P1
            decay = pql.measurement.get_analysis_curve(ANA_NAME_HISTO, ANA_CRV)
            pqt.plot(decay['data_x'], decay['data_y'], roi['name'], 1)

            ## get and print fit parameters
            param_types = pql.measurement.get_analysis_param_types(ANA_NAME_HISTO)
            if (param_types != None) and (ANA_PARAM in param_types):
                print(param_types)
                print(ANA_PARAM)
                params = pql.measurement.get_analysis_param(ANA_NAME_HISTO, ANA_PARAM)
                if params != None:
                    for param in params:
                        print(param)

        pqt.gui_sleep(WAIT_BETWEEN_REPEATS * 1000)

if __name__ == '__main__':
    main()
    print('Done.')
