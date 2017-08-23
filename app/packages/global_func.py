import socket

# helpers
def get_hostname(ip=None):
    if ip != None:
        name = socket.gethostbyaddr(ip)[0]
        return name

    name = socket.gethostname()
    return name


class Commands():
    def __init__(self, agent=None):
        self.agent = []

    def add_agent(self, transport):
        ip = transport.get_extra_info('peername')
        remote_host = get_hostname(ip[0])

        self.agent.append([remote_host, ip, transport])
        return self.agent

    def rem_agent(self, agent):
        if agent in self.agent:
            self.agent.pop(agent)
            return self.agent
        else:
            print('No such agent')
            return self.agent

    def send_agent(self):
        return self.agent

    def menu(self):
        return {
            '1': 'Currently running agents',
            '2': 'Run Vray Spawner on all agents',
            '3': 'Run Backburner Server on all agents'
            }

    def input(self):
        message = input(' >> ')
        if message in self.menu():
            return (True, message)

        else:
            return (False, 'Menu item does not exist.')

    def __repr__(self):
        return '<Commands Obj>'
