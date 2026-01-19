#-------------------------------------------------------------------------------
# Name:         pqlumi
# Version:      1.0
# Purpose:      Access to PicoQuant Luminosa functions
# Licence:      MIT
# Copyright (c) 2025 PicoQuant GmbH
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import sys
import os

is_fake = False
try:
    import delphi_pqlumi as dm
except:
    is_fake = True
    print('Could not import delphi_pqlumi module. Using fake module instead.')

class ImgConf:
    def __init__(self):
        """
        Initializes an instance of the ImgConf class.

        This class represents the configuration options for an image scan.

        Parameters:
            None

        Returns:
            None
        """

        pass

    @property
    def scan_speed(self) -> int:
        """
        Retrieves the scan speed in %.

        Returns:
            int: The scan speed in %.
        """
        if is_fake:
            return 0
        
        err, speed = dm.get_scan_property('Img', 'ScanSpeed')
        if err:
            raise Exception(err)
        return speed

    @scan_speed.setter
    def scan_speed(self, speed: int):
        """
        Sets the scan speed in %.

        Parameters:
            speed (int): The scan speed in %.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'ScanSpeed', speed)
        if err:
            raise Exception(err)

    @property
    def image_size(self) -> tuple[int, int]:
        """
        Retrieves the image size in x and y direction in pixels.

        Returns:
            tuple[int, int]: The image size in x and y direction in pixels.
        """
        if is_fake:
            return 0, 0
        
        err, size = dm.get_scan_property('Img', 'ImageSize')
        if err:
            raise Exception(err)
        return size

    @image_size.setter
    def image_size(self, size: tuple[int, int]):
        """
        Sets the image size in pixels.

        Parameters:
            size (tuple[int, int]): The image size in x and y direction in pixels.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'ImageSize', size)
        if err:
            raise Exception(err)

    @property
    def stop_on_num_frames(self) -> bool:
        """
        Retrieves the state of the option to stop the scan after a specified number of frames.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, stop = dm.get_scan_property('Img', 'StopOnNumFrames')
        if err:
            raise Exception(err)
        return stop

    @stop_on_num_frames.setter
    def stop_on_num_frames(self, stop: bool):
        """
        Sets the state of the option to stop the scan after a specified number of frames.

        Parameters:
            stop (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'StopOnNumFrames', stop)
        if err:
            raise Exception(err)

    @property
    def num_frames(self) -> int:
        """
        Retrieves the number of frames that will be acquired if the scan option StopOnNumFrames is enabled.

        Returns:
            int: The number of frames to be acquired.
        """
        if is_fake:
            return 0
        
        err, frames = dm.get_scan_property('Img', 'NumFrames')
        if err:
            raise Exception(err)
        return frames

    @num_frames.setter
    def num_frames(self, frames: int):
        """
        Sets the number of frames that will be acquired if the scan option StopOnNumFrames is enabled.

        Parameters:
            frames (int): The number of frames to be acquired.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'NumFrames', frames)
        if err:
            raise Exception(err)

    @property
    def stop_on_photons_in_brightest_px(self) -> bool:
        """
        Retrieves the state of the option to stop the scan after a specified number of photons have been detected in the brightest pixel.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, stop = dm.get_scan_property('Img', 'StopOnPhotonsInBrightestPx')
        if err:
            raise Exception(err)
        return stop

    @stop_on_photons_in_brightest_px.setter
    def stop_on_photons_in_brightest_px(self, stop: bool):
        """
        Sets the state of the option to stop the scan after a specified number of photons have been detected in the brightest pixel.

        Parameters:
            stop (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'StopOnPhotonsInBrightestPx', stop)
        if err:
            raise Exception(err)

    @property
    def photons_in_brightest_px(self) -> int:
        """
        Retrieves the number of photons in the brightest pixel that will be used to stop the scan if the option StopOnPhotonsInBrightestPx is enabled.

        Returns:
            int: The number of photons in the brightest pixel.
        """
        if is_fake:
            return 0
        
        err, photons = dm.get_scan_property('Img', 'PhotonsInBrightestPx')
        if err:
            raise Exception(err)
        return photons

    @photons_in_brightest_px.setter
    def photons_in_brightest_px(self, photons: int):
        """
        Sets the number of photons in the brightest pixel that will be used to stop the scan if the option StopOnPhotonsInBrightestPx is enabled.

        Parameters:
            photons (int): The number of photons in the brightest pixel.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'PhotonsInBrightestPx', photons)
        if err:
            raise Exception(err)

    @property
    def stop_on_meas_time(self) -> bool:
        """
        Retrieves the state of the option to stop the scan after a specified measurement time.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, stop = dm.get_scan_property('Img', 'StopOnMeasTime')
        if err:
            raise Exception(err)
        return stop

    @stop_on_meas_time.setter
    def stop_on_meas_time(self, stop: bool):
        """
        Sets the state of the option to stop the scan after a specified measurement time.

        Parameters:
            stop (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'StopOnMeasTime', stop)
        if err:
            raise Exception(err)

    @property
    def meas_time(self) -> float:
        """
        Retrieves the measurement time in seconds that will be used to stop the scan if the option StopOnMeasTime is enabled.

        Returns:
            float: The measurement time in seconds.
        """
        if is_fake:
            return 0.0
        
        err, time = dm.get_scan_property('Img', 'MeasTime')
        if err:
            raise Exception(err)
        return time

    @meas_time.setter
    def meas_time(self, time: float):
        """
        Sets the measurement time in seconds that will be used to stop the scan if the option StopOnMeasTime is enabled.

        Parameters:
            time (float): The measurement time in seconds.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Img', 'MeasTime', time)
        if err:
            raise Exception(err)

class PointConf:
    def __init__(self):
        """
        Initializes an instance of the PointConf class.

        This class represents the configuration options for a point scan.

        Parameters:
            None

        Returns:
            None
        """
        pass

    @property
    def point_list(self) -> list[tuple[float, float]]:
        """
        Retrieves the coordinates of all points in the overview.

        Returns:
            list[tuple[float, float]]: List of point coordinates in m.
        """
        if is_fake:
            return [(0.0, 0.0)]
        
        err, points = dm.get_scan_property('Point', 'PointList')
        if err:
            raise Exception(err)
        return points

    @point_list.setter
    def point_list(self, points: list[tuple[float, float]]):
        """
        Sets points in the overview.

        Parameters:
            points (list[tuple[float, float]]): List of point coordinates in m.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'PointList', points)
        if err:
            raise Exception(err)

    @property
    def selected_point(self) -> tuple[float, float]:
        """
        Retrieves the coordinates of the selected point.

        Returns:
            tuple[float, float]: Coordinates of the selected point in m. NaN if no point is selected.
        """
        if is_fake:
            return (0.0, 0.0)
        
        err, stop = dm.get_scan_property('Point', 'SelectedPoint')
        if err:
            raise Exception(err)
        return stop

    @selected_point.setter
    def selected_point(self, point: tuple[float, float]):
        """
        Sets the selected point.

        Parameters:
            point (tuple[float, float]): Coordinates of the selected point in m.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'SelectedPoint', point)
        if err:
            raise Exception(err)

    @property
    def stop_on_photons(self) -> bool:
        """
        Retrieves the state of the option to stop the point scan after a specified number of photons have been detected.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, stop = dm.get_scan_property('Point', 'StopOnPhotons')
        if err:
            raise Exception(err)
        return stop

    @stop_on_photons.setter
    def stop_on_photons(self, stop: bool):
        """
        Sets the state of the option to stop the point scan after a specified number of photons have been detected.

        Parameters:
            stop (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'StopOnPhotons', bool(stop))
        if err:
            raise Exception(err)

    @property
    def num_photons(self) -> int:
        """
        Retrieves the number of photons that will be used to stop the point scan if the option StopOnPhotons is enabled.

        Returns:
            int: The number of photons.
        """
        if is_fake:
            return 0
        
        err, photons = dm.get_scan_property('Point', 'NumPhotons')
        if err:
            raise Exception(err)
        return photons

    @num_photons.setter
    def num_photons(self, photons: int):
        """
        Sets the number of photons that will be used to stop the point scan if the option StopOnPhotons is enabled.

        Parameters:
            photons (int): The number of photons.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'NumPhotons', int(photons))
        if err:
            raise Exception(err)

    @property
    def stop_on_meas_time(self) -> bool:
        """
        Retrieves the state of the option to stop the point scan after a specified measurement time.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, stop = dm.get_scan_property('Point', 'StopOnMeasTime')
        if err:
            raise Exception(err)
        return stop

    @stop_on_meas_time.setter
    def stop_on_meas_time(self, stop: bool):
        """
        Sets the state of the option to stop the point scan after a specified measurement time.

        Parameters:
            stop (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'StopOnMeasTime', stop)
        if err:
            raise Exception(err)

    @property
    def meas_time(self) -> float:
        """
        Retrieves the measurement time in seconds that will be used to stop the point scan if the option StopOnMeasTime is enabled.

        Returns:
            float: The measurement time in seconds.
        """
        if is_fake:
            return 0.0
        
        err, time = dm.get_scan_property('Point', 'MeasTime')
        if err:
            raise Exception(err)
        return time

    @meas_time.setter
    def meas_time(self, time: float):
        """
        Sets the measurement time in seconds that will be used to stop the point scan if the option StopOnMeasTime is enabled.

        Parameters:
            time (float): The measurement time in seconds.
        """
        if is_fake:
            return
        
        err = dm.set_scan_property('Point', 'MeasTime', time)
        if err:
            raise Exception(err)

    def lumi_finder(self) -> None:
        """
        Use the 'LumiFinder' to select points based on a previous image measurement.

        Parameters:
            None

        Returns:
            None
        """
        if is_fake:
            return
        
        err = dm.run_lumi_finder()
        if err:
            raise Exception(err)

class Measurement:
    def __init__(self):
        """
        Initializes an instance of the Luminosa class.

        This class represents the configuration options for a Luminosa measurement.

        Parameters:
            None

        Returns:
            None
        """
        self._img_conf = ImgConf()
        self._point_conf = PointConf()
        pass

    @property
    def img_conf(self) -> ImgConf:
        """
        Retrieves the configuration options for an image scan.

        Returns:
            ImgConf: The configuration options for an image scan.
        """
        return self._img_conf

    @property
    def point_conf(self) -> PointConf:
        """
        Retrieves the configuration options for a point scan.

        Returns:
            PointConf: The configuration options for a point scan.
        """
        return self._point_conf

    @property
    def version(self) -> str:
        """
        Retrieves the version of the PicoQuant Luminosa SW.

        Returns:
            str: The Luminosa SW version as a string.
        """
        if is_fake:
            return '1.0'
        
        return dm.get_luminosa_version()

    @property
    def scan_range_min_x(self) -> float:
        """
        Retrieves the minimum X range value of the scan in meter.

        Returns:
            float: The minimum X range value in meter.
        """
        if is_fake:
            return -100E-6
        
        err, range = dm.get_scan_range('MinX')
        if err:
            raise Exception(err)
        return range

    @property
    def scan_range_max_x(self) -> float:
        """
        Retrieves the maximum X range value of the scan in meter.

        Returns:
            float: The maximum X range value in meter.
        """
        if is_fake:
            return 100E-6
        
        err, range = dm.get_scan_range('MaxX')
        if err:
            raise Exception(err)
        return range

    @property
    def scan_range_min_y(self) -> float:
        """
        Retrieves the minimum Y range value of the scan in meter.

        Returns:
            float: The minimum Y range value in meter.
        """
        if is_fake:
            return -100E-6
        
        err, range = dm.get_scan_range('MinY')
        if err:
            raise Exception(err)
        return range

    @property
    def scan_range_max_y(self) -> float:
        """
        Retrieves the maximum Y range value of the scan in meter.

        Returns:
            float: The maximum Y range value in meter.
        """
        if is_fake:
            return 100E-6
        
        err, range = dm.get_scan_range('MaxY')
        if err:
            raise Exception(err)
        return range

    @property
    def scan_range_left(self) -> float:
        """
        Retrieves the left range value of the scan in meter.

        Returns:
            float: The left range value in meter.
        """
        if is_fake:
            return 0.0
        
        err, range = dm.get_scan_range('Left')
        if err:
            raise Exception(err)
        return range

    @scan_range_left.setter
    def scan_range_left(self, left: float):
        """
        Sets the left range value of the scan in meter.

        Parameters:
            left (float): The left range value in meter.
        """
        if is_fake:
            return
        
        err = dm.set_scan_range('Left', left)
        if err:
            raise Exception(err)

    @property
    def scan_range_top(self) -> float:
        """
        Retrieves the top range value of the scan in meter.

        Returns:
            float: The top range value in meter.
        """
        if is_fake:
            return 0.0
        
        err, range = dm.get_scan_range('Top')
        if err:
            raise Exception(err)
        return range

    @scan_range_top.setter
    def scan_range_top(self, top: float):
        """
        Sets the top range value of the scan in meter.

        Parameters:
            top (float): The top range value in meter.
        """
        if is_fake:
            return
        
        err = dm.set_scan_range('Top', top)
        if err:
            raise Exception(err)

    @property
    def scan_range_width(self) -> float:
        """
        Retrieves the width of the scan in meter.

        Returns:
            float: The width of the scan in meter.
        """
        if is_fake:
            return 100E-6
        
        err, range = dm.get_scan_range('Width')
        if err:
            raise Exception(err)
        return range

    @scan_range_width.setter
    def scan_range_width(self, width: float):
        """
        Sets the width of the scan in meter.

        Parameters:
            width (float): The width of the scan in meter.
        """
        if is_fake:
            return
        
        err = dm.set_scan_range('Width', width)
        if err:
            raise Exception(err)

    @property
    def scan_range_height(self) -> float:
        """
        Retrieves the height of the scan in meter.

        Returns:
            float: The height of the scan in meter.
        """
        if is_fake:
            return 100E-6
        
        err, range = dm.get_scan_range('Height')
        if err:
            raise Exception(err)
        return range

    @scan_range_height.setter
    def scan_range_height(self, height: float):
        """
        Sets the height of the scan in meter.

        Parameters:
            height (float): The height of the scan in meter.
        """
        if is_fake:
            return
        
        err = dm.set_scan_range('Height', height)
        if err:
            raise Exception(err)

    @property
    def write_ptu_file(self) -> bool:
        """
        Retrieves the state of the option to write a PTU files during the scan.

        Returns:
            bool: True if the option is enabled, False otherwise.
        """
        if is_fake:
            return False
        
        err, write = dm.get_write_ptu_file()
        if err:
            raise Exception(err)
        return write

    @write_ptu_file.setter
    def write_ptu_file(self, write: bool):
        """
        Sets the state of the option to write a PTU files during the scan.

        Parameters:
            write (bool): Set to True to enable the option, False to disable it.
        """
        if is_fake:
            return
        
        err = dm.set_write_ptu_file(write)
        if err:
            raise Exception(err)

    @property
    def path_to_ptu(self) -> str:
        """
        Retrieves the absolute path to the last PTU file written.

        Returns:
            str: The path to the last PTU file written.
        """
        if is_fake:
            return ''
        
        err, path = dm.get_path_to_ptu()
        if err:
            raise Exception(err)
        return path


    def load_user_setting(self, name: str) -> None:
        """
        Loads a Luminosa user setting specified by the given name.

        Parameters:
            SettName (str): The name of the user setting to load.

        Returns:
            None
        """
        if is_fake:
            return
        
        err = dm.load_user_setting(str(name))
        if err:
            raise Exception(err)

    def set_next_measurement_name(self, name: str) -> None:
        """
        Sets the name for the next measurement.

        Parameters:
            name (str): The name of the next measurement. The default name will be used if name is the empty string.

        Returns:
            None
        """
        if is_fake:
            return
        
        err = dm.set_next_measurement_name(str(name))
        if err:
            raise Exception(err)

    def get_analysis_names(self) -> list:
        """
        Retrieves a list of all available live analysis names that have been configured in the Luminosa SW.

        Returns:
            list: The list of available analysis names.
        """
        if is_fake:
            return ['fake_analysis_name']
        
        err, names = dm.get_analysis_names()
        if err:
            raise Exception(err)
        return names

    def get_analysis_curve_types(self, name: str) -> list:
        """
        Retrieves a list of all available curve types for the given analysis name.

        Parameters:
            name (str): The name of the analysis to query.

        Returns:
            list (of strings): The list of available analysis curve types.
        """
        if is_fake:
            return []
        
        err, types = dm.get_analysis_types(str(name), 'Curve')
        if err:
            raise Exception(err)
        return types

    def get_analysis_curve(self, name: str, curve_type: str) -> dict:
        """
        Retrieves the curve for the given analysis name and curve type.

        Parameters:
            name (str): The name of the analysis to query.
            curve_type (str): The type identifier of the curve to retrieve.

        Returns:
            dict: The curve with the following properties.
                'name': The name of the curve (string),
                'data_x': The x-axis data of the curve (1D list of floats),
                'data_y': The y-axis data of the curve (1D list of floats),
                'axis_title_x': The x-axis title of the curve (string),
                'axis_title_y': The y-axis title of the curve (string),
                'unit_x': The x-axis unit of the curve (string),
                'unit_y': The y-axis unit of the curve (string),

                'data_delta_y': optional: The error of the y-axis data if Analysis is FCS (1D list of floats)

                optional properties below are only returned if the given analysis has a selected fit option:
                'fit_names': The names of the fits (1D list of strings),                    
                'fits_x': The fits x-axis data for each entry in 'fit_names' (2D list of floats with 1st dim: FitModel, 2nd dim: XValues),
                'fits_y': The fits y-axis data for each entry in 'fit_names' (2D list of floats with 1st dim: FitModel, 2nd dim: FitValues),
                'irf_x':  The x-axis data for the IRF used by the fit for each entry in 'fit_names' if Analysis is TCSPC (2D list of floats with 1st dim: FitModel, 2nd dim: XValues),
                'irf_y':  The y-axis data for the IRF used by the fit for each entry in 'fit_names' if Analysis is TCSPC (2D list of floats with 1st dim: FitModel, 2nd dim: IRFValues)
        """
        if is_fake:
            return {
                'name': 'AutoR Detector 2',
                'data_x': [1, 2, 3, 4, 5],
                'data_y': [0, 1, 10, 1, 0],
                'axis_title_x': 'AutoR Detector 2, PIE Window 1, Time',
                'axis_title_y': 'Intensity',
                'unit_x': 's',
                'unit_y': 'Counts'
            }
        
        err, curve = dm.get_analysis(str(name), str(curve_type), 'Curve')
        if err:
            raise Exception(err)
        return curve

    def get_analysis_image_types(self, name: str) -> list:
        """
        Retrieves a list of all available image types for the given analysis name.

        Parameters:
            name (str): The name of the analysis to query.

        Returns:
            list (of strings): The list of available analysis image types.
        """
        if is_fake:
            return []
        
        err, types = dm.get_analysis_types(str(name), 'Image')
        if err:
            raise Exception(err)
        return types

    def get_analysis_image(self, name: str, img_type: str) -> dict:
        """
        Retrieves the image for the given analysis name and image type.

        Parameters:
            name (str): The name of the analysis to query.
            img_type (str): The type identifier of the image to retrieve.

        Returns:
            dict: The image with the following properties:
                'img_name': The name of the image data (string),
                'img_data': The image data itself (2D list of floats),
                'img_unit': The units of the image data (string),
                'pos_min': The min x / y / z overview position of the image in meters (tuple of floats),
                'pos_max': The max x / y / z overview position of the image in meters (tuple of floats),
                'pos_title': The position labels of the image (tuple of strings),
                'pos_unit': The position units of the image (tuple of strings)
        """
        if is_fake:
            #return {}
            return {'img_name': 'Intensity',
                    'img_data': [[1,2,3],[4,5,6],[7,8,9]],
                    'img_unit': 'Counts',
                    'pos_min': (-100E-6, -100E-6, 0.0),
                    'pos_max': (100E-6, 100E-6, 0.0),
                    'pos_title': ('Pixel X', 'Pixel Y', 'Pixel Z'),
                    'pos_unit': ('m', 'm', 'm')}
        
        err, image = dm.get_analysis(str(name), str(img_type), 'Image')
        if err:
            raise Exception(err)
        return image

    def get_analysis_param_types(self, name: str) -> list:
        """
        Retrieves a list of all available parameter types for the given analysis name.

        Parameters:
            name (str): The name of the analysis to query.

        Returns:
            list (of strings): The list of available analysis parameter types.
        """
        if is_fake:
            return []
        
        err, types = dm.get_analysis_types(str(name), 'Param')
        if err:
            raise Exception(err)
        return types

    def get_analysis_param(self, name: str, param_type: str) -> dict:
        """
        Retrieves the parameter for the given analysis name and parameter type.

        Parameters:
            name (str): The name of the analysis to query.
            param_type (str): The type identifier of the parameter to retrieve.

        Returns:
            dict: The parameter with its properties. The available keys depend on analysis and parameter type.
        """
        if is_fake:
            return {}
        
        err, param = dm.get_analysis(str(name), str(param_type), 'Param')
        if err:
            raise Exception(err)
        return param

    def start_meas(self, meas_type: str) -> None:
        """
        Starts a measurement on a PicoQuant Luminosa system.

        Parameters
        ----------
        meas_type: str
            Type of the measurement to start: "image", "line", or "point".
        """
        if is_fake:
            return
        
        err = dm.start_meas(str(meas_type))
        if err:
            raise Exception(err)

    def meas_status(self) -> bool:
        """
        Retrieves the status of a measurement on a PicoQuant Luminosa system.

        Parameters
        ----------
        none

        Returns
        -------
        status : bool
            Measurement status (False: inactive/stopped, True: running)
        """
        if is_fake:
            return False
        
        return dm.meas_status()

    def stop_meas(self) -> None:
        """
        Stops a measurement on a PicoQuant Luminosa system.

        Parameters
        ----------
        none
        """
        if is_fake:
            return
        
        err = dm.stop_meas()
        if err:
            raise Exception(err)

    def get_elapsed_meas_time(self) -> float:
        """
        Retrieves the elapsed measurement time of a measurement on a PicoQuant Luminosa system.

        Parameters
        ----------
        none

        Returns
        -------
        meas_time : float
            Elapsed measurement time in seconds.
        """
        if is_fake:
            return 0.0
        
        err, meas_time = dm.get_elapsed_meas_time()
        if err:
            raise Exception(err)
        return meas_time

    def block_airy_adjustment(self, block: bool = False) -> None:
        """
        Blocks or unblocks the airy adjustment of the PicoQuant Luminosa system.
        This is usefull for a FRAP measurement to reduce the time between bleaching and post-bleraching steps.

        Parameters
        ----------
        block : bool
            Set to True to block the airy adjustment, False to unblock it.
        """
        if is_fake:
            return
        
        dm.block_airy_adjustment(block)

# global luminosa object
measurement = Measurement()

def get_version() -> str:
    """
    Retrieves the version of the pqlumi module (this module).

    Parameters
    ----------
    none

    Returns
    -------
    version : string
        The pqlumi module version as a string.
    """
    if is_fake:
        return '1.0'
    
    version = dm.get_version()
    return version

def get_pqdc_laser_assembly(wl: int = 640) -> tuple:
    """
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
    """
    if is_fake:
        return ({'device': 'Sepia2', 'param_int': 'Intensity1', 'param_cw': 'CW1', 'param_out': 'OutputEnabled1', 'param_off': 'OffsetCoarse1'},
                {'device': 'Attenuator_1', 'param': 'Position'},
                {'device': 'Attenuator_M1', 'param': 'Position'},
                {'device': 'Shutter_1', 'param': 'State'})

    conf_file = os.path.dirname(sys.executable) + '\\PQDevice.conf'
    tree = ET.parse(conf_file)
    root = tree.getroot()
    parent_map: dict = {c: p for p in root.iter() for c in p}

    find_str = './/*[@Wavelength="' + str(wl) + '"]'
    la = root.find(find_str)
    lcu = parent_map[la]

    lh = la.find('.TLaserHead')
    lint = lh.find('.TLaserIntensity')
    lcw = lh.find('.TLaserCW')
    lout = lh.find('.TLaserEnabled')
    loff = lh.find('.TLaserOffsetCoarse')
    las = { 'device'   : lh.get('DBDeviceName'),
            'param_int': lint.get('DBFieldName'),
            'param_cw' : lcw.get('DBFieldName'),
            'param_out': lout.get('DBFieldName'),
            'param_off': loff.get('DBFieldName') }

    latt = la.find('.TAttenuator')
    param = latt.find('.TPosition')
    att = { 'device': latt.get('DBDeviceName'),
            'param' : param.get('DBFieldName') }

    matt = lcu.find('.TMainAttenuator')
    param = matt.find('.TPosition')
    att_main = { 'device': matt.get('DBDeviceName'),
                 'param' : param.get('DBFieldName') }

    sh = lcu.find('.TShutter')
    param = sh.find('.TEnabled')
    shut = { 'device': sh.get('DBDeviceName'),
             'param' : param.get('DBFieldName') }

    return las, att, att_main, shut

def search_pqdc_devices(token1: str, token2: str = '') -> list:
    """
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
    """
    if is_fake:
        return []
    
    conf_file = os.path.dirname(sys.executable) + '\\PQDevice.conf'
    tree = ET.parse(conf_file)
    root = tree.getroot()

    xdevs = []
    for elem in tree.iter():
        try:
            name: str = elem.attrib['Name']
            label: str = elem.attrib['Label']
            db_name: str = elem.attrib['DBDeviceName']
        except:
            continue

        if (token1 in name or token1 in label):
            if token2:
                if (token2 in name or token2 in label):
                    xdevs.append(elem)
            else:
                xdevs.append(elem)

    devs = []
    for xdev in xdevs:
        xflds = xdev.findall('.//*[@DBFieldName]')
        params = []
        for xfld in xflds:
            if xfld.tag != 'TAutomationField':
                params.append(xfld.get('DBFieldName'))

        dev = { 'device': xdev.get('DBDeviceName'),
                'params': params }
        devs.append(dev)

    return devs

