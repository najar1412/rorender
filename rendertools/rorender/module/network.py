"""
Contains source code for scanning local windows(?) networks.
"""

import socket


class PortBuilder():
    def __init__(self):
        self._ports = []

    def add(self, ports):
        if isinstance(ports, list):
            for port in ports:
                self._ports.append(port)
            return self._ports

        return self._ports.append(ports)

    def ports(self):
        return self._ports

    def __iter__(self):
        return iter(self._ports)

    def __repr__(self):
        return f'<PortBuilder({len(self._ports)} ports)>'


class LocalNetworkScanner():
    """Tools to help explore a local network"""
    def __init__(self, local_ip_root=None, TEST=False, TEST_DATA=None):
        """AUG:
        local_ip_root: str: root ip address of a network to 
        scan, ex. 'xxx.xxx.xxx.'
        """
        # TODO: Remove local_ip_root from constructor, should be an aug for the function
        # that needs it.
        if not local_ip_root:
            self.local_ip_root = local_ip_root

        else:
            self.local_ip_root = local_ip_root

        self.TEST = TEST
        self.test_data = TEST_DATA


    def _socket_connect(self, ip, port):
        """checks to see if a connection can be able to `port` on `ip`.
        ip: str: ip of machine to check
        port: str: port number
        return type: bool"""
        # TODO: Currently only finds machines that are activing listening.
        # If a machine is rendering (recv) information on the port `is_accessable`
        # cannot find it. This is a problem.
        # look into using socket.bind() and process based on errors?
        # https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
        # TODO: whats the quickest way to check if a port is listening?
        #should i first check is the ip is even assessible?
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.01)

            if not sock.connect_ex((ip, port)):
                return True

        return False


    def _socket_connect_ports(self, ip, ports):
        """loops through a list of ports on an ip address
        ip: str: ip address
        return: list of str"""
        result = []

        for port in ports:
            if self._socket_connect(ip, port):
                result.append(str(port))

        return result


    def get_local_data(self):
        #TODO: Get all relative local machine info.
        return {'ip': socket.gethostbyname(socket.gethostname())}


    def _find_by_ip(self, ip):
        """find device by ip
        IP: str repr of ip address, 'xxx.xxx.xxx.xxx'
        return: dict
        return structure: {'HOSTNAME': ('IP', ['PORTS'])}"""
        #TODO: dont hardcore in port 20204, use allowed ports list
        try:
            print(ip)
            hostname_from_ip = socket.gethostbyaddr(ip)

            if hostname_from_ip:
                return {hostname_from_ip[0]: (ip, ['20204'])}

        except:
            print('ERR: IP not found on network')
            return False


    def refresh(self, ips, ports):
        """uses a list of ips to run port checks on.
        ips: list: str repr of ips.
        return type: dict
        return structure: {'HOSTNAME': ('IP', [FOUND_PORTS])}
        return: hostname and ip address"""
        result = {}

        if self.TEST:
            return self.test_data

        for ip in ips:
            found_ports = self._socket_connect_ports(ip, ports)

            if len(found_ports) > 0:
                result[socket.getfqdn(ip)] = (ip, found_ports)

        return result


    def scan(self, ip, ports):
        """scans local machines for accessable hostnames and ips, one ip
        column deep (192.168.30.xxx). approx 1 minute. two ip column deep 
        (192.168.xxx.xxx). approx 1 hour 30 minute :p
        return type: dict
        return: hostname and ip address"""
        #TODO: needs to include user entering full ip address
        result = {}

        if self.TEST:
            return self.test_data

        # get imp composition
        ip_comp = ip.split('.')
        if ip_comp[-1] == '':
            ip_comp = ip_comp[0:-1]

        if len(ip_comp) == 2:
            print('LLOONNGGG SSEEEAARRCCHHHH')
            for ip_third in range(1, 256):
                for ip_fourth in range(1, 256):
                    ip = f'{ip}{str(ip_third)}.{ip_fourth}'
                    found_ports = self._socket_connect_ports(ip, ports)

                    if len(found_ports) > 0:
                        result[socket.getfqdn(ip)] = (ip, found_ports)

            return result

        elif len(ip_comp) == 3:
            print('scanner')
            for ip_ext in range(1, 256):
                built_ip = f'{ip}{str(ip_ext)}'
                print(built_ip)
                found_ports = self._socket_connect_ports(built_ip, ports)

                if len(found_ports) > 0:
                    result[socket.getfqdn(built_ip)] = (built_ip, found_ports)

            return result

        elif len(ip_comp) == 4:
            print('find_by_ip')
            return self._find_by_ip(ip)


    def find_by_hostname(self, hostname):
        #TODO: dont hardcore in port 20204, use allowed ports list
        try:
            ip_from_hostname = socket.gethostbyname_ex(hostname)

            if ip_from_hostname:

                return {hostname_from_ip[0]: (ip_from_hostname[2][0], ['20204'])}

        except:
            print('ERR: Hostname not found on network.')
            return False


    def __repr__(self):
        return f'<LocalNetworkScanner: ip_root={self.local_ip_root}>'


def rdc_file_in_memory(HttpResponse, ip):
    """builds in memory rdc connection file.
    HttpResponse: django HttpResponse object.
    ip: str: ip address.
    return: django HttpResponse object.
    """
    data =  f'auto connect:i:1\nfull address:s:{ip}'
    response = HttpResponse(data, content_type='application/rdp')
    response['Content-Disposition'] = f'attachment; filename="{ip}.rdp"'

    return response