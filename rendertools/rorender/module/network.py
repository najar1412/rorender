"""
Contains source code for scanning local windows(?) networks.
"""

import socket


TEST_DATA = {
    '192.168.1.8': ('192.168.1.8', ['3389']), 
    'WS-CYRUS': ('192.168.1.10', ['135', '3389']), 
    'WS-BREWSTER': ('192.168.1.14', ['20204', '135', '3389']), 
    'WS-DEREK': ('192.168.1.16', ['135', '3389']), 
    'WS-CHEMI': ('192.168.1.17', ['135', '3389', '19667']), 
    'WS-CHAZ': ('192.168.1.18', ['30304', '135', '3389']), 
    'WS-ERNIE': ('192.168.1.19', ['20204', '135', '3389']), 
    'WS-CESAREA': ('192.168.1.20', ['20204', '135', '3389']), 
    'WS-BORIS': ('192.168.1.21', ['135']), 
    '192.168.1.60': ('192.168.1.60', ['30304', '3389']), 
    'WS-FIONA': ('192.168.1.80', ['30304', '135']), 
    'WS-DERMIT': ('192.168.1.81', ['30304', '135', '3389']), 
    'ws-Flubber': ('192.168.1.82', ['135', '3389', '19667']), 
    'WS-FRIDA': ('192.168.1.83', ['135', '3389']), 
    'WS-DONOVAN': ('192.168.1.84', ['20204', '19666', '3389']), 
    'WS-DORIS': ('192.168.1.86', ['135', '3389', '20204'])
    }

class LocalNetworkScanner():
    """manages the scanning of local networks"""
    def __init__(self, local_ip_root=None, TEST=False, TEST_DATA=TEST_DATA):
        """AUG:
        local_ip_root: str: root ip address of a network to 
        scan, ex. 'xxx.xxx.xxx.'
        """
        if not local_ip_root:
            self.local_ip_root = '192.168.1.'

        else:
            self.local_ip_root = local_ip_root

        self.corona_ports = [19667, 19666, 19668]
        self.vray_ports = [20204, 30304]
        self.open_windows_ports = [135, 3389]

        for port in self.corona_ports:
            self.open_windows_ports.insert(0, port)

        for port in self.vray_ports:
            self.open_windows_ports.insert(0, port)

        self.TEST = TEST


    def _found_ports(self, ip):
        """loops through a list of ports on an ip address
        ip: str: ip address
        return: list"""
        result = []

        for port in self.open_windows_ports:
            if self.ip_accessable(ip, port):
                result.append(str(port))

        return result


    def ip_accessable(self, ip, port):
        """checks if a machine is accessable via it's ip address
        ip: str: ip of machine to check
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


    def refresh(self, ips):
        """uses a list of ips to run port checks on.
        ips: list: str repr of ips.
        return type: dict
        return: hostname and ip address"""
        result = {}

        if self.TEST:
            return self.TEST_DATA

        for ip in ips:
            found_ports = self._found_ports(ip)

            if len(found_ports) > 0:
                result[socket.getfqdn(ip)] = (ip, found_ports)

        return result


    def scan(self):
        """scans local machines for accessable hostnames and ips
        return type: dict
        return: hostname and ip address"""
        result = {}

        if self.TEST == True:
            return self.TEST_DATA

        for ip_ext in range(1, 256):
            ip = f'{self.local_ip_root}{str(ip_ext)}'
            found_ports = self._found_ports(ip)

            if len(found_ports) > 0:
                result[socket.getfqdn(ip)] = (ip, found_ports)

        return result


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