from tornado import ioloop
from tornado.gen import Task
from tornado.tcpserver import TCPServer
import pdb, time, logging
from tornado import stack_context
from tornado.escape import native_str
from jsonrpcserver import methods
from jsonrpcserver.response import NotificationResponse

#JSON RPC routines
@methods.add
def hello(**kwargs):
    ret = 'hello'
    if 'name' in kwargs:
       ret = "{0} {1}".format(ret, kwargs['name'])
    return ret

@methods.add
def on_tick_received(**kwargs):
    """
    RPC notification: tick received from stretegy server
    """
    pass

@methods.add
def register(name):
    """
    RPC method: stretegy server registers its name
    """
    pass


#JSON RPC routines end

#JSON RPC Server
class RPCServer(TCPServer):
    def __init__(self, io_loop=None, **kwargs):
        TCPServer.__init__(self, io_loop=io_loop, **kwargs)
    def handle_stream(self, stream, address):
        TCPConnection(stream, address, io_loop=self.io_loop)

#TCP connection handling I/O on each established connection
class TCPConnection(object):
    def __init__(self, stream, address, io_loop):
        self.io_loop = io_loop
        self.stream = stream
        self.address = address
        self.address_family = stream.socket.family
        self.EOF = b'\n'
        self._clear_request_state()
        self._message_callback = stack_context.wrap(self._on_message)
        self.stream.set_close_callback(self._on_connection_close)
        self.stream.read_until(self.EOF, self._message_callback)
    def _on_timeout(self):
        logging.info("Send message..")
        #self.write(b"Hello client!" + self.EOF)
    def _on_message(self, data):
        try:
            timeout = 5
            msg = native_str(data.decode('utf-8'))
            logging.info("Received: %s", msg)
            response = methods.dispatch(msg)
            if not isinstance(response, NotificationResponse):
                #write response
                self.write(str(response).encode(encoding="utf-8") + self.EOF)
            self.io_loop.add_timeout(self.io_loop.time() + timeout, self._on_timeout)
        except Exception as ex:
            logging.error("Exception: %s", str(ex))
    def _clear_request_state(self):
        """Clears the per-request state.
        """
        self._write_callback = None
        self._close_callback = None
    def set_close_callback(self, callback):
        """Sets a callback that will be run when the connection is closed.
        """
        self._close_callback = stack_context.wrap(callback)
    def _on_connection_close(self):
        if self._close_callback is not None:
            callback = self._close_callback
            self._close_callback = None
            callback()
            self._clear_request_state()
    def close(self):
        self.stream.close()
        # Remove this reference to self, which would otherwise cause a
        self._clear_request_state()
    def write(self, chunk, callback=None):
        """Writes a chunk of output to the stream."""
        if not self.stream.closed():
            self._write_callback = stack_context.wrap(callback)
            self.stream.write(chunk, self._on_write_complete)
    def _on_write_complete(self):
        if self._write_callback is not None:
           callback = self._write_callback
           self._write_callback = None
           callback()

def main():
    init_logging()
    server = RPCServer()
    server.listen(8002)
    ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("Ocurred Exception: %s" % str(ex))
        quit()
