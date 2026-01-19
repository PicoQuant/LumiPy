#-------------------------------------------------------------------------------
# Name:         pqeasy
# Version:      1.0
# Purpose:      Access to EasyPy workspace and system information
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

import delphi_pqeasy as dm

def get_version() -> str:
    """
    Retrieves the version of the pqeasy module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqeasy module version as a string.
    """
    version = dm.get_version()
    return version

def get_workspace() -> str:
    """
    Returns the absolute path of the currently selected EasyPy workspace as a string.

    Parameters
    ----------
    none

    Returns
    -------
    ws : string
        Absolute path of the currently selected EasyPy workspace
    """
    _, ws = dm.get_workspace()
    return ws
