# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# It includes examples of sending and receiving string using both transparent and fixed transmission modes.
# The code also configures the module's address and channel for fixed transmission mode.
# Address and channel of this receiver:
# ADDH = 0x00
# ADDL = 0x01
# CHAN = 23
#
# Can be used with the send_fixed_string and send_transparent_string scripts
#
# Note: This code was written and tested using CircuitPython on an RPi Pico board.
#       It works with other boards, but you may need to change the UART pins.

import time

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
from lora_e220_constants import FixedTransmission, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

# Initialize the LoRaE220 module
# uart = UART(UART_TX, UART_RX, baudrate=9600)
uart = UART(UART_TX, UART_RX, baudrate=9600)
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)
# lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
new_config = Configuration(MODULE_MODEL)
new_config.ADDH = 0x00  # Address of this receive no sender
new_config.ADDL = 0x01  # Address of this receive no sender
new_config.CHAN = 23  # Address of this receive no sender
new_config.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
# To enable RSSI, you must also enable RSSI on sender
new_config.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(new_config)
print("Set configuration: {}".format(ResponseStatusCode.get_description(code)))

print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_message()
        # If the sender set RSSI
        code, value, rssi = lora.receive_message(rssi=True)
        print("RSSI: ", rssi)

        print(ResponseStatusCode.get_description(code))

        print(value)
        time.sleep(2)
