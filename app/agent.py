import asyncio
import json

from packages import global_func


# TODO: return running processes
# TODO: kill processes on agent
# TODO: load processes on agent

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        if self.message == None:
            self.message = f'Agent on {global_func.get_hostname()} has connected.'
        else:
            self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print('\n\n :: Agent connecting to Rorender...')

    def data_received(self, data):
        message = data.decode()
        print(message)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = json.dumps(['agent', global_func.get_hostname()])
coro = loop.create_connection(
    lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888
)


try:
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
except:
    print('\n\n :: Agent connecting to Rorender...')
    print(' :: Connection Failed - Is the Rorender server running?\n\n')
    loop.close()
