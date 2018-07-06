from django.shortcuts import render, redirect

from .models import Machine
from .module.network import LocalNetworkScanner


def index(request):
    machines = Machine.objects.all()
    context = {'machines': machines}

    return render(request, 'rorender/index.html', context)


def pop(request):
    # TODO: Move below logic to module.
    # TODO: build in checks to see if the machine already exists.
    local_machines = LocalNetworkScanner().scan()

    for key, value in local_machines.items():
        new_machine = Machine(name=key, ip=value[0], port=value[1])
        new_machine.save()

    return redirect('index')
