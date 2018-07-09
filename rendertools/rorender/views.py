from django.shortcuts import render, redirect

from .models import Machine
from .module.network import LocalNetworkScanner


def machine_exist(machine):
    if Machine.objects.filter(name=machine).exists():
        return True
    else:
        return False


def index(request):
    machines = Machine.objects.all()
    context = {'machines': machines}

    return render(request, 'rorender/index.html', context)


def pop(request):
    # TODO: Move below logic to module.
    local_machines = LocalNetworkScanner().scan()
    print(local_machines)

    for k, v in local_machines.items():
        existing_machine = Machine.objects.filter(ip=v[0]).first()
        if existing_machine:
            if '20204' in v[1]:
                existing_machine.vray_running = True

            else:
                existing_machine.vray_running = False

            if '19666' in v[1]:
                existing_machine.corona_running = True

            else:
                existing_machine.corona_running = False

            existing_machine.save()

        else:
            new_machine = Machine(name=k, ip=v[0], port=' '.join(v[1]))
            if '20204' in v[1]:
                new_machine.vray_running = True

            if '19666' in v[1]:
                new_machine.corona_running = True

            new_machine.save()
            
        '''
        machine = Machine.objects.filter(ip=v[0]).first()
        if machine:
            if '19667' in v[1]:
                print(f'Corona is running on {machine.name}')

        else:
            new_machine = Machine(name=k, ip=v[0], port=' '.join(v[1]))
            new_machine.save()
        '''


    '''
    print(local_machines)

    for key, value in local_machines.items():
        if machine_exist(key):
            pass
        else:
            new_machine = Machine(name=key, ip=value[0], port=value[1])
            new_machine.save()
    '''

    return redirect('index')
