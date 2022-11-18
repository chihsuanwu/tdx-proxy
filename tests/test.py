import sys
sys.path.append('../')

from src.tdx_proxy import TDXProxy

def __test():
    proxy = TDXProxy.from_credential_file("credential.json")

    params = {
        "$filter": "Scope/Routes/Any(route: route/RouteID eq '309')",
        '$format': 'JSON'
    }
    result = proxy.get('v2/Bus/Alert/City/Taichung', params=params)

    print(result.text)


if __name__ == '__main__':
    __test()
