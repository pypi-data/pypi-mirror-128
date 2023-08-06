#!/usr/bin/env python


import click
from ecs import project_loader, ecs
import yaml
import json
from pprint import pprint
import os 
import boto3
import botocore


# Shared options
_shared_options = [
    click.option('-p', '--project-path', 'project_path', show_default=True, default="ecs/"),
    click.option('-v', '--val', 'values', type=click.Path(exists=True), multiple=True),
    click.option('-e', 'envs', type=str, multiple=True)
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


# Definition of group necessary for building arguments
@click.group()
def group(**kwargs):
    pass


def _render_project(**kwargs):
    """ Function used for handling project_path, values, and envs options"""
    # Convert env input into dict
    envs = list(kwargs.get('envs', []))
    envs = dict([x.split('=') for x in envs])

    # Load and interpolate project
    return project_loader.load_project(
        kwargs.get('project_path'),
        list(kwargs.get('values', [])),
        envs)


@group.command()
@add_options(_shared_options)
@click.option('-f', '--format', 'oformat', type=click.Choice(['json', 'yaml']), default='json')
def render(**kwargs):
    """ Interpolate and print project configuration """

    # Interpolate the project
    ld = _render_project(**kwargs)
   
    # Print
    for i in zip(['Task definition', 'Service'], ld):
        # Generate in the output format
        if kwargs['oformat'].lower() == 'yaml':
            g = yaml.dump(i[1])
        if kwargs['oformat'].lower() == 'json':
            g = json.dumps(i[1],indent=2)
        
        # Print
        click.secho("* {}:".format(i[0]), fg='green')
        click.echo(g)
    click.secho("* Output:", fg='green')
    click.echo(ld[2])


@group.command()
@add_options(_shared_options)
@click.option('-f', '--format', 'oformat', type=click.Choice(['json', 'yaml']), default='json')
def output(**kwargs):
    """ Interpolate output.j2 file """
    # Interpolate the project
    ld = _render_project(**kwargs)
   
    # Print the output
    click.echo(ld[2])


@group.command()
@add_options(_shared_options)
@click.option('-td', '--task-definition', 'task_definition', default='task-definition.json')
@click.option('-s', '--service', 'service', default='service.json')
@click.option('-o', '--output', 'output', default='output.txt')
def generate(**kwargs):
    """ Generate configuration files which can be used by aws-cli """

    # Interpolate the project
    ld = _render_project(**kwargs)
   
    # Portion generating output files
    for i in zip([kwargs['task_definition'], kwargs['service'], kwargs['output']], ld):
        # Helper print
        click.secho("Generating {}".format(i[0]))

        # Generate output file
        with open(i[0], "w") as f:
            g = json.dumps(i[1],indent=2)
            f.write(g)


@group.command()
@add_options(_shared_options)
@click.option('--force-task-definition', "force_td", is_flag=True)
@click.option('--fast-redeploy', "fast_redeploy", is_flag=True)
@click.option('--wait', "wait_for_service", is_flag=True)
@click.option('-r', '--region', 'aws_region', show_default=True, default="us-east-1")
def install(**kwargs):
    """ Installs task definition and service to given cluster """

    # Interpolate the project
    td, ts, output = _render_project(**kwargs)
    service_name = ts['serviceName']

    # Install task-definition
    os.environ['AWS_DEFAULT_REGION'] = kwargs['aws_region']
    arn_td = ecs.install_or_update_task_definition(td, kwargs['force_td'])
    arn_s = ecs.install_service(ts, arn_td)

    # Echo ARNS
    click.secho("Task-definition ARN: {}".format(arn_td))
    click.secho("Service ARN: {}".format(arn_s))

    # Kill all currently running tasks
    if kwargs['fast_redeploy']:
        ecs.kill_tasks(ts.get('cluster'), arn_s)

    # Waiter
    if kwargs['wait_for_service']:
        client = boto3.client('ecs')
        waiter = client.get_waiter('services_stable')

        click.secho('Waiting until service is stable.')
        for i in range(5):
            try:
                waiter.wait(cluster=ts['cluster'], services=[service_name])
            except botocore.exceptions.WaiterError as e:
                if "Max attempts exceeded" in e.message:
                    click.secho("Service wasn't started in 600s")
                    continue
                click.secho(e.message)


if __name__ == '__main__':
    group()