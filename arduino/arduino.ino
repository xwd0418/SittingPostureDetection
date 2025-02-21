#include <Arduino_LSM9DS1.h>

float pitch, roll, tilt;

void setup() {
    Serial.begin(115200);
    while (!Serial);
    
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
    
    Serial.println("IMU initialized");
}

void loop() {
    float accX, accY, accZ;

    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(accX, accY, accZ);
        
        // Calculate pitch and roll from accelerometer data
        pitch = atan2(accX, sqrt(accY * accY + accZ * accZ)) * 180.0 / PI;
        // Roll is calculated using the Y and Z axes
        roll = atan2(accY, sqrt(accX * accX + accZ * accZ)) * 180.0 / PI;

        tilt = atan2(accZ, sqrt(accX * accX + accZ * accZ)) * 180.0 / PI;

        // Serial.print("Pitch: ");
        // Serial.print(pitch);
        // Serial.print("\t Roll: ");
        // Serial.println(roll);
        float imuData[3] = {pitch, roll, tilt};
        Serial.write((uint8_t*)imuData, sizeof(imuData));  // Send raw binary data

        
        // if (abs(pitch) > 15 || abs(roll) > 30) {
        //     Serial.println("Warning: Bad posture detected!");
        // }
    }

    delay(1000);
}
