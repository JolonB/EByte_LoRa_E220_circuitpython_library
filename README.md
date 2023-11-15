# EBYTE LoRa E220 devices CircuitPython library (LLCC68)

## Setup

If your device supports [`circup`](https://github.com/adafruit/circup), you can simply run

```shell
circup install -r requirements.txt
```

If it doesn't support `circup` (for example, ESP32 due to lack of native USB), you can follow [these instructions](https://learn.adafruit.com/circuitpython-with-esp32-quick-start/overview) and then copy [this file](https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Ticks/1.0.12/adafruit_ticks.py) into the filesystem.

<!-- ## Installation
To install the library execute the following command:

```bash
pip install ebyte-lora-e220
``` -->

## Library usage

Here an example of constructor, you must pass the UART interface and (if you want, but it's reccomended)
the AUX pin, M0 and M1.

### Initialization

```python
import board
from busio import UART
from lora_e220 import LoRaE220

uart = UART(board.GP4, board.GP5, baudrate=9600)
lora = LoRaE220("900T22D", uart, aux_pin=board.GP10, m0_pin=board.GP11, m1_pin=board.GP12)
```

### Start the module transmission

```python
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))
```

### Example Scripts

The following examples can also be found in the `examples` directory.
Be sure to edit the `example_config.py` before running.

#### Get Configuration

```python
from lora_e220 import LoRaE220, print_configuration
from lora_e220_operation_constant import ResponseStatusCode

code, configuration = lora.get_configuration()

print("Retrieve configuration: {}", ResponseStatusCode.get_description(code))

print_configuration(configuration)
```

The result

```
----------------------------------------
Initialization: {} Success
Retrieve configuration: {} Success
----------------------------------------
HEAD :  0xc1   0x0   0x8
AddH :  0x0
AddL :  0x0
Chan :  23  ->  433
SpeedParityBit :  0b0  ->  8N1 (Default)
SpeedUARTDatte :  0b11  ->  9600bps (default)
SpeedAirDataRate :  0b10  ->  2.4kbps (default)
OptionSubPacketSett:  0b0  ->  200bytes (default)
OptionTranPower :  0b0  ->  22dBm (Default)
OptionRSSIAmbientNo:  0b0  ->  Disabled (default)
TransModeWORPeriod :  0b11  ->  2000ms (default)
TransModeEnableLBT :  0b0  ->  Disabled (default)
TransModeEnableRSSI:  0b0  ->  Disabled (default)
TransModeFixedTrans:  0b0  ->  Transparent transmission (default)
----------------------------------------
```

#### Set Configuration

You can set only the desidered parameter, the other will be set to default value.

```python
new_config = Configuration('400T22D')
new_config.ADDL = 0x02
new_config.ADDH = 0x01
new_config.CHAN = 23

new_config.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_100_96
new_config.SPED.uartParity = UARTParity.MODE_00_8N1
new_config.SPED.uartBaudRate = UARTBaudRate.BPS_9600

new_config.OPTION.transmissionPower = TransmissionPower('400T22D').\
                                                    get_transmission_power().POWER_10
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
```

I create a CONSTANTS class for each parameter, here a list:
AirDataRate, UARTBaudRate, UARTParity, TransmissionPower, ForwardErrorCorrectionSwitch, WirelessWakeUpTime, IODriveMode, FixedTransmission

#### Send string message

Here is an example of sending data, you can pass a string

```python
lora.send_transparent_message('pippo')
```

```python
lora.send_fixed_message(0, 2, 23, 'pippo')
```

Here the receiver code

```python
while True:
    if lora.available() > 0:
        code, value = lora.receive_message()
        print(ResponseStatusCode.get_description(code))

        print(value)
        utime.sleep_ms(2000)
```

If you want receive RSSI also you must enable it in the configuration

```python
new_config.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
```

and set the flag to True in the receive_message method

```python
code, value, rssi = lora.receive_message(True)
```

Result

```
Success!
pippo
```

#### Send dictionary message

Here is an example of sending data, you can pass a dictionary

```python
lora.send_transparent_dict({'pippo': 'fixed', 'pippo2': 'fixed2'})
```

```python
lora.send_fixed_dict(0, 0x01, 23, {'pippo': 'fixed', 'pippo2': 'fixed2'})
```

Here is the receiver code

```python
while True:
    if lora.available() > 0:
        code, value = lora.receive_dict()
        print(ResponseStatusCode.get_description(code))
        print(value)
        print(value['pippo'])
        utime.sleep_ms(2000)
```

If you want receive RSSI also you must enable it in the configuration

```python
new_config.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
```

and set the flag to True in the receive_dict method

```python
code, value, rssi = lora.receive_dict(True)
```

Result

```
Success!
{'pippo': 'fixed', 'pippo2': 'fixed2'}
fixed
```

## Acknowledgements

This is a port of the [MicroPython library for EBYTE LoRa E220 devices](https://github.com/xreef/EByte_LoRa_E220_micropython_library) (which itself is a port from the [Arduino version](https://github.com/xreef/EByte_LoRa_E220_Series_Library)) to CircuitPython.
Consider looking at those repositories for further information about the hardware.

## Changelog

- 2023-11-14 1.0.0 Functioning and tested on ESP32 and RPi Pico using 900T22D module.
- 2023-11-09 0.0.1 Working library. Not fully tested.
