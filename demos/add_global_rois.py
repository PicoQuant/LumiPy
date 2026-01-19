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
