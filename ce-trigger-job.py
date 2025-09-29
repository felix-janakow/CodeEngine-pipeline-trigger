#!/usr/bin/env python3
import os
import json
import requests
import sys
import logging
# VALIDIERUNG IMPORTS - NACH TEST WIEDER LÖSCHEN
import boto3
from botocore.client import Config

# ============================================
# VALIDIERUNG - NACH TEST WIEDER LÖSCHEN
# ============================================

def create_cos_client():
    """COS Client erstellen - NUR FÜR VALIDIERUNG"""
    cos_api_key = os.environ.get("COS_API_KEY")
    cos_service_instance_id = os.environ.get("COS_SERVICE_INSTANCE_ID")
    cos_endpoint = os.environ.get("COS_ENDPOINT", "https://s3.eu-de.cloud-object-storage.appdomain.cloud")
    
    if not cos_api_key or not cos_service_instance_id:
        print("ERROR: COS_API_KEY oder COS_SERVICE_INSTANCE_ID fehlt", file=sys.stderr)
        sys.exit(1)
    
    cos_client = boto3.client(
        "s3",
        aws_access_key_id="",
        aws_secret_access_key="",
        endpoint_url=cos_endpoint,
        config=Config(signature_version="oauth"),
        region_name="eu-de"
    )
    
    # IAM Token für COS setzen
    token_url = "https://iam.cloud.ibm.com/identity/token"
    token_data = {
        "grant_type": "urn:iam:params:oauth:grant-type:apikey",
        "apikey": cos_api_key
    }
    token_resp = requests.post(token_url, data=token_data)
    token = token_resp.json()["access_token"]
    
    cos_client._request_signer._credentials.token = token
    return cos_client

def create_and_upload_txt(bucket, filename, cos_client):
    """TXT-Datei erstellen und in COS hochladen - NUR FÜR VALIDIERUNG"""
    # TXT-Inhalt erstellen
    txt_content = f"bucket: {bucket}\nfilename: {filename}\n"
    
    # TXT-Dateiname aus ursprünglichem Filename ableiten
    if filename.endswith(('.txt', '.csv', '.json', '.xml')):
        txt_filename = filename.rsplit('.', 1)[0] + '_info.txt'
    else:
        txt_filename = filename + '_info.txt'
    
    try:
        # TXT-Datei in COS hochladen
        cos_client.put_object(
            Bucket=bucket,
            Key=txt_filename,
            Body=txt_content.encode('utf-8')
        )
        print(f"SUCCESS: {txt_filename} erfolgreich in Bucket {bucket} hochgeladen")
        return True
    except Exception as e:
        print(f"ERROR: Upload fehlgeschlagen: {e}", file=sys.stderr)
        return False

# ============================================
# ENDE VALIDIERUNG - BIS HIER LÖSCHEN
# ============================================

def main():
    # CE_DATA enthält im JSON-Format bucket, key etc.
    ce_data = os.environ.get("CE_DATA")
    filename = os.environ.get("CE_SUBJECT")
    if not ce_data:
        print("KEIN CE_DATA gefunden", file=sys.stderr)
        sys.exit(1)
    
    # JSON parsen und Keys extrahieren
    data = json.loads(ce_data)
    bucket = data.get("bucket")
    key = data.get("key")

    print(f"Processing: bucket={bucket}, filename={filename}")
    
    # ============================================
    # VALIDIERUNG CODE - NACH TEST WIEDER LÖSCHEN
    # ============================================
    
    # COS Client erstellen
    cos_client = create_cos_client()
    
    # TXT-Datei erstellen und hochladen
    success = create_and_upload_txt(bucket, filename, cos_client)
    
    if success:
        print("TXT-Datei erfolgreich erstellt und hochgeladen")
    else:
        print("Fehler beim Upload der TXT-Datei", file=sys.stderr)
        sys.exit(1)
    
    # ============================================
    # ENDE VALIDIERUNG CODE
    # ============================================

'''   
    # Watson Studio Pipeline triggern (auskommentiert)
    pipeline_id = os.environ.get("PIPELINE_ID")
    api_key = os.environ.get("IBM_CLOUD_APIKEY")
    cpd_url = os.environ.get("CPD_URL") 

    token = get_iam_token(api_key)
    trigger_resp = trigger_pipeline(cpd_url, pipeline_id, token, bucket, key)
    print("Trigger-Response:", trigger_resp.status_code, trigger_resp.text)
'''



if __name__ == "__main__":
    main()