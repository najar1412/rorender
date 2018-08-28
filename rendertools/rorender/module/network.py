"""
Contains source code for scanning local windows(?) networks.
"""

import socket
from collections import namedtuple

DEVICE_MAPPING = namedtuple('DeviceMapping', 'ip, hostname, ports')

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
    """Explore a local network"""
    #TODO: imp DEVICE_MAPPING as dto.
    def __init__(self, TEST=False, TEST_DATA=None):
        """AUG:
        TEST, ex. 'xxx.xxx.xxx.'
        TEST_DATA, ex. 'xxx.xxx.xxx.'
        """
        self.TEST = TEST
        self.test_data = TEST_DATA


    def _hostname_from_ip(self, ip):
        """attempts to get hostname of device from ip alone
        AUG: ip: str: ipaddress, 'xxx.xxx.xxx.xxx'
        Return: DEVICE_MAPPING, or None"""
        #TODO: Imple into a realllly slow `deep scan`?
        #TODO: remove from try/except or catch accordingly
        #TODO: imp port check
        #TODO: imp evice_mappinf
        try:
            conn_info = socket.gethostbyaddr(ip)
            device = DEVICE_MAPPING(conn_info[2][0], conn_info[0], [])

            return conn_info

        except:
            return None


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
        #TODO: imp DEVICE_MAPPING obj.
        #TODO: convertions i.e. result should be up to the user, or under 
        #`as_dict()`
        hostname = socket.gethostname()
        device = DEVICE_MAPPING(
            socket.gethostbyname(hostname), 
            hostname, 
            []
        )
        result = {
            'ip': device[0],
            'device_name': device[1]
            }

        return result

    def _to_dict(self, device):
        _key_values = dict(device._asdict())
        result = {}
        result[_key_values['hostname']] = (_key_values['ip'], _key_values['ports'])
        print('_to_dict()')
        print(result)

        return result


    def _find_by_ip(self, device, ports):
        """find device by ip
        device: DEVICE_MAPPING namedtuple.
        return: DEVICE_MAPPING namedtuple."""
        #TODO: refactor heavily
        #TODO: ip returning the device
        try:
            hostname_from_ip = self._hostname_from_ip(device[0])
            if hostname_from_ip:                
                connected_ports = self._socket_connect_ports(device[0], ports)
                device = device._replace(hostname=hostname_from_ip[0], ports=connected_ports)

                return device

        except:
            print('ERR: IP not found on network')
            return None


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


    def _ip_comp(self, ip):
        result = []
        ip_comp = ip.split('.')
        for comp in ip_comp:
            if comp == '' or comp == None or comp == 'None':
                pass
            else:
                result.append(comp)

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

        # get ip composition
        ip_comp = self._ip_comp(ip)
        print(ip_comp)

        if len(ip_comp) == 2:
            print('LLOONNGGG SSEEEAARRCCHHHH')
            for ip_third in range(1, 256):
                for ip_fourth in range(1, 256):
                    ip = f'{".".join(ip_comp)}.{str(ip_third)}.{str(ip_fourth)}'
                    print(ip)
                    found_ports = self._socket_connect_ports(ip, ports)

                    if len(found_ports) > 0:
                        result[socket.getfqdn(ip)] = (ip, found_ports)

            return result

        elif len(ip_comp) == 3:
            print('scanner')
            for ip_ext in range(1, 256):
                built_ip = f'{".".join(ip_comp)}.{str(ip_ext)}'
                found_ports = self._socket_connect_ports(built_ip, ports)

                if len(found_ports) > 0:
                    result[socket.getfqdn(built_ip)] = (built_ip, found_ports)
            return result


        elif len(ip_comp) == 4:
            print('find_by_ip')
            device = DEVICE_MAPPING(
                ip, 
                None, 
                ports
            )
            found_device = self._find_by_ip(device, ports)
            # naked
            print(self._to_dict(found_device))
            return self._to_dict(found_device)


    def find_by_hostname(self, hostname, ports=None):
        """attempts to find a device on the next using hostname only.
        AUG: hostname: str: hostname of the device.
        ports:list: post numbers
        return: dict:"""
        #TODO: dont catch everything...
        try:
            ip = socket.gethostbyname_ex(hostname)

            if ip:
                if ports:
                    found_ports = self._socket_connect_ports(ip[2][0], ports)
                    return {hostname: (ip[2][0], found_ports)}
                else:
                    print('portscan didnt fire')
                    return {hostname: (ip[2][0], [])}

        except:
            print('ERR: Hostname not found on network.')
            return False


    def __repr__(self):
        return f'<LocalNetworkScanner: ip_root:>'


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