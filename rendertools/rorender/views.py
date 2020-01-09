from django.shortcuts import render, redirect, HttpResponse

from .forms import find_by_hostname, scan_ip
from .models import Machine, User as Users
from .module.network import LocalNetworkScanner, PortBuilder
from .module.database import (
    process_new_ports, is_workstation, is_manager, has_rhino, has_autocad,
    machine_exists, delete_machine
)

from django.contrib.auth.models import User
from django.http import JsonResponse

#TODO: database file management, if db_file.sqite3 exists... etv
#TODO: sometimes a machine is found, but cant be find in database, but it is.
#TODO: handle computers that cant be found by hostname, just ip.

# global ports to be used while scanning
corona_ports = [19667, 19666, 19668]
vray_ports = [20204, 30304]
backburner_ports = [3234, 3233]
open_windows_ports = [135, 3389]

# add them to the PortBuilder for later use
PORTS = PortBuilder()
PORTS.add(corona_ports)
PORTS.add(vray_ports)
PORTS.add(open_windows_ports)
PORTS.add(backburner_ports)

# helpers
def rdc_file_in_memory(HttpResponse, ip):
    """DJANGO ONLY
    builds in memory rdc connection file.
    HttpResponse: django HttpResponse object.
    ip: str: ip address of remote machine.
    return: django HttpResponse object.
    """
    data =  f'auto connect:i:1\nfull address:s:{ip}'
    response = HttpResponse(data, content_type='application/rdp')
    response['Content-Disposition'] = f'attachment; filename="{ip}.rdp"'

    return response


def remote_connect(request):
    if request.method=='GET':
        ip = request.GET.get('ip')

        return rdc_file_in_memory(HttpResponse, ip)

    else:
        return redirect('index')


# ajax endpoints
def assign_user(request):
    assignment = request.GET.get('assignment', None)
    user, machine = assignment.split('@')

    userObj = Users.objects.all().filter(name=user)[0]
    machineObject = Machine.objects.all().filter(name=machine)[0]
    machineObject.user = userObj
    machineObject.save()
    
    res = {}
    res['username'] = assignment

    """
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    """

    return JsonResponse(res)


def clear_assignment(request):
    assignment = request.GET.get('assignment', None)
    _, machine = assignment.split('@')

    machineObject = Machine.objects.all().filter(name=machine)[0]
    machineObject.user = None

    machineObject.save()

    res = {}
    res['username'] = assignment

    return JsonResponse(res)

# views
def index(request):
    """Landing page"""
    #TODO: imp: check if new/empty database
    machines = Machine.objects.all().order_by('name')
    users = Users.objects.all()

    local_data = LocalNetworkScanner().get_local_data()

    context = {
        'machines': machines,
        'manage': False,
        'form': find_by_hostname,
        'form_scan_ip': scan_ip,
        'local_data': local_data,
        'users': users
        }

    return render(request, 'rorender/index.html', context)


def manage(request):
    #TODO: imp: check if new/empty database
    machines = Machine.objects.all().order_by('name')

    local_data = LocalNetworkScanner().get_local_data()

    context = {
        'machines': machines,
        'manage': True,
        'form': find_by_hostname,
        'form_scan_ip': scan_ip,
        'local_data': local_data
        }

    return render(request, 'rorender/index.html', context)


# TODO: Make ajax
def refresh(request):
    """Endpoint that'll use the database information to update running
    process"""

    ips_from_database = [x.ip for x in Machine.objects.all()]
    database_machines_found = LocalNetworkScanner().refresh(ips_from_database, PORTS)

    # if machine in database found on netowkr
    ips_from_found_machines = []
    for k, v in database_machines_found.items():
        ips_from_found_machines.append(v[0])
        machine = process_new_ports(
            ports=v[1], machine=Machine.objects.filter(ip=v[0]).first()
        )
        machine.save()
    # else not found on network
    for ip in ips_from_database:
        if ip not in ips_from_found_machines:
            machine = Machine.objects.filter(ip=ip).first()
            machine.running = False
            machine.save()


    return redirect('index')


def scan_ip_range(request):
    """Endpoint that scans the local network for machines with selected
    ports open"""
    if request.method == 'POST':
        form = scan_ip(request.POST)
        if form.is_valid():
            #get user ip, ip composition, sanitation
            _ip = {}
            for k, v in form.cleaned_data.items():
                if v:
                    _ip[k] = v
                else:
                    _ip[k] = None
            print(_ip)

            user_ip = f"{_ip['ip_one']}.{_ip['ip_two']}.{_ip['ip_three']}.{_ip['ip_four']}"
            print(user_ip)
            local_machines = LocalNetworkScanner().scan(user_ip, PORTS)

            for k, v in local_machines.items():
                if Machine.objects.filter(ip=v[0]).exists():
                    machine = process_new_ports(ports=v[1], ip=v[0])
                    machine.save()

                else:
                    new_machine = Machine(name=k, ip=v[0], port=' '.join(v[1]))
                    process_new_ports(ports=v[1], machine=new_machine)
                    new_machine.save()

            return redirect('index')

    return redirect('manager')


def scan_hostname(request):
    """Endpoint that scans lan for hostname"""
    if request.method == 'POST':
        form = find_by_hostname(request.POST)
        if form.is_valid():
            hostname = form.cleaned_data['hostname']

            if machine_exists(hostname):
                pass
            else:
                machine = LocalNetworkScanner().find_by_hostname(hostname, ports=PORTS)
                if machine:
                    machine_hostname = list(machine.keys())[0]
                    new_machine = Machine(
                        name=machine_hostname, ip=machine[machine_hostname][0], 
                        port=' '.join(machine[machine_hostname][1])
                    )
                    new_machine.save()

                return redirect('index')

    return redirect('manager')


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