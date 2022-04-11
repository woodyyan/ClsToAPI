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


def send_data(records):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_Key
    }

    for record in records:
        payload = json.dumps(record)
        response = requests.request("POST", URL, headers=headers, data=payload)
        logger.info(response.status_code)
        logger.info(response.text)


def main_handler(event, context):
    logger.debug("start main_handler")
    logger.info(event)

    debase = base64.b64decode(event['clslogs']['data'])
    data = gzip.decompress(debase).decode()
    logger.info(data)

    send_data(data)
    return 'success'
