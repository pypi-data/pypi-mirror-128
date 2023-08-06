#!/usr/bin/env python
# Copyright 2021 Vincent Texier
#
# This file is part of MADAM.
#
# MADAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MADAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MADAM.  If not, see <https://www.gnu.org/licenses/>.
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional, Union
from urllib.error import URLError

import click
from rich.console import Console
from rich.table import Table

from madam.domains.application import MainApplication
from madam.domains.entities import job as data_job
from madam.domains.entities.constants import MADAM_CONFIG_PATH, MADAM_LOG_LEVEL
from madam.domains.entities.watchfolder import Watchfolder
from madam.domains.entities.workflow import Workflow
from madam.domains.entities.workflow_instance import WorkflowInstance
from madam.libs.http import RESPONSE_JSON, HTTPClient
from madam.slots.graphql import server as graphql_server


@click.group()
@click.option(
    "--config",
    "-c",
    default=MADAM_CONFIG_PATH,
    type=click.Path(),
    show_default=True,
    help="madam.yaml config path",
)
@click.option(
    "--level",
    "-l",
    default=MADAM_LOG_LEVEL,
    type=str,
    show_default=True,
    help="Log level",
)
@click.option(
    "--endpoint",
    "-e",
    default=None,
    type=str,
    help="MADAM server API endpoint host:port like localhost:5000",
)
@click.option(
    "--ssl",
    default=None,
    help="Use SSL on MADAM server API endpoint",
)
@click.pass_context
def cli(context, config, level, endpoint, ssl):
    """
    Madam cli console command
    """
    # configure log level
    if os.getenv("MADAM_LOG_LEVEL", None) is not None:
        # from env var
        logging.basicConfig(level=os.getenv("MADAM_LOG_LEVEL").upper())
    else:
        # from --level option
        logging.basicConfig(level=level.upper())

    # check context
    context.ensure_object(dict)

    if os.getenv("MADAM_CONFIG_PATH", None) is not None:
        # from env var
        config_path = os.getenv("MADAM_CONFIG_PATH")
    else:
        # from --config option
        config_path = config

    # create Application instance
    context.obj["application"] = MainApplication(config_path)
    if endpoint is not None:
        scheme = "http"
        if ssl is not None:
            scheme += "s"

        context.obj["endpoint"] = f"{scheme}://{endpoint}"


@cli.command()
@click.pass_context
def server(context):
    """
    Run Madam server
    """
    graphql_server.run(context.obj["application"], MADAM_LOG_LEVEL)


@cli.group()
def workflows():
    """
    Manage workflows
    """


@workflows.command("load")
@click.argument("filepath", type=click.Path(exists=True))
@click.pass_context
def workflows_load(context, filepath):
    """
    Load FILEPATH BPMN file and create workflow from it
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    with open(filepath, encoding="utf-8") as fh:
        content = fh.read()

    mutation = """
    mutation ($content: String!) {
        createWorkflow(content: $content) {
            status
            error
            workflow {
                id
                name
                version
                }
        }
    }
    """
    variables = {"content": content}
    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["createWorkflow"]["status"] is False:
        click.echo("error: " + response["data"]["createWorkflow"]["error"])
        return
    click.echo(
        f'Workflow "{response["data"]["createWorkflow"]["workflow"]["name"]}" (id: {response["data"]["createWorkflow"]["workflow"]["id"]}) Version {response["data"]["createWorkflow"]["workflow"]["version"]} loaded.'
    )


@workflows.command("list")
@click.pass_context
def workflows_list(context):
    """
    List workflows
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="WORKFLOWS",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Version", justify="right")
    table.add_column("Name")
    table.add_column("Timer")
    table.add_column("Created At")

    query = """
    query {
        workflows {
            count
            result {
                id
                version
                name
                timer
                created_at
            }
        }
    }
    """
    response = query_endpoint(query, context.obj["endpoint"])

    for workflow_ in response["data"]["workflows"]["result"]:
        table.add_row(
            workflow_["id"],
            str(workflow_["version"]),
            workflow_["name"],
            "None" if workflow_["timer"] is None else workflow_["timer"],
            workflow_["created_at"],
        )

    Console().print(table)


@workflows.command("clear_instances")
@click.argument("id", type=str)
@click.option(
    "--version",
    "-v",
    type=int,
    default=None,
    show_default=True,
    help="Workflow version",
)
@click.pass_context
def workflows_clear_instances(
    context, id, version
):  # pylint: disable=redefined-builtin
    """
    Delete instances of workflow ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: String!, $version: Int) {
        deleteWorkflowInstancesByWorkflow(id: $id, version: $version) {
            status
            error
        }
    }
    """
    variables = {"id": id}
    if version is not None:
        variables["version"] = int(version)

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["deleteWorkflowInstancesByWorkflow"]["status"] is False:
        click.echo(
            "error: " + response["data"]["deleteWorkflowInstancesByWorkflow"]["error"]
        )
        return

    if version is None:
        version = "latest"
    click.echo(f"Instances of workflow {id}, {version} deleted.")


@workflows.command("abort_instances")
@click.argument("id", type=str)
@click.option(
    "--version",
    "-v",
    type=int,
    default=None,
    show_default=True,
    help="Workflow version",
)
@click.pass_context
def workflows_abort_instances(
    context, id, version
):  # pylint: disable=redefined-builtin
    """
    Abort instances of workflow ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
     mutation ($id: String!, $version: Int) {
         abortWorkflowInstancesByWorkflow(id: $id, version: $version) {
             status
             error
         }
     }
    """
    variables = {"id": id}
    if version is not None:
        variables["version"] = int(version)

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["abortWorkflowInstancesByWorkflow"]["status"] is False:
        click.echo(
            "error: " + response["data"]["abortWorkflowInstancesByWorkflow"]["error"]
        )
        return

    if version is None:
        version = "latest"
    click.echo(f"Instances of workflow {id}, {version} aborted.")


@workflows.command("delete")
@click.argument("id", type=str)
@click.pass_context
def workflows_delete(context, id):  # pylint: disable=redefined-builtin
    """
    Delete workflow by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: String!) {
        deleteWorkflow(id: $id) {
            status
            error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["deleteWorkflow"]["status"] is False:
        click.echo("error: " + response["data"]["deleteWorkflow"]["error"])
        return

    click.echo(f"Workflow {id} deleted.")


@workflows.command("start")
@click.argument("id", type=str)
@click.argument("variables", type=str, nargs=-1)
@click.option(
    "--version",
    "-v",
    type=int,
    default=None,
    show_default=True,
    help="Workflow version",
)
@click.pass_context
def workflows_start(
    context, id, version, variables
):  # pylint: disable=redefined-builtin
    """
    Start processing workflow

    ID: workflow ID

    VARIABLES: initial variables as key=value
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    if len(variables) == 0:
        variables_dict = None
    else:
        variables_dict = {}
        for var in variables:
            key, value = var.split("=")
            variables_dict[key] = value
    mutation = """
    mutation ($id: String!, $version: Int, $variables: JSON) {
        startWorkflow(id: $id, version: $version, variables: $variables) {
            status
            error
        }
    }
    """
    if variables_dict is None:
        variables_dict = {}
    variables_dict["id"] = id
    if version is not None:
        variables_dict["version"] = int(version)

    response = query_endpoint(mutation, context.obj["endpoint"], variables_dict)

    if response["data"]["startWorkflow"]["status"] is False:
        click.echo("error: " + response["data"]["startWorkflow"]["error"])
        return

    if version is None:
        version = "latest"
    click.echo(f"Workflow {id}, {version} started.")


@workflows.command("abort")
@click.argument("id", type=str)
@click.option(
    "--version",
    "-v",
    type=int,
    default=None,
    show_default=True,
    help="Workflow version",
)
@click.pass_context
def workflows_abort(context, id, version):  # pylint: disable=redefined-builtin
    """
    Abort workflow (instances and timers) by ID and optionally version
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: String!, $version: Int) {
        abortWorkflow(id: $id, version: $version) {
            status
            error
        }
    }
    """
    variables = {"id": id}
    if version is not None:
        variables["version"] = int(version)

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["abortWorkflow"]["status"] is False:
        click.echo("error: " + response["data"]["abortWorkflow"]["error"])
        return

    if version is None:
        version = "latest"
    click.echo(f"Workflow {id}, {version} instances and timers aborted.")


@workflows.command("show")
@click.argument("id", type=str)
@click.option(
    "--version",
    "-v",
    type=int,
    default=None,
    show_default=True,
    help="Workflow version",
)
@click.pass_context
def workflows_show(context, id, version):  # pylint: disable=redefined-builtin
    """
    Show workflow by ID and optionally version
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    query = """
    query ($id: String!, $version: Int) {
        workflow (id: $id, version: $version) {
            id
            name
            version
            sha256
            timer
            created_at
        }
    }
    """
    variables = {"id": id}
    if version is not None:
        variables["version"] = int(version)

    response = query_endpoint(query, context.obj["endpoint"], variables)

    workflow_ = Workflow(
        response["data"]["workflow"]["id"],
        response["data"]["workflow"]["version"],
        response["data"]["workflow"]["name"],
        "",
        response["data"]["workflow"]["sha256"],
        response["data"]["workflow"]["timer"],
        datetime.fromisoformat(response["data"]["workflow"]["created_at"]),
    )

    table = Table(
        show_header=True,
        header_style="bold blue",
        title=f"WORKFLOW {workflow_.id} Version {workflow_.version}",
        title_style="bold blue",
    )
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Name", workflow_.name)
    table.add_row("Sha256", workflow_.sha256)
    table.add_row("Timer", workflow_.timer)
    table.add_row("Created At", workflow_.created_at.isoformat())

    Console().print(table)

    if workflow_.timer is not None:
        table = Table(
            show_header=True,
            header_style="bold blue",
            title="TIMERS",
            title_style="bold blue",
        )
        table.add_column("ID")
        table.add_column("Status")
        table.add_column("Start At")
        table.add_column("End At")
        table.add_column("Input")

        query = """
        query ($workflow: WorkflowInput) {
            timers (workflow: $workflow) {
                count
                result {
                    id
                    status
                    start_at
                    end_at
                    input
                }
            }
        }
        """
        variables = {"workflow": {"id": workflow_.id, "version": workflow_.version}}

        response = query_endpoint(query, context.obj["endpoint"], variables)

        for timer_ in response["data"]["timers"]["result"]:
            table.add_row(
                str(timer_["id"]),
                timer_["status"],
                timer_["start_at"],
                timer_["end_at"],
                str(timer_["input"]),
            )

        Console().print(table)

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="INSTANCES",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Status")
    table.add_column("Start At")
    table.add_column("End At")
    table.add_column("Input")
    table.add_column("Output")

    query = """
    query ($workflow: WorkflowInput) {
        workflow_instances (workflow: $workflow) {
            count
            result {
                id
                status
                start_at
                end_at
                input
                output
            }
        }
    }
    """
    variables = {"workflow": {"id": workflow_.id, "version": workflow_.version}}

    response = query_endpoint(query, context.obj["endpoint"], variables)

    for workflow_instance_ in response["data"]["workflow_instances"]["result"]:
        table.add_row(
            str(workflow_instance_["id"]),
            workflow_instance_["status"],
            workflow_instance_["start_at"],
            workflow_instance_["end_at"],
            str(workflow_instance_["input"]),
            str(workflow_instance_["output"]),
        )

    Console().print(table)


@cli.group()
def instances():
    """
    Manage workflow instances
    """


@instances.command("list")
@click.pass_context
def instances_list(context):
    """
    List workflow instances
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="WORKFLOW INSTANCES",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Workflow")
    table.add_column("Version")
    table.add_column("Status")
    table.add_column("Start At")
    table.add_column("End At")

    query = """
    query {
        workflow_instances {
            count
            result {
                id
                workflow {
                    id
                    version
                }
                status
                start_at
                end_at
            }
        }
    }
    """
    response = query_endpoint(query, context.obj["endpoint"])

    for workflow_instance_ in response["data"]["workflow_instances"]["result"]:
        table.add_row(
            str(workflow_instance_["id"]),
            workflow_instance_["workflow"]["id"],
            str(workflow_instance_["workflow"]["version"]),
            workflow_instance_["status"],
            workflow_instance_["start_at"],
            workflow_instance_["end_at"],
        )

    Console().print(table)


@instances.command("abort")
@click.argument("id", type=str)
@click.pass_context
def instances_abort(context, id):  # pylint: disable=redefined-builtin
    """
    Abort workflow instance by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
        abortWorkflowInstance(id: $id) {
            status
            error
        }
    }
        """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["abortWorkflowInstance"]["status"] is False:
        click.echo("error: " + response["data"]["abortWorkflowInstance"]["error"])
        return

    click.echo(f"Workflow instance {id} aborted.")


@instances.command("delete")
@click.argument("id", type=str)
@click.pass_context
def instances_delete(context, id):  # pylint: disable=redefined-builtin
    """
    Delete workflow instance by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
        deleteWorkflowInstance(id: $id) {
            status
            error
        }
    }
        """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["deleteWorkflowInstance"]["status"] is False:
        click.echo("error: " + response["data"]["deleteWorkflowInstance"]["error"])
        return

    click.echo(f"Workflow instance {id} deleted.")


@instances.command("show")
@click.argument("id", type=str)
@click.pass_context
def instances_show(context, id):  # pylint: disable=redefined-builtin
    """
    Show workflow instance by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    query = """
    query ($id: ID!) {
        workflow_instance (id: $id) {
            id
            start_at
            end_at
            status
            input
            output
            error
            workflow {
                id
                version
            }
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(query, context.obj["endpoint"], variables)

    if response["data"]["workflow_instance"] is None:
        click.echo(f"Workflow instance {id} not found.")
        return

    workflow_ = Workflow(
        response["data"]["workflow_instance"]["workflow"]["id"],
        response["data"]["workflow_instance"]["workflow"]["version"],
        "",
        "",
        "",
        "",
        datetime.now(),
    )
    instance_ = WorkflowInstance(
        response["data"]["workflow_instance"]["id"],
        datetime.fromisoformat(response["data"]["workflow_instance"]["start_at"]),
        datetime.fromisoformat(response["data"]["workflow_instance"]["end_at"])
        if response["data"]["workflow_instance"]["end_at"] is not None
        else None,
        response["data"]["workflow_instance"]["status"],
        response["data"]["workflow_instance"]["input"],
        response["data"]["workflow_instance"]["output"],
        response["data"]["workflow_instance"]["error"],
        workflow_,
    )

    table = Table(
        show_header=True,
        header_style="bold blue",
        title=f"WORKFLOW INSTANCE {instance_.id}",
        title_style="bold blue",
    )
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Workflow ID", str(instance_.workflow.id))
    table.add_row("Workflow Version", str(instance_.workflow.version))
    table.add_row("Status", instance_.status)
    table.add_row("Input", str(instance_.input))
    table.add_row("Output", str(instance_.output))
    table.add_row("Start At", instance_.start_at.isoformat())
    table.add_row("End At", instance_.end_at.isoformat() if instance_.end_at else None)

    Console().print(table)

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="JOBS",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Agent ID")
    table.add_column("Agent Type")
    table.add_column("Status")
    table.add_column("Error")
    table.add_column("Start At")
    table.add_column("End At")

    query = """
    query ($workflow_instance_id: ID) {
        jobs (workflow_instance_id: $workflow_instance_id) {
            count
            result {
                id
                status
                agent_id
                agent_type
                start_at
                end_at
                error
            }
        }
    }
    """
    variables = {"workflow_instance_id": str(instance_.id)}

    response = query_endpoint(query, context.obj["endpoint"], variables)

    for job_ in response["data"]["jobs"]["result"]:
        table.add_row(
            job_["id"],
            job_["agent_id"],
            job_["agent_type"],
            job_["status"],
            job_["error"],
            job_["start_at"],
            job_["end_at"],
        )

    Console().print(table)

    query = """
    query ($workflow_instance_id: ID, $status: JobStatus) {
        jobs (workflow_instance_id: $workflow_instance_id, status: $status) {
            count
            result {
                id
                status
                agent_id
                agent_type
                start_at
                end_at
                error
                headers
                input
                output
            }
        }
    }
    """
    variables = {
        "workflow_instance_id": str(instance_.id),
        "status": data_job.STATUS_ERROR,
    }
    response = query_endpoint(query, context.obj["endpoint"], variables)

    for job_ in response["data"]["jobs"]["result"]:
        table = Table(
            show_header=True,
            header_style="bold blue",
            title=f"JOB {job_['id']}",
            title_style="bold blue",
        )
        table.add_column("Field")
        table.add_column("Value")

        table.add_row("Agent ID", job_["agent_id"])
        table.add_row("Agent Type", job_["agent_type"])
        table.add_row("Status", job_["status"])
        table.add_row("Error", job_["error"])
        table.add_row("Headers", str(job_["headers"]))
        table.add_row("Input", str(job_["input"]))
        table.add_row("Output", str(job_["output"]))
        table.add_row("Start At", job_["start_at"])
        table.add_row("End At", job_["end_at"])

        Console().print(table)

        query = """
        query ($job_id: ID) {
            applications (job_id: $job_id) {
                count
                result {
                    id
                    name
                    status
                    arguments
                    logs
                    container_id
                    container_name
                    container_error
                    start_at
                    end_at
                }
            }
        }
        """
        variables = {"job_id": str(job_["id"])}

        response = query_endpoint(query, context.obj["endpoint"], variables)

        for job_application_ in response["data"]["applications"]["result"]:
            table = Table(
                show_header=True,
                header_style="bold blue",
                title=f"JOB APPLICATION {job_application_['id']}",
                title_style="bold blue",
            )
            table.add_column("Field")
            table.add_column("Value")

            table.add_row("ID", str(job_application_["id"]))
            table.add_row("Name", job_application_["name"])
            table.add_row("Status", job_application_["status"])
            table.add_row("Arguments", job_application_["arguments"])
            table.add_row("Logs", job_application_["logs"])
            table.add_row("Container ID", job_application_["container_id"])
            table.add_row("Container Name", job_application_["container_name"])
            table.add_row("Container Error", job_application_["container_error"])
            table.add_row("Start At", job_application_["start_at"])
            table.add_row("End At", job_application_["end_at"])

            Console().print(table)


@cli.group()
def jobs():
    """
    Manage jobs
    """


@jobs.command("list")
@click.pass_context
def jobs_list(context):
    """
    List jobs
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="JOBS",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Instance")
    table.add_column("Workflow")
    table.add_column("Version")
    table.add_column("Status")
    table.add_column("Error")
    table.add_column("Start At")
    table.add_column("End At")

    query = """
    query {
        jobs {
            count
            result {
                id
                workflow_instance {
                    id
                    workflow {
                        id
                        version
                    }
                }
                status
                start_at
                end_at
                error
            }
        }
    }
    """
    response = query_endpoint(query, context.obj["endpoint"])

    for job_ in response["data"]["jobs"]["result"]:
        table.add_row(
            job_["id"],
            job_["workflow_instance"]["id"],
            job_["workflow_instance"]["workflow"]["id"],
            str(job_["workflow_instance"]["workflow"]["version"]),
            job_["status"],
            job_["error"],
            job_["start_at"],
            job_["end_at"],
        )

    Console().print(table)


@cli.group()
def timers():
    """
    Manage timers
    """


@timers.command("list")
@click.pass_context
def timers_list(context):
    """
    List timers
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="TIMERS",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Workflow")
    table.add_column("Version")
    table.add_column("Status")
    table.add_column("Start At")
    table.add_column("End At")
    table.add_column("Input")

    query = """
    query {
        timers {
            count
            result {
                id
                workflow {
                    id
                    version
                }
                status
                start_at
                end_at
                input
            }
        }
    }
    """
    response = query_endpoint(query, context.obj["endpoint"])

    for timer_ in response["data"]["timers"]["result"]:
        table.add_row(
            timer_["id"],
            timer_["workflow"]["id"],
            str(timer_["workflow"]["version"]),
            timer_["status"],
            timer_["start_at"],
            timer_["end_at"],
            str(timer_["input"]),
        )

    Console().print(table)


@timers.command("abort")
@click.argument("id", type=str)
@click.pass_context
def timers_abort(context, id):  # pylint: disable=redefined-builtin
    """
    Abort timer by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
        abortTimer(id: $id) {
            status
            error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["abortTimer"]["status"] is False:
        click.echo("error: " + response["data"]["abortTimer"]["error"])
        return

    click.echo(f"Timer {id} aborted.")


@timers.command("delete")
@click.argument("id", type=str)
@click.pass_context
def timers_delete(context, id):  # pylint: disable=redefined-builtin
    """
    Delete Timer by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
        deleteTimer(id: $id) {
            status
            error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["deleteTimer"]["status"] is False:
        click.echo("error: " + response["data"]["deleteTimer"]["error"])
        return

    click.echo(f"Timer {id} deleted.")


@cli.group()
def watchfolders():
    """
    Manage watchfolders
    """


@watchfolders.command("create")
@click.argument("data", type=str)
@click.pass_context
def watchfolders_create(context, data):
    """
    Create a new watchfolder with field values from JSON data

    To create or update use a JSON string in data argument:

    {\n
        "path": "YOUR PATH",\n
        "re_files": optional, default=None or "REGEXP",\n
        "re_dirs": optional, default=None or "REGEXP",\n
        "added_workflow": optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "added_variables": optional, default=None or "JSON",\n
        "modified_workflow":  optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "modified_variables": optional, default=None or "JSON",\n
        "deleted_workflow":  optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "deleted_variables": optional, default=None or "JSON",\n
        "added_items_key": optional, default="watchfolder" or "ADDED_ITEMS_VARIABLE_NAME",\n
        "modified_items_key": optional, default="watchfolder" or "MODIFIED_ITEMS_VARIABLE_NAME",\n
        "deleted_items_key": optional, default="watchfolder" or "DELETED_ITEMS_VARIABLE_NAME",\n
    }\n
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    variables = json.loads(data)

    mutation = """
    mutation (
        $path: String!,
        $re_files: String = null,
        $re_dirs: String = null,
        $added_workflow: WorkflowInput = null,
        $added_variables: JSON = null,
        $modified_workflow: WorkflowInput = null,
        $modified_variables: JSON = null,
        $deleted_workflow: WorkflowInput = null,
        $deleted_variables: JSON = null,
        $added_items_key: String = "watchfolder",
        $modified_items_key: String = "watchfolder",
        $deleted_items_key: String = "watchfolder"
        ) {
            createWatchfolder(
                path: $path,
                re_files: $re_files,
                re_dirs: $re_dirs,
                added_workflow: $added_workflow,
                added_variables: $added_variables,
                modified_workflow: $modified_workflow,
                modified_variables: $modified_variables,
                deleted_workflow: $deleted_workflow,
                deleted_variables: $deleted_variables,
                added_items_key: $added_items_key,
                modified_items_key: $modified_items_key,
                deleted_items_key: $deleted_items_key
            ) {
            status
            error
            watchfolder {
                id
                path
            }
        }
    }
    """
    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["createWatchfolder"]["status"] is False:
        click.echo("error: " + response["data"]["createWatchfolder"]["error"])
        return
    click.echo(
        f'Watchfolder id {response["data"]["createWatchfolder"]["watchfolder"]["id"]}) created for path {response["data"]["createWatchfolder"]["watchfolder"]["path"]}.'
    )


@watchfolders.command("update")
@click.argument("data", type=str)
@click.pass_context
def watchfolders_update(context, data):
    """
    Update watchfolder by id with field values from JSON data

    To create or update use a JSON string in data argument:

    {\n
        "id": "WATCHFOLDER_ID",\n
        "path": "YOUR PATH",\n
        "re_files": optional, default=None or "REGEXP",\n
        "re_dirs": optional, default=None or "REGEXP",\n
        "added_workflow": optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "added_variables": optional, default=None or "JSON",\n
        "modified_workflow":  optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "modified_variables": optional, default=None or "JSON",\n
        "deleted_workflow":  optional, default=None or {\n
            "id": "WORKFLOW_ID",\n
            "version": optional, default=None\n
        },\n
        "deleted_variables": optional, default=None or "JSON",\n
        "added_items_key": optional, default="watchfolder" or "ADDED_ITEMS_VARIABLE_NAME",\n
        "modified_items_key": optional, default="watchfolder" or "MODIFIED_ITEMS_VARIABLE_NAME",\n
        "deleted_items_key": optional, default="watchfolder" or "DELETED_ITEMS_VARIABLE_NAME",\n
    }\n
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    variables = json.loads(data)

    mutation = """
    mutation (
        $id: ID!,
        $path: String!,
        $re_files: String = null,
        $re_dirs: String = null,
        $added_workflow: WorkflowInput = null,
        $added_variables: JSON = null,
        $modified_workflow: WorkflowInput = null,
        $modified_variables: JSON = null,
        $deleted_workflow: WorkflowInput = null,
        $deleted_variables: JSON = null,
        $added_items_key: String = "watchfolder",
        $modified_items_key: String = "watchfolder",
        $deleted_items_key: String = "watchfolder"
        ) {
            updateWatchfolder(
                id: $id,
                path: $path,
                re_files: $re_files,
                re_dirs: $re_dirs,
                added_workflow: $added_workflow,
                added_variables: $added_variables,
                modified_workflow: $modified_workflow,
                modified_variables: $modified_variables,
                deleted_workflow: $deleted_workflow,
                deleted_variables: $deleted_variables,
                added_items_key: $added_items_key,
                modified_items_key: $modified_items_key,
                deleted_items_key: $deleted_items_key
            ) {
            status
            error
            watchfolder {
                id
                path
            }
        }
    }
    """

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["updateWatchfolder"]["status"] is False:
        click.echo("error: " + response["data"]["updateWatchfolder"]["error"])
        return
    click.echo(
        f'Watchfolder id: {response["data"]["updateWatchfolder"]["watchfolder"]["id"]}) updated for path {response["data"]["updateWatchfolder"]["watchfolder"]["path"]}.'
    )


@watchfolders.command("start")
@click.argument("id", type=str)
@click.pass_context
def watchfolders_start(context, id):  # pylint: disable=redefined-builtin
    """
    Start watchfolder by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
            startWatchfolder(id: $id) {
                status
                error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["startWatchfolder"]["status"] is False:
        click.echo("error: " + response["data"]["startWatchfolder"]["error"])
        return

    click.echo(f"Watchfolder {id} started.")


@watchfolders.command("stop")
@click.argument("id", type=str)
@click.pass_context
def watchfolders_stop(context, id):  # pylint: disable=redefined-builtin
    """
    Stop watchfolder by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
            stopWatchfolder(id: $id) {
                status
                error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["stopWatchfolder"]["status"] is False:
        click.echo("error: " + response["data"]["stopWatchfolder"]["error"])
        return

    click.echo(f"Watchfolder {id} stopped.")


@watchfolders.command("delete")
@click.argument("id", type=str)
@click.pass_context
def watchfolders_delete(context, id):  # pylint: disable=redefined-builtin
    """
    Delete watchfolder by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    mutation = """
    mutation ($id: ID!) {
            deleteWatchfolder(id: $id) {
                status
                error
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(mutation, context.obj["endpoint"], variables)

    if response["data"]["deleteWatchfolder"]["status"] is False:
        click.echo("error: " + response["data"]["deleteWatchfolder"]["error"])
        return

    click.echo(f"Watchfolder {id} deleted.")


@watchfolders.command("show")
@click.argument("id", type=str)
@click.pass_context
def watchfolders_show(context, id):  # pylint: disable=redefined-builtin
    """
    Show watchfolder by ID
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    query = """
    query ($id: ID!) {
        watchfolder (id: $id) {
            id
            path
            start_at
            end_at
            status
            re_files
            re_dirs
            added_workflow {
                id
                version
            }
            added_variables
            modified_workflow {
                id
                version
            }
            modified_variables
            deleted_workflow {
                id
                version
            }
            deleted_variables
            added_items_key
            modified_items_key
            deleted_items_key
        }
    }
    """
    variables = {"id": id}

    response = query_endpoint(query, context.obj["endpoint"], variables)

    added_workflow = None
    if response["data"]["watchfolder"]["added_workflow"] is not None:
        added_workflow = Workflow(
            response["data"]["watchfolder"]["added_workflow"]["id"],
            response["data"]["watchfolder"]["added_workflow"]["version"],
            "",
            "",
            "",
            "",
            datetime.now(),
        )
    modified_workflow = None
    if response["data"]["watchfolder"]["modified_workflow"] is not None:
        modified_workflow = Workflow(
            response["data"]["watchfolder"]["modified_workflow"]["id"],
            response["data"]["watchfolder"]["modified_workflow"]["version"],
            "",
            "",
            "",
            "",
            datetime.now(),
        )
    deleted_workflow = None
    if response["data"]["watchfolder"]["deleted_workflow"] is not None:
        deleted_workflow = Workflow(
            response["data"]["watchfolder"]["deleted_workflow"]["id"],
            response["data"]["watchfolder"]["deleted_workflow"]["version"],
            "",
            "",
            "",
            "",
            datetime.now(),
        )

    watchfolder = Watchfolder(
        response["data"]["watchfolder"]["id"],
        response["data"]["watchfolder"]["path"],
        None
        if response["data"]["watchfolder"]["start_at"] is None
        else datetime.fromisoformat(response["data"]["watchfolder"]["start_at"]),
        None
        if response["data"]["watchfolder"]["end_at"] is None
        else datetime.fromisoformat(response["data"]["watchfolder"]["end_at"]),
        response["data"]["watchfolder"]["status"],
        response["data"]["watchfolder"]["re_files"],
        response["data"]["watchfolder"]["re_dirs"],
        added_workflow,
        response["data"]["watchfolder"]["added_variables"],
        None if modified_workflow is None else modified_workflow,
        response["data"]["watchfolder"]["modified_variables"],
        None if deleted_workflow is None else deleted_workflow,
        response["data"]["watchfolder"]["deleted_variables"],
        response["data"]["watchfolder"]["added_items_key"],
        response["data"]["watchfolder"]["modified_items_key"],
        response["data"]["watchfolder"]["deleted_items_key"],
    )

    table = Table(
        show_header=True,
        header_style="bold blue",
        title=f"WATCHFOLDER {watchfolder.id}",
        title_style="bold blue",
    )
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Path", watchfolder.path)
    table.add_row(
        "Start At", watchfolder.start_at.isoformat() if watchfolder.start_at else None
    )
    table.add_row(
        "End At", watchfolder.end_at.isoformat() if watchfolder.end_at else None
    )
    table.add_row("Status", watchfolder.status)
    table.add_row("Files RegExp", watchfolder.re_files)
    table.add_row("Dirs RegExp", watchfolder.re_dirs)
    table.add_row(
        "Added Workflow ID",
        None if added_workflow is None else watchfolder.added_workflow.id,
    )
    table.add_row(
        "Added Workflow Version",
        None if added_workflow is None else str(watchfolder.added_workflow.version),
    )
    table.add_row("Added Variables", str(watchfolder.added_variables))
    table.add_row(
        "Modified Workflow ID",
        None if modified_workflow is None else watchfolder.modified_workflow.id,
    )
    table.add_row(
        "Modified Workflow Version",
        None
        if modified_workflow is None
        else str(watchfolder.modified_workflow.version),
    )
    table.add_row("Modified Variables", str(watchfolder.modified_variables))
    table.add_row(
        "Deleted Workflow ID",
        None if deleted_workflow is None else watchfolder.deleted_workflow.id,
    )
    table.add_row(
        "Deleted Workflow Version",
        None if deleted_workflow is None else str(watchfolder.deleted_workflow.version),
    )
    table.add_row("Deleted Variables", str(watchfolder.deleted_variables))
    table.add_row("Added Items Key", watchfolder.added_items_key)
    table.add_row("Modified Items Key", watchfolder.modified_items_key)
    table.add_row("Deleted Items Key", watchfolder.deleted_items_key)

    Console().print(table)


@watchfolders.command("list")
@click.pass_context
def watchfolders_list(context):
    """
    List watchfolders
    """
    if "endpoint" not in context.obj:
        raise click.ClickException(Exception("Missing option '--endpoint' / '-e'."))

    table = Table(
        show_header=True,
        header_style="bold blue",
        title="WATCHFOLDERS",
        title_style="bold blue",
    )
    table.add_column("ID")
    table.add_column("Path")
    table.add_column("Start At")
    table.add_column("End At")
    table.add_column("Status")
    table.add_column("Added Workflow")
    table.add_column("Modified Workflow")
    table.add_column("Deleted Workflow")

    query = """
    query {
        watchfolders {
            count
            result {
                id
                path
                start_at
                end_at
                status
                added_workflow {
                    id
                    version
                }
                modified_workflow {
                    id
                    version
                }
                deleted_workflow {
                    id
                    version
                }
            }
        }
    }
    """
    response = query_endpoint(query, context.obj["endpoint"])

    for watchfolder in response["data"]["watchfolders"]["result"]:
        table.add_row(
            watchfolder["id"],
            watchfolder["path"],
            watchfolder["start_at"],
            watchfolder["end_at"],
            watchfolder["status"],
            None
            if watchfolder["added_workflow"] is None
            else f"{watchfolder['added_workflow']['id']},{watchfolder['added_workflow']['version']}",
            None
            if watchfolder["modified_workflow"] is None
            else f"{watchfolder['modified_workflow']['id']},{watchfolder['modified_workflow']['version']}",
            None
            if watchfolder["deleted_workflow"] is None
            else f"{watchfolder['deleted_workflow']['id']},{watchfolder['deleted_workflow']['version']}",
        )

    Console().print(table)


def query_endpoint(query: str, url: str, variables: Optional[dict] = None) -> Any:
    """
    GraphQL query or mutation request on endpoint

    :param query: GraphQL query string
    :param url: Endpoint url
    :param variables: Variables for the query (optional, default None)
    :return:
    """
    payload = {"query": query}  # type: Dict[str, Union[str, dict]]

    if variables is not None:
        payload["variables"] = variables

    client = HTTPClient()

    try:
        # get json response
        response = client.request(url, "POST", rtype=RESPONSE_JSON, json_data=payload)
    except URLError as exception:
        print(str(exception))
        raise click.ClickException(exception)

    if "errors" in response:
        for error in response["errors"]:
            click.echo(f"{error['message']} ({error['path']})")
        raise click.ClickException(Exception("API returned errors."))

    return response


if __name__ == "__main__":
    cli(obj={})  # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
