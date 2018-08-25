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
    """manages the scanning of local networks"""
    def __init__(self, local_ip_root=None, ports=None, TEST=False, TEST_DATA=None):
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

        self.ports = ports

        self.TEST = TEST
        self.test_data = TEST_DATA


    def _attempt_connection(self, ip, port):
        """checks if a machine is accessable via it's ip address and port
        ip: str: ip of machine to check
        port: str: port number
        return type: bool"""
        # TODO: Currently only finds machines that are activing listening.
        # If a machine is rendering (recv) information on the port `is_accessable`
        # cannot find it. This is a problem.
        # look into using socket.bind() and process based on errors?
        # https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.01)

            if not sock.connect_ex((ip, port)):
                return True


    def _scan_ports(self, ip):
        """loops through a list of ports on an ip address
        ip: str: ip address
        return: list"""
        result = []

        for port in self.ports:
            if self._attempt_connection(ip, port):
                result.append(str(port))

        return result


    def get_local_data(self):
        return {'ip': socket.gethostbyname(socket.gethostname())}


    def refresh(self, ips):
        """uses a list of ips to run port checks on.
        ips: list: str repr of ips.
        return type: dict
        return: hostname and ip address"""
        result = {}

        if self.TEST:
            return self.test_data

        for ip in ips:
            found_ports = self._scan_ports(ip)

            if len(found_ports) > 0:
                result[socket.getfqdn(ip)] = (ip, found_ports)
                print(result)

        return result

    def _portscan_forth(ip):
        return True


    def scan(self):
        """scans local machines for accessable hostnames and ips, one ip column
        deep (192.168.30.xxx). approx 1 minute. two ip column deep 
        (192.168.xxx.xxx). approx 1 hour 30 minute :p
        return type: dict
        return: hostname and ip address"""
        #TODO: needs to include user entering full ip address
        result = {}

        if self.TEST:
            return self.test_data

        if len(self.local_ip_root.split('.')) == 3:
            print('LLOONNGGG SSEEEAARRCCHHHH')
            for ip_third in range(1, 256):
                for ip_fourth in range(1, 256):
                    ip = f'{self.local_ip_root}{str(ip_third)}.{ip_fourth}'
                    found_ports = self._scan_ports(ip)

                    if len(found_ports) > 0:
                        result[socket.getfqdn(ip)] = (ip, found_ports)

            return result

        elif len(self.local_ip_root.split('.')) == 4:
            for ip_ext in range(1, 256):
                ip = f'{self.local_ip_root}{str(ip_ext)}'
                found_ports = self._scan_ports(ip)

                if len(found_ports) > 0:
                    result[socket.getfqdn(ip)] = (ip, found_ports)

            return result

        elif len(self.local_ip_root.split('.')) == 5:
            print('full ip weeeee')
            #TODO: IMP adding a whole ip address

            return result


    def find_by_hostname(self, hostname):
        #TODO: dont hardcore in port 20204, use allowed ports list
        try:
            ip_from_hostname = socket.gethostbyname_ex(hostname)
            hostname_from_ip = socket.gethostbyaddr(ip_from_hostname[0])

            if ip_from_hostname:
                return {hostname_from_ip[0]: (ip_from_hostname[2][0], ['20204'])}

        except:
            print('ERR: Hostname not found on network.')
            return False


    def find_by_ip(self, ip):
        #TODO: dont hardcore in port 20204, use allowed ports list
        try:
            #ip_from_hostname = socket.gethostbyname_ex(hostname)
            hostname_from_ip = socket.gethostbyaddr(ip)

            if hostname_from_ip:
                return {hostname_from_ip[0]: (ip, ['20204'])}

        except:
            print('ERR: IP not found on network')
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