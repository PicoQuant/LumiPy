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
