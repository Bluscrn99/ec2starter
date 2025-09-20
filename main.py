import boto3, time, os

ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("accesskey"),
    aws_secret_access_key=os.getenv("secretkey")
)

INSTANCE_ID = "i-0268811ed956a0b52"

while True:
    resp = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
    state = resp["Reservations"][0]["Instances"][0]["State"]["Name"]

    if state == "stopped":
        print(f"{INSTANCE_ID} stopped — starting...")
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
    else:
        print(f"{INSTANCE_ID} is {state}")

    time.sleep(10)
