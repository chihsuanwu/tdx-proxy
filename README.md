# TDX Proxy

[English docs](https://github.com/chihsuanwu/tdx-proxy/blob/main/README.en.md)

台灣交通部「[TDX運輸資料流通服務平臺](https://tdx.transportdata.tw/)」之python介接套件

TDX Proxy 將與 TDX 平台之介接流程簡化，只要給予 Client ID 與 Secret Key，
便能直接對 TDX 平台之 API 進行呼叫。

TDX Proxy 支援不使用 API 金鑰呼叫 TDX 平台，但含有部分
[限制](https://tdx.transportdata.tw/api-service/swagger)，如每個呼叫來源端IP的上限為每日50次等。

一個簡單範例：

```python
from tdx_proxy import TDXProxy

proxy = TDXProxy(app_id=YOUR_TDX_ID, app_key=YOUR_TDX_KEY)

result = proxy.get(TDX_SERVICE_URL)
```

# Installing TDX Proxy

TDX Proxy 可透過 [PyPI](https://pypi.org/project/motc-tdx-proxy/) 安裝

```console
$ pip install motc-tdx-proxy
```

需求 python 3.9+

# Features

- 自動進行身分驗證並取得 **Access Token**
- **Access Token** 快取機制，只在過期或驗證錯誤時再自動重新取得 Token
- 自動處理 [TDX 呼叫頻率限制](https://github.com/tdxmotc/SampleCode#api%E4%BD%BF%E7%94%A8%E6%AC%A1%E6%95%B8%E9%99%90%E5%88%B6)
- 支援不使用 API 金鑰呼叫 TDX 平台 [(含部分限制)](https://tdx.transportdata.tw/api-service/swagger)

# Documentation

## Initialize Proxy

初始化 Proxy 可將 ID 與 KEY 直接作為參數帶入，或使用 credential 檔案

```python
# 直接帶入參數
proxy = TDXProxy(app_id=YOUR_TDX_ID, app_key=YOUR_TDX_KEY)

# 使用 credential 檔案
# file_name 若不指定，將會使用環境變數 TDX_CREDENTIALS_FILE 作為預設路徑
proxy = TDXProxy.from_credential_file(file_name=YOUR_CREDENTAIL_FILE)
```

其中 credential 檔案為 Json 檔，格式如下
```json
{
    "app_id": "YOUR_ID",
    "app_key": "YOUR_KEY"
}
```

也可以不使用 API 金鑰初始化 proxy，但含有部分
[限制](https://tdx.transportdata.tw/api-service/swagger)，如每個呼叫來源端IP的上限為每日50次等。

```python
# 不使用 API 金鑰
proxy = TDXProxy.no_auth()
```

## Calling TDX API

使用 `TDXProxy.get()` 呼叫 TDX API，
回傳為 [requests.Response](https://requests.readthedocs.io/en/latest/api/#requests.Response) 物件

```python
result = proxy.get('v3/Rail/TRA/DailyTrainTimetable/TrainDates')
```

### **Parameters:**
- **url** - TDX API URL，不須包含 base 以及 parameter ，如下所述
- **url_base** - (Optional) 預設為 `https://tdx.transportdata.tw/api/basic/`
- **params** - (Optional) Dict，額外的參數，預設為 `{ 'format': 'JSON' }`
- **headers** - (Optional) Dict，額外的 headers 如 `If-Modified-Since`，authorization header 會在呼叫 API 時自動加入