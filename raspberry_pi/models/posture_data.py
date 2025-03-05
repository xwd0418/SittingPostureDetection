import json
from datetime import datetime

class PostureData:
    def __init__(self,
                 timestamp: str = None,
                 device_id: str = "RPi-001",
                 tilt_angle: float = 12.5,
                 accelerometer: dict = None,
                 gyroscope: dict = None,
                 sitting_state: str = "sitting",
                 ultrasonic_distance: float = 50.0,
                 posture_status: str = "incorrect",
                 posture_confidence: float = 0.85,
                 led_indicator: str = "red",
                 voice_alert: str = "enabled",
                 connection: str = "connected",
                 error: str = None,
                 feedback_received: str = "acknowledged",
                 feedback_timestamp: str = "2025-03-03T10:05:00Z"):
        
        self.timestamp = timestamp if timestamp is not None else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.device_id = device_id

        self.sensor_data = {
            "arduinoData": {
                "tiltAngle": tilt_angle,
                "accelerometer": accelerometer if accelerometer is not None else {"x": 0.01, "y": 0.02, "z": 9.81},
                "gyroscope": gyroscope if gyroscope is not None else {"x": 0.0, "y": 0.1, "z": 0.0},
                "sittingState": sitting_state
            },
            "ultrasonicSensor": {
                "distance": ultrasonic_distance
            }
        }

        self.posture_classification = {
            "status": posture_status,
            "confidence": posture_confidence
        }

        self.reminder_event = {
            "ledIndicator": led_indicator,
            "voiceAlert": voice_alert
        }

        self.system_status = {
            "connection": connection,
            "error": error
        }

        self.user_feedback = {
            "feedbackReceived": feedback_received,
            "feedbackTimestamp": feedback_timestamp
        }

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "deviceId": self.device_id,
            "sensorData": self.sensor_data,
            "postureClassification": self.posture_classification,
            "reminderEvent": self.reminder_event,
            "systemStatus": self.system_status,
            "userFeedback": self.user_feedback
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

if __name__ == '__main__':
    sample_posture = PostureData()
    print(sample_posture.to_json())
