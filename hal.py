import json
import collections
import serial
import importlib
 
 
uart_properties = collections.namedtuple("uart_properties", ["device", "rx", "tx"]);
 
# beaglebone uart setup
bb_uart1_properties = uart_properties("/dev/tty01", "P9_26", "P9_24");
bb_uart2_properties = uart_properties("/dev/tty02", "P9_22", "P9_21");
bb_uart3_properties = uart_properties("/dev/tty03", "", "P9_42");
bb_uart4_properties = uart_properties("/dev/tty04", "P9_11", "P9_13");
bb_uart5_properties = uart_properties("/dev/tty05", "P8_38", "P8_37");
 
bb_uart_lists = {'UART1' : bb_uart1_properties, \
              'UART2' : bb_uart2_properties, \
              'UART3' : bb_uart3_properties, \
              'UART4' : bb_uart4_properties, \
              'UART5' : bb_uart5_properties}
 
 
 
class hw_interface(object):
    def __init__(self, platform=0):
           
        if (platform == 0):
            self.module = importlib.import_module('mock_Adafruit_BBIO');
            self.uart_lists = bb_uart_lists;
        elif (platform == 1):
            self.module = importlib.import_module('Adafruit_BBIO');
            self.uart_lists = bb_uart_lists;
 
        self.setup_funcdict = {
            'comms': self._setup_serial,
            'gpio': self._setup_gpio,
            'dac': self._setup_dac,
            'adc': self._setup_adc,
        }
       
        # not sure should I use set as we need to determine whether the pins is configure for gpio, dac, adc, uart
        self.pins_used_list = set();
 
    def configure(self, config):
        parsed_config = json.loads(config);
 
        for i in parsed_config:
            config_type = parsed_config[i]["type"];
            configuration = parsed_config[i];
            self.setup_funcdict[config_type](configuration);
    def _setup_serial(self, config):
 
        if (self.uart_lists[config["uart_name"]].rx in self.pins_used_list):
            print("Pins is in used");
            return;
    
        if (self.uart_lists[config["uart_name"]].tx in self.pins_used_list):
            print("Pins is in used");
            return;
    
        self.pins_used_list.add(self.uart_lists[config["uart_name"]].rx);
        self.pins_used_list.add(self.uart_lists[config["uart_name"]].tx);
    
        self.module.UART.setup(config["uart_name"]);
        self.ser = serial.Serial(port = self.uart_lists[config["uart_name"]].device, baudrate=9600)
        self.ser.close()
        self.ser.open()
    
    def _setup_gpio(self, config):
    
        if (config["pin_name"] in self.pins_used_list):
            print("Pins is in used");
            return;
    
        self.pins_used_list.add(config["pin_name"]);
 
        if (config["io_type"] == "input"):
            self.module.GPIO.setup(config["pin_name"], self.module.GPIO.IN);
        else:
            self.module.GPIO.setup(config["pin_name"], self.module.GPIO.OUT);
    
    def _setup_dac(self, config):
    
        if (config["pin_name"] in self.pins_used_list):
            print("Pins is in used");
            return;
    
        self.pins_used_list.add(config["pin_name"]);
 
        self.module.PWM.start(config["pin_name"], 0, 250, 1);
 
        print(config["pin_name"]);
    
     
    def _setup_adc(self, config):
 
        if (config["pin_name"] in self.pins_used_list):
            print("Pins is in used");
            return;
    
        self.pins_used_list.add(config["pin_name"]);
        self.module.ADC.setup();
 
    def readInput(self, pin_name):
        # check if it is in the gpio list
        val = self.module.GPIO.input(pin_name);
        return val;
 
    def writeOutput(self, pin_name, value):
        # check if it is in the gpio list
        if (value == 1):
            self.module.GPIO.output(pin_name, self.module.GPIO.HIGH);
        else:
            self.module.GPIO.output(pin_name, self.module.GPIO.LOW);
 
    def readADC(self, pin_name):
        # check if it is in the adc list
        # There is currently a bug in the ADC driver. You'll need to read the values twice in order to get the latest value.
        value = ADC.read(pin_name);
        value = ADC.read(pin_name);
        return value;
 
    def setVoltage(self, pin_name, value):
        # check if it is in the dac list
        pass;
  
    def writeComms(self, uart_name, data):
        # check if it is in the comms list
        pass;
    def readComms(self, uart_name):
        # check if it is in the comms list
        pass;
 
    def cleanUp(self):   
        pass;
        # GPIO.cleanup();
        # PWM.stop("P9_14")
        # PWM.cleanup()