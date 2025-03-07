# SittingPostureDetection

## Setup Python Virtual Environment
```
python3 -m venv ~/venv
source ~/venv/bin/activate
```

## Arduino CLI
First, install the Arduino CLI, and add the bin directory to your PATH.

Arduino compile command:
```
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble .
```

Arduino upload command:
```
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:mbed_nano:nano33ble .
```

## Connect Raspberry Pi and Amazon Echo via Bluetooth
Using GUI to connect the devices is recommended.

## Run the Project
Make sure to add $AWS_IOT_ENDPOINT to your environment variables before running the project.

To run the project, simply run the following command:
```
./run.sh
```