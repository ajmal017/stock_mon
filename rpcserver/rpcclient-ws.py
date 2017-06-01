import asyncio
import websockets
from jsonrpcclient.websockets_client1 import WebSocketsClient1

@asyncio.coroutine
def main():
    ws = yield from websockets.connect('ws://localhost:5000')
    response  = yield from WebSocketsClient1(ws).request('hello', name="jason")
    print(response)

asyncio.get_event_loop().run_until_complete(main())
