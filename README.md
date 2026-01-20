# LumiPy

LumiPy is a Python interface for controlling and acquiring data from PicoQuant's Luminosa microscope systems. This library provides a high-level API to interact with various components of the Luminosa system, including confocal imaging, point scanning, and data acquisition.

## Features

- Control of Luminosa microscope hardware
- Image and point scanning capabilities
- Data acquisition and analysis
- Integration with PicoQuant's TCSPC devices
- Live analysis and visualization tools

## Installation

1. Ensure you have Python 3.7 or later installed
2. Install the required dependencies:
   ```bash
   pip install numpy matplotlib
   ```

## Getting Started

### Basic Usage

```python
import pqlumi
import pqtool

# Create a measurement instance
measurement = pqlumi.measurement

# Set up scan parameters
measurement.scan_range_width = 100e-6  # 100 μm
measurement.scan_range_height = 100e-6  # 100 μm

# Start an image measurement
measurement.start_meas("image")

# Check measurement status
while measurement.meas_status():
    elapsed = measurement.get_elapsed_meas_time()
    print(f"Measurement running: {elapsed:.1f} seconds")
    pqtool.gui_sleep(25)

# Access measurement data
analysis_names = measurement.get_analysis_names()
for name in analysis_names:
    print(f"Available analysis: {name}")
```

## Examples

The `demos/` directory contains various example scripts demonstrating different functionalities:

- `Demo_pqlumi_*.py` - Basic Luminosa operations
- `Demo_pqdc_*.py` - Device control examples
- `Demo_pqharp.py` - TCSPC control examples
- `Demo_pqharp_CountMeter.py` - A simple countmeter chart
- `Demo_pqharp_LevelScan.py` - A simple program for scanning the trigger level of an input channel
- `Demo_pqcam.py` - Camera control examples
- `Demo_pqscan.py` - Scanner control examples
- `UC_*.py` - Use case examples (FRAP, FCS, etc.)

## Documentation

### Main Modules

- `pqlumi.py` - Main interface for Luminosa control
- `pqtool.py` - Helper functions for plotting, logging, etc.
- `pqdc.py` - Device control module (all devices except cameras, TCSPC (Harp) & scanner)
- `pqcam.py` - Camera control module
- `pqharp.py` - Time-correlated single photon counting (TCSPC) module
- `pqscan.py` - Scanner control module

### Key Classes

- `Measurement` - Main class for controlling measurements
- `ImgConf` - Configuration for image scanning
- `PointConf` - Configuration for point scanning

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please contact PicoQuant support at support@picoquant.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

**Use LumiPy at your own risk. We are not responsible for any damages or losses resulting from the use of this software.**

<img src="Icon.png" alt="LumiPy logo" style="height: 100px; width:100px;"/>