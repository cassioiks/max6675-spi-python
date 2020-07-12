# max6675-spi-python

The MAX6675 is a cold-junction-compensated K-type thermocouple-to-digital converter from Maxim, commonly found on cheap thermocouple interfaces designed for Arduino and so on (such as the "HW-550" board).

With the included library (which depends on [spidev](https://pypi.org/project/spidev/)) you can read from one of these chips using Python on Linux with Linux's `spidev` kernel module.

This code was tested with a CH341A based USB SPI interface, though I imagine it should work with any Linux `spidev` supported interface.

## Usage

Instantiate the `Max6675` object, optionally passing it a `bus` and `device` number (otherwise these will both default to `0`).

    >>> from max6675 import Max6675
    >>> sensor = Max6675()

Then simply poll the sensor by calling its `read` method. Note that other drivers for this chip enforce a minimum interval between reads of 250 milliseconds, which I have also implemented here. You may be able to experiment with this by editing the class, at the cost of accuracy. Polling more often than the minimum interval will otherwise return a cached value.

    >>> while True:
    ...     print(sensor.read())
    ...     time.sleep(sensor.read_period)
    ... 
    22.75
    23.5
    22.75
    23.5
    23.25
    23.25
    23.25
    23.5

If the MAX6675 chip can't detect a thermocouple connected it will raise a `max6675.ThermocoupleError` exception.
