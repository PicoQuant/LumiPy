# LumiPy

LumiPy is a Python interface for controlling and acquiring data from PicoQuant's Luminosa microscope systems. This library provides a high-level API to interact with various components of the Luminosa system, including confocal imaging, point scanning, and data online analyses.
The Python interface allows for feedback adaptive workflows for smart microscopy and for connecting open source software projects to the microscope.

## Main Modules and Classes:

- `pqlumi.py` - Main interface for Luminosa control
  - `Measurement` - Main class for controlling measurements
  - `ImgConf` - Configuration class for image scanning
  - `PointConf` - Configuration class for point scanning
- `pqtool.py` - Helper functions for plotting, logging, etc.
- `pqdc.py` - Device control module (all devices except cameras, TCSPC (Harp) & scanner)
- `pqcam.py` - Camera control module
- `pqharp.py` - Time-correlated single photon counting (TCSPC) module
- `pqscan.py` - Scanner control module

### pqlumi.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqlumi
    # Version:      1.0
    # Purpose:      Access to PicoQuant Luminosa functions
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

CLASSES
    builtins.object
        ImgConf
        Measurement
        PointConf

    class ImgConf(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initializes an instance of the ImgConf class.
     |
     |      This class represents the configuration options for an image scan.
     |
     |      Parameters:
     |          None
     |
     |      Returns:
     |          None
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  image_size
     |      Retrieves the image size in x and y direction in pixels.
     |
     |      Returns:
     |          tuple[int, int]: The image size in x and y direction in pixels.
     |
     |  meas_time
     |      Retrieves the measurement time in seconds that will be used to stop the scan if the option StopOnMeasTime is enabled.
     |
     |      Returns:
     |          float: The measurement time in seconds.
     |
     |  num_frames
     |      Retrieves the number of frames that will be acquired if the scan option StopOnNumFrames is enabled.
     |
     |      Returns:
     |          int: The number of frames to be acquired.
     |
     |  photons_in_brightest_px
     |      Retrieves the number of photons in the brightest pixel that will be used to stop the scan if the option StopOnPhotonsInBrightestPx is enabled.
     |
     |      Returns:
     |          int: The number of photons in the brightest pixel.
     |
     |  scan_speed
     |      Retrieves the scan speed in %.
     |
     |      Returns:
     |          int: The scan speed in %.
     |
     |  stop_on_meas_time
     |      Retrieves the state of the option to stop the scan after a specified measurement time.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.
     |
     |  stop_on_num_frames
     |      Retrieves the state of the option to stop the scan after a specified number of frames.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.
     |
     |  stop_on_photons_in_brightest_px
     |      Retrieves the state of the option to stop the scan after a specified number of photons have been detected in the brightest pixel.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.

    class Measurement(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initializes an instance of the Luminosa class.
     |
     |      This class represents the configuration options for a Luminosa measurement.
     |
     |      Parameters:
     |          None
     |
     |      Returns:
     |          None
     |
     |  block_airy_adjustment(self, block: bool = False) -> None
     |      Blocks or unblocks the airy adjustment of the PicoQuant Luminosa system.
     |      This is usefull for a FRAP measurement to reduce the time between bleaching and post-bleraching steps.
     |
     |      Parameters
     |      ----------
     |      block : bool
     |          Set to True to block the airy adjustment, False to unblock it.
     |
     |  get_analysis_curve(self, name: str, curve_type: str) -> dict
     |      Retrieves the curve for the given analysis name and curve type.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |          curve_type (str): The type identifier of the curve to retrieve.
     |
     |      Returns:
     |          dict: The curve with the following properties.
     |              'name': The name of the curve (string),
     |              'data_x': The x-axis data of the curve (1D list of floats),
     |              'data_y': The y-axis data of the curve (1D list of floats),
     |              'axis_title_x': The x-axis title of the curve (string),
     |              'axis_title_y': The y-axis title of the curve (string),
     |              'unit_x': The x-axis unit of the curve (string),
     |              'unit_y': The y-axis unit of the curve (string),
     |
     |              'data_delta_y': optional: The error of the y-axis data if Analysis is FCS (1D list of floats)
     |
     |              optional properties below are only returned if the given analysis has a selected fit option:
     |              'fit_names': The names of the fits (1D list of strings),
     |              'fits_x': The fits x-axis data for each entry in 'fit_names' (2D list of floats with 1st dim: FitModel, 2nd dim: XValues),
     |              'fits_y': The fits y-axis data for each entry in 'fit_names' (2D list of floats with 1st dim: FitModel, 2nd dim: FitValues),
     |              'irf_x':  The x-axis data for the IRF used by the fit for each entry in 'fit_names' if Analysis is TCSPC (2D list of floats with 1st dim: FitModel, 2nd dim: XValues),
     |              'irf_y':  The y-axis data for the IRF used by the fit for each entry in 'fit_names' if Analysis is TCSPC (2D list of floats with 1st dim: FitModel, 2nd dim: IRFValues)
     |
     |  get_analysis_curve_types(self, name: str) -> list
     |      Retrieves a list of all available curve types for the given analysis name.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |
     |      Returns:
     |          list (of strings): The list of available analysis curve types.
     |
     |  get_analysis_image(self, name: str, img_type: str) -> dict
     |      Retrieves the image for the given analysis name and image type.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |          img_type (str): The type identifier of the image to retrieve.
     |
     |      Returns:
     |          dict: The image with the following properties:
     |              'img_name': The name of the image data (string),
     |              'img_data': The image data itself (2D list of floats),
     |              'img_unit': The units of the image data (string),
     |              'pos_min': The min x / y / z overview position of the image in meters (tuple of floats),
     |              'pos_max': The max x / y / z overview position of the image in meters (tuple of floats),
     |              'pos_title': The position labels of the image (tuple of strings),
     |              'pos_unit': The position units of the image (tuple of strings)
     |
     |  get_analysis_image_types(self, name: str) -> list
     |      Retrieves a list of all available image types for the given analysis name.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |
     |      Returns:
     |          list (of strings): The list of available analysis image types.
     |
     |  get_analysis_names(self) -> list
     |      Retrieves a list of all available live analysis names that have been configured in the Luminosa SW.
     |
     |      Returns:
     |          list: The list of available analysis names.
     |
     |  get_analysis_param(self, name: str, param_type: str) -> dict
     |      Retrieves the parameter for the given analysis name and parameter type.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |          param_type (str): The type identifier of the parameter to retrieve.
     |
     |      Returns:
     |          dict: The parameter with its properties. The available keys depend on analysis and parameter type.
     |
     |  get_analysis_param_types(self, name: str) -> list
     |      Retrieves a list of all available parameter types for the given analysis name.
     |
     |      Parameters:
     |          name (str): The name of the analysis to query.
     |
     |      Returns:
     |          list (of strings): The list of available analysis parameter types.
     |
     |  get_elapsed_meas_time(self) -> float
     |      Retrieves the elapsed measurement time of a measurement on a PicoQuant Luminosa system.
     |
     |      Parameters
     |      ----------
     |      none
     |
     |      Returns
     |      -------
     |      meas_time : float
     |          Elapsed measurement time in seconds.
     |
     |  load_user_setting(self, name: str) -> None
     |      Loads a Luminosa user setting specified by the given name.
     |
     |      Parameters:
     |          SettName (str): The name of the user setting to load.
     |
     |      Returns:
     |          None
     |
     |  meas_status(self) -> bool
     |      Retrieves the status of a measurement on a PicoQuant Luminosa system.
     |
     |      Parameters
     |      ----------
     |      none
     |
     |      Returns
     |      -------
     |      status : bool
     |          Measurement status (False: inactive/stopped, True: running)
     |
     |  set_next_measurement_name(self, name: str) -> None
     |      Sets the name for the next measurement.
     |
     |      Parameters:
     |          name (str): The name of the next measurement. The default name will be used if name is the empty string.
     |
     |      Returns:
     |          None
     |
     |  start_meas(self, meas_type: str) -> None
     |      Starts a measurement on a PicoQuant Luminosa system.
     |
     |      Parameters
     |      ----------
     |      meas_type: str
     |          Type of the measurement to start: "image", "line", or "point".
     |
     |  stop_meas(self) -> None
     |      Stops a measurement on a PicoQuant Luminosa system.
     |
     |      Parameters
     |      ----------
     |      none
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  img_conf
     |      Retrieves the configuration options for an image scan.
     |
     |      Returns:
     |          ImgConf: The configuration options for an image scan.
     |
     |  path_to_ptu
     |      Retrieves the absolute path to the last PTU file written.
     |
     |      Returns:
     |          str: The path to the last PTU file written.
     |
     |  point_conf
     |      Retrieves the configuration options for a point scan.
     |
     |      Returns:
     |          PointConf: The configuration options for a point scan.
     |
     |  scan_range_max_x
     |      Retrieves the maximum X range value of the scan in meter.
     |
     |      Returns:
     |          float: The maximum X range value in meter.
     |
     |  scan_range_max_y
     |      Retrieves the maximum Y range value of the scan in meter.
     |
     |      Returns:
     |          float: The maximum Y range value in meter.
     |
     |  scan_range_min_x
     |      Retrieves the minimum X range value of the scan in meter.
     |
     |      Returns:
     |          float: The minimum X range value in meter.
     |
     |  scan_range_min_y
     |      Retrieves the minimum Y range value of the scan in meter.
     |
     |      Returns:
     |          float: The minimum Y range value in meter.
     |
     |  version
     |      Retrieves the version of the PicoQuant Luminosa SW.
     |
     |      Returns:
     |          str: The Luminosa SW version as a string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  scan_range_height
     |      Retrieves the height of the scan in meter.
     |
     |      Returns:
     |          float: The height of the scan in meter.
     |
     |  scan_range_left
     |      Retrieves the left range value of the scan in meter.
     |
     |      Returns:
     |          float: The left range value in meter.
     |
     |  scan_range_top
     |      Retrieves the top range value of the scan in meter.
     |
     |      Returns:
     |          float: The top range value in meter.
     |
     |  scan_range_width
     |      Retrieves the width of the scan in meter.
     |
     |      Returns:
     |          float: The width of the scan in meter.
     |
     |  write_ptu_file
     |      Retrieves the state of the option to write a PTU files during the scan.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.

    class PointConf(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initializes an instance of the PointConf class.
     |
     |      This class represents the configuration options for a point scan.
     |
     |      Parameters:
     |          None
     |
     |      Returns:
     |          None
     |
     |  lumi_finder(self) -> None
     |      Use the 'LumiFinder' to select points based on a previous image measurement.
     |
     |      Parameters:
     |          None
     |
     |      Returns:
     |          None
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  meas_time
     |      Retrieves the measurement time in seconds that will be used to stop the point scan if the option StopOnMeasTime is enabled.
     |
     |      Returns:
     |          float: The measurement time in seconds.
     |
     |  num_photons
     |      Retrieves the number of photons that will be used to stop the point scan if the option StopOnPhotons is enabled.
     |
     |      Returns:
     |          int: The number of photons.
     |
     |  point_list
     |      Retrieves the coordinates of all points in the overview.
     |
     |      Returns:
     |          list[tuple[float, float]]: List of point coordinates in m.
     |
     |  selected_point
     |      Retrieves the coordinates of the selected point.
     |
     |      Returns:
     |          tuple[float, float]: Coordinates of the selected point in m. NaN if no point is selected.
     |
     |  stop_on_meas_time
     |      Retrieves the state of the option to stop the point scan after a specified measurement time.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.
     |
     |  stop_on_photons
     |      Retrieves the state of the option to stop the point scan after a specified number of photons have been detected.
     |
     |      Returns:
     |          bool: True if the option is enabled, False otherwise.

FUNCTIONS
    get_pqdc_laser_assembly(wl: int = 640) -> tuple
        Retrieves the device and parameter names for a laser assembly of the given wavelength.
        A laser assembly is made up of a laser head, attenuator, main attenuator and shutter.
        The device and parameter names are ment to be used with the pqdc module to access these devices.

        Parameters
        ----------
        wl : int
            Wavelength in nm (default: 640)

        Returns
        -------
        tuple
            A tuple containing the following dictionaries:
                las : Laser head dictionary with the following keys:
                    - 'device': the name of the laser head device
                    - 'param_int': the name of the intensity parameter
                    - 'param_cw': the name of the CW parameter
                    - 'param_off': the name of the offset parameter
                    - 'param_out': the name of the output parameter

                att : Laser attenuator dictionary with the following keys:
                    - 'device': the name of the attenuator device
                    - 'param': the name of the position parameter

                att_main : Main attenuator dictionary with the following keys:
                    - 'device': the name of the main attenuator device
                    - 'param': the name of the position parameter

                shut : Shutter dictionary with the following keys:
                    - 'device': the name of the shutter device
                    - 'param': the name of the state parameter

    get_version() -> str
        Retrieves the version of the pqlumi module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqlumi module version as a string.

    search_pqdc_devices(token1: str, token2: str = '') -> list
        Returns a list of dictionaries containing device and parameter names ment to be used with the pqdc module.

        Each dictionary contains the following information:
            - 'device': the name of the device
            - 'params': a list of parameter names available on the device

        If token1 is specified, only devices with a name or label containing token1 will be returned.
        If token2 is specified, only devices with a name or label containing both token1 and token2 will be returned.

        Parameters
        ----------
        token1: string
        token2: string, optional

        Returns
        -------
        devs : list of dictionaries

````

### pqtool.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqtool
    # Version:      1.0
    # Purpose:      Provides some PicoQuant helper functions to be used in python scripts
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

FUNCTIONS
    get_version() -> str
        Retrieves the version of the pqtool module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqtool module version as a string.

    gui_sleep(wait: int = 0) -> None
        Pauses the script execution and gives control back to the GUI by polling the Windows Message Queue every 25 ms
        for 'wait' milliseconds. This can be used to give the user a chance to
        abort the script while it is running.

        Parameters
        ----------
        wait : int
            The time to wait in milliseconds. If 0, the function will just poll the Windows Message Queue once and return
            immediately. Use a multiple of 25 ms.

    log_out(msg: str = '') -> None
        Adds a message tagged as 'Info' to PicoQuants logging system.

        Parameters
        ----------
        msg : str
            The message to log

    plot(x=None, y=None, name: str = '', win_idx: int = 1) -> None
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

    show_image(img=None, name: str = '', win_idx: int = 1) -> None
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

````

### pqdc.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqdc
    # Version:      1.0
    # Purpose:      Access to PicoQuant automation devices
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

FUNCTIONS
    create_transaction() -> int
        Creates a transaction for a sequence of write operations and returns a transaction handle to be used with set_value and start_transaction.
        The purpose of a transaction is to set multiple parameters for multiple devices in parallel and wait for them all to finish.

        Parameters
        ----------
        none

        Returns
        -------
        trans_hdl : int
            Transaction handle to be used with set_value and start_transaction.

    destroy_transaction(trans_hdl=0) -> None
        Destroys a transaction previously created with create_transaction.
        After a transaction has been started and is finished (can be checked with wait_until_done), it must be destroyed to free up resources.

        Parameters
        ----------
        trans_hdl : int
            Transaction handle returned by create_transaction.

    get_device_info(dev: str = '') -> dict
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

    get_device_names() -> list
        Retrieves a list of device names of all automation devices connected to the system.

        Parameters
        ----------
        none

        Returns
        -------
        names : list of strings
            List of device names.

    get_param_info(dev: str = '', param: str = '') -> dict
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

    get_param_names(dev='') -> list
        Retrieves a list of parameter names of a given automation device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        names : list of strings
            List of parameter names.

    get_request_status(req_id=-1) -> int
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

    get_value(dev='', param='', array_idx=-1)
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

    get_version() -> str
        Retrieves the version of the pqdc module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqdc module version as a string.

    reinit_device(dev='') -> None
        This low level function reinitializes an automation device. This can be necessary, e.g. after an internal device parameter has been changed.
        These internal parameters are not returned by get_param_names() and they should be accessed with care.

        Parameters
        ----------
        dev : string
            Device name.

    search_devices(token: str = '') -> list

    set_value(dev='', param='', val='', trans_hdl=0, timeout=60000, array_idx=-1) -> tuple
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

    set_value_no_wait(dev='', param='', val='', trans_hdl=0, array_idx=-1) -> int
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

    start_transaction(trans_hdl=0) -> int
        Starts a transaction for a sequence of write operations.

        Parameters
        ----------
        trans_hdl : int
            Transaction handle returned by create_transaction.

        Returns
        -------
        req_id : int
            Request ID for the entire transaction. Must be used with wait_until_done to wait for the transaction to finish.

    wait_until_done(req_id=-1, timeout=60000) -> int
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

````

### pqharp.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqharp
    # Version:      1.0
    # Purpose:      Access to PicoQuant TCSPC devices (Harps)
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

FUNCTIONS
    end_measurement(dev='') -> None
        Ends a measurement on a given TCSPC device.
        If the measurement is not running, nothing happens.

        Parameters
        ----------
        dev : string
            Device name.

    get_TTTRdata(dev='') -> list
        Retrieves the TTTR data for a given TCSPC device (T2 or T3 data; depends on the measurement mode).

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        TTTRdata : array of uint64
            TTTR data array.

    get_all_countrates(dev='') -> list
        Retrieves the count rates of all channels (including the SYNC channel) for a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        counts : list of int
            List of count rates for each channel.

    get_channel_count(dev='') -> int
        Retrieves the number of channels (including the SYNC channel) for a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        chan_count : int
            Number of channels on the device.

    get_device_names() -> list
        Retrieves a list of device names of all TCSPC (Harp) devices connected to the system.

        Parameters
        ----------
        none

        Returns
        -------
        names : list of strings
            List of device names.

    get_elapsed_measurement_time(dev='') -> float
        Retrieves the elapsed measurement time for a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        meas_time : float
            Elapsed measurement time in seconds.

    get_flags(dev='') -> list
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

    get_histo_length(dev='') -> int
        Retrieves the length of a histogram for a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        histo_length : int
            Length of the histogram array.

    get_histogram(dev='', chan_idx=1) -> list
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

    get_param_info(dev: str, param: str, chan_idx=-1) -> dict
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

    get_param_names(dev='') -> list
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

    get_value(dev='', param='', chan_idx=-1)
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

    get_version() -> str
        Retrieves the version of the pqharp module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqharp module version as a string.

    measurement_running(dev='') -> bool
        Retrieves the status of a measurement on a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        status : bool
            Measurement status (False: inactive/stopped, True: running).

    set_value(dev='', param='', val=0, chan_idx=-1) -> None
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

    start_measurement(dev='') -> None
        Starts a measurement on a given TCSPC device.

        Parameters
        ----------
        dev : string
            Device name.

````

### pqscan.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqscan
    # Version:      1.0
    # Purpose:      Access to PicoQuant scan devices
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

FUNCTIONS
    get_device_names() -> list
        Retrieves a list of device names of all scanner devices connected to the system.

        Parameters
        ----------
        none

        Returns
        -------
        names : list of strings
            List of device names.

    get_param_info(dev: str, param: str) -> dict
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

    get_param_names(dev: str = '') -> list
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

    get_value(dev: str = '', param: str = '')
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

    get_version() -> str
        Retrieves the version of the pqscan module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqscan module version as a string.

    is_moving(dev: str = '') -> bool
        Retrieves the status of a move on a given scanner device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        status : bool
            Move status (False: inactive/stopped, True: running).

    is_scanning(dev: str = '') -> bool
        Retrieves the status of a scan on a given scanner device.

        Parameters
        ----------
        dev : string
            Device name.

        Returns
        -------
        status : bool
            Scan status (False: inactive/stopped, True: running).

    scan_start(dev: str = '') -> None
        Starts a scan on a given scanner device.

        Parameters
        ----------
        dev : string
            Device name.

    scan_stop(dev: str = '') -> None
        Stops a scan on a given scanner device.

        Parameters
        ----------
        dev : string
            Device name.

    set_value(dev: str = '', param: str = '', val=0) -> None
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

````

### pqcam.py

````python
DESCRIPTION
    #-------------------------------------------------------------------------------
    # Name:         pqcam
    # Version:      1.0
    # Purpose:      Access to PicoQuant camera devices (ids_ueye, ids_peak)
    # Licence:      MIT
    # Copyright (c) 2025 PicoQuant GmbH
    #-------------------------------------------------------------------------------

FUNCTIONS
    get_device_names() -> list
        Retrieves a list of device names of all camera devices connected to the system.

        Parameters
        ----------
        none

        Returns
        -------
        names : list of strings
            List of device names.

    get_image(dev='') -> numpy.ndarray
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

    get_param_info(dev: str, param: str) -> dict
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

    get_param_names(dev='') -> list
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

    get_value(dev='', param='')
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

    get_version() -> str
        Retrieves the version of the pqcam module (this module).

        Parameters
        ----------
        none

        Returns
        -------
        version : string
            The pqcam module version as a string.

    set_value(dev='', param='', val=0) -> None
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

````

## Demos and use cases scripts:

- `Demo_pqlumi_*.py` - Basic Luminosa operations
- `Demo_pqdc_*.py` - Device control examples
- `Demo_pqharp.py` - TCSPC control examples
- `Demo_pqharp_CountMeter.py` - A simple countmeter chart
- `Demo_pqharp_LevelScan.py` - A script for scanning the trigger level of an input channel
- `Demo_pqcam.py` - Camera control examples
- `Demo_pqscan.py` - Scanner control examples
- `UC_*.py` - Use case examples (FRAP, FCS, etc.)


### Demo_pqlumi_0_GetParam.py

````python
'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Image scan parameter
print('Get image scan parameter:')
print('  Scan speed: ' , pql.measurement.img_conf.scan_speed)
print('  NumFrames: '  , pql.measurement.img_conf.num_frames)
print('  StopOnNumFrames: '           , pql.measurement.img_conf.stop_on_num_frames)
print('  StopOnPhotonsInBrightestPx: ', pql.measurement.img_conf.stop_on_photons_in_brightest_px)
print('  PhotonsInBrightestPx: '      , pql.measurement.img_conf.photons_in_brightest_px)
print('  StopOnMeasTime: '            , pql.measurement.img_conf.stop_on_meas_time)
print('  MeasTime: '                  , pql.measurement.img_conf.meas_time)

## Scan parameter (Overview)
print('\nGet scan parameter:')
scan_width = pql.measurement.scan_range_width # in SI units (m)
scan_width = round(scan_width * 1E6, 3)       # convert to um
print(f'  ScanRangeWidth: {scan_width} um')
print('  ScanRangeLeft: ' , pql.measurement.scan_range_left)
print('  ScanRangeTop: '  , pql.measurement.scan_range_top)
print('  ScanRangeMinX: ' , pql.measurement.scan_range_min_x)
print('  ScanRangeMaxX: ' , pql.measurement.scan_range_max_x)

## Point meas parameter
print('\nPoint meas parameter:')
print('  StopOnPhotons: '  , pql.measurement.point_conf.stop_on_photons)
print('  NumPhotons: '     , pql.measurement.point_conf.num_photons)
print('  StopOnMeasTime: ' , pql.measurement.point_conf.stop_on_meas_time)
print('  MeasTime: '       , pql.measurement.point_conf.meas_time)
print()
````

### Demo_pqlumi_1_SetParam.py

````python
'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Image scan parameter
print('Set image scan parameter:')
## set scan_speed
pql.measurement.img_conf.scan_speed = 10
print('  ScanSpeed: ', pql.measurement.img_conf.scan_speed)
## set num_frames
pql.measurement.img_conf.num_frames = 2
print('  NumFrames: ', pql.measurement.img_conf.num_frames)

## Scan parameter (Overview)
print('\nSet scan parameter:')
## set scan_range_width
pql.measurement.scan_range_width = 123.0E-6 # in SI units (m)
scan_width = round(pql.measurement.scan_range_width * 1E6, 3)
print(f'  ScanRangeWidth: {scan_width} um')
````

### Demo_pqlumi_2_StartImgMeas.py

````python
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
````

### Demo_pqlumi_3_GetImgAnalyses.py

````python
'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql
import pqtool as pqt

import numpy as np

## Get available live analyses for image measurements configured in Luminosa SW
print('Live Analyses:')
anas = pql.measurement.get_analysis_names()
print('  ', anas)

for ana in anas:
    print('\nAnalysis name: ', ana)

    # images
    its = pql.measurement.get_analysis_image_types(ana)
    print('    Num images: ', len(its))
    for it in its:
        print('      Image name: ', it)
        img = pql.measurement.get_analysis_image(ana, it)
        print('        Image keys: ', img.keys())

        img_data = np.array(img['img_data'])
        if it == 'Intensity':
            pqt.show_image(img_data, 'FLIM Intensity', 1)
        elif it == 'Fast Lifetime':
            pqt.show_image(img_data, 'Fast Lifetime', 2)

    # curves
    cts = pql.measurement.get_analysis_curve_types(ana)
    print('    Num curves: ', len(cts))
    for ct in cts:
        print('      Curve name: ', ct)
        curve = pql.measurement.get_analysis_curve(ana, ct)
        print('        Curve keys: ', curve.keys())
        pqt.plot(curve['data_x'], curve['data_y'], curve['name'])

    # params
    pts = pql.measurement.get_analysis_param_types(ana)
    print('    Num param types: ', len(pts))
    for pt in pts:
        print('      Param type: ', pt)
        params = pql.measurement.get_analysis_param(ana, pt)
        print('        Num params', len(params))
        for param in params:
            print('          Param keys: ', param.keys())


````

### Demo_pqlumi_4_Points.py

````python
'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql

## Dealing with points
print('Points:')
print('  Current points defined: ', pql.measurement.point_conf.point_list)
left = pql.measurement.scan_range_left
top = pql.measurement.scan_range_top
MY_POINTS = [(left + 5E-6, top + 5E-6),
             (left + 20E-6, top + 20E-6),
             (left + 40E-6, top + 40E-6)]
pql.measurement.point_conf.point_list = MY_POINTS
print('  New points defined: ', pql.measurement.point_conf.point_list)
````

### Demo_pqlumi_5_PntMeas.py

````python
'''
This script provides some code snippets demonstrating the use of the pqlumi module.
'''
import pqlumi as pql
import pqtool as pqt

## Start a point measurement
#USR_SET = 'MyFCSSettings' <- enter your user settings name here
#pql.measurement.load_user_setting(USR_SET)

pql.measurement.point_conf.stop_on_meas_time = True
pql.measurement.point_conf.meas_time = 10 # in SI units (s)
pql.measurement.start_meas('point')
print('Measurement started')
while True:
    if not pql.measurement.meas_status():
        break
    pqt.gui_sleep(100)
print('ElapsedMeasTime: ', pql.measurement.get_elapsed_meas_time(), ' s\n')

## Get available live analyses for point measurements configured in Luminosa SW
print('Live Analyses:')
anas = pql.measurement.get_analysis_names()
print('  ', anas)
plt_idx = 1
for ana in anas:
    print('\nAnalysis name: ', ana)

    # curves
    cts = pql.measurement.get_analysis_curve_types(ana)
    print('    Num curves: ', len(cts))
    for ct in cts:
        print('      Curve name: ', ct)
        curve = pql.measurement.get_analysis_curve(ana, ct)
        print('        Curve keys: ', curve.keys())
        pqt.plot(curve['data_x'], curve['data_y'], curve['name'], plt_idx)
        plt_idx += 1

    # params
    pts = pql.measurement.get_analysis_param_types(ana)
    print('    Num param types: ', len(pts))
    for pt in pts:
        print('      Param type: ', pt)
        params = pql.measurement.get_analysis_param(ana, pt)
        print('        Num params', len(params))
        for param in params:
            print('          Param keys: ', param.keys())
````

### Demo_pqtool.py

````python
'''
This script provides some code snippets demonstrating the use of the pqtool module.
'''
## Basic PQ imports
import pqtool as pqt

## Help for PQ imports
#help(pqt)

## External imports
import numpy as np


print('Module version: ', pqt.get_version())

## Plot some curves to PlotView 1 to 4
x = np.linspace(0, 10, 1000)
y = 100 * np.sin(x) + np.random.randn(1000)
 
pqt.plot(None, y, 'MyCurve (no X)')

pqt.plot(x, y, 'MyCurve', 2)
y = 80 * np.sin(2*x) + np.random.randn(1000) 
pqt.plot(x, y, 'MyCurve 2', 2)

y = 10 * np.sin(x) + np.random.randn(1000)
x_ = 10 * np.cos(x) + np.random.randn(1000)  
pqt.plot(x_, y, 'MyCurve (scatter)', 3)

for i in range(20):
    y = np.sin(2*x + i)
    print('Plot curve ', i, '/20')
    pqt.plot(x, y, 'MyCurve (with gui sleep)', 4)
    pqt.gui_sleep(100)

## Plot some images to ImageView 1 to 2
img = []
allZeroes = []
allOnes = []
for i in range(0,800):
    allZeroes.append(0)
    allOnes.append(1)
allZeroes += 0.1 * np.random.randn(800)    
allOnes += 0.1 * np.random.randn(800)
 
for i in range(0, 400):
    img.append(allZeroes)
for i in range(0,400):
    img.append(allOnes)
img = np.array(img)

pqt.show_image(img, 'MyImage 1', 1)
img = np.flipud(img)
pqt.show_image(img, 'MyImage 2', 2)
````

### Demo_pqdc_0_GetParam.py

````python
'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

print('Module version: ', pqd.get_version())

# Assume that the devices database (*.db) has an entry for a device with name 'Attenuator_1'.
# Then this device should have a parameter called 'Position'
dev = 'Attenuator_1'
param = 'Position'

## To check if dev is present in the database and connected to the system, one can use the following code:
devs = pqd.get_device_names()
print('Available devices: ', devs)
if not dev in devs:
    print('Device ', dev, ' not present in database.')
    exit()

## To check if param is available on dev, one can use the following code:
params = pqd.get_param_names(dev)
print('Available parameter for device ', dev, ': ', params)
if not param in params:
    print('Parameter ', param, ' not present on device ', dev)
    exit()

## Get the current value of the device parameter and print it
val = pqd.get_value(dev, param)
print(f'Current value of parameter {param} on device {dev}: {val}')
````

### Demo_pqdc_1_SetParam.py

````python
'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

dev = 'Attenuator_1'
param = 'Position'

## Get the current value of the device parameter
val = pqd.get_value(dev, param)

## Change the value of the device parameter and print it
# for this demo: increment the value by 10 and take the modulo 100 to ensure that the value is between 0 and 99
val = val + 10
val = val % 100
pqd.set_value(dev, param, val)
# get the changed value of the device parameter and print it
val = pqd.get_value(dev, param)
print(f'Current value of parameter {param} on device {dev}: {val}')

````

### Demo_pqdc_2_Set2Params.py

````python
'''
This script provides some code snippets demonstrating the use of the pqdc module.
This module handles all PQ automation devices, i.e. all devices connected to the system except cameras, scanner and harps.
'''
import pqdc as pqd

## Set parameter values on two devices simultaneously
devs = ['Attenuator_1', 'Attenuator_2']
params = ['Position', 'Position']

val = pqd.get_value(devs[0], params[0])
val = val + 10
val = val % 100
vals = [val, val]

hdl = pqd.create_transaction()
for dev, param, val in zip(devs, params, vals):
    pqd.set_value(dev, param, val, hdl)
req_id = pqd.start_transaction(hdl)
pqd.wait_until_done(req_id)
pqd.destroy_transaction(hdl)
````

### Demo_pqdc_3_pqlumi.py

````python
'''
This script demonstrates the use of a helper function to retrieves the device and parameter names for a laser assembly of the given wavelength.
A laser assembly is made up of a laser head, attenuator, main attenuator and shutter.
The device and parameter names are ment to be used with the pqdc module to access these devices.
'''
import pqlumi as pql

las, att, att_main, shut = pql.get_pqdc_laser_assembly(640)
print(att)
print(att_main)
print(shut)
print(las)
````

### Demo_pqharp.py

````python
'''
This script provides some code snippets demonstrating the use of the pqharp module.
'''
## Basic PQ imports
import pqharp as pqh

## Help for PQ imports
#help(pqh)

print('Module version: ', pqh.get_version())

## Get and print all available parameter for a MultiHarp device
params = pqh.get_param_names('MultiHarp')
print('\nAvailable parameters for MultiHarp:')
for param in params:
    if param.startswith('pa'): # a channel parameter
        for chan in range(0, pqh.get_channel_count('MultiHarp')):
            print('  ', param, ' (' + str(chan) + '): ', pqh.get_value('MultiHarp', param, chan))
    else:
        print('  ', param, ': ', pqh.get_value('MultiHarp', param))

## Get and print additional infos
print('\nInfo:')
print('  ChannelCount: ', pqh.get_channel_count('MultiHarp'))
print('  Flags: ', pqh.get_flags('MultiHarp'))

## Get all available countrates
print('\nCountrates:')
cnts = pqh.get_all_countrates('MultiHarp')
for i, cnt in enumerate(cnts):
    print('  Channel ', i, ': ', cnt, ' cps')
````

### Demo_pqharp_CountMeter.py

````python
'''
This script demonstrates how to use the pqharp module to plot a simple countrate chart for all MultiHarp channels.
Every time the script is run the new countrates will be added to a global list and ploted.
'''
## Basic PQ imports
import pqharp as pqh
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

def add_global_count_rates() -> list:
    # check if global_count_rates already exists
    if not 'global_count_rates' in globals():
        global global_count_rates
        global_count_rates = []
    else:
        if not type(global_count_rates) == list:
            print('global_count_rates is not a list.')
            return

    cnts = pqh.get_all_countrates('MultiHarp')
    global_count_rates.append(cnts)
    return global_count_rates

if __name__ == '__main__':
    count_rates = add_global_count_rates()
    for i in range(1, len(count_rates[0])):
        y = [cnt[i] for cnt in count_rates]
        pqt.plot(y = y, name = 'Channel ' + str(i))````

### Demo_pqharp_LevelScan.py

````python
'''
This script demonstrates how to use the pqharp module to perform a TriggerLevel scan on one channel.
'''
## Basic PQ imports
import pqharp as pqh
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

## External imports
import numpy as np

## Define channel to scan (Channel 0 = Sync channel) and range
CHANNEL = 1

## Triggel levels in mV.
## Use positive levels for SPADs and negative levels for HPDs.
LEVELS = np.arange(0, 301, 10)  

## Scan and plot on PlotView 1
counts = np.zeros(LEVELS.size)
curr_level = pqh.get_value('MultiHarp', 'paTriggerLevel', CHANNEL)
print('Current triggel level of channel ', CHANNEL, ': ', curr_level, 'mV')
try:
    for i, level in enumerate(LEVELS):
        pqh.set_value('MultiHarp', 'paTriggerLevel', level, CHANNEL)
        print('Set TriggerLevel to ', level, ' mV')
        pqt.gui_sleep(1000)
        cnts = pqh.get_all_countrates('MultiHarp')
        counts[i] = cnts[CHANNEL]
        print('Count rate: ', counts[i], ' cps')
        pqt.plot(LEVELS, counts, 'LevelScan Chan ' + str(CHANNEL), 1)
finally:
    pqh.set_value('MultiHarp', 'paTriggerLevel', curr_level, CHANNEL)
    
````

### Demo_pqscan.py

````python
'''
This script provides some code snippets demonstrating the use of the pqscan module.
'''
## Basic PQ imports
import pqscan as pqs
import pqtool as pqt

## Help for PQ imports
#help(pqs)
#help(pqt)

## Additional imports
import time


print('Module version: ', pqs.get_version())

dev = 'MainScanner'

## Get and print position
print('\nScanner position:')
print('  X: ', pqs.get_value(dev, 'spXPos'))
print('  Y: ', pqs.get_value(dev, 'spYPos'))
print('  Z: ', pqs.get_value(dev, 'spZPos'))

## Get and print all scan parameter
print('\nScanner parameter:')
params = pqs.get_param_names(dev)
for param in params:
    print('  ', param, ': ', pqs.get_value(dev, param))

# Start a scan for one 3 seconds
var = pqs.get_value(dev, 'spNumberOfFrames') # save number of frames
try:
    pqs.set_value(dev, 'spNumberOfFrames', -1)
    pqs.scan_stop(dev)
    pqs.scan_start(dev)
    start_time = time.time()
    print('\nScan started for 3 sec....')
    while True:
        if not pqs.is_scanning(dev):
            break
        pqt.gui_sleep(100)
        if time.time() - start_time > 3:
            pqs.scan_stop(dev)
            break 
    print('Scan stopped')
finally:
    pqs.set_value(dev, 'spNumberOfFrames', var) # restore number of frames


````

### Demo_pqcam.py

````python
'''
This script provides some code snippets demonstrating the use of the pqcam module.
'''
## Basic PQ imports
import pqcam as pqc
import pqtool as pqt

## Help for PQ imports
#help(pqcam)
#help(pqt)


print('Module version: ', pqc.get_version())

## Get and print all available camera device names
devs = pqc.get_device_names()
print('\nAvailable camera names:')
for dev in devs:
    print('  ', dev)

## Take first device and get all available parameters and print their names and values
dev = devs[0]
print('\nDeviceName: ', dev)
params = pqc.get_param_names(dev)
for param in params:
    print('  ', param, ': ', pqc.get_value(dev, param))


## Get an image from device and show it on ImageView 1
img = pqc.get_image(dev)
print('\nImage shape: ', img.shape)
pqt.show_image(img, dev, 1)

## Change the gain and get another image and show it on ImageView 2
var = pqc.get_value(dev, 'cpGain') # save current value
try:
    pqc.set_value(dev, 'cpGain', 50)
    print('\nGain was set to: ', pqc.get_value(dev, 'cpGain'), '%')
    pqt.gui_sleep(200) # wait to make sure a new image has been queued by the camera
    img = pqc.get_image(dev)
    pqt.show_image(img, dev + '(Gain 50%)', 2)
finally:
    pqc.set_value(dev, 'cpGain', var) # restore value
    print('\nGain was set back to: ', pqc.get_value(dev, 'cpGain'), '%')
````

### add_global_rois.py

````python
import pqlumi as pql

def add_global_rois(name: str = '') -> list:
    """
    Adds a new ROI based on the current scan range to the global_rois list.

    Parameters
    ----------
    name : str, optional
        Name of the ROI, by default an empty string.

    Returns
    -------
    list
        A list containing all the ROIs.

    Notes
    -----
    If the list does not exist, it is created and the ROI is appended to it.
    If the list already exists, the ROI is appended to it.
    """
    if not 'global_rois' in globals():
        global global_rois
        global_rois = []
    else:
        if not type(global_rois) == list:
            print('global_rois is not a list.')
            return
        
    roi = {
        'name': str(name),
        'left': pql.measurement.scan_range_left,
        'top': pql.measurement.scan_range_top,
        'width': pql.measurement.scan_range_width,
        'height': pql.measurement.scan_range_height
    }
    global_rois.append(roi)
    return global_rois
    
if __name__ == '__main__':
    rois = add_global_rois()
    for roi in rois:
        print(roi)
````

### UC_AiTools.py

````python
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
````

### UC_FRAP.py

````python
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
````

### UC_MultiRoiTimeLapse.py

````python
"""
USE CASE:  Multi-ROIs - Time Lapse
The user defines Multiple rectangular ROIs (e.g. 20 ROIs: #1 - #20)
In each ROI a 100-frames-image is acquired, for all ROIs.
Then the system waits for 1 hour and then again a 100-frames-image is acquired for all ROIs.
This cycle  is repeated for 5 iterations in total.
The same variant can be used while instead of Time-lapse a z-stack is acquired in each ROI.

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
USR_SET = '' #'LumiPy_UC_MultiRoi'
## parameters according to loaded/active USR_SET
ANA_NAME_FLIM = 'FLIM'
ANA_IMG_INT = 'Intensity'
ANA_IMG_FLT = 'Fast Lifetime'

ANA_NAME_HISTO = 'TCSPC histogram'
ANA_CRV = 'AutoR Detector 2'
ANA_PARAM = 'AutoR Detector 2'

##
NUM_FRAMES_PER_ROI = 2
NUM_REPEATS = 2
WAIT_BETWEEN_REPEATS = 1 # in sec.

## use global_rois defined elsewhere (e.g. add_global_rois.py)
USE_GLOBAL_ROIS = False
## or define rois manually
SCAN_LEFT = pql.measurement.scan_range_left
SCAN_TOP = pql.measurement.scan_range_top

MY_ROIS =  [
         {
            'name'  : 'Overview',
            'left'  : SCAN_LEFT,
            'top'   : SCAN_TOP,
            'width' : 100.0*1E-6,
            'height': 100.0*1E-6,
         },
         {
            'name'  : 'ROI 1',
            'left'  : SCAN_LEFT + 25.0*1E-6,
            'top'   : SCAN_TOP  + 25.0*1E-6,
            'width' : 50.0*1E-6,
            'height': 50.0*1E-6,
         },
         {
            'name'  : 'ROI 2',
            'left'  :  SCAN_LEFT + 50.0*1E-6,
            'top'   :  SCAN_TOP  + 50.0*1E-6,
            'width' : 10.0*1E-6,
            'height': 10.0*1E-6,
         },
        ]
## End User Input ###################################################################

def print_scan_range():
    print('Scan range:')
    print('  Left: ', pql.measurement.scan_range_left*1E6, ' um')
    print('  Top: ', pql.measurement.scan_range_top*1E6, ' um')
    print('  Width: ', pql.measurement.scan_range_width*1E6, ' um')
    print('  Height: ', pql.measurement.scan_range_height*1E6, ' um')

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## set meas duration to num frames
    pql.measurement.img_conf.stop_on_photons_in_brightest_px = False
    pql.measurement.img_conf.stop_on_meas_time = False
    pql.measurement.img_conf.stop_on_num_frames = True
    pql.measurement.img_conf.num_frames = NUM_FRAMES_PER_ROI

    ## assign roi list
    if USE_GLOBAL_ROIS and 'global_rois' in globals() and type(global_rois) == list:
        rois = global_rois
    else:
        rois = MY_ROIS

    ## start measurement loop
    for i in range(NUM_REPEATS):
        for roi in rois:
            ## set roi
            pql.measurement.scan_range_left = roi['left']
            pql.measurement.scan_range_top = roi['top']
            pql.measurement.scan_range_width = roi['width']
            pql.measurement.scan_range_height = roi['height']
            print_scan_range()

            ## start measurement
            pql.measurement.start_meas('image')
            print('Measurement started')
            while True:
                if not pql.measurement.meas_status():
                    break
                pqt.gui_sleep(100)

                ## get intensity image and show on ImgView1
                img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_INT)
                img = np.array(img['img_data'])
                pqt.show_image(img, 'Intensity ' + roi['name'], 1)

                ## get fast lifetime image and show on ImgView2
                img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_FLT)
                img = np.array(img['img_data'])
                pqt.show_image(img, 'Fast Lifetime ' + roi['name'], 2)

                ## get decay and show on P1
                decay = pql.measurement.get_analysis_curve(ANA_NAME_HISTO, ANA_CRV)
                pqt.plot(decay['data_x'], decay['data_y'], roi['name'], 1)

            print('Measurement stopped')
            print('-------------------------------------------------------------')

            ## get intensity image and show on Imgview1
            img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_INT)
            img = np.array(img['img_data'])
            pqt.show_image(img, 'Intensity ' + roi['name'], 1)

            ## get fast lifetime image and show on Imgview2
            img = pql.measurement.get_analysis_image(ANA_NAME_FLIM, ANA_IMG_FLT)
            img = np.array(img['img_data'])
            pqt.show_image(img, 'Fast Lifetime ' + roi['name'], 2)

            ## get decay and show on P1
            decay = pql.measurement.get_analysis_curve(ANA_NAME_HISTO, ANA_CRV)
            pqt.plot(decay['data_x'], decay['data_y'], roi['name'], 1)

            ## get and print fit parameters
            param_types = pql.measurement.get_analysis_param_types(ANA_NAME_HISTO)
            if (param_types != None) and (ANA_PARAM in param_types):
                print(param_types)
                print(ANA_PARAM)
                params = pql.measurement.get_analysis_param(ANA_NAME_HISTO, ANA_PARAM)
                if params != None:
                    for param in params:
                        print(param)

        pqt.gui_sleep(WAIT_BETWEEN_REPEATS * 1000)

if __name__ == '__main__':
    main()
    print('Done.')
````

### UC_MultiWellFCS.py

````python
'''
USE CASE: Multi-well acquisition FCS
- Load a grid corresponding to the central position on each well of an 18 well or 96 well plate,
  load proper sample preparation metadata and naming of each well.
- Go to each position and record a short FCS curve for 30s for all wells.
- Analyse the results for each FCS curve calculate apparent concentration of the donor, acceptor and double labeled species.

To use this script see the 'User Input' section below.
'''

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

## Additional imports
import json

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_MuliWell
## parameters according to loaded/active USR_SET
ANA_NAME     = 'FCS'
ANA_CRV_AA   = 'AA'
ANA_CRV_AB   = 'AB'
ANA_CRV_BB   = 'BB'
ANA_PARAM_AA = 'AA'
ANA_PARAM_AB = 'AB'
ANA_PARAM_BB = 'BB'

MEAS_TIME = 10 # in seconds
## starting position of the grid measurement in mm 
START_X = -1.0 # in mm
START_Y = -1.0 # in mm
## End User Input ###################################################################

def generate_grid(num_rows: int, num_cols: int, row_spacing: float, col_spacing: float, start_x: float, start_y: float) -> list[tuple[float, float]]:
    '''
    Generate a grid of wells.

    Parameters
    ----------
    num_rows : int
        Number of rows in the grid.
    num_cols : int
        Number of columns in the grid.
    row_spacing : float
        Spacing between rows in mm.
    col_spacing : float
        Spacing between columns in mm.
    start_x : float
        Starting x position in mm.
    start_y : float
        Starting y position in mm.

    Returns
    -------
    list[tuple[float, float]]
        List of well coordinates in m.
    '''

    row_spacing_m = row_spacing * 1e-3
    col_spacing_m = col_spacing * 1e-3
    start_x_m = start_x * 1e-3
    start_y_m = start_y * 1e-3
    grid = []
    row_lbls = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for row in range(num_rows):
        for col in range(num_cols):
            x = start_x_m + col * col_spacing_m
            y = start_y_m + row * row_spacing_m
            grid.append({'name': str(row_lbls[row]) + str(col + 1), 'x': x, 'y': y, 'meta_data': 'Some meta data'})
    return grid

def save_grid(fname: str = '', grid: list = None):
    with open(fname, 'w') as fout:
        json.dump(grid, fout)

def load_grid(fname: str = '') -> list:
    with open(fname, 'r') as file:
        list_of_dicts = json.load(file)
    return list_of_dicts

def plot_grid(grid):
    x = [well['x'] for well in grid]
    y = [well['y'] for well in grid]
    pqt.plot(x, y, 'Grid', 1)

def plot_fcs_curves():
    fcs_crv = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV_AA)
    pqt.plot(fcs_crv['data_x'], fcs_crv['data_y'], fcs_crv['name'], 1)
    fcs_crv = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV_AB)
    pqt.plot(fcs_crv['data_x'], fcs_crv['data_y'], fcs_crv['name'], 1)
    fcs_crv = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV_BB)
    pqt.plot(fcs_crv['data_x'], fcs_crv['data_y'], fcs_crv['name'], 1)

def print_fcs_concentration():
    fcs_params = pql.measurement.get_analysis_param(ANA_NAME, ANA_PARAM_AA)
    for param in fcs_params:
        print('Concentration AA (', param['parameter_set_name'], '): ', param['C'][0], u"\u00B1", param['C'][1], ' ', param['C'][2])
    fcs_params = pql.measurement.get_analysis_param(ANA_NAME, ANA_PARAM_AB)
    for param in fcs_params:
        print('Concentration AB (', param['parameter_set_name'], '): ', param['C'][0], u"\u00B1", param['C'][1], ' ', param['C'][2])
    fcs_params = pql.measurement.get_analysis_param(ANA_NAME, ANA_PARAM_BB)
    for param in fcs_params:
        print('Concentration BB (', param['parameter_set_name'], '): ', param['C'][0], u"\u00B1", param['C'][1], ' ', param['C'][2])

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## generate or load a grid    
    grid = generate_grid(3, 3, 1.0, 1.0, START_X, START_Y)
    #save_grid('grid.json', grid)
    #grid = load_grid('grid.json')
    #plot_grid(grid)
        
    ## set meas duration to time
    pql.measurement.point_conf.stop_on_photons = False
    pql.measurement.point_conf.stop_on_meas_time = True
    pql.measurement.point_conf.meas_time = MEAS_TIME

    ## start measurement loop
    for i, well in enumerate(grid): # loop over grid:
        ## set scan position to well position
        pql.measurement.point_conf.selected_point = (well['x'], well['y'])
        print('Measurement number: ', i + 1, ' Well: ', well['name'])

        ## start measurement
        pql.measurement.start_meas('point')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## plot fcs curves and print concentration
        plot_fcs_curves()
        print_fcs_concentration()
        #return

        ## add your analysis of fcs parameters here
        

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
````

### UC_MultiWellsmFRET.py

````python
'''
USE CASE: Multi-well acquisition smFRET
- Load a grid corresponding to the central position on each well of an 18 well or 96 well plate,
  load proper sample preparation metadata and naming of each well.
- Go to each position and record a smFRET curve for 30s for all wells.
- Report the corresponding S-E histograms, and also their corresponding naming and sample preparation metadata.

To use this script see the 'User Input' section below.
'''

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Help for PQ imports
#help(pql)
#help(pqt)

## External imports
import numpy as np

## Additional imports
import json

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_MuliWell
## parameters according to loaded/active USR_SET
ANA_NAME     = 'Burst FRET'
ANA_IMG = 'SE hist (corr.)'

MEAS_TIME = 10 # in seconds
## starting position of the grid measurement in mm
START_X = -1.0 # in mm
START_Y = -1.0 # in mm
## End User Input ###################################################################

def generate_grid(num_rows: int, num_cols: int, row_spacing: float, col_spacing: float, start_x: float, start_y: float) -> list[tuple[float, float]]:
    '''
    Generate a grid of wells.

    Parameters
    ----------
    num_rows : int
        Number of rows in the grid.
    num_cols : int
        Number of columns in the grid.
    row_spacing : float
        Spacing between rows in mm.
    col_spacing : float
        Spacing between columns in mm.
    start_x : float
        Starting x position in mm.
    start_y : float
        Starting y position in mm.

    Returns
    -------
    list[tuple[float, float]]
        List of well coordinates in m.
    '''

    row_spacing_m = row_spacing * 1e-3
    col_spacing_m = col_spacing * 1e-3
    start_x_m = start_x * 1e-3
    start_y_m = start_y * 1e-3
    grid = []
    row_lbls = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for row in range(num_rows):
        for col in range(num_cols):
            x = start_x_m + col * col_spacing_m
            y = start_y_m + row * row_spacing_m
            grid.append({'name': str(row_lbls[row]) + str(col + 1), 'x': x, 'y': y, 'meta_data': ''})
    return grid

def save_grid(fname: str = '', grid: list = None):
    with open(fname, 'w') as fout:
        json.dump(grid, fout)

def load_grid(fname: str = '') -> list:
    with open(fname, 'r') as file:
        list_of_dicts = json.load(file)
    return list_of_dicts

def plot_grid(grid):
    x = [well['x'] for well in grid]
    y = [well['y'] for well in grid]
    pqt.plot(x, y, 'Grid', 1)

def print_anas():
    anas = pql.measurement.get_analysis_names()
    for ana in anas:
        print('Analysis: ', ana)
        crv_types = pql.measurement.get_analysis_curve_types(ana)
        img_types = pql.measurement.get_analysis_image_types(ana)
        param_types = pql.measurement.get_analysis_param_types(ana)

        if crv_types != None:
            for crv_type in crv_types:
                print('  Curve type: ', crv_type)
        if img_types != None:
            for img_type in img_types:
                print('  Image type: ', img_type)
        if param_types != None:
            for param_type in param_types:
                print('  Parameter type: ', param_type)

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## generate or load a grid
    grid = generate_grid(3, 3, 1.0, 1.0, START_X, START_Y)
    #save_grid('grid.json', grid)
    #grid = load_grid('grid.json')
    #plot_grid(grid)

    ## set meas duration to time
    pql.measurement.point_conf.stop_on_photons = False
    pql.measurement.point_conf.stop_on_meas_time = True
    pql.measurement.point_conf.meas_time = MEAS_TIME

    ## start measurement loop
    for i, well in enumerate(grid): # loop over grid:
        ## set scan position to well position
        pql.measurement.point_conf.selected_point = (well['x'], well['y'])
        print('Measurement number: ', i + 1, ' Well: ', well['name'])

        ## start measurement
        pql.measurement.start_meas('point')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## get SE histogram and show on ImageView1
        img = pql.measurement.get_analysis_image(ANA_NAME, ANA_IMG)
        img_data = np.array(img['img_data'])
        pqt.show_image(img_data, img['img_name'] + ' - ' + well['name'], 1)

        # plot efficiency and stoichiometry on P1
        eff = np.sum(img_data, axis=0)
        eff_x = np.linspace(img['pos_min'][0], img['pos_max'][0], len(eff))
        pqt.plot(eff_x, eff, 'FRET Efficiency', 1)
        stoi = np.sum(img_data, axis=1)
        stoi_x = np.linspace(img['pos_min'][1], img['pos_max'][1], len(stoi))
        pqt.plot(stoi_x, stoi, 'Stoichiometry', 1)
        print('Sample data: ', well['meta_data'])
        
        ## add your analysis of smFRET here

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
````

### UC_PowerOptimizerFCS.py

````python
"""
USE CASE: Power Optimizer for FCS
A problem is how to select the proper power for FCS measurements.
The following process can help:
Record the FCS curve and calculate Mol.brightness, diffusion time and triplet fraction (in case needed) for several different excitation powers.
The maximum power used should be either the maximum power available or a power for which we are clearly in the saturation regime.

To use this script see the 'User Input' section below.
"""

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Low level PQ device imports
import pqdc as pqd

## Help for PQ imports
#help(pql)
#help(pqt)
#help(pqd)

## External imports
import numpy as np

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_OptimizeFCS
## parameters according to loaded/active USR_SET

ANA_NAME  = 'FCS'
ANA_CRV   = 'AA'
ANA_PARAM = 'AA'
WL = 640    ## wavelength in nm

## attenuation parameters in %
ATT_MIN = 40
ATT_MAX = 100
ATT_DELTA = 20

MEAS_TIME = 30
## End User Input ###################################################################

def print_anas():
    anas = pql.measurement.get_analysis_names()
    for ana in anas:
        print('Analysis: ', ana)
        crv_types = pql.measurement.get_analysis_curve_types(ana)
        img_types = pql.measurement.get_analysis_image_types(ana)
        param_types = pql.measurement.get_analysis_param_types(ana)

        if crv_types != None:
            for crv_type in crv_types:
                print('  Curve type: ', crv_type)
        if img_types != None:
            for img_type in img_types:
                print('  Image type: ', img_type)
        if param_types != None:
            for param_type in param_types:
                print('  Parameter type: ', param_type)

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## get attenuator from wavelength
    _, att, _, _ = pql.get_pqdc_laser_assembly(WL)
    att_dev = att['device']
    att_param = att['param']

    ## set meas duration to time
    pql.measurement.point_conf.stop_on_photons = False
    pql.measurement.point_conf.stop_on_meas_time = True
    pql.measurement.point_conf.meas_time = MEAS_TIME

    ## prepare lists and start measurement loop
    att_vals = np.arange(ATT_MIN, ATT_MAX + 1, ATT_DELTA)
    mol_brightness = np.zeros(len(att_vals))
    diff_time = np.zeros(len(att_vals))
    for i, att_val in enumerate(att_vals):
        ## set attenuation of laser attenuator
        pqd.set_value(att_dev, att_param, att_val)
        pos = pqd.get_value(att_dev, att_param)
        att_vals[i] = pos
        print('Attenuator: ', pos, '%')

        ## start measurement
        pql.measurement.start_meas('point')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## print available analyses, curve types, image types and parameter types
        #print_anas()

        # get fcs curve and plot on P1
        fcs_crv = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        pqt.plot(fcs_crv['data_x'], fcs_crv['data_y'], fcs_crv['name'], 1)

        # get mol.brightness and diff.time for 'Pure Diff. (Species: 1)' and plot on P2 and P3
        fcs_params = pql.measurement.get_analysis_param(ANA_NAME, ANA_PARAM)
        fsc_param = fcs_params[0]
        mol_brightness[i] = fsc_param['mol. Brt.'][0]
        diff_time[i] = fsc_param['%tau_1'][0]
        pqt.plot(att_vals, mol_brightness, 'Mol.brightness', 2)
        pqt.plot(att_vals, diff_time, 'Diff.time', 3)

        ## add your stop condition here (e.g. if mol.brightness is saturated)

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
````

### UC_PowerOptimizerFLIM.py

````python
"""
USE CASE: Power Optimizer for FLIM
Set the proper excitation power for FLIM such that no pile up and/or no or only low bleaching is taking place.
This script changes the excitation power while recording the TCSPC decay and the overall intensity.
The optimal power could be the maximum power where
a)  no artifacts appear in the TCSPC decay
b)  no or low bleaching occurs within 10 consecutive frames

To use this script see the 'User Input' section below.
"""

## Basic PQ imports
import pqlumi as pql
import pqtool as pqt

## Low level PQ device imports
import pqdc as pqd

## Help for PQ imports
#help(pql)
#help(pqt)
#help(pqd)

## External imports
import numpy as np

## User Input #######################################################################
USR_SET = '' #LumiPy_UC_OptimizeFLIM
## parameters according to loaded/active usr_set
ANA_NAME      = 'TCSPC histogram'
#ANA_CRV = 'AutoR Detector 2'
#WL = 640    ## wavelength in nm
ANA_CRV = 'Cy3 Detector 4'
WL = 530    ## wavelength in nm

## attenuation parameters
ATT_MIN = 0
ATT_MAX = 100
ATT_DELTA = 20

NUM_FRAMES_1 = 1
NUM_FRAMES_2 = 10
## End User Input ###################################################################

def print_anas():
    anas = pql.measurement.get_analysis_names()
    for ana in anas:
        print('Analysis: ', ana)
        crv_types = pql.measurement.get_analysis_curve_types(ana)
        img_types = pql.measurement.get_analysis_image_types(ana)
        param_types = pql.measurement.get_analysis_param_types(ana)

        if crv_types != None:
            for crv_type in crv_types:
                print('  Curve type: ', crv_type)
        if img_types != None:
            for img_type in img_types:
                print('  Image type: ', img_type)
        if param_types != None:
            for param_type in param_types:
                print('  Parameter type: ', param_type)

def main():
    ## load user settings
    if USR_SET != '':
        print('Load user setting: ', USR_SET)
        pql.measurement.load_user_setting(USR_SET)

    ## get attenuator from wavelength
    _, att, _, _ = pql.get_pqdc_laser_assembly(WL)
    att_dev = att['device']
    att_param = att['param']

    ## set meas duration to num frames
    pql.measurement.img_conf.stop_on_num_frames = True
    pql.measurement.StopOnPhotonsInBrightestPx = False
    pql.measurement.img_conf.stop_on_meas_time = False

    ## prepare lists and start measurement loop
    att_vals = np.arange(ATT_MIN, ATT_MAX + 1, ATT_DELTA)
    bleaching = np.zeros(len(att_vals))
    bleaching_abs = np.zeros(len(att_vals))
    for i, att_val in enumerate(att_vals):
        ## set attenuation of laser attenuator
        pqd.set_value(att_dev, att_param, att_val)
        pos = pqd.get_value(att_dev, att_param)
        att_vals[i] = pos
        print('Attenuator: ', pos, '%')

        ## set num frames to 'num_frames1' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_1
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## print available analyses, curve types, image types and parameter types
        #print_anas()

        ## get decay and calculate count rate
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        counts0 = sum(decay['data_y'])
        print('Counts(0): ', counts0)

        ## set num frames to 'num_frames2' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_2
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## get decay, normalize decay and plot on P1
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        m = max(decay['data_y'])
        ndecay = [x / m for x in decay['data_y']]
        ndecay_x = np.multiply(decay['data_x'], 1E9) ## in ns
        pqt.plot(ndecay_x, ndecay, 'Att: ' + str(att_val) + ' %', 1)

        ## set num frames to 'num_frames1' and start measurement
        pql.measurement.img_conf.num_frames = NUM_FRAMES_1
        pql.measurement.start_meas('image')
        print('Measurement started')
        while True:
            if not pql.measurement.meas_status():
                break
            pqt.gui_sleep(100)
        print('Measurement stopped')

        ## get decay and calculate count rate
        decay = pql.measurement.get_analysis_curve(ANA_NAME, ANA_CRV)
        counts1 = sum(decay['data_y'])
        print('Counts: ', counts1)

        ## calc bleaching and plot on P2
        bleaching[i] = (1 - counts1 / counts0) * 100
        pqt.plot(att_vals, bleaching, 'Bleaching', 2)

        ## add your stop condition here (bleaching, pile up, etc.)
        ## e.g. if bleaching[i] > 30: break

if __name__ == '__main__':
    main()
    print('Done ==============================================================')
````
