import json
import collections
import serial


if debug:
    from mock_Adafruit_BBIO import ADC
    from mock_Adafruit_BBIO import GPIO
    from mock_Adafruit_BBIO import PWM
    from mock_Adafruit_BBIO import UART 
else:
    import Adafruit_BBIO.ADC as ADC
    import Adafruit_BBIO.GPIO as GPIO
    import Adafruit_BBIO.PWM as PWM
    import Adafruit_BBIO.UART as UART
 
json_data = '{"commlon": {"type" : "comms", "uart_name": "UART1", "baud": "9600"}, \
              "fc_temp": {"type": "dac", "pin_name": "P9_14"}, \
              "pc_temp": {"type": "dac", "pin_name": "P9_14"}, \
              "fc_door": {"type": "gpio", "io_type" : "input", "pin_name" : "P8_10"}}';
 
uart_properties = collections.namedtuple("uart_properties", ["device", "rx", "tx"]);
 
uart1_properties = uart_properties("/dev/tty01", "P9_26", "P9_24");
uart2_properties = uart_properties("/dev/tty02", "P9_22", "P9_21");
uart3_properties = uart_properties("/dev/tty03", "", "P9_42");
uart4_properties = uart_properties("/dev/tty04", "P9_11", "P9_13");
uart5_properties = uart_properties("/dev/tty05", "P8_38", "P8_37");
 
 
uart_lists = {'UART1' : uart1_properties, \
              'UART2' : uart2_properties, \
              'UART3' : uart3_properties, \
              'UART4' : uart4_properties, \
              'UART5' : uart5_properties}
 
pins_used_list = set();
 
 
def _setup_serial(config):
    # print("setup serial");
    # print(config["uart_name"]);
    # print(config["baud"]);
    # print(uart_lists[config["uart_name"]]);
 
    if (uart_lists[config["uart_name"]].rx in pins_used_list):
        # do stuff
        print("Pins is in used");
        return;
 
    if (uart_lists[config["uart_name"]].tx in pins_used_list):
        # do stuff
        print("Pins is in used");
        return;
 
    pins_used_list.add(uart_lists[config["uart_name"]].rx);
    pins_used_list.add(uart_lists[config["uart_name"]].tx);
 
    UART.setup(config["uart_name"]);
    ser = serial.Serial(port = uart_lists[config["uart_name"]].device, baudrate=9600)
    ser.close()
    ser.open()
 
    # if ser.isOpen():
    #     print "Serial is open!"
    #     ser.write("Hello World!")
    # ser.close()
 
def _setup_gpio(config):
    # print("setup gpio");
    # print(config["io_type"]);
    # print(config["pin_name"]);
 
    if (config["pin_name"] in pins_used_list):
        # do stuff
        print("Pins is in used");
        return;
 
    pins_used_list.add(config["pin_name"]);

    GPIO.setup(config["pin_name"], GPIO.OUT)
 
    # GPIO.setup("P8_10", GPIO.OUT)
    # GPIO.output("P8_10", GPIO.HIGH)
 
    # GPIO.setup("P8_14", GPIO.IN)
 
 
def _setup_dac(config):
    # print("setup dac");
    # print(config["pin_name"]);
 
    if (config["pin_name"] in pins_used_list):
        print("Pins is in used");
        return;
 
    pins_used_list.add(config["pin_name"]);

    PWM.start(config["pin_name"], 0, 250, 1);
 
# PWM.start("P9_14", 50)
# #optionally, you can set the frequency as well as the polarity from their defaults:
# PWM.start("P9_14", 50, 1000, 1)
#PWM.start(channel, duty, freq=2000, polarity=0)
 
 
# PWM.set_duty_cycle("P9_14", 25.5)
# PWM.set_frequency("P9_14", 10)
 
# fPWM = 250 Hz, VL=0V, VH=5V, R=10K, C=1uF.
 
 
 
def _setup_adc(config):
    # print("setup adc");
    # print(config["pin_name"]);
 
    if (config["pin_name"] in pins_used_list):
        print("Pins is in used");
        return;
 
    pins_used_list.add(config["pin_name"]);
    ADC.setup();
 
setup_funcdict = {
    'comms': _setup_serial,
    'gpio': _setup_gpio,
    'dac': _setup_dac,
    'adc': _setup_adc,           
}
 
 
# class hardware_interface:
#     def __init__(self, config):
       
 
#     def _setup_serial(self):
 
#     def _setup_adc(self):
 
#     def _setup_gpio(self):
 
#     def _setup_dac(self):
 
 
#     def readinput(self, pin_name):
       
          # GPIO.input("P8_14")
#         return value;
 
#     def write_output(self, pin_name, value):
 
    # GPIO.output("P8_10", GPIO.HIGH)
 
 
#     def readADC(self, pin_name):
 
 
# There is currently a bug in the ADC driver. You'll need to read the values twice in order to get the latest value.
 
#     value = ADC.read("P9_40")
# voltage = value * 1.8 #1.8V
#         return value;
 
#     def setVoltage(self, pin_name, value):
 
   
#     def writeComms(self, uart_name, data):
 
 
#     def readComms(self, uart_name):
 
#         return data;
 
#     def cleanUp(self):
#         GPIO.cleanup();
# PWM.stop("P9_14")
# PWM.cleanup()
 
 
 
if __name__ == "__main__" :
    parsed_json = json.loads(json_data);
    # print(parsed_json['103']['class'])
 
    # print(uart_lists["UART1"]);
 
    for i in parsed_json:
        # print(parsed_json[i]["type"]);
        config_type = parsed_json[i]["type"];
        configuration = parsed_json[i];
        # print(config_type);
        setup_funcdict[config_type](configuration);
    # print(json.loads(json_data));
 
    print(pins_used_list);