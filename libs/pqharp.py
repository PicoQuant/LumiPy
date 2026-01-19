#-------------------------------------------------------------------------------
# Name:         pqharp
# Version:      1.0
# Purpose:      Access to PicoQuant TCSPC devices (Harps)
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

is_fake = False
try:
    import delphi_pqharp as dm
except:
    is_fake = True
    print('Could not import delphi_pqharp module. Using fake module instead.')

def get_version() -> str:
    """
    Retrieves the version of the pqharp module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqharp module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def get_device_names() -> list:
    """
    Retrieves a list of device names of all TCSPC (Harp) devices connected to the system.

    Parameters
    ----------
    none

    Returns
    -------
    names : list of strings
        List of device names.
    """
    if is_fake:
        return ['fake_harp']
    
    err, names = dm.get_device_names()
    if err:
        raise Exception(err)
    return names

def get_param_names(dev = '') -> list:
    """
    Retrieves a list of parameter names of the given TCSPC (Harp) device.
    Available parameters depend on the device type. Currently available parameters are:

    Device params (for functions get_value() and set_value(), set chan_idx = -1):
        dpBinning
        dpSyncDiv
        dpOffset
        dpAcqTime
        dpMarkerHoldOffTime
        dpTriggerOutPeriod
        dpOflCompression
        dpStopOnOverflow

    Channel params (for functions get_value() and set_value(), set chan_idx = 0 .. (ChannelCount - 1)):
        paCFDLevel / paTriggerLevel    (if cpHasCFD / cpHasLevelTrigger)
        paCFDZeroCross / paTriggerEdge (if cpHasCFD / cpHasLevelTrigger)
        paChanOffset                   (if cpHasOffset)
        paDeadTime                     (if cpHasDeadTime)
        paEnabled

    Misc params (for functions get_value() and set_value(), set chan_idx = -1):
        MeasMode
        BaseResolution (read-only)
        Resolution     (read-only)

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    names : list of strings
        List of parameter names.
    """
    if is_fake:
        return ['fake_harp_param']
    
    err, names = dm.get_param_names(str(dev))
    if err:
        raise Exception(err)
    return names

def get_param_info(dev: str, param: str, chan_idx = -1) -> dict:
    """
    Retrieves information of a given parameter of a given TCSPC (Harp) device.

    Parameters
    ----------
    dev : string
        Device name.
	param : string
        Parameter name.
    chan_idx : int
        Channel index for channel parameters (0 to ChannelCount - 1) or -1 for device or misc parameters.

    Returns
    -------
    info : dict
        Information of the parameter with the following keys:
        name:  name of the parameter
        label: label of the parameter
        type: value type of the parameter
        read_only: whether the parameter is read-only
        min: minimum value of the parameter
        max: maximum value of the parameter
        unit: unit of the parameter
    """
    if is_fake:
        return {'name': 'fake_harp_param', 'label': 'Fake Harp Param', 'type': 'vtInt', 'read_only': False, 'min': 0.0, 'max': 100.0, 'unit': ''}
    
    err, info = dm.get_param_info(str(dev), str(param), int(chan_idx))
    if err:
        raise Exception(err)
    return info

def get_value(dev = '', param = '', chan_idx = -1):
    """
    Retrieves the value of the given parameter of the given TCSPC (Harp) device.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    chan_idx : int
        Channel index for channel parameters (0 to ChannelCount - 1) or -1 for device or misc parameters.

    Returns
    -------
    val : int or float or bool or string
        Parameter value (type depends on the parameter).
    """
    if is_fake:
        return 0
    
    err, val = dm.get_value(str(dev), str(param), int(chan_idx))
    if err:
        raise Exception(err)
    return val

def set_value(dev = '', param = '', val = 0, chan_idx = -1) -> None:
    """
    Sets the value of the given parameter of the given TCSPC (Harp) device.
    The function returns after the parameter was set.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    val : int
        New parameter value.
    chan_idx : int
        Channel index for channel parameters (0 to ChannelCount - 1) or -1 for device or misc parameters.
    """
    if is_fake:
        return
    
    err = dm.set_value(str(dev), str(param), int(chan_idx), int(val))
    if err:
        raise Exception(err)

def start_measurement(dev = '') -> None:
    """
    Starts a measurement on a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.
    """
    if is_fake:
        return
    
    err = dm.start_measurement(str(dev))
    if err:
        raise Exception(err)

def measurement_running(dev = '') -> bool:
    """
    Retrieves the status of a measurement on a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    status : bool
        Measurement status (False: inactive/stopped, True: running).
    """
    if is_fake:
        return False
    
    err, status = dm.measurement_running(str(dev))
    if err:
        raise Exception(err)
    return status

def get_histo_length(dev = '') -> int:
    """
    Retrieves the length of a histogram for a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    histo_length : int
        Length of the histogram array.
    """
    if is_fake:
        return 3
    
    err, histo_length = dm.get_histo_length(str(dev))
    if err:
        raise Exception(err)
    return histo_length

def get_histogram(dev = '', chan_idx = 1) -> list:
    """
    Retrieves the histogram for a given TCSPC device and channel.

    Parameters
    ----------
    dev : string
        Device name.
    chan_idx : int
        Channel index (1 .. ChannelCount - 1); channel index = 0 is SYNC channel.

    Returns
    -------
    histo : array of uint64
        Histogram array.
    """
    if is_fake:
        return [0, 1, 0]
    
    err, histo = dm.get_histogram(str(dev), int(chan_idx))
    if err:
        raise Exception(err)
    return histo

def get_TTTRdata(dev = '') -> list:
    """
    Retrieves the TTTR data for a given TCSPC device (T2 or T3 data; depends on the measurement mode).

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    TTTRdata : array of uint64
        TTTR data array.
    """
    if is_fake:
        return [0]
    
    err, TTTRdata = dm.get_TTTRdata(str(dev))
    if err:
        raise Exception(err)
    return TTTRdata

def end_measurement(dev = '') -> None:
    """
    Ends a measurement on a given TCSPC device.
    If the measurement is not running, nothing happens.

    Parameters
    ----------
    dev : string
        Device name.
    """
    if is_fake:
        return
    
    err = dm.end_measurement(str(dev))
    if err:
        raise Exception(err)

def get_elapsed_measurement_time(dev = '') -> float:
    """
    Retrieves the elapsed measurement time for a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    meas_time : float
        Elapsed measurement time in seconds.
    """
    if is_fake:
        return 0.0
    
    err, meas_time = dm.get_elapsed_measurement_time(str(dev))
    if err:
        raise Exception(err)
    return meas_time

def get_all_countrates(dev = '') -> list:
    """
    Retrieves the count rates of all channels (including the SYNC channel) for a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    counts : list of int
        List of count rates for each channel.
    """
    if is_fake:
        return [0, 0, 0, 0, 0, 0, 0, 0]
    
    err,  counts = dm.get_all_countrates(str(dev))
    if err:
        raise Exception(err)
    return counts

def get_channel_count(dev = '') -> int:
    """
    Retrieves the number of channels (including the SYNC channel) for a given TCSPC device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    chan_count : int
        Number of channels on the device.
    """
    if is_fake:
        return 8
    
    err,  chan_count = dm.get_channel_count(str(dev))
    if err:
        raise Exception(err)
    return chan_count

def get_flags(dev = '') -> list:
    """
    Retrieves the status flags for a given TCSPC device.
    The following flags are currently available:

    flSysError: 0
    flFifoFull: 1
    flSoftError: 2
    flSyncLost: 4
    flRefLost: 5
    flFifoHalf: 6
    flFifoEmpty: 7
    flOverflow: 8
    flTimeOver: 9
    flRamReady: 10
    flScanActive: 11
    flRunning: 12
    flEventsLost: 13

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    flags : list of int
        Status flags.
    """
    if is_fake:
        return []
    
    err, flags = dm.get_flags(str(dev))
    if err:
        raise Exception(err)
    return flags

