#!/usr/bin/python3

"""
Connect to a MAX6675 thermocouple sensor over SPI and read the temperature
from it in ℃.

The datasheet for the MAX6675 is available from
<https://datasheets.maximintegrated.com/en/ds/MAX6675.pdf>.

Michael Fincham <michael@hotplate.co.nz> 2020-07-12
"""

import time

import spidev


class ThermocoupleError(Exception):
    """
    Raised if the MAX6675 doesn't think a working thermocouple is connected.
    """

    pass


class Max6675(object):
    fault = 0x04
    read_period = 0.25  # minimum seconds to wait before reading the chip again
    conversion = 0.25

    def __init__(self, bus=0, device=0):
        self.last_read_time = 0
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 10000
        self.spi.mode = 0b01
        self.spi.lsbfirst = False
        self.spi.bits_per_word = 8

    def read(self):
        """
        If enough time has elapsed since the last reading, poll the chip
        for the current temperature and return a value from 0-1024℃.

        >>> sensor.read()
        22.25
        """
        now = time.time()
        if now - self.last_read_time > self.read_period:
            self.last_read_time = now
            high, low = self.spi.readbytes(2)
            raw = ((high & 0xFF) << 8) | (low & 0xFF)

            if low & self.fault:
                raise ThermocoupleError("No thermocouple detected.")
            else:
                self.last_reading = (raw >> 3) * self.conversion
        return self.last_reading

    def close(self):
        self.spi.close()


if __name__ == "__main__":
    sensor = Max6675()
    while True:
        print(sensor.read())
        time.sleep(sensor.read_period)
