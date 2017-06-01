
import sys
from jsonrpc2 import JsonRpcApplication
from wsgiref.simple_server import make_server

def hello(name):
    return dict(message="Hello, %s!" % name)

if __name__ == '__main__':
    host = ''
    port = 8888
    app = JsonRpcApplication(rpcs = dict(hello=hello))
    print ('runserver %s:%d' % (host, port))
    httpd  = make_server(host, port, app)
    httpd.serve_forever()
