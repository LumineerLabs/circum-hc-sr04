# circum-hc-sr04

![build](https://travis-ci.com/LumineerLabs/circum-hc-sr04.svg?branch=master) ![PyPI](https://img.shields.io/pypi/v/circum-hc-sr04)

HC-SR04 sensor plugin for [circum](https://github.com/LumineerLabs/circum).

NOTE: this package installs, but it has not been tested with hardware.

## Install

```bash
pip3 install circum-hc-sr04
```

## Usage

```bash
Usage: circum-endpoint hc-sr04 [OPTIONS]

Options:
  --num-samples INTEGER     The number of samples to average per reading.
  --trigger-pin INTEGER     The pin used to trigger the HC-SR04.  [required]
  --echo-pin INTEGER        The pin the HC-SR04 will signal the echo on.
                            [required]
  --speed-of-sound INTEGER  Override the speed of sound to a calibrated value
                            in m/s.
  --threshold INTEGER       Only register an object if it is at least
                            threshold cm closer than the furthest distance
                            returned so far. This accounts for unmoving
                            objects in the sensors range at the cost of
                            missing moving objects that are present when the
                            sensor starts.
  --help                    Show this message and exit.
```

To get more accurate readings, you can calibrate the sensor. Place an object a known distance from the sensor and pass the appropriate values to the calibration script. This will result in a value that can be passed to the endpoint sensor.
```bash
Usage: calibrate-hc-sr04 [OPTIONS]

Options:
  --trigger-pin INTEGER  The pin used to trigger the HC-SR04.  [required]
  --echo-pin INTEGER     The pin the HC-SR04 will signal the echo on.
                         [required]
  --samples INTEGER      The number of samples to calibrate with.
  --distance INTEGER     The distance to the calibration object in cm.
                         [required]
  --help                 Show this message and exit.
```
