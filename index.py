#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import gzip
import json
import logging
import os

import requests as requests

logger = logging.getLogger('scf')
logger.setLevel(logging.INFO)

API_Key = os.getenv("API_Key")
URL = os.getenv("URL")
SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")


def send_data_to_api(content):
    records = content['records']
    logger.info("Records count: %s" % len(records))

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_Key
    }

    payload = json.dumps(records)
    response = requests.request("POST", URL, headers=headers, data=payload)
    logger.info(response.status_code)
    logger.info(response.text)


def send_data_to_splunk(content):
    records = content['records']
    logger.info("Start to send to splunk")

    headers = {
        'Authorization': 'Splunk ' + SPLUNK_TOKEN,
        'Content-Type': 'application/json'
    }

    payload = ""
    for record in records:
        event = {
            # "sourcetype": "_json",
            "event": record
        }
        payload += json.dumps(event)

    response = requests.request("POST", SPLUNK_URL, headers=headers, data=payload)
    logger.info(response.status_code)
    logger.info(response.text)


def main_handler(event, context):
    logger.debug("start main_handler")
    logger.info(event)

    debase = base64.b64decode(event['clslogs']['data'])
    data = gzip.decompress(debase).decode()
    logger.info(data)

    content = json.loads(data)
    send_data_to_api(content)

    if SPLUNK_URL and SPLUNK_TOKEN:
        send_data_to_splunk(content)

    return 'success'
