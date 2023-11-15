# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# Sending dictionary
#
# Note: This code was written and tested using CircuitPython on an RPi Pico board.
#       It works with other boards, but you may need to change the UART pins.

import board
from busio import UART

from examples.example_config import (
    LORA_AUX,
    LORA_M0,
    LORA_M1,
    MODULE_MODEL,
    UART_RX,
    UART_TX,
)
from lora_e220 import Configuration, LoRaE220
from lora_e220_constants import RssiAmbientNoiseEnable, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

# Initialize the LoRaE220 module
uart = UART(UART_TX, UART_RX, baudrate=9600)
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
new_config = Configuration(MODULE_MODEL)
# To enable RSSI, you must also enable RSSI on receiver
new_config.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
code, confSetted = lora.set_configuration(new_config)
print("Set configuration: {}".format(ResponseStatusCode.get_description(code)))

# Send a dictionary message (transparent)
data = {"key1": "value1", "key2": "value2"}
code = lora.send_transparent_dict(data)
print("Send message: {}".format(ResponseStatusCode.get_description(code)))
