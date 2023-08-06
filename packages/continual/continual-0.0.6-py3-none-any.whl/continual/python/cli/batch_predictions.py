import typer
import os

from continual.rpc.management.v1.types import BatchPredictionState
from continual.python.cli import utils
from continual import Client

from rich.console import Console
from enum import Enum
from pathlib import Path
from typing import List

app = typer.Typer(help="Manage batch predictions.")


class PredictionDestType(str, Enum):
    csv = "CSV"
    store = "STORE"


def format_batch_prediction_data(bpj, zipped=False, all_projects=False):
    name_parts = bpj.name.split("/")
    model = name_parts[3]
    model_version = name_parts[5]
    end_time = bpj.end_time
    start_time = bpj.start_time
    if start_time:
        start_time = start_time.replace(microsecond=0)
    if end_time and start_time:
        end_time = end_time.replace(microsecond=0)
        duration = (end_time - start_time).seconds
    else:
        end_time = "N/A"
        duration = "N/A"
    if zipped:
        data = [
            bpj.id,
            bpj.name,
            bpj.state.value,
            bpj.incremental,
            start_time,
            end_time,
            duration,
            bpj.prediction_count,
            bpj.source_type.value,
            bpj.dest_type.value,
        ]
        headers = [
            "ID",
            "Name",
            "State",
            "Incremental",
            "Start Time",
            "End Time",
            "Duration (s)",
            "Predictions",
            "Source Type",
            "Destination Type",
        ]
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        data = [
            bpj.id,
            bpj.state.value,
            bpj.incremental,
            model,
            model_version,
            start_time,
            end_time,
            duration,
            bpj.prediction_count,
        ]
        headers = [
            "ID",
            "State",
            "Incremental",
            "Model",
            "Model Version",
            "Start Time",
            "End Time",
            "Duration (s)",
            "Predictions",
        ]
        if all_projects:
            data.insert(0, bpj.parent.split("/")[1])
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
    """List batch prediction jobs in a project.

    Filters can include:
        - state  (i.e. state:FAILED)
        - incremental (i.e. incremental: True)
    """
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    data = []
    headers = []
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
    for bpj in c.batch_prediction_jobs.list(
        n, filters=filters, all_projects=all_projects
    ):
        (bpj_data, headers) = format_batch_prediction_data(
            bpj, all_projects=all_projects
        )
        data.append(bpj_data)
    typer.secho(
        "\nFound %s batch prediction jobs %sin %s%s:"
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
    batch_prediction: str = typer.Argument(..., help="Batch prediction ID"),
    project: str = typer.Option(None, help="Project ID"),
    json: bool = typer.Option(False, "--json", help="Show full JSON representation."),
):
    """Get batch prediction job details."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    bpj = c.batch_prediction_jobs.get(batch_prediction)
    if json:
        console = Console()
        console.print(bpj.to_dict())
    else:
        data = format_batch_prediction_data(bpj, zipped=True)
        typer.secho(
            "\nRetrieving batch prediction job %s:\n" % batch_prediction, fg="blue"
        )
        utils.print_info(data)


@app.command("run")
@utils.exit_on_error
def run(
    model: str = typer.Argument(None, help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    wait: bool = typer.Option(
        False, "--wait", help="Wait for batch prediction to finish."
    ),
    dest_type: PredictionDestType = typer.Option(
        PredictionDestType.store, help="Destination type.", hidden=True
    ),
    dest_path: Path = typer.Option(
        None, help="Destination path (CSV only)", hidden=True
    ),
    source_type: PredictionDestType = typer.Option(
        PredictionDestType.store, help="Source type.", hidden=True
    ),
    source_path: Path = typer.Option(None, help="Source path (CSV only).", hidden=True),
    debug: bool = typer.Option(False, help="Print full name of batch prediction job."),
    all: bool = typer.Option(False, "--all", help="Run all batch prediction jobs?"),
    state: BatchPredictionState = typer.Option(
        None, help="Only re-run batch predictions job with a certain state."
    ),
    prediction_model: str = typer.Option(None, help="Optional model type override"),
):
    """Runs a batch prediction job for a model.

    If --all or --state is used, it will bulk run all batch prediction jobs
    or all with the given state (i.e --state FAILED will rerun all failed batch prediction jobs)

    --all overrides --state if both are provided.
    """
    if all or state is not None:
        bulk_run(
            project=project,
            dest_type=dest_type,
            dest_path=dest_path,
            all=all,
            state=state,
        )
    elif model is not None:
        c = Client(project=project)
        if project is None:
            project = utils.get_default_project()
        m = c.models.get(model)
        bpj = m.batch_predict(
            source_type.value,
            source_path,
            dest_type.value,
            prediction_model=prediction_model,
        )
        if wait:
            bpj.wait()
            typer.secho(
                "Successfully ran batch prediction job %s for model %s"
                % (bpj.id, m.id),
                fg="green",
            )
            if dest_type == PredictionDestType.csv:
                try:
                    os.remove(dest_path)
                except:
                    pass
                bpj.download(dest_path)
                typer.secho(
                    "Downloaded predictions to file %s" % (dest_path), fg="green"
                )
        else:
            typer.secho(
                "Started running batch prediction job %s for model %s" % (bpj.id, m.id),
                fg="green",
            )
            endpoint = utils.get_endpoint()
            typer.secho("You can access the batch prediction job at: ")
            typer.secho(
                f"  {endpoint}/projects/{project}/models/-/batchPredictions", fg="blue"
            )

        if dest_type == PredictionDestType.store:
            p = c.projects.get(m.parent)
            db_type = p.data_store.type
            typer.secho("Predictions can be found in feature store at")
            typer.secho(
                "   %s: %s.model_%s_predictions" % (db_type, p.id, m.id), fg="blue"
            )
        if debug:
            typer.echo("DEBUG: Full name = %s" % bpj.name)
    else:
        typer.secho(
            "Error: You must either provide model or one of --all or --state.", fg="red"
        )


def bulk_run(
    project: str = typer.Option(None, help="Project ID"),
    dest_type: PredictionDestType = typer.Option(
        PredictionDestType.store, help="Destination type.", hidden=True
    ),
    dest_path: Path = typer.Option(
        None, help="Destination path (CSV only)", hidden=True
    ),
    all: bool = typer.Option(False, "--all", help="Run all batch prediction jobs?"),
    state: BatchPredictionState = typer.Option(
        None, help="Only re-run batch predictions job with a certain state."
    ),
):
    """Bulk run batch prediction jobs."""
    if not (all or state is not None):
        typer.secho(
            "Error: You must specify either --all or --state <state> to specify which batch prediction jobs to run. ",
            fg="red",
        )
        raise typer.Exit(code=0)
    else:
        c = Client(project=project)

        if project is None:
            project = utils.get_default_project()
        model_list = []

        if all == True:
            model_list = c.models.list_all().to_list()
        else:
            for m in c.models.list_all():
                try:
                    bpj = c.batch_prediction_jobs.get(m.latest_batch_prediction)
                    if bpj.state.value == state:
                        model_list.append(m)
                except:
                    continue

        if len(model_list) > 0:
            for model in model_list:
                try:
                    bpj = model.batch_predict(dest_type=dest_type)
                    typer.secho(
                        "Started running batch prediction job %s for model %s."
                        % (bpj.id, model.id),
                        fg="green",
                    )
                    if dest_type == PredictionDestType.store:
                        db = c.projects.get(model.parent).data_store.database
                        typer.secho("Predictions can be found in feature store at: ")
                        typer.secho(
                            "   %s.%s.model_%s_predictions" % (db, project, model.id),
                            fg="blue",
                        )
                except Exception as e:
                    typer.secho(
                        "Failed to start batch prediction for model %s: %s"
                        % (model.id, str(e)),
                        fg="red",
                    )
                    continue
            endpoint = utils.get_endpoint()
            typer.secho("You can access the batch prediction jobs at: ")
            typer.secho(
                f"  {endpoint}/projects/{project}/models/-/batchPredictions", fg="blue"
            )
        else:
            typer.secho("No batch prediction found to run.")


@app.command("cancel")
@utils.exit_on_error
def cancel(
    batch_prediction: str = typer.Argument(..., help="Batch prediction ID."),
    project: str = typer.Option(None, help="Project ID."),
    model: str = typer.Option(None, help="Model ID."),
):
    """Cancel a batch prediction that is currently running."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    bpj = c.batch_prediction_jobs.get(batch_prediction)
    bpj.cancel()
    typer.secho("Successfully cancelled batch prediction %s" % (bpj.id), fg="green")


@app.command("download")
@utils.exit_on_error
def download(
    batch_prediction: str = typer.Argument(..., help="Batch prediction ID."),
    project: str = typer.Option(None, help="Project ID."),
    path: Path = typer.Option(..., help="Local path to save redictions."),
):
    """Download a batch prediction job to CSV."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    bpj = c.batch_prediction_jobs.get(batch_prediction)
    bpj.download("%s/%s_predictions.csv" % (path, bpj.id))
    typer.secho(
        "Successfully downloaded batch prediction job %s to path %s/%s_predictions.csv."
        % (bpj.id, path, bpj.id),
        fg="green",
    )
