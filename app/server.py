import asyncio
import datetime
import json

from packages import global_func


class RorenderServer(asyncio.Protocol):
    first_time = True
    commands = global_func.Commands()

    def connection_made(self, transport):
        self.transport = transport
        # TODO: figure out a better way to add a key to the object?
        # possibly overriding it?
        # init new key to transport object
        self.transport.__dict__['_extra']['connection_type'] = []
        print(f'Connection from remote_host @ ip')

    def data_received(self, data):
        # init connection
        if self.first_time:
            message = json.loads(data.decode())
            # add connected agent to agent list
            if message[0] == 'agent':
                self.transport.__dict__['_extra']['connection_type'] = message
                self.commands.add_agent(self.transport)
            self.transport.write(bytes(' :: Successfully connected to Rorender', 'utf-8'))
            self.first_time = False

        # additional connects after the initial
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

        try:
            # try for agent
            agent_from_transport = self.transport.__dict__['_extra']['connection_type'][1]
            for agent in self.commands.agent:
                if agent[0] == agent_from_transport:
                    self.commands.rem_agent(agent_from_transport)
            print(f' :: Agent {agent_from_transport} disconnected')
        except:
            # except if client
            pass


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
