import requests
import boto3
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BUCKET_NAME = "zee-nba-pipeline-2026"

response = requests.get(
    "https://api.balldontlie.io/v1/teams",
    headers={"Authorization": API_KEY}
)

data = response.json()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"teams_{timestamp}.json"

with open(filename, "w") as f:
    json.dump(data, f)

s3 = boto3.client("s3")
s3_key = f"raw/teams/{filename}"
s3.upload_file(filename, BUCKET_NAME, s3_key)

print(f"Uploaded {filename} to s3://{BUCKET_NAME}/{s3_key}")