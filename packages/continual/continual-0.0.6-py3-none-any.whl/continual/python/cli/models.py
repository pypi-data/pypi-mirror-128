import typer

from continual.python.cli import utils
from continual import Client
from continual.rpc.management.v1.types import ModelVersionState

from rich.console import Console
from typing import List

app = typer.Typer(help="Manage models.")


def format_model_data(m, zipped=False, all_projects=False):
    create_time = m.create_time.replace(microsecond=0)
    update_time = m.update_time.replace(microsecond=0)
    num_bpj = len(m.batch_prediction_jobs.list(1000))
    num_d = len(m.promotions.list(1000))
    num_mv = len(m.model_versions.list(1000))
    latest_version = m.latest_model_version.split("/")[-1]
    if latest_version:
        mv = m.model_versions.get(latest_version)
        mv_state = mv.state.value
        try:
            mv_type = mv.experiment.type
        except:
            mv_type = "N/A"
        # would like to get winning experiment metric & algo, but currently not coming through.
    else:
        mv_state = "N/A"
        mv_type = "N/A"
    current_version = m.current_version.split("/")[-1]
    entity = m.schema.entity
    project = m.parent.split("/")[-1]
    if zipped:
        data = [
            m.id,
            m.name,
            m.state,
            project,
            entity,
            latest_version,
            mv_state,
            mv_type,
            m.latest_batch_prediction,
            current_version,
            num_mv,
            num_d,
            num_bpj,
            create_time,
            update_time,
        ]
        headers = [
            "ID",
            "Name",
            "State",
            "Project",
            "Entity",
            "Latest Model Version",
            "Latest Model Version State",
            "Latest Model Version Type",
            "Latest Batch Prediction",
            "Current Promotion",
            "Model Versions",
            "Promotions",
            "Batch Predictions",
            "Created",
            "Updated",
        ]
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        data = [
            m.id,
            entity,
            m.state,
            latest_version,
            mv_state,
            mv_type,
            current_version,
            num_mv,
            num_d,
            num_bpj,
            create_time,
            # update_time,
        ]
        headers = [
            "ID",
            "Entity",
            "State",
            "Latest Model Version",
            "Model Version State",
            "Model Version Type",
            "Current Promotion",
            "Model Versions",
            "Promotions",
            "Batch Predictions",
            "Created",
            # "Updated",
        ]
        if all_projects:
            data.insert(0, m.parent.split("/")[1])
            headers.insert(0, "Project")
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
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    all_projects: bool = typer.Option(False, "--all", "-a", help="Show all projects."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List models.

    Filter can include:
        - state  (i.e. state:HEALTHY)
        - latest_mv_state (i.e. latest_mv_state:SUCCEEDED)
    """
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    else:
        c = c.projects.get(project)
    filter_snippet = ""
    project_snippet = "project %s" % project
    if all_projects:
        project_snippet = "all accessible projects"
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters)
    data = []
    headers = []
    for m in c.models.list(n, filters=filters, all_projects=all_projects):
        (m_data, headers) = format_model_data(m, all_projects=all_projects)
        data.append(m_data)
    typer.secho(
        "\nFound %s models in %s%s:" % (len(data), project_snippet, filter_snippet),
        fg="blue",
    )
    if style is None:
        style = c.config.style
    style = utils.get_style(style)
    utils.print_table(data, headers, style=style)


@app.command("get")
@utils.exit_on_error
def get(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    json: bool = typer.Option(False, help="Show full JSON representation."),
):
    """Get model details."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    m = c.models.get(model)
    if json:
        console = Console()
        console.print(m.to_dict())
    else:
        data = format_model_data(m, zipped=True)
        typer.secho("\nRetrieving model %s: \n" % (model), fg="blue")
        utils.print_info(data)


@app.command("train")
@utils.exit_on_error
def train(
    model: str = typer.Argument(None, help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    wait: bool = typer.Option(False, "--wait", help="Wait for training to finish."),
    debug: bool = typer.Option(False, "--debug", help="Print full name of model."),
    all: bool = typer.Option(False, "--all", help="Train all models."),
    state: ModelVersionState = typer.Option(
        None, help="Only train models with a certain state."
    ),
):
    """Train model."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()

    if all or state is not None:
        model_list = []
        if all == True:
            model_list = c.models.list_all().to_list()
        else:
            for m in c.models.list_all():
                try:
                    mv = c.model_versions.get(m.latest_model_version)
                    if mv.state.value == state:
                        model_list.append(m)
                except:
                    continue

        if len(model_list) > 0:
            endpoint = utils.get_endpoint()
            for model in model_list:
                try:
                    mv = model.train()
                    typer.secho(
                        "Started training model version %s for model %s."
                        % (mv.id, model.id),
                        fg="green",
                    )
                    typer.secho("You can access the model version at: ", fg="blue")
                    typer.secho(
                        f"  {endpoint}/projects/{project}/model/{model.id}/versions/{mv.id}\n",
                        fg="blue",
                    )
                except:
                    typer.secho("Failed to train model %s: " % model.id, fg="red")
                    continue
        else:
            typer.secho("No models found to train.")

    elif model is not None:
        m = c.models.get(model)
        mv = m.train()
        if wait:
            mv.wait()
            typer.secho(
                "Successfully trained model version %s for model %s." % (m.id, mv.id),
                fg="green",
            )
        else:
            typer.secho(
                "Started training model version %s for model %s." % (m.id, mv.id),
                fg="blue",
            )
        endpoint = utils.get_endpoint()
        typer.secho("You can access the model version at: ", fg="blue")
        typer.secho(
            f"  {endpoint}/projects/{project}/model/{m.id}/versions/{mv.id}\n",
            fg="blue",
        )
        if debug:
            typer.echo("DEBUG: Full name = %s." % mv.name)
    else:
        typer.secho(
            "Error: You must either provide model or one of --all or --state.", fg="red"
        )


@app.command("delete")
@utils.exit_on_error
def delete(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
):
    """Delete model."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    m = c.projects.get(project).models.get(model)
    m.delete()
    typer.echo("Successfully deleted model %s." % m.id)


@app.command("get-training-data")
@utils.exit_on_error
def get_training_data(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    path: str = typer.Option(..., help="Path to save training data CSV into."),
    num_records: int = typer.Option(None, help="Number of records to retrieve."),
    normalized: bool = typer.Option(
        False,
        "--normalized",
        help="Only return base feature set data (normalized).",
    ),
    fetch_metadata: bool = typer.Option(
        False, "--fetch-metadata", help="Fetch metadata fields "
    ),
    latest: bool = typer.Option(
        False, "--latest", help="Return latest record for each ID."
    ),
):
    """Get training data for model."""
    c = Client(project=project)
    if project is None:
        project = utils.get_default_project()
    m = c.models.get(model)
    (df, q) = m.get_training_data(
        n=num_records, normalized=normalized, metadata=fetch_metadata
    )  # , latest=latest)
    df.to_csv(path, index=False)
    typer.secho("Saved training data for model %s to %s." % (model, path), fg="blue")
    typer.echo(df.head())


@app.command("diff")
@utils.exit_on_error
def diff(
    right_yaml: str = typer.Option(None, help="YAML location."),
    right_project: str = typer.Option(None, help="Right project."),
    right_model: str = typer.Option(None, help="Right model."),
    left_yaml: str = typer.Option(None, help="YAML location."),
    left_project: str = typer.Option(None, help="Left project."),
    left_model: str = typer.Option(None, help="Left model"),
):
    """
    Diff model configuration.

    Can either provide a local YAML file or a model ID already
    contained in Continual. To use local YAML files, use the
    *_yaml options. Otherwise use *_project and *_model options.
    """
    c = Client()
    (right, left, diff_text) = c.models.diff(
        right_yaml, right_project, right_model, left_yaml, left_project, left_model
    )
    typer.secho("Diffing left=%s with right=%s" % (left, right), fg="blue")
    if len(diff_text) > 0:
        typer.secho(diff_text, fg="green")
    else:
        typer.secho("No changes found.", fg="green")
