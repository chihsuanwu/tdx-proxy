import sys
sys.path.append('../')

from src.tdx_proxy import TDXProxy

def __fetch_basic(proxy: TDXProxy):
    params = {
        "$filter": "Scope/Routes/Any(route: route/RouteID eq '309')",
        '$format': 'JSON'
    }
    return proxy.get('v2/Bus/Alert/City/Taichung', params=params)

def test_from_credentials_file():
    proxy = TDXProxy.from_credential_file("credential.json")
    result = __fetch_basic(proxy)
    assert result.status_code == 200

def test_no_auth():
    proxy = TDXProxy.no_auth()
    result = __fetch_basic(proxy)
    assert result.status_code == 200


if __name__ == '__main__':
    test_from_credentials_file()
    test_no_auth()
