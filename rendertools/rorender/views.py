from django.shortcuts import render, redirect, HttpResponse

from .forms import find_by_hostname, scan_ip
from .models import Machine
from .module.network import LocalNetworkScanner, rdc_file_in_memory
from .module.database import (
    process_new_ports, is_workstation, is_manager, has_rhino, has_autocad,
    machine_exists, delete_machine
)


#TODO: database file management, if db_file.sqite3 exists... etv
#TODO: refactor FAKE_DATA, FAKE_LAN_IP
#TODO: add via ip
#TODO: sometimes a machine is found, but cant be find in database, but it is.
#TODO: handle computers that cant be found by hostname, just ip.

FAKE_LAN_IP = '192.168.56.'
FAKE_DEEP_LAN_IP = '172.16.'

FAKE_DATA = {
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

def index(request):
    """Landing page"""
    #TODO: imp: check if new/empty database
    machines = Machine.objects.all().order_by('name')
    context = {
        'machines': machines,
        'manage': False,
        'form': find_by_hostname,
        'form_scan_ip': scan_ip
        }

    return render(request, 'rorender/index.html', context)


def refresh(request):
    """Endpoint that'll use the database information to update running
    process"""

    ips_from_database = [x.ip for x in Machine.objects.all()]
    database_machines_found = LocalNetworkScanner(FAKE_LAN_IP).refresh(ips_from_database)

    # if machine in database found on netowkr
    for k, v in database_machines_found.items():
        machine = process_new_ports(
            ports=v[1], machine=Machine.objects.filter(ip=v[0]).first()
        )
        machine.save()

    # else machines in database not found in networkscan
    machines = Machine.objects.all().order_by('name')
    print(machines)
    print(database_machines_found)
    for machine in machines:
        if machine.name in database_machines_found:
            pass
        else:
            machine.running = False
            machine.save()


    return redirect('index')


def scan_ip_range(request):
    """Endpoint that scans the local network for machines with selected
    ports open"""
    local_machines = LocalNetworkScanner(FAKE_LAN_IP).scan()

    for k, v in local_machines.items():
        if Machine.objects.filter(ip=v[0]).exists():
            machine = process_new_ports(ports=v[1], ip=v[0])
            machine.save()

        else:
            new_machine = Machine(name=k, ip=v[0], port=' '.join(v[1]))
            process_new_ports(ports=v[1], machine=new_machine)
            new_machine.save()

    return redirect('index')


def scan_hostname(request):
    """Endpoint that scans lan for hostname"""
    #TODO: IMP process_new_ports
    if request.method == 'POST':
        form = find_by_hostname(request.POST)
        if form.is_valid():
            hostname = form.cleaned_data['hostname']

            if machine_exists(hostname):
                print(hostname)
                pass
            else:
                machine = LocalNetworkScanner().find_by_hostname(hostname)
                if machine:
                    machine_hostname = list(machine.keys())[0]
                    new_machine = Machine(name=machine_hostname, ip=machine[machine_hostname][0], port=' '.join(machine[machine_hostname][1]))
                    # process_new_ports(ports=machine[machine[0]][1], machine=new_machine)
                    new_machine.save()

                return redirect('index')

    return redirect('index')


def manage(request):
    """Manager page"""
    machines = Machine.objects.all().order_by('name')
    context = {
        'machines': machines,
        'manage': True
    }

    return render(request, 'rorender/index.html', context)


def make_manager(request):
    print('make manage')

    return redirect('manage')


def delete_machine_from_db(request):
    if request.method=='GET':
        machine_pk = request.GET.get('pk')
        delete_machine(machine_pk)

    return redirect('manage')


def make_workstation(request):
    if request.method=='GET':
        machine_pk = request.GET.get('pk')
        machine = is_workstation(machine_pk)
        machine.save()

    return redirect('manage')


def make_manager(request):
    if request.method=='GET':
        machine_pk = request.GET.get('pk')
        machine = is_manager(machine_pk)
        machine.save()

    return redirect('manage')


def make_rhino(request):
    if request.method=='GET':
        machine_pk = request.GET.get('pk')
        machine = has_rhino(machine_pk)
        machine.save()

    return redirect('manage')


def make_autocad(request):
    if request.method=='GET':
        machine_pk = request.GET.get('pk')
        machine = has_autocad(machine_pk)
        machine.save()

    return redirect('manage')


def remote_connect(request):
    if request.method=='GET':
        ip = request.GET.get('ip')

        return rdc_file_in_memory(HttpResponse, ip)

    else:
        return redirect('index')