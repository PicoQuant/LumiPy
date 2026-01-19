"""
USE CASE: Power Optimizer for FCS
A problem is how to select the proper power for FCS measurements.
The following process can help:
Record the FCS curve and calculate Mol.brightness, diffusion time and triplet fraction (in case needed) for several different excitation powers.
The maximum power used should be either the maximum power available or a power for which we are clearly in the saturation regime.

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
USR_SET = '' #LumiPy_UC_OptimizeFCS
## parameters according to loaded/active USR_SET

ANA_NAME  = 'FCS'
ANA_CRV   = 'AA'
ANA_PARAM = 'AA'
WL = 640    ## wavelength in nm

## attenuation parameters in %
ATT_MIN = 40
ATT_MAX = 100
ATT_DELTA = 20

MEAS_TIME = 30
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

    ## set meas duration to time
    pql.measurement.point_conf.stop_on_photons = False
    pql.measurement.point_conf.stop_on_meas_time = True
    pql.measurement.point_conf.meas_time = MEAS_TIME

    ## prepare lists and start measurement loop
    att_vals = np.arange(ATT_MIN, ATT_MAX + 1, ATT_DELTA)
    mol_brightness = np.zeros(len(att_vals))
    diff_time = np.zeros(len(att_vals))
    for i, att_val in enumerate(att_vals):
        ## set attenuation of laser attenuator
        pqd.set_value(att_dev, att_param, att_val)
        pos = pqd.get_value(att_dev, att_param)
        att_vals[i] = pos
        print('Attenuator: ', pos, '%')

        ## start measurement
        pql.measurement.start_meas('point')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## print available analyses, curve types, image types and parameter types
        #print_anas()

        # get fcs curve and plot on P1
        fcs_crv = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        pqt.plot(fcs_crv['data_x'], fcs_crv['data_y'], fcs_crv['name'], 1)

        # get mol.brightness and diff.time for 'Pure Diff. (Species: 1)' and plot on P2 and P3
        fcs_params = pql.measurement.get_analysis_param(ANA_NAME, ANA_PARAM)
        fsc_param = fcs_params[0]
        mol_brightness[i] = fsc_param['mol. Brt.'][0]
        diff_time[i] = fsc_param['%tau_1'][0]
        pqt.plot(att_vals, mol_brightness, 'Mol.brightness', 2)
        pqt.plot(att_vals, diff_time, 'Diff.time', 3)

        ## add your stop condition here (e.g. if mol.brightness is saturated)

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
