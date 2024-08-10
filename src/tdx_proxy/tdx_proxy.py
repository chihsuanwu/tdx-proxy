import json
from datetime import datetime
import os
import time
import requests
import logging
from logging import Logger

_Timeout = float | tuple[float, float] | None

class TDXProxy():
    """ TDXProxy
    ~~~~~~~~~~~~~~~~~~~~~
    TDX Proxy simplifies the interface process with the TDX platform,
    you can directly call the TDX platform's API as long as
    the Client ID and Secret Key are provided.

    A simple example:

    >>> from tdx_proxy import TDXProxy
    >>> proxy = TDXProxy(app_id=YOUR_TDX_ID, app_key=YOUR_TDX_KEY)
    >>> result = proxy.get(TDX_SERVICE_URL)
    """

    TDX_URL_BASE = 'https://tdx.transportdata.tw/api/basic/'

    AUTH_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

    def __init__(self, app_id: str | None, app_key: str | None, logger: Logger = logging.getLogger(__name__)):
        """ Initialize proxy by `app_id` and `app_key` """
        self.app_id = app_id
        self.app_key = app_key

        self._auth_token = None
        self._expired_time = datetime.now().timestamp()
        self.logger = logger

    @classmethod
    def from_credential_file(cls, file_name: str | None = None, logger: Logger = logging.getLogger(__name__)):
        """ Initialize proxy by credentials file.

        If `file_name` not specified, the environment variable TDX_CREDENTIALS_FILE
        will be used by default,
        """
        if file_name is None:
            file_name = os.getenv("TDX_CREDENTIALS_FILE")

        if file_name is None:
            raise ValueError("No credential file specified and TDX_CREDENTIALS_FILE environment variable is not set")

        with open(file_name, "r", encoding='utf-8') as f:
            credentials = json.load(f)
            app_id = credentials['app_id']
            app_key = credentials['app_key']

        return cls(app_id, app_key, logger)

    @classmethod
    def no_auth(cls, logger: Logger = logging.getLogger(__name__)):
        """ Initialize proxy without authorization.
        NOTE: There are some restrictions in this mode.
        """
        return cls(None, None, logger)

    def get(self, url: str, 
            url_base: str = TDX_URL_BASE, 
            params: dict = {'$format': 'JSON'}, 
            headers: dict | None = None,
            timeout: _Timeout | None = None) -> requests.Response:
        """ Send an API request to TDX platform

        :param url: TDX platfrom api url. No need to include base and params
        :param url_base: TDX url base, default is `https://tdx.transportdata.tw/api/basic/`.
        :param params: (optional) Dictionary, additional params to send in the query string,
            default is `{ '$format': 'JSON' }`.
        :param headers: (optional) Dictionary, additional request headers, e.g. `If-Modified-Since`.
            NOTE: authorization header will be added automatically.
        :param timeout: (optional) Float or Tuple, how long to wait for the server to send data before giving up.
        """

        return self._get_api(url, url_base, params, headers, timeout)

    def _get_api(
            self, 
            url: str, 
            url_base: str, 
            params: dict, 
            headers: dict | None, 
            timeout: _Timeout | None = None,
            retry_times=0) -> requests.Response:
        request_headers = self._get_auth_header(timeout=timeout)
        if headers:
            request_headers = request_headers | headers

        response = requests.get(
            f'{url_base}{url}', params=params, headers=request_headers, timeout=timeout)

        code = response.status_code

        if code != 200 and code != 304:
            self.logger.error(f'TDX Proxy get {url}, status {code}')
            # Retry 3 times, return.
            if retry_times >= 2:
                return response
        else:
            self.logger.info(f'TDX Proxy get {url}, status {code}')

        if code == 401:  # 401 Unauthorized
            if not (self.app_id or self.app_key):
                self.logger.warn(
                    'Authentication requires, please provide APP ID and KEY to continue')
                return response

            # Update authorization.
            self.logger.warn('Fetch new token ...')
            self._update_auth()
            self.logger.warn('Retrying ...')
            return self._get_api(url, url_base, params, headers, retry_times+1)
        elif code == 429:  # 429 rate limit exceeded.
            # If no key provided, return.
            if not (self.app_id or self.app_key):
                self.logger.warn(
                    'TDX api daily limit exceeded, please provide APP ID and KEY to continue')
                return response

            # wait one second and retry.
            self.logger.warn('Waiting 1 sec ...')
            time.sleep(1)
            self.logger.warn('Retrying ...')
            return self._get_api(url, url_base, params, headers, retry_times+1)

        return response

    def _get_auth_header(self, timeout: _Timeout | None = None) -> dict:
        # If no key provide, call api as browser.
        if not (self.app_id or self.app_key):
            return {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
            }

        # If token not yet fetchs, or is expired, fetch new token.
        if not self._auth_token or datetime.now().timestamp() > self._expired_time:
            self._update_auth(timeout=timeout)

        return {
            'authorization': f'Bearer {self._auth_token}'
        }

    def _update_auth(self, timeout: _Timeout | None = None):
        data = {
            'content-type': 'application/x-www-form-urlencoded',
            'grant_type': 'client_credentials',
            'client_id': self.app_id,
            'client_secret': self.app_key
        }
        response = requests.post(self.AUTH_URL, data, timeout=timeout).json()
        self._auth_token = response['access_token']
        self._expired_time = datetime.now().timestamp() + response['expires_in'] - 60
