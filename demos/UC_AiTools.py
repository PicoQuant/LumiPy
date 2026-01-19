"""
USE CASE:  AI Tools for e.g. cell segmentation
The user records an image with measurement parameters set in the Luminosa GUI.
The Intensity or Fast Lifetime image is then used for AI tools like segmentation.

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
USR_SET = '' #LumiPy_UC_AiTools
## parameters according to loaded/active USR_SET
ANA_NAME = 'FLIM'
ANA_IMG_INT = 'Intensity'
ANA_IMG_FLT = 'Fast Lifetime'
## End User Input ###################################################################

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## start measurement
    pql.measurement.start_meas('image')
    print('Measurement started')
    while True:
        if not pql.measurement.meas_status():
            break
        pqt.gui_sleep(100)
    print('Measurement stopped')

    ## get Intensity and Fast Lifetime image and show on ImageView 1 & 2
    img = pql.measurement.get_analysis_image(ANA_NAME, ANA_IMG_INT)
    img_int = np.array(img['img_data'])
    pqt.show_image(img_int,'FLIM Intensity', 1)
    img = pql.measurement.get_analysis_image(ANA_NAME, ANA_IMG_FLT)
    img_flt = np.array(img['img_data'])
    pqt.show_image(img_flt,'Fast Lifetime', 2)

    ## add your AI tools (e.g. image segementation) here

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
