import asyncio
import datetime

from packages import func

# TODO: IMP tracking of connections. agents and client.

class EchoServerClientProtocol(asyncio.Protocol):
    agents = []
    clients = []

    def connection_made(self, transport):
        ip = transport.get_extra_info('peername')
        remote_host = func.get_hostname(ip[0])
        print(f'Connection from {remote_host} @ {ip}')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        if message not in func.commands:
            # return data to valid connection
            self.transport.write(data)
        else:
            print(func.commands[str(message)])


print(EchoServerClientProtocol.tester)

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
