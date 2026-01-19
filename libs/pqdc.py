#-------------------------------------------------------------------------------
# Name:         pqdc
# Version:      1.0
# Purpose:      Access to PicoQuant automation devices
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

is_fake = False
try:
    import delphi_pqdc as dm
except:
    is_fake = True
    print('Could not import delphi_pqdc module. Using fake module instead.')


def get_version() -> str:
    """
    Retrieves the version of the pqdc module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqdc module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def get_device_names() -> list:
    """
    Retrieves a list of device names of all automation devices connected to the system.

    Parameters
    ----------
    none

    Returns
    -------
    names : list of strings
        List of device names.
    """
    if is_fake:
        return ['fake_device']

    err, names = dm.get_device_names()
    if err:
        raise Exception(err)
    return names

def get_device_info(dev: str = '') -> dict:
    """
    Retrieves information of a given automation device.

    Parameters
    ----------
    dev : string
        Device name.

    Returns
    -------
    info : dict
        Information of the device with the following keys:
        name:  name of the device
        label: label of the device
        status: status of the device
        last_error_code: last error code of the device
        num_params: number of parameters of the device
    """
    if is_fake:
        return {'name': 'fake_device', 'label': 'Fake Device', 'status': 'OK', 'last_error_code': 0, 'num_params': 1}
    
    err, info = dm.get_device_info(str(dev))
    if err:
        raise Exception(err)
    return info

def get_param_names(dev = '') -> list:
    """
    Retrieves a list of parameter names of a given automation device.

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
        return ['fake_parameter']
    
    err, names = dm.get_param_names(str(dev))
    if err:
        raise Exception(err)
    return names

def get_param_info(dev: str = '', param: str = '') -> dict:
    """
    Retrieves information of a given parameter of a given automation device.

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
    e.g.
        'name': 'Position', 'label': 'Attenuation', 'type': 'vtInt', 'read_only': False, 'min': 0.0, 'max': 100.0, 'unit': '%'
    """
    if is_fake:
        return {'name': 'fake_parameter', 'label': 'Fake Parameter', 'type': 'vtInt', 'read_only': False, 'min': 0.0, 'max': 100.0, 'unit': ''}
    
    err, info = dm.get_param_info(str(dev), str(param))
    if err:
        raise Exception(err)
    return info

def reinit_device(dev = '') -> None:
    """
    This low level function reinitializes an automation device. This can be necessary, e.g. after an internal device parameter has been changed.
    These internal parameters are not returned by get_param_names() and they should be accessed with care.

    Parameters
    ----------
    dev : string
        Device name.
    """
    if is_fake:
        return
    
    err = dm.reinit_device(str(dev))
    if err:
        raise Exception(err)

def get_value(dev = '', param = '', array_idx = -1):
    """
    Retrieves the value of a given parameter of an automation device.

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    array_idx : int
        Index of a parameter array element (default -1 for scalar parameters).

    Returns
    -------
    val : int or float or bool or string
        Parameter value (type depends on the parameter).
    """
    if is_fake:
        return 0
    
    err, val = dm.get_value(str(dev), str(param), int(array_idx))
    if err:
        raise Exception(err)
    return val

def set_value_no_wait(dev = '', param = '', val = '', trans_hdl = 0, array_idx = -1) -> int:
    """
    Sets the value of a given parameter of an automation device and returns a request ID.
    The function returns immediately and does not wait for the write operation to finish.
    The returned request ID can be used with wait_until_done(req_id) to wait for the write operation to finish.

    If a transaction handle > 0 is given (can be created with create_transaction()), the write operation is added to a transaction list
    and the returned request ID can be ignored. The transaction list can be started with start_transaction(trans_hdl).

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    val : string
        New parameter value.
    trans_hdl : int
        Transaction handle (default 0 for non-transactional write).
    array_idx : int
        Index of a parameter array element (default -1 for scalar parameters).

    Returns
    -------
    req_id : int
        Request ID for non-transactional writes.
    """
    if is_fake:
        return 0
    
    err, req_id = dm.set_value_as_string(str(dev), str(param), int(array_idx), str(val), trans_hdl)
    if err:
        raise Exception(err)
    return req_id

def wait_until_done(req_id = -1, timeout = 60000) -> int:
    """
    Waits until a write operation is finished.

    Parameters
    ----------
    req_id : int
        Request ID as returned by set_value or set_value_and_wait or start_transaction.
    timeout : int
        Timeout in milliseconds (default 60 seconds).

    Returns
    -------
    req_status : int
        Request status (0: success, 1: failure, 2: timeout, 3: in progress).
    """
    if is_fake:
        return 0
    
    err, req_status = dm.wait_until_done(int(req_id), int(timeout))
    if err:
        raise Exception(err)
    return req_status

def set_value(dev = '', param = '', val = '', trans_hdl = 0, timeout = 60000, array_idx = -1) -> tuple:
    """
    Sets the value of a given parameter of an automation device and waits for the given timeout for the write operation to finish (if no transaction handle is provided, i.e. trans_hdl = 0).

    If a transaction handle > 0 is given (can be created with create_transaction()), the write operation is added to a transaction list
    and the timeout is ignored. The transaction list can be started with start_transaction(trans_hdl).

    Parameters
    ----------
    dev : string
        Device name.
    param : string
        Parameter name.
    val : int or float or bool or string, is casted to string
        New parameter value.
    trans_hdl : int
        Transaction handle (default 0 for non-transactional write).
    timeout : int
        Timeout in milliseconds (default 60 seconds).
    array_idx : int
        Index of a parameter array element (default -1 for scalar parameters).

    Returns
    -------
    req_id : int
        Request ID for the write operation.
    req_status : int
        Request status (0: success, 1: failure, 2: timeout, 3: in progress).
    """
    req_id = set_value_no_wait(dev, param, val, trans_hdl, array_idx)
    req_status = None
    if trans_hdl <= 0:
        req_status = wait_until_done(req_id, timeout)
    return req_id, req_status

def get_request_status(req_id = -1) -> int:
    """
    Retrieves the status of a previously sent request returned by set_value.
    This is a low level function that doesn't have to be used if set_value and wait_until_done or set_value_and_wait are used.

    Parameters
    ----------
    req_id : int
        Request ID of the write operation.

    Returns
    -------
    req_status : int
        Request status (0: success, 1: failure, 2: timeout, 3: in progress).
    """
    if is_fake:
        return 0
    
    err, req_status = dm.get_request_status(int(req_id))
    if err:
        raise Exception(err)
    return req_status

def create_transaction() -> int:
    """
    Creates a transaction for a sequence of write operations and returns a transaction handle to be used with set_value and start_transaction.
    The purpose of a transaction is to set multiple parameters for multiple devices in parallel and wait for them all to finish.

    Parameters
    ----------
    none

    Returns
    -------
    trans_hdl : int
        Transaction handle to be used with set_value and start_transaction.
    """
    if is_fake:
        return 0
    
    err, trans_hdl = dm.create_transaction()
    if err:
        raise Exception(err)
    return trans_hdl

def start_transaction(trans_hdl = 0) -> int:
    """
    Starts a transaction for a sequence of write operations.

    Parameters
    ----------
    trans_hdl : int
        Transaction handle returned by create_transaction.

    Returns
    -------
    req_id : int
        Request ID for the entire transaction. Must be used with wait_until_done to wait for the transaction to finish.
    """
    if is_fake:
        return 0
    
    err, req_id = dm.start_transaction(trans_hdl)
    if err:
        raise Exception(err)
    return req_id

def destroy_transaction(trans_hdl = 0) -> None:
    """
    Destroys a transaction previously created with create_transaction.
    After a transaction has been started and is finished (can be checked with wait_until_done), it must be destroyed to free up resources.

    Parameters
    ----------
    trans_hdl : int
        Transaction handle returned by create_transaction.
    """
    if is_fake:
        return
    
    err = dm.destroy_transaction(trans_hdl)
    if err:
        raise Exception(err)

def search_devices(token: str = '') -> list:
    devs = get_device_names()
    devlist = []
    token = token.strip()
    for dev in devs:
        dev_info = get_device_info(dev)
        if token in dev_info['name'] or token in dev_info['label']:
            devlist.append(dev_info)

    return devlist