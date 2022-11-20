import os, sys
ABS_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(ABS_PATH, os.pardir))

from src.tdx_proxy import TDXProxy


def __fetch_basic(proxy: TDXProxy):
    params = {
        "$filter": "Scope/Routes/Any(route: route/RouteID eq '309')",
        '$format': 'JSON'
    }
    return proxy.get('v2/Bus/Alert/City/Taichung', params=params)


def test_from_credentials_file():
    proxy = TDXProxy.from_credential_file("tests/credential.json")
    result = __fetch_basic(proxy)
    assert result.status_code == 200


def test_no_auth():
    proxy = TDXProxy.no_auth()
    result = __fetch_basic(proxy)
    assert result.status_code == 200
