import typer

from continual.python.cli import utils
from continual import Client

from rich.console import Console
from typing import List

app = typer.Typer(help="Manage model versions.")


def format_model_version_data(mv, zipped=False, all_projects=False):
    try:
        experiment = mv.experiment.id
    except:
        experiment = "N/A"
    if mv.promoted:
        last_promoted = Client().promotions.get(mv.promotion).promoted_time
        if last_promoted:
            last_promoted = last_promoted.replace(microsecond=0)
    else:
        last_promoted = "N/A"
    update_time = mv.update_time.replace(microsecond=0)
    create_time = mv.create_time.replace(microsecond=0)
    if zipped:
        data = [
            mv.id,
            mv.name,
            mv.state.value,
            experiment,
            mv.performance_metric,
            mv.performance_metric_val,
            mv.promoted,
            last_promoted,
            create_time,
            update_time,
        ]
        headers = [
            "ID",
            "Name",
            "State",
            "Winning Experiment",
            "Metric",
            "Metric Value",
            "Promoted",
            "Promotion",
            "Promoted Time",
            "Created",
            "Updated",
        ]
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        data = [
            mv.id,
            mv.state.value,
            mv.name.split("/")[3],
            experiment,
            mv.performance_metric,
            mv.performance_metric_val,
            mv.promoted,
            last_promoted,
            create_time,
            # update_time,
        ]
        headers = [
            "ID",
            "State",
            "Model",
            "Winning Experiment",
            "Metric",
            "Metric Value",
            "Promoted",
            "Promoted Time",
            "Created",
            # "Updated",
        ]
        if all_projects:
            data.insert(0, mv.parent.split("/")[1])
            headers.insert(0, "Project")
        return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        list(model=None, project=None, n=30, filters=[], all_projects=False, style=None)


@app.command("list")
@utils.exit_on_error
def list(
    model: str = typer.Option(None, help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    all_projects: bool = typer.Option(False, "--all", "-a", help="Show all projects."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List model versions.

    Filters can include:
        --state (i.e. state:FAILED)
    """
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    model_snippet = ""
    filter_snippet = ""
    project_snippet = "project %s" % project
    if model is not None:
        c = c.models.get(model)
        model_snippet = "for model %s " % model
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters)
    if all_projects:
        project_snippet = "all accessible projects"
    data = []
    headers = []
    for mv in c.model_versions.list(n, filters=filters, all_projects=all_projects):
        (mv_data, headers) = format_model_version_data(mv, all_projects=all_projects)
        data.append(mv_data)
    typer.secho(
        "\nFound %s model versions %sin  %s%s: "
        % (len(data), model_snippet, project_snippet, filter_snippet),
        fg="blue",
    )
    if style is None:
        style = c.config.style
    style = utils.get_style(style)
    utils.print_table(data, headers, style=style)


@app.command("get")
@utils.exit_on_error
def get(
    model_version: str = typer.Argument(..., help="Model version ID."),
    project: str = typer.Option(None, help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Show full JSON representation."),
):
    """Get model version information."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    mv = c.model_versions.get(model_version)
    if json:
        console = Console()
        console.print(mv.to_dict())
    else:
        data = format_model_version_data(mv, zipped=True)
        typer.secho("\nRetrieving model version %s: \n" % (model_version), fg="blue")
        utils.print_info(data)


@app.command("promote")
@utils.exit_on_error
def promote(
    model_version: str = typer.Argument(..., help="Model version ID."),
    project: str = typer.Option(None, help="Project ID."),
    model: str = typer.Option(None, help="Model ID."),
    wait: bool = typer.Option(False, "--wait", help="Wait for promotion to finish."),
    debug: bool = typer.Option(
        False, "--debug", help="Print full name of model version."
    ),
):
    """Promotes a model version."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    mv = c.model_versions.get(model_version)
    d = mv.promote()
    if wait:
        d.wait()
        typer.secho(
            "Successfully promoted %s for model version %s." % (d.id, mv.id),
            fg="green",
        )
    else:
        typer.secho(
            "Started promotion %s for model version %s." % (d.id, mv.id),
            fg="green",
        )
    endpoint = utils.get_endpoint()
    model = mv.parent.split("/")[-1]
    typer.secho("You can review the promotion at: ", fg="blue")
    typer.secho(
        f"  {endpoint}/projects/{project}/model/{model}/promotions/\n", fg="blue"
    )

    if debug:
        typer.echo("DEBUG: Full name = %s." % d.name)


@app.command("cancel")
@utils.exit_on_error
def cancel(
    model_version: str = typer.Argument(..., help="Model version ID."),
    project: str = typer.Option(None, help="Project ID."),
):
    """Cancel a model version that is currently training."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    mv = c.model_versions.get(model_version)
    mv.cancel()
    typer.secho(
        "Successfully cancelled training for model version %s." % (mv.id), fg="green"
    )
