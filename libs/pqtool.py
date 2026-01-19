#-------------------------------------------------------------------------------
# Name:         pqtool
# Version:      1.0
# Purpose:      Provides some PicoQuant helper functions to be used in python scripts
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

is_fake = False
try:
    import delphi_pqtool as dm
except:
    is_fake = True
    print('Could not import delphi_pqtool module. Using fake module instead.')

import numpy as np

def get_version() -> str:
    """
    Retrieves the version of the pqtool module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqtool module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def gui_sleep(wait: int = 0) -> None:
    """
    Pauses the script execution and gives control back to the GUI by polling the Windows Message Queue every 25 ms
    for 'wait' milliseconds. This can be used to give the user a chance to
    abort the script while it is running.

    Parameters
    ----------
    wait : int
        The time to wait in milliseconds. If 0, the function will just poll the Windows Message Queue once and return
        immediately. Use a multiple of 25 ms.
    """
    if is_fake:
        return
    
    err = dm.gui_sleep(int(wait))
    if err:
        raise Exception(err)

def plot(x = None, y = None, name: str = '', win_idx: int = 1) -> None:
    """
    Adds a 2D line graph with the given name to a plot window with the given index.
    If a graph with the same name already exists, it will be overwritten, otherwise a new graph will be added to the plot window.
    Colors are assigned automatically to added graphs.
    The x and y data points can be either python lists or numpy arrays.

    Parameters
    ----------
    x : list or numpy array
        x data points
    y : list or numpy array
        y data points
    name : string
        Name of the graph
    win_idx : int
        Index of the plot view window
    """
    if not isinstance(x, list) and not isinstance(x, np.ndarray) and x is not None:
        err = 'Error: x data must be a python list or a numpy array'
        raise Exception(err)

    if not isinstance(y, list) and not isinstance(y, np.ndarray):
        err = 'Error: y data must be a python list or a numpy array'
        raise Exception(err)

    if isinstance(x, np.ndarray):
        x = x.tolist()

    if isinstance(y, np.ndarray):
        y = y.tolist()

    if is_fake:
        return
    
    err = dm.plot(x, y, str(name), int(win_idx))
    if err:
        raise Exception(err)

def show_image(img = None, name: str = '', win_idx: int = 1) -> None:
    """
    Displays a 2D image in a new window with the given index.
    The image data must be a numpy array, either 2D (grayscale) or 3D (color).
    The image data is not copied, but the numpy array is flattened and passed to the underlying function.

    Parameters
    ----------
    img : numpy array
        2D (grayscale) or 3D (color) image data
    name : string
        Name of the window
    win_idx : int
        Index of the image view window
    """
    if not isinstance(img, np.ndarray):
        err = 'Error: image data must be a numpy array'
        raise Exception(err)

    if img.ndim < 2:
        err = 'Error: dimension of image is wrong'
        raise Exception(err)

    if img.ndim < 3:
        height, width = np.shape(img)
        chan = 1
    else:
        height, width, chan = np.shape(img)

    if img.dtype != np.uint8:
        pix_max = np.max(img)
        pix_min = np.min(img)
        m = 255/(pix_max - pix_min)
        b = (255 * pix_min)/(pix_min - pix_max)
        img = m * img + b
        img = img.astype(np.uint8)

    img = img.flatten()

    if is_fake:
        return

    err = dm.show_image(img.tolist(), height, width, chan, str(name), int(win_idx))
    if err:
        raise Exception(err)

def log_out(msg: str = '') -> None:
    """
    Adds a message tagged as 'Info' to PicoQuants logging system.

    Parameters
    ----------
    msg : str
        The message to log
    """
    if is_fake:
        return
    
    dm.log_out(str(msg))
