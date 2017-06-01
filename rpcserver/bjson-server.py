import bjsonrpc
from bjsonrpc.handlers import BaseHandler

class MyServerHandler(BaseHandler):
    def hello(self, txt):
        response = "hello, %s!." % txt
        print ("*%s" % response)
        return response

s = bjsonrpc.createserver(host = '0.0.0.0', port = 8002, handler_factory = MyServerHandler )
s.debug_socket(True)
s.serve()
