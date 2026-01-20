# LumiPy

LumiPy is a Python interface for controlling and acquiring data from PicoQuant's Luminosa microscope systems. This library provides a high-level API to interact with various components of the Luminosa system, including confocal imaging, point scanning, and data acquisition.

## Features

- Control of Luminosa microscope hardware at high and low level
- Image and point scanning capabilities
- Data acquisition and live analysis
- Visualization tools
- ...

## Installation

1. Ensure you have Python 3.9 or later installed
2. Install the required dependencies:
   ```bash
   pip install numpy
   ```

## Getting Started

### Basic Usage

```python
# Import the measurement instance
from pqlumi import measurement
import pqtool

# Set up scan parameters
measurement.img_conf.stop_on_num_frames = True
measurement.img_conf.num_frames = 1

# Start an image measurement
measurement.start_meas('image')
print('Measurement started')

# Check measurement status
while measurement.meas_status():
    elapsed = measurement.get_elapsed_meas_time()
    print(f"Measurement running: {elapsed:.1f} seconds")
    pqtool.gui_sleep(500)
print('Measurement stopped')

# Access live analysis data
analysis_names = measurement.get_analysis_names()
for name in analysis_names:
    print(f"Available analysis: {name}")
```

**Note:**

When using Luminosas integrated Python editor on a real system, all necessary PQ libraries can be imported directly (as shown above).

If you want to develop on a remote PC without HW you need to make sure that the libraries can be found (e.g. by including the path to the libs/ directory; copying the libs to your project path; etc.)

## Examples

The `demos/` directory contains various example scripts demonstrating different functionalities:

- `Demo_pqlumi_*.py` - Basic Luminosa operations
- `Demo_pqdc_*.py` - Device control examples
- `Demo_pqharp.py` - TCSPC control examples
- `Demo_pqharp_CountMeter.py` - A simple countmeter chart
- `Demo_pqharp_LevelScan.py` - A script for scanning the trigger level of an input channel
- `Demo_pqcam.py` - Camera control examples
- `Demo_pqscan.py` - Scanner control examples
- `UC_*.py` - Use case examples (FRAP, FCS, etc.)

## Main Modules and Classes

- `pqlumi.py` - Main interface for Luminosa control
  - `Measurement` - Main class for controlling measurements
  - `ImgConf` - Configuration class for image scanning
  - `PointConf` - Configuration class for point scanning
- `pqtool.py` - Helper functions for plotting, logging, etc.
- `pqdc.py` - Device control module (all devices except cameras, TCSPC (Harp) & scanner)
- `pqcam.py` - Camera control module
- `pqharp.py` - Time-correlated single photon counting (TCSPC) module
- `pqscan.py` - Scanner control module

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact PicoQuant support at support@picoquant.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

**Use LumiPy at your own risk. We are not responsible for any damages or losses resulting from the use of this software.**

<img src="Icon.png" alt="LumiPy logo" style="height: 256px; width:256px;"/>
