import typer
import humanize

from datetime import datetime
from rich.console import Console
from typing import List

from continual.python.cli import utils
from continual import Client


app = typer.Typer(help="Manage changes.")


def truncate(data, n=40):
    """Truncate string with elipses."""
    return (data[:n] + "...") if len(data) > n else data


def format_changes_data(changes, project, n, filters, all_projects):
    data = []
    for push in changes:
        success = 0
        fs_count = 0
        fs_success = 0
        model_count = 0
        model_success = 0
        for step in push.plan:
            if step.resource_name.split("/")[2] == "featureSets":
                fs_count += 1
                if step.state == "SUCCEEDED":
                    fs_success += 1
                    success += 1
            else:
                model_count += 1
                if step.state == "SUCCEEDED":
                    model_success += 1
                    success += 1
        total = len(push.plan)
        age = humanize.naturaltime(datetime.now() - push.create_time)
        push_id = push.name.split("/")[-1]
        push_data = [
            push_id,
            f"{fs_success}/{fs_count}",
            f"{model_success}/{model_count}",
            f"{success}/{total}",
            push.state,
            age,
            truncate(push.message),
        ]
        if all_projects:
            push_data.insert(0, push.parent.split("/")[1])
        data.append(push_data)
    headers = [
        "ID",
        "Feature Set Steps",
        "Model Steps",
        "Total Steps",
        "State",
        "Age",
        "Message",
    ]
    filter_snippet = ""
    project_snippet = "project %s" % project
    if all_projects:
        project_snippet = "all accessible projects"
        headers.insert(0, "Project")
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters)
    typer.secho(
        "\nFound %s changes in %s%s:" % (len(data), project_snippet, filter_snippet),
        fg="blue",
    )
    return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        list(project=None, n=30, filters=[], all_projects=False, style=None)


@app.command("list")
@utils.exit_on_error
def list(
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option("", "--env", help="Environment ID."),
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    all_projects: bool = typer.Option(False, "--all", "-a", help="Show all projects."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List all changes.

    Filters can include:
        --state (i.e. state:FAILED)
    """
    project = utils.get_project(project)
    environment = utils.get_environment(project, environment)

    c = Client(project=utils.get_environment_name(project, environment))
    push_list = c.changes.list(n, filters=filters, all_projects=all_projects)
    pushes = sorted(push_list, key=lambda x: x.create_time, reverse=True)
    (data, headers) = format_changes_data(pushes, project, n, filters, all_projects)
    if style is None:
        style = c.config.style
    style = utils.get_style(style)
    utils.print_table(data, headers, style=style)


@app.command("get")
@utils.exit_on_error
def get(
    push_id: str = typer.Argument(..., help="Change ID."),
    project: str = typer.Option(False, help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Show full JSON representation"),
):
    """Get change details."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    push = c.changes.get(push_id)
    if json:
        console = Console()
        console.print(push.to_dict())
    else:
        typer.secho("Operations for %s:" % push.id, fg="magenta")
        if len(push.plan) > 0:
            steps = sorted(
                push.plan,
                key=lambda x: int(x.id),
                reverse=False,
            )
            typer.secho(
                f"\n  {'Operation':20s}{'State':20s}{'Duration(s)':10s}{'Start Time':30s}{'End Time':30s}",
                fg="magenta",
            )
            old_resource = ""
            featuresets = []
            models = []
            for step in steps:
                if step.resource_name.split("/")[2] == "models":
                    models.append(step)
                else:
                    featuresets.append(step)
            for step in featuresets + models:
                step_id = step.resource_name.split("/")[-1]
                if step.resource_name.split("/")[2] == "models":
                    step_type = "Model"
                else:
                    step_type = "Feature Set"
                start_time = step.start_time
                end_time = step.finish_time
                if start_time:
                    start_time = step.start_time.replace(microsecond=0)
                    if end_time:
                        end_time = end_time.replace(microsecond=0)
                        duration = (end_time - start_time).seconds
                    else:
                        end_time = "N/A"
                        duration = "N/A"
                else:
                    start_time = "N/A"
                    end_time = "N/A"
                    duration = "N/A"
                if not (old_resource == step_id):
                    typer.secho("\n  %s: %s" % (step_type, step_id), fg="blue")
                    old_resource = step_id
                typer.echo(
                    f"  {step.operation:20s}{step.state:20s}{str(duration):10s}{str(start_time):30s}{str(end_time):30s}"
                )
        else:
            typer.secho("\n  No changes found.", fg="red")


@app.command("rerun")
@utils.exit_on_error
def rerun(
    push_id: str = typer.Argument(..., help="Change ID."),
    project: str = typer.Option(False, help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Show full JSON representation."),
):
    """Rerun a previous change."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    push = c.changes.rerun(push_id)
    if json:
        console = Console()
        console.print(push.to_dict())
    else:
        typer.secho("Operations for %s:" % push.id, fg="magenta")
        if len(push.plan) > 0:
            steps = sorted(
                push.plan,
                key=lambda x: int(x.id),
                reverse=False,
            )
            typer.secho(
                f"\n  {'Operation':20s}{'State':20s}{'Duration(s)':10s}{'Start Time':30s}{'End Time':30s}",
                fg="magenta",
            )
            old_resource = ""
            featuresets = []
            models = []
            for step in steps:
                if step.resource_name.split("/")[2] == "models":
                    models.append(step)
                else:
                    featuresets.append(step)
            for step in featuresets + models:
                step_id = step.resource_name.split("/")[-1]
                if step.resource_name.split("/")[2] == "models":
                    step_type = "Model"
                else:
                    step_type = "Feature Set"
                start_time = step.start_time
                end_time = step.finish_time
                if start_time:
                    start_time = step.start_time.replace(microsecond=0)
                    if end_time:
                        end_time = end_time.replace(microsecond=0)
                        duration = (end_time - start_time).seconds
                    else:
                        end_time = "N/A"
                        duration = "N/A"
                else:
                    start_time = "N/A"
                    end_time = "N/A"
                    duration = "N/A"
                if not (old_resource == step_id):
                    typer.secho("\n  %s: %s" % (step_type, step_id), fg="blue")
                    old_resource = step_id
                typer.echo(
                    f"  {step.operation:20s}{step.state:20s}{str(duration):10s}{str(start_time):30s}{str(end_time):30s}"
                )
        else:
            typer.secho("\n  No changes found.", fg="red")


@app.command("cancel")
@utils.exit_on_error
def cancel(
    push_id: str = typer.Argument(..., help="Change ID."),
    project: str = typer.Option(None, help="Project ID."),
):
    """Cancel change."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    c.changes.cancel(push_id)
    typer.echo("Change %s successfully cancelled." % push_id)
