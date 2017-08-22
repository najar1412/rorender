import asyncio
import datetime
import json

from packages import func

# TODO: IMP tracking of connections. agents and client.

class EchoServerClientProtocol(asyncio.Protocol):
    agents = []
    clients = []
    first_time = True

    def connection_made(self, transport):
        self.transport = transport
        ip = transport.get_extra_info('peername')
        remote_host = func.get_hostname(ip[0])
        print(f'Connection from {remote_host} @ {ip}')

    def data_received(self, data):
        if self.first_time:
            self.transport.write(bytes('connected', 'utf-8'))
            self.first_time = False

        message = json.loads(data.decode())
        if isinstance(message, list):
            if message[0] == 'client':
                if message in self.clients:
                    pass
                else:
                    self.clients.append(message)
            elif message[0] == 'agent':
                if message in self.agents:
                    pass
                else:
                    self.agents.append(message)
        else:
            message = str(message)
            if message in func.commands:
                if message == '1':
                    agents_to_send = []
                    for x in self.agents:
                        agents_to_send.append(x[1])

                    self.transport.write(json.dumps(agents_to_send).encode())
                    print(' :: Sending Agents list to someone...')


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print(f' \n\n :: Rorender running on {func.get_hostname()} @ {server.sockets[0].getsockname()}')
print(f' :: Started on {datetime.datetime.utcnow()}\n\n')
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
