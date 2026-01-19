"""
USE CASE: FRAP - Fluorescence Recovery after photobleaching
Sample: live cell expressing proteins labeled with an organic dye or a Fluorescent Protein.
Lasers: 1 used for bleaching , N lasers used for imaging

    1. Select a laser for Bleaching. Set mode (pulsed /CW) , (attenuation). Defaults should be: CW & maximum power.
    2. Take a FLIM Image.
    3. Draw a rectangular or circular (circular area higher PRIO as rectangular) area as „ROI for bleaching“.
        (Explicitly stated here that a FREE ROI is not wished for this USE CASE).
        The are can be scaled and its size can be given in pixel numbers.
        Maximum number of pixels should be 100. Pixel sizes for bleaching can be as large as 200-300 nm ~ 1 PSF diameter.
    4. Draw a rectangular or circular area as reference area. Maximum number of pixels should be 100.
        Pixel sizes for bleaching can be as large as 200-300 nm ~ 1 PSF diameter.
    5. Set parameters necessary for a bleaching experiment.
        ◦ Pre bleaching part: Number of frames, scanning speed. Relevant analysis channels.
        ◦ Bleaching step: Number of frames, or total time.
        ◦ Post-bleaching part; Number of frames scanning speed. The same analysis channels as before
    6. Start bleaching experiment.
    7. Switch on active lasers and acquire the given number of frames for the „ROI for bleaching“ and the „reference area“.
        Display in an online FRAP analysis, the total number of photons per area (bleached area and reference area)as a function of of time (frame number * time per frame).
        Save the image with automated naming „PRE-BLEACH „. Save ROI mascs for „ROI for bleaching“ and „reference“ areas as ASCII files.
    8. Switch off the imaging laser, Switch off the detectors . Switch on the bleaching laser as defined in step #1.
    9. Bleach by scanning as defineds as defined in step #5 for the „ROI for bleaching“. The „reference area“ is not bleached.
        In the live FRAP analysis, note the duration of the bleaching step.
    10. Switch off the bleaching laser. Switch on the detectors. Swtich on the imaging laser and acquire images as described in post-bleaching part of step #5.
        In the live FRAP analysis, display the total number of photons per area (bleached area and reference area)as a function of of time (frame number * time per frame).
        Save the overall image with automated naming „POST-BLEACH „
    11. The online FRAP analysis is saved and can be exported as ASCII or Bitmap.
    12. If one double clicks the analysis, the one get an analysis wondow, similar to the FCS analysis.
        Basic fitting of the FRAP curve should be available recovering , mobile, immobile fraction and the fitted half-time of the recovery.

To use this script see the 'User Input' section below.
"""

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Low level PQ device imports
import pqdc as pqd
import pqscan as pqs

## Help for PQ imports
#help(pql)
#help(pqt)
#help(pqd)
#help(pqs)

## External imports
import numpy as np

## Additional imports
import time

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_FRAP
## parameters according to loaded/active USR_SET
ANA_NAME = 'FLIM'
ANA_IMG_INT = 'Intensity'
MEAS_WL = 640      ## wavelength in nm
BLEACHING_WL = 405 ## wavelength for bleaching laser in nm

## use pinhole led as shutter for bleaching step to protect detectors
LED = 'Pinhole_LED'
LED_IN_PATH = 'LEDIsInPath'

## decide if bleaching is done via a measurement or a scan
BLEACH_BY_SCAN = True

NUM_BLEACHING_FRAMES = 50
NUM_REPEATS = 30
WAIT_BETWEEN_REPEATS = 1000 # in ms

## create three rois: 1. for overview, 2. for bleaching, 3. for reference
OVERVIEW_LEFT  = -50.0*1E-6  # in m
OVERVIEW_TOP   = -50.0*1E-6
OVERVIEW_WIDTH = 100.0*1E-6
BLEACH_WIDTH   =   2.0*1E-6
MY_ROIS =  [
         {
           'name'  : 'Overview',
           'left'  : OVERVIEW_LEFT,
           'top'   : OVERVIEW_TOP,
           'width' : OVERVIEW_WIDTH,
           'height': OVERVIEW_WIDTH,
         },
         {
           'name'  : 'Bleaching area',
           'left'  : OVERVIEW_LEFT + OVERVIEW_WIDTH * 0.3,
           'top'   : OVERVIEW_TOP + OVERVIEW_WIDTH * 0.3,
           'width' : BLEACH_WIDTH,
           'height': BLEACH_WIDTH,
         },
         {
           'name'  : 'Reference area',
           'left'  : OVERVIEW_LEFT + OVERVIEW_WIDTH * 0.6,
           'top'   : OVERVIEW_TOP + OVERVIEW_WIDTH * 0.6,
           'width' : BLEACH_WIDTH,
           'height': BLEACH_WIDTH,
         },
        ]

## or use global_rois defined elsewhere (e.g. LumiPy_GetRoi.py)
USE_GLOBAL_ROIS = False
## End User Input ###################################################################

def print_scan_range():
    print('Scan range left: ', pql.measurement.scan_range_left*1E6, ' um')
    print('Scan range top: ', pql.measurement.scan_range_top*1E6, ' um')
    print('Scan range width: ', pql.measurement.scan_range_width*1E6, ' um')
    print('Scan range height: ', pql.measurement.scan_range_height*1E6, ' um')

def meas_roi(roi):
    # set roi
    pql.measurement.scan_range_left = roi['left']
    pql.measurement.scan_range_top = roi['top']
    pql.measurement.scan_range_width = roi['width']
    pql.measurement.scan_range_height = roi['height']
    print_scan_range()

    # start measurement
    pql.measurement.start_meas('image')
    print('Measurement started')
    while True:
        if not pql.measurement.meas_status():
            break
        pqt.gui_sleep(100)
    print('Measurement stopped')

def scan_roi(roi):
    # set scan range
    xs = pqd.get_value('SampleStage', 'Position_X') # in µm
    x = roi['left'] * 1E6 - xs
    ys = pqd.get_value('SampleStage', 'Position_Y') # in µm
    y = roi['top'] * 1E6 - ys
    pqs.set_value('MainScanner', 'spXPos', x)
    pqs.set_value('MainScanner', 'spYPos', y)
    pqs.set_value('MainScanner', 'spFastLength', roi['width'] * 1E6)
    pqs.set_value('MainScanner', 'spSlowLength', roi['height'] * 1E6)

    # start scan
    pqs.scan_start('MainScanner')
    print('Scan started')
    while True:
        if not pqs.is_scanning('MainScanner'):
            break
        pqt.gui_sleep(100)

def get_roi_from_image(img, img_roi, roi) -> tuple:
    img_width = img.shape[1]
    img_height = img.shape[0]

    mx = (img_width - 1) / img_roi['width']
    my = (img_height - 1) / img_roi['height']
    bx = -mx * img_roi['left']
    by = -my * img_roi['top']
    roi_ = {
        'left'  : round(mx * roi['left'] + bx),
        'top'   : round(my * roi['top'] + by),
        'width' : round(mx * roi['width']),
        'height': round(my * roi['height']),
    }
    roi_right = roi_['left'] + roi_['width']
    roi_bottom = roi_['top'] + roi_['height']
    if roi_right >= img_width or roi_bottom >= img_height or roi_['left'] < 0 or roi_['top'] < 0:
        return None

    roi_data = img[roi_['top']:roi_bottom, roi_['left']:roi_right]
    return roi_, roi_data

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## set meas duration to num frames
    pql.measurement.img_conf.stop_on_meas_time = False
    pql.measurement.img_conf.stop_on_photons_in_brightest_px = False
    pql.measurement.img_conf.stop_on_num_frames = True

    ## assign roi list
    if USE_GLOBAL_ROIS and 'global_rois' in globals() and type(global_rois) == list:
        rois = global_rois
    else:
        rois = MY_ROIS

    ## overview scan #############################################################
    meas_frames = pql.measurement.img_conf.num_frames 
    meas_roi(rois[0])

    ## get intensity image and show on ImageView1
    img = pql.measurement.get_analysis_image(ANA_NAME, ANA_IMG_INT)
    img_data = np.array(img['img_data'])
    pqt.show_image(img_data, 'Intensity', 1)

    ## get measurement laser assembly from wavelength and save current values
    meas_las, meas_att, meas_att_main, _ = pql.get_pqdc_laser_assembly(MEAS_WL)
    meas_las_val_int = pqd.get_value(meas_las['device'], meas_las['param_int'])
    meas_las_val_cw = pqd.get_value(meas_las['device'], meas_las['param_cw'])
    meas_att_val = pqd.get_value(meas_att['device'], meas_att['param'])
    meas_att_main_val = pqd.get_value(meas_att_main['device'], meas_att_main['param'])

    ## bleaching step ##############################################################
    ## get bleaching laser assembly from wavelength and save current values of laser head
    bl_las, bl_att, bl_att_main, bl_shut = pql.get_pqdc_laser_assembly(BLEACHING_WL)
    bl_las_val_int = pqd.get_value(bl_las['device'], bl_las['param_int'])
    bl_las_val_cw = pqd.get_value(bl_las['device'], bl_las['param_cw'])

    ## set values of bleaching laser assembly components
    # block adjustment of pinhole and tube lens when changing the active laser to make things faster
    pql.measurement.block_airy_adjustment(True) # saves about 700 ms between bleaching and post-bleaching step
    # create a transaction to set all values at once
    hdl = pqd.create_transaction()
    # turn off measurement laser and turn non bleaching laser
    pqd.set_value(meas_las['device'], meas_las['param_out'], False)
    pqd.set_value(bl_las['device'], bl_las['param_out'], True)
    # put led in opt. path
    pqd.set_value(LED, LED_IN_PATH, True, hdl)
    # set intensity to max, mode to cw
    pqd.set_value(bl_las['device'], bl_las['param_int'], 100, hdl)
    pqd.set_value(bl_las['device'], bl_las['param_cw'], True, hdl)
    # set attenuator and main attenuator to maximum
    pqd.set_value(bl_att['device'], bl_att['param'], 100, hdl)
    pqd.set_value(bl_att_main['device'], bl_att_main['param'], 100, hdl)
    # start transaction
    reqID = pqd.start_transaction(hdl)
    pqd.wait_until_done(reqID)
    pqd.destroy_transaction(hdl)

    if not BLEACH_BY_SCAN:
        ## either measure bleaching area definded in rois[1] for num_bleaching_framesand get reference time
        pql.measurement.img_conf.num_frames = NUM_BLEACHING_FRAMES
        meas_roi(rois[1])
        start_time = time.time()
    else:
        ## or just scan bleaching area definded in rois[1] without a measurement and hence no data recording
        # set number of scanner frames to num_bleaching_frames and open bleaching shutter
        pqs.set_value('MainScanner', 'spNumberOfFrames', NUM_BLEACHING_FRAMES)
        pqd.set_value(bl_shut['device'], bl_shut['param'], True)
        # scan bleaching area and get reference time
        scan_roi(rois[1])
        start_time = time.time()
        # close bleaching shutter after scan
        pqd.set_value(bl_shut['device'], bl_shut['param'], False)

    ## prepare after bleaching step ###############################################
    pql.measurement.img_conf.num_frames = meas_frames

    ## restore measurement laser assembly
    hdl = pqd.create_transaction()
    # turn on measurement laser and turn off bleaching laser
    pqd.set_value(meas_las['device'], meas_las['param_out'], True)
    pqd.set_value(bl_las['device'], bl_las['param_out'], False)
    # put led out of opt. path
    pqd.set_value(LED, LED_IN_PATH, False, hdl)
    # turn off bleaching laser and restore saved values
    pqd.set_value(bl_las['device'], bl_las['param_int'], bl_las_val_int, hdl)
    pqd.set_value(bl_las['device'], bl_las['param_cw'], bl_las_val_cw, hdl)
    # restore intensity, mode and turn on measurement laser
    pqd.set_value(meas_las['device'], meas_las['param_int'], meas_las_val_int, hdl)
    pqd.set_value(meas_las['device'], meas_las['param_cw'], meas_las_val_cw, hdl)
    # restore attenuator and main attenuator
    pqd.set_value(meas_att['device'], meas_att['param'], meas_att_val, hdl)
    pqd.set_value(meas_att_main['device'], meas_att_main['param'], meas_att_main_val, hdl)
    # start transaction
    reqID = pqd.start_transaction(hdl)
    pqd.wait_until_done(reqID)
    pqd.destroy_transaction(hdl)

    ## prepare lists and start measurement loop
    sum_counts_bl = []
    sum_counts_ref = []
    sum_counts_t = []
    for i in range(NUM_REPEATS):
        ## overview scan
        print('Overview scan: ', i, ' of ', NUM_REPEATS)
        meas_roi(rois[0])
        stop_time = time.time() - start_time
        sum_counts_t += [stop_time]

        ## get intensity image and show on ImageView1
        #img = pql.luminosa.get_analysis_image(ANA_NAME, ANA_IMG_INT)
        #img_data = np.array(img['img_data'])
        #pqt.show_image(img_data, 'Intensity', 1)

        ## calc intensitiy in bleaching roi and reference roi and plot on P1
        print('OverView area: ', rois[0])
        print('Bleaching area: ', rois[1])
        roi, roi_data = get_roi_from_image(img_data, rois[0], rois[1])
        print('Bleaching area pixles: ', roi)
        sum_counts_bl += [np.sum(roi_data)]
        pqt.show_image(roi_data, 'Bleaching area', 2)
        roi, roi_data = get_roi_from_image(img_data, rois[0], rois[2])
        sum_counts_ref += [np.sum(roi_data)]
        print('Reference area pixles: ', roi)

        pqt.plot(sum_counts_t, sum_counts_bl, 'Bleaching area', 1)
        pqt.plot(sum_counts_t, sum_counts_ref, 'Reference area', 1)

        pqt.gui_sleep(WAIT_BETWEEN_REPEATS)

    # unblock adjustment of pinhole and tube lens when changing the active laser
    pql.measurement.block_airy_adjustment(False)

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
