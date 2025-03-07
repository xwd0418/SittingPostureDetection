sudo XDG_RUNTIME_DIR=/run/user/$(id -u) \
    DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus \
    PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
    python /home/xw0418/cse237A/SittingPostureDetection/raspberry_pi/main.py\
        --endpoint $AWS_IOT_ENDPOINT \
        --ca_file ./aws/certs/root-CA.crt \
        --cert ./aws/certs/demoPostureDetection.cert.pem \
        --key ./aws/certs/demoPostureDetection.private.key \
        --client_id basicPubSub \
        --count 0 \
        --topic sdk/test/python