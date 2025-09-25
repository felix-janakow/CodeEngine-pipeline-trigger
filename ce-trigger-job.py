#!/usr/bin/env python3
import os
import json
import requests
import sys
import logging

def main():
    # CE_DATA enthält im JSON-Format bucket, key etc.
    ce_data = os.environ.get("CE_DATA")
    if not ce_data:
        print("KEIN CE_DATA gefunden", file=sys.stderr)
        sys.exit(1)
    data = json.loads(ce_data)
    bucket = data.get("bucket")
    key = data.get("key")

    print(f"Empfangenes Event: bucket={bucket}, key={key}")
    logging.info(f"bucket={bucket}, key={key}")

'''   
    # Watson Studio Pipeline triggern
    pipeline_id = os.environ.get("PIPELINE_ID")
    api_key = os.environ.get("IBM_CLOUD_APIKEY")
    cpd_url = os.environ.get("CPD_URL") 

    token = get_iam_token(api_key)
    trigger_resp = trigger_pipeline(cpd_url, pipeline_id, token, bucket, key)
    print("Trigger-Response:", trigger_resp.status_code, trigger_resp.text)

def get_iam_token(api_key: str) -> str:
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def trigger_pipeline(cpd_url, pipeline_id, token, bucket, key):
    # Pipeline starten; Beispiel POST
    url = f"{cpd_url}/v2/pipelines/{pipeline_id}/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "params": {
            "bucket": bucket,
            "key": key
        }
    }
    return requests.post(url, json=payload, headers=headers)

'''
if __name__ == "__main__":
    main()
