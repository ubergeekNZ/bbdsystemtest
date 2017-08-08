import sys

class ADC(object):
    def setup(self, pinname, direction):
        pass;

class GPIO(object):
    OUT = 1;
    def setup(self, pinname, direction):
        pass;


class PWM(object):
    def start(self, pinname, duty, freq, polarity):
        pass;

class UART(object):
    def setup(self, pinname):
        pass;