import json
import sys
import serial

from mock_Adafruit_BBIO import ADC
from mock_Adafruit_BBIO import GPIO
from mock_Adafruit_BBIO import PWM
from mock_Adafruit_BBIO import UART 

import builtins
builtins.debug = True;

import hardware_interface


def test_gpio_setup(mocker):
    mocker.patch.object(GPIO, 'setup') 
    json_data = '{"fc_door": {"type": "gpio", "io_type" : "input", "pin_name" : "P8_10"}}';
    parsed_json = json.loads(json_data);
    hardware_interface._setup_gpio(parsed_json["fc_door"]);
    GPIO.setup.assert_called_with("P8_10", 1);


def test_dac_setup(mocker):
    mocker.patch.object(PWM, 'start') 
    json_data = '{"fc_temp": {"type": "dac", "pin_name": "P9_14"}}';
    parsed_json = json.loads(json_data);
    hardware_interface._setup_dac(parsed_json["fc_temp"]);
    PWM.start.assert_called_with("P9_14", 0, 250, 1);

def test_adc_setup(mocker):
    mocker.patch.object(ADC, 'setup') 
    json_data = '{"dummy_adc": {"type": "adc", "pin_name": "P9_13"}}';
    parsed_json = json.loads(json_data);
    hardware_interface._setup_adc(parsed_json["dummy_adc"]);
    ADC.setup.assert_called_with();


def test_serial_setup(mocker):
    mocker.patch.object(UART, 'setup')
    mocker.patch('serial.Serial');
    ser = serial.Serial(port="/dev/tty01", baudrate=9600);
    ser.open();
    ser.close();
    json_data = '{"commlon": {"type" : "comms", "uart_name": "UART1", "baud": "9600"}}';
    parsed_json = json.loads(json_data);
    hardware_interface._setup_serial(parsed_json["commlon"]);
    UART.setup.assert_called_with("UART1")
    # serial.Serial.assert_called_with(port="/dev/tty01", baudrate=9600);

