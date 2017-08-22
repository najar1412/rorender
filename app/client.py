import asyncio
import json

from packages import func

class EchoClientProtocol(asyncio.Protocol):
    first_time = True

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print(f'\n\n :: Successfully connected to Rorender on host {func.get_hostname()}\n\n')

    def data_received(self, data):
        if self.first_time:
            func.client_menu()
            self.first_time = False

        func.client_send(self)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = json.dumps(['client', func.get_hostname()])
coro = loop.create_connection(
    lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888
)


try:
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
except:
    print('\n\n :: Connecting to Rorender...')
    print(' :: Connection Failed - Is the Rorender server running?\n\n')
    loop.close()
