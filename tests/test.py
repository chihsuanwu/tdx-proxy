import sys
sys.path.append('../')

from src.tdx_proxy import TDXProxy

def __test():
    proxy = TDXProxy.from_credential_file("credential.json")

    result = proxy.get('v3/Rail/TRA/DailyTrainTimetable/TrainDates')

    print(result.text)


if __name__ == '__main__':
    __test()
