#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import gzip
import json
import logging
import os
import time

import requests as requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger('scf')
logger.setLevel(logging.INFO)

API_Key = os.getenv("API_Key")
URL = os.getenv("URL")
SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")
SPLUNK_SOURCETYPE = os.getenv("SPLUNK_SOURCETYPE")
SPLUNK_INDEX = os.getenv("SPLUNK_INDEX")


def send_data_to_api(content):
    records = content['records']
    logger.info("Records count: %s" % len(records))

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_Key
    }

    payload = json.dumps(records)

    send_request(URL, headers, payload)


def send_request(url, headers, payload):
    logger.info('Start http request：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    s = requests.Session()
    retries = Retry(total=8,
                    backoff_factor=0.1,
                    allowed_methods=frozenset(['GET', 'POST']),
                    status_forcelist=[500, 502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.mount('http://', HTTPAdapter(max_retries=retries))
    response = s.post(url, headers=headers, data=payload, timeout=10)
    logger.info(response.status_code)
    logger.info(response.text)
    logger.info('End http request：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


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
            "sourcetype": SPLUNK_SOURCETYPE,
            "event": record
        }
        payload += json.dumps(event)

    url = SPLUNK_URL
    if SPLUNK_INDEX:
        url = url + "?index=" + SPLUNK_INDEX

    send_request(url, headers, payload)


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
