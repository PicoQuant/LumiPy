#-------------------------------------------------------------------------------
# Name:         pqcam
# Version:      1.0
# Purpose:      Access to PicoQuant camera devices (ids_ueye, ids_peak)
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

is_fake = False
try:
    import delphi_pqcam as dm
except:
    is_fake = True
    print('Could not import delphi_pqcam module. Using fake module instead.')

import numpy as np

def get_version() -> str:
    """
    Retrieves the version of the pqcam module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqcam module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def get_device_names() -> list:
    """
    Retrieves a list of device names of all camera devices connected to the system.

    Parameters
    ----------
    none

    Returns
    -------
    names : list of strings
        List of device names.
    """
    if is_fake:
        return ['fake_camera']
    
    err, names = dm.get_device_names()
    if err:
        raise ValueError(err)
    return names

def get_param_names(dev = '') -> list:
    """
    Retrieves a list of parameter names of the given camera device.
    Available parameters depend on the device type. Currently available parameters are:

    Device params:
        cpFramesPerSecond         (if caHasFPSSetting)
        cpAutoFramesPerSecond     (if caHasAutoFPS)
        cpIntegrationTime         (if caHasIntegrationTime)
        cpAutoIntegrationTime     (if caHasAutoIntegrationTime)
        cpGain                    (if caHasGain)
        cpAutoGain                (if caHasAutoGain)
        cpGainBoost               (if caHasGainBoost)
        cpMirrorX                 (if caHasMirrorX)
        cpMirrorY                 (if caHasMirrorY)
        cpHardwarePixelResolution
        cpTransferRate            (if caHasTransferRate)
        cpBinningX                (if caHasBinning)
        cpBinningY                (if caHasBinning)

    Misc params:
        IsLive

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
        return ['fake_camera_param']
    
    err, names = dm.get_param_names(str(dev))
    if err:
        raise ValueError(err)
    return names

def get_param_info(dev: str, param: str) -> dict:
    """
    Retrieves information of a given parameter of a given camera device.

    Parameters
    ----------
    dev : string
        Device name.
	param : string
        Parameter name.

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
        return {'name': 'fake_camera_param', 'label': 'Fake Camera Param', 'type': 'vtInt', 'read_only': False, 'min': 0.0, 'max': 100.0, 'unit': ''}
    
    err, info = dm.get_param_info(str(dev), str(param))
    if err:
        raise Exception(err)
    return info

def get_value(dev = '', param = ''):
    """
    Retrieves the value of the given parameter of the given camera device.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.

    Returns
    -------
    val : int or float or bool
        Parameter value (type depends on the parameter).
    """
    if is_fake:
        return 0
    
    err, val = dm.get_value(str(dev), str(param))
    if err:
        raise Exception(err)
    return val

def set_value(dev = '', param = '', val = 0) -> None:
    """
    Sets the value of the given parameter of the given camera device.
    The function returns after the parameter was set.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    val : int or float or bool
        New parameter value.
    """
    if is_fake:
        return
    
    err = dm.set_value(str(dev), str(param), val)
    if err:
        raise ValueError(err)

def get_image(dev = '') -> np.ndarray:
    """
    Retrieves the current image of the given camera device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    img : array of uint8
        Image data (3 color planes, height x width x 3).

    Notes
    -----
    The returned image data is a 3D numpy array with shape (height, width, 3),
    where the 3rd dimension contains the 3 color planes (R, G, B). The data type
    of the array is uint8.
    """
    if is_fake:
        return np.zeros((3, 3, 3), dtype = np.uint8)
    
    err, img, width, height = dm.get_image(str(dev))
    if err:
        raise ValueError(err)
    img = np.reshape(img, (height, width))
    img = img.astype(np.uint32, copy = False)
    img = img[:, :, np.newaxis].view('uint8')
    img = img[:, :, :3]
    return img


