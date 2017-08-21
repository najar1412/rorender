import asyncio

from packages import func

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        if self.message == None:
            self.message = f'{func.get_hostname()} has connected.'
        else:
            self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print('\n\n :: Connecting to Rorender...')

    def data_received(self, data):
        func.client_menu()
        while True:
            message = input(' >> ')
            if message in func.commands.keys():
                self.transport.write(message.encode())
                print('Data sent: {!r}'.format(message))
            else:
                print('Menu item does not exist.')

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = None
coro = loop.create_connection(
    lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888
)

loop.run_until_complete(coro)
loop.run_forever()
loop.close()
