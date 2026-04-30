'''
This script demonstrates how to switch illumination mode (confocal <-> epi).
'''
import pqdc as pqd

# ==================== devices and parameter ====================================
EPI_ILLUMINATION = 'EpiIllumination'
EPI_ILLUMINATION_ENABLED = 'Enabled'
EPI_ILLUMINATION_INT1 = 'Intensity1'
EPI_ILLUMINATION_INT2 = 'Intensity2'
EPI_ILLUMINATION_INT3 = 'Intensity3'

EPI_SHUTTER = 'OlympusFilter'
EPI_SHUTTER_STATE = 'ShutterStatus'

EPI_FILTER = 'OlympusFilter'
EPI_FILTER_POS = 'FilterNumber'
# epi filter index to set (starts with 1)
EPI_FILTER_POS_IDX = 3


SIDE_PORT = 'SidePort'
SIDE_PORT_POS = 'Position'
# side port index to set
SIDE_PORT_POS_EYEPICE = 0
SIDE_PORT_POS_PIEZO = 1
SIDE_PORT_POS_FLIMBEE = 2

# ==================== check if devices exist ====================================
devs = pqd.get_device_names()
if EPI_ILLUMINATION not in devs:
    print(EPI_ILLUMINATION, ' device not present in database.')
    exit()
if EPI_SHUTTER not in devs:
    print(EPI_SHUTTER, ' device not present in database.')
    exit()
if EPI_FILTER not in devs:
    print(EPI_FILTER, ' device not present in database.')
    exit()
if SIDE_PORT not in devs:
    print(SIDE_PORT, ' device not present in database.')
    exit()

# ==================== check if parameters exist ====================================
params = pqd.get_param_names(EPI_ILLUMINATION)
if EPI_ILLUMINATION_ENABLED not in params:
    print('Parameter ', EPI_ILLUMINATION_ENABLED , ' not present on device ', EPI_ILLUMINATION)
    exit()
if EPI_ILLUMINATION_INT1 not in params:
    print('Parameter ', EPI_ILLUMINATION_INT1 , ' not present on device ', EPI_ILLUMINATION)
    exit()
if EPI_ILLUMINATION_INT2 not in params:
    print('Parameter ', EPI_ILLUMINATION_INT2 , ' not present on device ', EPI_ILLUMINATION)
    exit()
if EPI_ILLUMINATION_INT3 not in params:
    print('Parameter ', EPI_ILLUMINATION_INT3 , ' not present on device ', EPI_ILLUMINATION)
    exit()

params = pqd.get_param_names(EPI_SHUTTER)
if EPI_SHUTTER_STATE not in params:
    print('Parameter ', EPI_SHUTTER_STATE , ' not present on device ', EPI_SHUTTER)
    exit()

params = pqd.get_param_names(EPI_FILTER)
if EPI_FILTER_POS not in params:
    print('Parameter ', EPI_FILTER_POS , ' not present on device ', EPI_FILTER)
    exit()

params = pqd.get_param_names(SIDE_PORT)
if SIDE_PORT_POS not in params:
    print('Parameter ', SIDE_PORT_POS , ' not present on device ', SIDE_PORT)
    exit()

# ==================== functions ====================================================
def set_epi_mode(epi_filter_idx: int) -> None:
    hdl = pqd.create_transaction()
    pqd.set_value(EPI_ILLUMINATION, EPI_ILLUMINATION_ENABLED, True, hdl)
    pqd.set_value(EPI_SHUTTER, EPI_SHUTTER_STATE, True, hdl)
    pqd.set_value(EPI_FILTER, EPI_FILTER_POS, epi_filter_idx, hdl)
    pqd.set_value(SIDE_PORT, SIDE_PORT_POS, SIDE_PORT_POS_EYEPICE, hdl)
    reqID = pqd.start_transaction(hdl)
    pqd.wait_until_done(reqID)
    pqd.destroy_transaction(hdl)

def set_confocal_mode(side_port_idx: int) -> None:
    hdl = pqd.create_transaction()
    pqd.set_value(EPI_ILLUMINATION, EPI_ILLUMINATION_ENABLED, False, hdl)
    pqd.set_value(EPI_SHUTTER, EPI_SHUTTER_STATE, False, hdl)
    pqd.set_value(EPI_FILTER, EPI_FILTER_POS, 1, hdl)
    pqd.set_value(SIDE_PORT, SIDE_PORT_POS, side_port_idx, hdl)
    reqID = pqd.start_transaction(hdl)
    pqd.wait_until_done(reqID)
    pqd.destroy_transaction(hdl)

# ==================== main ====================================================
if __name__ == '__main__':
    set_epi_mode(EPI_FILTER_POS_IDX)
    #set_confocal_mode(SIDE_PORT_POS_FLIMBEE)