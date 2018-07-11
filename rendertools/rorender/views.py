from django.shortcuts import render, redirect, HttpResponse

from .models import Machine
from .module.network import LocalNetworkScanner, rdc_file_in_memory
from .module.database import process_new_ports, is_workstation, is_manager


def index(request):
    """Landing page"""
    machines = Machine.objects.all()
    context = {'machines': machines}

    return render(request, 'rorender/index.html', context)


def refresh(request):
    """Endpoint that'll use the database information to update running
    process"""

    ips = [x.ip for x in Machine.objects.all()]
    local_machines = LocalNetworkScanner().refresh(ips)

    for k, v in local_machines.items():
        machine = process_new_ports(
            ports=v[1], machine=Machine.objects.filter(ip=v[0]).first()
        )
        machine.save()

    return redirect('index')


def pop(request):
    """Endpoint that scans the local network for machines with selected
    ports open"""
    local_machines = LocalNetworkScanner().scan()

    for k, v in local_machines.items():
        if Machine.objects.filter(ip=v[0]).exists():
            machine = process_new_ports(ports=v[1], ip=v[0])
            machine.save()

        else:
            new_machine = Machine(name=k, ip=v[0], port=' '.join(v[1]))
            process_new_ports(ports=v[1], machine=new_machine)
            new_machine.save()

    return redirect('index')


def manage(request):
    """Manager page"""
    machines = Machine.objects.all()
    context = {
        'machines': machines,
        'manage': True
    }

    return render(request, 'rorender/index.html', context)


def make_manager(request):
    print('make manage')

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


def remote_connect(request):
    if request.method=='GET':
        ip = request.GET.get('ip')

        return rdc_file_in_memory(HttpResponse, ip)

    else:
        return redirect('index')