# SittingPostureDetection

## Install Packages
```
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install pyserial
```

## Arduino CLI
In In /arduino/ directory:

Arduino compile command:
```
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble .
```

Arduino upload command:
```
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed_nano:nano33ble .
```