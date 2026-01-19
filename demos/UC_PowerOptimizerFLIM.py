"""
USE CASE: Power Optimizer for FLIM
Set the proper excitation power for FLIM such that no pile up and/or no or only low bleaching is taking place.
This script changes the excitation power while recording the TCSPC decay and the overall intensity.
The optimal power could be the maximum power where
a)  no artifacts appear in the TCSPC decay
b)  no or low bleaching occurs within 10 consecutive frames

To use this script see the 'User Input' section below.
"""

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Low level PQ device imports
import pqdc as pqd

## Help for PQ imports
#help(pql)
#help(pqt)
#help(pqd)

## External imports
import numpy as np

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_OptimizeFLIM
## parameters according to loaded/active usr_set
ANA_NAME      = 'TCSPC histogram'
#ANA_CRV = 'AutoR Detector 2'
#WL = 640    ## wavelength in nm
ANA_CRV = 'Cy3 Detector 4'
WL = 530    ## wavelength in nm

## attenuation parameters
ATT_MIN = 0
ATT_MAX = 100
ATT_DELTA = 20

NUM_FRAMES_1 = 1
NUM_FRAMES_2 = 10
## End User Input ###################################################################

def print_anas():
    anas = pql.measurement.get_analysis_names()
    for ana in anas:
        print('Analysis: ', ana)
        crv_types = pql.measurement.get_analysis_curve_types(ana)
        img_types = pql.measurement.get_analysis_image_types(ana)
        param_types = pql.measurement.get_analysis_param_types(ana)

        if crv_types != None:
            for crv_type in crv_types:
                print('  Curve type: ', crv_type)
        if img_types != None:
            for img_type in img_types:
                print('  Image type: ', img_type)
        if param_types != None:
            for param_type in param_types:
                print('  Parameter type: ', param_type)

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## get attenuator from wavelength
    _, att, _, _ = pql.get_pqdc_laser_assembly(WL)
    att_dev = att['device']
    att_param = att['param']

    ## set meas duration to num frames
    pql.measurement.img_conf.stop_on_num_frames = True
    pql.measurement.StopOnPhotonsInBrightestPx = False
    pql.measurement.img_conf.stop_on_meas_time = False

    ## prepare lists and start measurement loop
    att_vals = np.arange(ATT_MIN, ATT_MAX + 1, ATT_DELTA)
    bleaching = np.zeros(len(att_vals))
    bleaching_abs = np.zeros(len(att_vals))
    for i, att_val in enumerate(att_vals):
        ## set attenuation of laser attenuator
        pqd.set_value(att_dev, att_param, att_val)
        pos = pqd.get_value(att_dev, att_param)
        att_vals[i] = pos
        print('Attenuator: ', pos, '%')

        ## set num frames to 'num_frames1' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_1
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## print available analyses, curve types, image types and parameter types
        #print_anas()

        ## get decay and calculate count rate
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        counts0 = sum(decay['data_y'])
        print('Counts(0): ', counts0)

        ## set num frames to 'num_frames2' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_2
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## get decay, normalize decay and plot on P1
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        m = max(decay['data_y'])
        ndecay = [x / m for x in decay['data_y']]
        ndecay_x = np.multiply(decay['data_x'], 1E9) ## in ns
        pqt.plot(ndecay_x, ndecay, 'Att: ' + str(att_val) + ' %', 1)

        ## set num frames to 'num_frames1' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_1
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## get decay and calculate count rate
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        counts1 = sum(decay['data_y'])
        print('Counts: ', counts1)

        ## calc bleaching and plot on P2
        bleaching[i] = (1 - counts1 / counts0) * 100
        pqt.plot(att_vals, bleaching, 'Bleaching', 2)

        ## add your stop condition here (bleaching, pile up, etc.)
        ## e.g. if bleaching[i] > 30: break

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
