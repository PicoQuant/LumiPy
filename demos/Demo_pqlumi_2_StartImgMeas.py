'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql
import pqtool as pqt

## Start a image measurement
#USR_SET = 'MyFLIMSettings' <- enter your user settings name here
#pql.measurement.load_user_setting(USR_SET)

# set stop_on_num_frames to True
pql.measurement.img_conf.stop_on_num_frames = True
# set num_frames to 1
pql.measurement.img_conf.num_frames = 1

pql.measurement.start_meas('image')
print('Measurement started')
while True:
    if not pql.measurement.meas_status():
        break
    pqt.gui_sleep(100)
print('ElapsedMeasTime: ', pql.measurement.get_elapsed_meas_time(), ' s')
