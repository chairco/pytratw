# -*- coding: utf-8 -*-
import requests
import hmac
import hashlib
import base64

from datetime import datetime

try:
    from .stationid import *
    from .env import APPID_L1, APPKEY_L1
except Exception as e:
    from stationid import *
    from env import APPID_L1, APPKEY_L1


AppID = APPID_L1  # apply's id
AppKey = APPKEY_L1  # apply's secret
x_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')  # SPEC require
message = "x-date: " +  x_date


def create_hmac(secretkey, message):
    """create hmac object
    types: secretkey: str
    types: message: str
    rtypes: auth: object hmac.HMAC
    """
    auth = hmac.new(bytes(secretkey, 'utf-8'), digestmod=hashlib.sha1)
    auth.update(bytes(message, 'utf-8'))
    return auth


def base64_digest(auth):
    """encode hmac to base64
    types: auth: hmac's object
    rtype: singnature: base64.decode('utf-8')
    """
    if not isinstance(auth, hmac.HMAC):
        raise Exception("'auth' Invalid Input type")

    signature = base64.b64encode(auth.digest())  # auth.hexdigest()
    signature = signature.decode('utf-8')
    return signature


