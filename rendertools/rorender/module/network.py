"""
Contains source code for scanning local windows(?) networks.
"""

import socket


class LocalNetworkScanner():
    """manages the scanning of local networks"""
    def __init__(self, local_ip_root=None):
        """AUG:
        local_ip_root: str: root ip address of a network to scan, ex. 'xxx.xxx.xxx.'
        """
        if not local_ip_root:
            self.local_ip_root = '192.168.1.'

        else:
            self.local_ip_root = local_ip_root

        self.corona_ports = [19666, 19667, 19668]
        self.vray_ports = [20204]
        self.open_windows_ports = [135]

        for port in self.corona_ports:
            self.open_windows_ports.insert(0, port)
        for port in self.vray_ports:
            self.open_windows_ports.insert(0, port)


    def hostname_from_ip(self, ip):
        """uses ip address to resolve a windows machines hostname"""
        # TODO: returns `ip` whether it exits or not.
        return socket.getfqdn(ip)


    def ip_from_hostname(self, hostname):
        """users windows hostname to get machines ip address"""
        try:
            return socket.gethostbyname(hostname)

        except socket.error:
            return (False, f'ERR: {hostname} not found')


    def ip_accessable(self, ip, port):
        """checks if a machine is accessable via it's ip address
        ip: str: ip of machine to check
        return type: bool"""
        # TODO: Currently only returns windows machines. This is okay, but it
        # it would be nice to return any NAS devices attached to the network.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.01)

            if not sock.connect_ex((ip, port)):
                return True


    def scan(self):
        """scans local machines for accessable hostnames and ips
        return type: dict
        return: hostname and ip address"""
        result = {}

        for ip_ext in range(1, 256):
            for port in self.open_windows_ports:
                ip = f'{self.local_ip_root}{str(ip_ext)}'

                if self.ip_accessable(ip, port):
                    result[socket.getfqdn(ip)] = [ip, port]

        return result


    def __repr__(self):
        return f'<LocalNetworkScanner: ip_root={self.local_ip_root}>'

