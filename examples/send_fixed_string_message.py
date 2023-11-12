# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# Sending string to a specified address (receiver)
# ADDH = 0x00
# ADDL = 0x02
# CHAN = 23
#
# Note: This code was written and tested using CircuitPython on an RPi Pico board.
#       It works with other boards, but you may need to change the UART pins.

import board
from busio import UART

from lora_e220 import LoRaE220, Configuration
from lora_e220_constants import FixedTransmission, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

MODULE_MODEL = "900T22D"

# Initialize the LoRaE220 module
uart = UART(board.GP4, board.GP5, baudrate=9600)
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=board.GP10, m0_pin=board.GP11, m1_pin=board.GP12)
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration(MODULE_MODEL)
configuration_to_set.ADDL = 0x02 # Address of this sender no receiver
configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
# To enable RSSI, you must also enable RSSI on receiver
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}".format(ResponseStatusCode.get_description(code)))

# Send a string message (fixed)
message = 'Hello, world!'
code = lora.send_fixed_message(0, 0x01, 23, message)
# The receiver must be configured with ADDH = 0x00, ADDL = 0x01, CHAN = 23
print("Send message: {}".format(ResponseStatusCode.get_description(code)))
