# SittingPostureDetection

## Install Packages
```
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install pyserial
```

## Arduino CLI
In In /arduino/ directory:

```
export PATH=$PATH:/home/xw0418/cse237A/SittingPostureDetection/arduino/bin/
```

Arduino compile command:
```
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble .
```

Arduino upload command:
```
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed_nano:nano33ble .
```

## Connect Raspberry Pi and Amazon Echo via Bluetooth
```
sudo apt-get install pulseaudio pulseaudio-module-bluetooth pavucontrol bluez
```

## Text-to-Speech
```
sudo apt-get install espeak
espeak "hello"
```

Or use the `gTTS` library:
```
pip install gTTS
sudo apt-get install mpg123
```