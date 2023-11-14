# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script initializes the E220 LoRa module with CircuitPython,
# retrieves the current configuration, and prints it to the console.
# The code demonstrates how to use the LoRaE32 library to interact with the module and read its configuration.
#
# Note: This code was written and tested using CircuitPython on an RPi Pico board.
#       It works with other boards, but you may need to change the UART pins.


import board
from busio import UART

from lora_e220 import LoRaE220, print_configuration
from lora_e220_operation_constant import ResponseStatusCode

from examples.example_config import MODULE_MODEL, UART_TX, UART_RX, LORA_AUX, LORA_M0, LORA_M1

uart = UART(UART_TX, UART_RX, baudrate=9600)

lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)

code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

code, configuration = lora.get_configuration()

print("Retrieve configuration: {}".format(ResponseStatusCode.get_description(code)))

print_configuration(configuration)

#
# Initialization: {} Success
# Retrieve configuration: {} Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  23  ->  433
#
# SpeedParityBit :  0b0  ->  8N1 (Default)
# SpeedUARTDatte :  0b11  ->  9600bps (default)
# SpeedAirDataRate :  0b10  ->  2.4kbps (default)
#
# OptionSubPacketSett:  0b0  ->  200bytes (default)
# OptionTranPower :  0b0  ->  22dBm (Default)
# OptionRSSIAmbientNo:  0b0  ->  Disabled (default)
#
# TransModeWORPeriod :  0b11  ->  2000ms (default)
# TransModeEnableLBT :  0b0  ->  Disabled (default)
# TransModeEnableRSSI:  0b0  ->  Disabled (default)
# TransModeFixedTrans:  0b0  ->  Transparent transmission (default)
# ----------------------------------------
