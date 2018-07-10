"""
Contains source code for working with the django orm
"""

from ..models import Machine


def process_new_ports(ports, ip=None, machine=None):
    """Loops over a list of ports and updates database accordingly.
    ports: list: str repr of ports.
    ip: str: ip address.
    machine: django model: #.
    return: query object."""
    if ip != None:
        machine = Machine.objects.filter(ip=ip).first()

    if '20204' in ports:
        machine.vray_running = True

    else:
        machine.vray_running = False

    if '19667' in ports or '19666' in ports:
        print(f'corona on {machine.name}')
        machine.corona_running = True

    else:
        machine.corona_running = False


    return machine
