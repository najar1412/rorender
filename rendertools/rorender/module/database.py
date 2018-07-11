"""
Contains source code for working with the django orm
"""

from ..models import Machine


def process_new_ports(ports, ip=None, machine=None):
    """Loops over a list of ports and updates django object accordingly.
    ports: list: str repr of ports.
    ip: str: ip address.
    machine: django model: #.
    return: query object."""
    if ip != None:
        machine = Machine.objects.filter(ip=ip).first()

    elif ip == None and machine == None:
        raise AttributeError(
            """`process_new_ports` requires either `ip` or 
            `machine` to not be `None`"""
        )

    if '20204' in ports:
        machine.vray_running = True

    else:
        machine.vray_running = False

    if '19667' in ports or '19666' in ports or '19668' in ports:
        machine.corona_running = True

    else:
        machine.corona_running = False


    return machine


def is_workstation(pk):
    machine = Machine.objects.filter(pk=pk).first()

    if machine.is_workstation == True:
        machine.is_workstation = False
    else:
        machine.is_workstation = True

    return machine


def is_manager(pk):
    machine = Machine.objects.filter(pk=pk).first()

    if machine.is_manager == True:
        machine.is_manager = False
    else:
        machine.is_manager = True

    return machine


def has_rhino(pk):
    machine = Machine.objects.filter(pk=pk).first()

    if machine.has_rhino == True:
        machine.has_rhino = False
    else:
        machine.has_rhino = True

    return machine


def has_autocad(pk):
    machine = Machine.objects.filter(pk=pk).first()

    if machine.has_autocad == True:
        machine.has_autocad = False
    else:
        machine.has_autocad = True

    return machine