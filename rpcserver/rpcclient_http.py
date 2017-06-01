from jsonrpcclient.http_client import HTTPClient

if __name__ == '__main__':
    response = HTTPClient('http://localhost:5000/').request('hello', name='jason')
    print(response)
