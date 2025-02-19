void setup() {
    Serial.begin(115200);
    while (!Serial);
}

void loop() {
    int tilt_value = analogRead(A0);
    int shock_value = analogRead(A1);

    Serial.print("Tilt: ");
    Serial.print(tilt_value);
    Serial.print(", Shock: ");
    Serial.println(shock_value);

    delay(1000);
}
