# TDX Proxy

[中文 doc](https://github.com/chihsuanwu/tdx-proxy/blob/main/README.md)

A python package for [TDX platform](https://tdx.transportdata.tw/) (MOTC, Taiwan)

TDX Proxy simplifies the interface process with the TDX platform, you can directly call the TDX platform's API as long as the Client ID and Secret Key are provided.

TDX Proxy supports calling the TDX platform without using the API keys, but there are some [restrictions](https://tdx.transportdata.tw/api-service/swagger), such as the limitation of each call per IP is 50 times per day, etc.

A simple example:

```python
from tdx_proxy import TDXProxy

proxy = TDXProxy(app_id=YOUR_TDX_ID, app_key=YOUR_TDX_KEY)

result = proxy.get(TDX_SERVICE_URL)
```

# Installing TDX Proxy

Installing via [Pypi](https://pypi.org/project/motc-tdx-proxy/)

```console
$ pip install motc-tdx-proxy
```

Requires python 3.9+

# Features

- Automatically authenticate and get the **Access Token**
- **Access Token** caching, and automatically re-acquire another token only when it expires or verification fails
- Automatically handle [TDX API rate limie](https://github.com/tdxmotc/SampleCode#api%E4%BD%BF%E7%94%A8%E6%AC%A1%E6%95%B8%E9%99%90%E5%88%B6)
- Supporting calling the TDX platform without using the API keys with some [restrictions](https://tdx.transportdata.tw/api-service/swagger)

# Documentation

## Initialize Proxy

To initialize the Proxy, use the ID and KEY as parameters, or use the credential file

```python
# Use the ID and KEY directly
proxy = TDXProxy(app_id=YOUR_TDX_ID, app_key=YOUR_TDX_KEY)

# Use the credential file
# If file_name is not specified, the environment variable TDX_CREDENTIALS_FILE will be used by default
proxy = TDXProxy.from_credential_file(file_name=YOUR_CREDENTAIL_FILE)
```

The credential file is a Json file with the following format:
```json
{
    "app_id": "YOUR_ID",
    "app_key": "YOUR_KEY"
}
```

It is also possible to initialize the proxy without using the API key, but there are some [restrictions](https://tdx.transportdata.tw/api-service/swagger),
such as the limitation of each call per IP is 50 times per day, etc.

```python
# Without using the API key
proxy = TDXProxy.no_auth()
```

## Calling TDX API

Use `TDXProxy.get()` to call TDX API, return is a [requests.Response](https://requests.readthedocs.io/en/latest/api/#requests.Response) object.

```python
result = proxy.get('v3/Rail/TRA/DailyTrainTimetable/TrainDates')
```

### **Parameters:**
- **url** - TDX API URL, no need to include base and params
- **url_base** - (Optional) default is `https://tdx.transportdata.tw/api/basic/`
- **params** - (Optional) Dict，extra params, default is `{ 'format': 'JSON' }`
- **headers** - (Optional) Dict，extra headers, e.q. `If-Modified-Since`, authorization header will be added automatically