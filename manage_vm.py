#!/usr/bin/env python

import re

import click
import virtualbox

@click.group()
def cli():
    pass

@click.command()
@click.option('--vm-name', prompt='VM name:',
              help='The name of the vm to start.')
def start(vm_name):
    click.echo('Starting the vm...')

    vbox = virtualbox.VirtualBox()

    session = virtualbox.Session()

    vm = vbox.find_machine(vm_name)

    progress = vm.launch_vm_process(session, 'headless', '')
    progress.wait_for_completion()

    vm_ip = vm.get_guest_property("/VirtualBox/GuestInfo/Net/0/V4/IP")[0]
    click.echo('Ip: %s'%vm_ip)

    #Update the hosts file
    with open('/private/etc/hosts', 'r+') as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.truncate()
        for line in lines:
            line = re.sub(r'([0-9]{1,3}.){4}\s*(.*%s.*)', '%s \g<2>'%(vm_name, vm_ip), line)
            fd.write(line)

    click.echo('Updated the hosts file.')

    click.echo('Done!')

@click.command()
@click.option('--vm-name', prompt='VM name:',
              help='The name of the vm to start.')
def stop(vm_name):
    click.echo('Stopping the vm...')

    vbox = virtualbox.VirtualBox()
    vm = vbox.find_machine(vm_name)

    session = vm.create_session()
    progress = session.console.power_down()
    progress.wait_for_completion()
    click.echo('Done!')

cli.add_command(start)
cli.add_command(stop)

if __name__ == '__main__':
    cli()
