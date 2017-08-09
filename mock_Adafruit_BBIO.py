
class ADC(object):
    def setup(pinname, direction):
        pass;
 
class GPIO(object):
    IN = 0;
    OUT = 1;
 
    LOW = 0;
    HIGH = 1;
    def setup(pinname, direction):
        pass;
    def input(pinname):
        pass;
    def output(pinname, value):
        pass;
 
class PWM(object):
    def start(pinname, duty, freq, polarity):
        pass;
 
class UART(object):
    def setup(pinname):
        pass;