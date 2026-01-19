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
