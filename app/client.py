import asyncio
import json

from packages import global_func
from packages import client_func


# TODO: request connected agents
# TODO: load processes on all agents
# TODO: kill processes on all agents
# TODO: load individual processes on selected agents
# TODO: kill individial processes on selected agents

class EchoClientProtocol(asyncio.Protocol):
    first_time = True

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print(f'\n\n :: Connecting to Rorender on host {global_func.get_hostname()}...')

    def data_received(self, data):
        print(f' :: {data.decode()}\n\n')
        # init menu on first time connection
        if self.first_time:
            print(' :: Rorender Commands')
            for menu_item in global_func.Commands().menu():
                print(f' :: {menu_item}: {global_func.Commands().menu()[menu_item]}')
            print('\n')
            self.first_time = False

        client_input = global_func.Commands().input()
        if client_input[0]:
            self.transport.write(client_input[1].encode())
        else:
            print(client_input[1])

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = json.dumps(['client', global_func.get_hostname()])
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
