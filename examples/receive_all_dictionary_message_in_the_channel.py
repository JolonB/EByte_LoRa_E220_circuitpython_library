# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# Receiving string from all address by setting BROADCAST ADDRESS
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
from lora_e220 import BROADCAST_ADDRESS, Configuration, LoRaE220
from lora_e220_constants import FixedTransmission, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

# Initialize the LoRaE220 module
uart = UART(UART_TX, UART_RX, baudrate=9600)
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
new_config = Configuration(MODULE_MODEL)
# Comment this section if you want test transparent trasmission
new_config.ADDH = BROADCAST_ADDRESS  # Address of this receive no sender
new_config.ADDL = BROADCAST_ADDRESS  # Address of this receive no sender
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
        # code, value = lora.receive_dict()
        # If the sender set RSSI
        code, value, rssi = lora.receive_dict(rssi=True)
        print("RSSI: {}".format(rssi))

        print(ResponseStatusCode.get_description(code))

        print(value)
        print(value["key1"])
        time.sleep(2)
