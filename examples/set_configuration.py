# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# It initializes the module, retrieves the current configuration,
# sets a new configuration, and restores the default configuration.
# It also includes examples of sending and receiving data using the module.
#
# Note: This code was written and tested using CircuitPython on a RPi Pico board.
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
from lora_e220 import Configuration, LoRaE220, print_configuration
from lora_e220_constants import (
    AirDataRate,
    FixedTransmission,
    LbtEnableByte,
    OperatingFrequency,
    RssiAmbientNoiseEnable,
    RssiEnableByte,
    SubPacketSetting,
    TransmissionPower,
    TransmissionPower22,
    UARTBaudRate,
    UARTParity,
    WorPeriod,
)
from lora_e220_operation_constant import ResponseStatusCode

# Create a UART object to communicate with the LoRa module
uart = UART(UART_TX, UART_RX, baudrate=9600)

# Create a LoRaE220 object, passing the UART object and pin configurations
lora = LoRaE220(MODULE_MODEL, uart, aux_pin=LORA_AUX, m0_pin=LORA_M0, m1_pin=LORA_M1)

# Initialize the LoRa module and print the initialization status code
code = lora.begin()
print("Initialization: {}".format(ResponseStatusCode.get_description(code)))

##########################################################################################
# GET CONFIGURATION
##########################################################################################

# Retrieve the current configuration of the LoRa module and print it to the console
code, configuration = lora.get_configuration()
print("Retrieve configuration: {}".format(ResponseStatusCode.get_description(code)))
print("------------- CONFIGURATION BEFORE CHANGE -------------")
print_configuration(configuration)

##########################################################################################
# SET CONFIGURATION
# To set the configuration, you must set the configuration with the new values
##########################################################################################

# Create a new Configuration object with the desired settings
new_config = Configuration(MODULE_MODEL)
new_config.ADDL = 0x02
new_config.ADDH = 0x01
new_config.CHAN = 23

new_config.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_100_96
new_config.SPED.uartParity = UARTParity.MODE_00_8N1
new_config.SPED.uartBaudRate = UARTBaudRate.BPS_9600

new_config.OPTION.transmissionPower = (
    TransmissionPower(MODULE_MODEL).get_transmission_power().POWER_10
)
# or
# new_config.OPTION.transmissionPower = TransmissionPower22.POWER_10

new_config.OPTION.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED
new_config.OPTION.subPacketSetting = SubPacketSetting.SPS_064_10

new_config.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
new_config.TRANSMISSION_MODE.WORPeriod = WorPeriod.WOR_1500_010
new_config.TRANSMISSION_MODE.enableLBT = LbtEnableByte.LBT_DISABLED
new_config.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

new_config.CRYPT.CRYPT_H = 1
new_config.CRYPT.CRYPT_L = 1


# Set the new configuration on the LoRa module and print the updated configuration to the console
code, confSetted = lora.set_configuration(new_config)
print("------------- CONFIGURATION AFTER CHANGE -------------")
print(ResponseStatusCode.get_description(code))
print_configuration(confSetted)

##########################################################################################
# RESTORE DEFAULT CONFIGURATION
# To restore the default configuration, you must set the configuration with the default values
##########################################################################################

# Set the configuration to default values and print the updated configuration to the console
print("------------- RESTORE ALL DEFAULT -------------")
new_config = Configuration(MODULE_MODEL)
code, confSetted = lora.set_configuration(new_config)
print(ResponseStatusCode.get_description(code))
print_configuration(confSetted)


# Initialization: {} Success
# Retrieve configuration: {} Success
# ------------- CONFIGURATION BEFORE CHANGE -------------
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  0  ->  410
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
# ------------- CONFIGURATION AFTER CHANGE -------------
# Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x1
# AddL :  0x2
#
# Chan :  23  ->  433
#
# SpeedParityBit :  0b0  ->  8N1 (Default)
# SpeedUARTDatte :  0b11  ->  9600bps (default)
# SpeedAirDataRate :  0b100  ->  9.6kbps
#
# OptionSubPacketSett:  0b10  ->  64bytes
# OptionTranPower :  0b11  ->  10dBm
# OptionRSSIAmbientNo:  0b1  ->  Enabled
#
# TransModeWORPeriod :  0b10  ->  1500ms
# TransModeEnableLBT :  0b0  ->  Disabled (default)
# TransModeEnableRSSI:  0b1  ->  Enabled
# TransModeFixedTrans:  0b1  ->  Fixed transmission (first three bytes can be used
#  as high/low address and channel)
# ----------------------------------------
# ------------- RESTORE ALL DEFAULT -------------
# Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  0  ->  410
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
