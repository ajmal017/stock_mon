import logging
import tornado.ioloop
import tornado.iostream
import socket
from jsonrpcclient.client import Client
from jsonrpcclient.request import Request

#Init logging
def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))
class TCPClient(Client):
    def __init__(self, host, port, io_loop=None):
        super(TCPClient, self).__init__(host)
        self.host = host
        self.port = port
        self.io_loop = io_loop
        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self.EOF = b'\n'
    def _send_message(self, request, **kwargs):
        logging.info("sending RPC request %s" % request)
        self.stream.write(request.encode(encoding="utf-8") + self.EOF)

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
        self.stream.set_close_callback(self.on_close)
    def connect(self):
        self.get_stream()
        self.stream.connect((self.host, self.port), self.send_message)
    def on_receive(self, data):
        response = self._process_response(data.decode('utf-8'))
        logging.info("Received: %s", response)
        self.stream.close()
    def on_close(self):
        if self.shutdown:
            self.io_loop.stop()
    def send_message(self):
        logging.info("Send message....")
        myrequest = Request('hello', name='world')
        #self.stream.write(b"Hello Server!" + self.EOF)
        self.send(myrequest)
        self.stream.read_until(self.EOF, self.on_receive)
        logging.info("After send....")
    def set_shutdown(self):
        self.shutdown = True

def main():
    init_logging()
    io_loop = tornado.ioloop.IOLoop.instance()
    c1 = TCPClient("127.0.0.1", 8001, io_loop)
    c1.connect()
    c1.set_shutdown()
    logging.info("**********************start ioloop******************")
    io_loop.start()
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("Ocurred Exception: %s" % str(ex))
    quit()
