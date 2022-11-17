import json
from datetime import datetime
import os
import time
import requests
import logging
from logging import Logger


class TDXProxy():
    """ TDX api proxy """

    TDX_URL_BASE = 'https://tdx.transportdata.tw/api/basic/'

    AUTH_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

    def __init__(self, app_id: str, app_key: str, logger: Logger = logging.getLogger(__name__)):
        self.app_id = app_id
        self.app_key = app_key

        self._auth_token = None
        self._expired_time = datetime.now().timestamp()
        self.logger = logger


    @classmethod
    def from_credential_file(cls, file_name: str = None, logger: Logger = logging.getLogger(__name__)):
        if not file_name:
            file_name = os.getenv("TDX_CREDENTIALS_FILE")

        with open(file_name, "r", encoding='utf-8') as f:
            credentials = json.load(f)
            app_id = credentials['app_id']
            app_key = credentials['app_key']

        return cls(app_id, app_key, logger)


    def get(self, url: str, url_base = TDX_URL_BASE, encoded_parameter = '?$format=JSON', headers: dict = None) -> requests.Response:

        request_headers = self._get_auth_header()
        if headers:
            request_headers = request_headers | headers

        response = requests.get(f'{url_base}{url}{encoded_parameter}', headers=request_headers)

        code = response.status_code

        if code != 200 and code != 304:
            self.logger.error(f'TDX Proxy get {url}, status {code}')
        else:
            self.logger.info(f'TDX Proxy get {url}, status {code}')

        if code == 401:
            self._update_auth()
            return self.get(url, encoded_parameter)
        elif code == 429:
            time.sleep(1)
            return self.get(url, encoded_parameter)

        return response


    def _get_auth_header(self) -> dict:
        if not self._auth_token or datetime.now().timestamp() > self._expired_time:
            self._update_auth()

        return  {
            'authorization': 'Bearer ' + self._auth_token
        }


    def _update_auth(self):
        data = {
            'content-type' : 'application/x-www-form-urlencoded',
            'grant_type' : 'client_credentials',
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }
        response = requests.post(self.AUTH_URL, data).json()
        self._auth_token = response['access_token']
        self._expired_time = datetime.now().timestamp() + response['expires_in'] - 60
