import asyncio
import datetime
import json

from packages import global_func


# TODO: can i override transport.get_extra_info to include the host name?
class RorenderServer(asyncio.Protocol):
    first_time = True
    commands = global_func.Commands()

    def connection_made(self, transport):
        self.transport = transport
        self.commands.add_agent(self.transport)
        print(f'Connection from remote_host @ ip')

    def data_received(self, data):
        # init connection
        if self.first_time:
            self.transport.write(bytes(' :: Successfully connected to Rorender', 'utf-8'))
            self.first_time = False

        message = str(json.loads(data.decode()))
        if message in self.commands.menu():
            if message == '1':
                self.transport.write(str(self.commands.send_agent()).encode())
                print(' :: Sending Agents list to someone...')

            elif message == '2':
                print('IMP: sending to agents')
                try:
                    self.commands.send_agent()[0][2].write(message.encode())
                    self.transport.write(' :: Request sent to Agents'.encode())
                    print('IMP: sending to agents')
                except:
                    self.transport.write(' :: Request Failed'.encode())


    def connection_lost(self, exc):
        # TODO: figure out how to tell what connection was dropped
        print('IMP: connection closed')


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(RorenderServer, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print(f' \n\n :: Rorender running on {global_func.get_hostname()} @ {server.sockets[0].getsockname()}')
print(f' :: Started on {datetime.datetime.utcnow()}\n\n')

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
