# max6675-spi-python

The MAX6675 is a cold-junction-compensated K-type thermocouple-to-digital converter from Maxim, commonly found on cheap thermocouple interfaces sold for the Arduino (such as the "HW-550" board). The datasheet for the MAX6675 is available [from Maxim's website](https://datasheets.maximintegrated.com/en/ds/MAX6675.pdf).

With the included library (which depends on Python [spidev](https://pypi.org/project/spidev/)) you can read a thermocouple temperature from one of these chips using Python 3 on Linux through Linux's kernel `spidev` driver.

This code was tested with a `CH341A` based USB SPI interface, though it should work with other interfaces so long as they're supported by `spidev`.

## Usage

Create a `Max6675` object, optionally passing it a `bus` and `device` number (otherwise these both default to `0`).

    >>> from max6675 import Max6675
    >>> sensor = Max6675()

Then read the temperature from the converter by calling the `read` method. Note that other drivers for this converter enforce a minimum interval between reads of 250 milliseconds, which I have also implemented. You may be able to reduce this period at the cost of accuracy. Polling more often than the minimum interval will otherwise return a locally cached value.

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

If the MAX6675 chip can't detect a thermocouple connected then calling `read` will raise a `max6675.ThermocoupleError` exception.

Optionally when finished with the converter call the object's `close` method to release the SPI bus.

    >>> sensor.close()
