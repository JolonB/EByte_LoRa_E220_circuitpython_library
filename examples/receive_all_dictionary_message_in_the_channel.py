# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# Receiving string from all address by setting BROADCAST ADDRESS
#
# Note: This code was written and tested using CircuitPython on an RPi Pico board.
#       It works with other boards, but you may need to change the UART pins.

import board
import time
from busio import UART

from lora_e220 import LoRaE220, Configuration, BROADCAST_ADDRESS
from lora_e220_operation_constant import ResponseStatusCode

from lora_e220_constants import FixedTransmission, RssiEnableByte

MODULE_MODEL = "900T22D"

# Initialize the LoRaE220 module
uart = UART(board.GP4, board.GP5, baudrate=9600)
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=board.GP10, m0_pin=board.GP11, m1_pin=board.GP12)
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration(MODULE_MODEL)
# Comment this section if you want test transparent trasmission
configuration_to_set.ADDH = BROADCAST_ADDRESS # Address of this receive no sender
configuration_to_set.ADDL = BROADCAST_ADDRESS # Address of this receive no sender
configuration_to_set.CHAN = 23 # Address of this receive no sender
configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
# To enable RSSI, you must also enable RSSI on sender
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}".format(ResponseStatusCode.get_description(code)))

print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_dict()
        # If the sender set RSSI
        code, value, rssi = lora.receive_dict(rssi=True)
        print('RSSI: {}'.format(rssi))

        print(ResponseStatusCode.get_description(code))

        print(value)
        print(value['key1'])
        time.sleep(2)
