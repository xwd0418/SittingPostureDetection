#!/bin/bash
if [ -z "$AWS_IOT_ENDPOINT" ]; then
    echo "Please set the AWS_IOT_ENDPOINT environment variable."
    exit 1
fi

# python3 ./raspberry_pi/test/PubSub.py --endpoint $AWS_IOT_ENDPOINT \
#                 --ca_file $AWS_IOT_CA_FILE \
#                 --cert $AWS_IOT_CERT \
#                 --key $AWS_IOT_KEY \
#                 --client_id postureDetection \
#                 --topic sdk/test/python \

echo "Starting Sitting Posture Detection..."
python3 ./raspberry_pi/test/PubSub.py \
    --endpoint $AWS_IOT_ENDPOINT \
    --ca_file ./aws/certs/root-CA.crt \
    --cert ./aws/certs/demoPostureDetection.cert.pem \
    --key ./aws/certs/demoPostureDetection.private.key \
    --client_id basicPubSub \
    --count 0 \
    --topic sdk/test/python
    # --topic rpi/posture/data