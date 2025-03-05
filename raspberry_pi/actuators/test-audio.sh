sudo XDG_RUNTIME_DIR=/run/user/$(id -u) \
    DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus \
    PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
    python echo_audio_output.py