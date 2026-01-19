#-------------------------------------------------------------------------------
# Name:         pqscan
# Version:      1.0
# Purpose:      Access to PicoQuant scan devices
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

is_fake = False
try:
    import delphi_pqscan as dm
except:
    is_fake = True
    print('Could not import delphi_pqscan module. Using fake module instead.')

def get_version() -> str:
    """
    Retrieves the version of the pqscan module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqscan module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def get_device_names() -> list:
    """
    Retrieves a list of device names of all scanner devices connected to the system.

    Parameters
    ----------
    none

    Returns
    -------
    names : list of strings
        List of device names.
    """
    if is_fake:
        return ['fake_scanner']
    
    err, names = dm.get_device_names()
    if err:
        raise Exception(err)
    return names

def get_param_names(dev: str = '') -> list:
    """
    Retrieves a list of parameter names of the given scanner device.
    Available parameters depend on the device type. Currently available parameters are:

      spXPos
      spYPos
      spZPos

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
        return ['fake_scanner_param']
    
    err, names = dm.get_param_names(str(dev))
    if err:
        raise Exception(err)
    return names

def get_param_info(dev: str, param: str) -> dict:
    """
    Retrieves information of a given parameter of a given scanner device.

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
        return {'name': 'fake_scanner_param', 'label': 'Fake Scanner Param', 'type': 'vtInt', 'read_only': False, 'min': 0.0, 'max': 100.0, 'unit': ''}
    
    err, info = dm.get_param_info(str(dev), str(param))
    if err:
        raise Exception(err)
    return info

def get_value(dev: str = '', param: str = ''):
    """
    Retrieves the value of the given parameter of the given scanner device.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.

    Returns
    -------
    val : int or float or bool or string
        Parameter value (type depends on the parameter).
    """
    if is_fake:
        return 0
    
    err, val = dm.get_value(str(dev), str(param))
    if err:
        raise Exception(err)
    return val

def set_value(dev: str = '', param: str = '', val = 0) -> None:
    """
    Sets the value of the given parameter of the given scanner device.
    The function returns after the parameter was set.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    val : int
        New parameter value.
    """
    if is_fake:
        return
    
    err = dm.set_value(str(dev), str(param), val)
    if err:
        raise Exception(err)

def scan_start(dev: str = '') -> None:
    """
    Starts a scan on a given scanner device.

    Parameters
    ----------
    dev : string
        Device name.
    """
    if is_fake:
        return
    
    err = dm.scan_start(str(dev))
    if err:
        raise Exception(err)
    
def is_scanning(dev: str = '') -> bool:
    """
    Retrieves the status of a scan on a given scanner device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    status : bool
        Scan status (False: inactive/stopped, True: running).
    """
    if is_fake:
        return False
    
    err, status = dm.is_scanning(str(dev))
    if err:
        raise Exception(err)
    return status

def is_moving(dev: str = '') -> bool:
    """
    Retrieves the status of a move on a given scanner device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    status : bool
        Move status (False: inactive/stopped, True: running).
    """
    if is_fake:
        return False
    
    err, status = dm.is_moving(str(dev))
    if err:
        raise Exception(err)
    return status

def scan_stop(dev: str = '') -> None:
    """
    Stops a scan on a given scanner device.

    Parameters
    ----------
    dev : string
        Device name.
    """
    if is_fake:
        return
    
    err = dm.scan_stop(str(dev))
    if err:
        raise Exception(err)