import asyncio
from jsonrpcserver import methods
from jsonrpcserver.response import NotificationResponse

@methods.add
def hello(**kwargs):
    ret = 'hello'
    if 'name' in kwargs:
        "{0} {1}".format(ret, kwargs['name'])
    return ret


@asyncio.coroutine
def handle_request(reader, writer):
    while True:
        request = yield from reader.read(1024)
        message = request.decode()
        addr = writer.get_extra_info('peename')
        response = methods.dispatch(request)
        if not isinstance(response, NotificationResponse):
            print("received %r from %r" % (message, addr))
            writer.write(response)
            yield from writer.drain()
    
    
