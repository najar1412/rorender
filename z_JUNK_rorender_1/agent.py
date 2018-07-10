import asyncio
import json

from packages import global_func
from packages import agent_func


# TODO: return running processes
# TODO: kill processes on agent
# TODO: load processes on agent

class RorenderAgent(asyncio.Protocol):
    first_time = True


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
        if self.first_time:
            message = data.decode()
            print(message)
            self.first_time = False
        else:
            message = data.decode()
            print(f' :: Receiving message from server. {message}.')

            if message == '2':
                print(message)
                agent_func.load_vrayspawner()
                self.transport.write('Message received.'.encode())
            elif message == '3':
                print(message)
                agent_func.load_backburner_server()
                self.transport.write('Message received.'.encode())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = json.dumps(['agent', global_func.get_hostname()])
coro = loop.create_connection(
    lambda: RorenderAgent(message, loop), '127.0.0.1', 8888
)

try:
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
except:
    print('\n\n :: Agent connecting to Rorender...')
    print(' :: Connection Failed - Is the Rorender server running?\n\n')
    loop.close()
