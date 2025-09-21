import boto3, time, os, threading
from flask import Flask

ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("accesskey"),
    aws_secret_access_key=os.getenv("secretkey")
)

INSTANCE_ID = "i-0268811ed956a0b52"

# the actual code
def ec2_watchdog():
    print("Watchdog started")
    while True:
        resp = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        state = resp["Reservations"][0]["Instances"][0]["State"]["Name"]
        if state == "stopped":
            print(f"{INSTANCE_ID} stopped — starting...")
            ec2.start_instances(InstanceIds=[INSTANCE_ID])
        time.sleep(10)  # check every 10 seconds

# a web server because i need to host this on render as a free web service
app = Flask(__name__)

@app.route("/")
def index():
    return "Dummy web server"

@app.route("/ping")
def ping():
    print("Pong!")
    return "Pong!", 200

import time
import requests
import os

URL_TO_PING = "https://keepalive-blxl.onrender.com"

def ping():
    while True:
        try:
            requests.get(URL_TO_PING, timeout=5)
            print("Ping!")
        except Exception as e:
            print("Bonk. ", e)
        time.sleep(60)  # ping every minute
# run em
if __name__ == "__main__":
    # Run watchdog in a separate thread
    threading.Thread(target=ec2_watchdog, daemon=True).start()
    threading.Thread(target=ping, daemon=True).start()
    # Run Flask web server on the port Render expects
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
