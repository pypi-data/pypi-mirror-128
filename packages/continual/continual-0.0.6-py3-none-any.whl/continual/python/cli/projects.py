#!/usr/bin/env python3

import typer
import os
import yaml

from continual.python.cli import utils
from continual.python.sdk.featurestore_config import FeaturestoreConfig
from continual import Client

from rich.console import Console
from typing import List
from pathlib import Path
from enum import Enum

app = typer.Typer(help="Manage projects.")


class SchemaType(str, Enum):
    FeatureSet = "FeatureSet"
    Model = "Model"


def format_project_data(p, zipped=False):
    create_time = p.create_time.replace(microsecond=0)
    update_time = p.update_time.replace(microsecond=0)
    org = p.organization.split("/")[-1]
    fs_type = p.data_store.type
    c = Client()
    project_id = p.id
    current_project = c.config.project
    if current_project and current_project.startswith(p.name):
        project_id = f"{project_id} (active)"
    data = [
        project_id,
        p.display_name,
        org,
        fs_type,
        p.summary.feature_set_count,
        p.summary.feature_count,
        p.summary.model_count,
        p.summary.model_version_count,
        p.summary.prediction_count,
        create_time,
        # update_time,
    ]
    headers = [
        "ID",
        "Display Name",
        "Organization",
        "Data Warehouse",
        "Feature Sets",
        "Features",
        "Models",
        "Model Versions",
        "Predictions",
        "Created",
        # "Updated",
    ]

    if zipped:
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        list(n=30, filters=[], style=None)


@app.command("list")
@utils.exit_on_error
def list(
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List projects."""
    c = Client()
    data = []
    headers = []
    filter_snippet = ""
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters)
    for p in c.projects.list(n, filters=filters):
        (p_data, headers) = format_project_data(p)
        data.append(p_data)
    typer.secho("Found %s projects%s:" % (len(data), filter_snippet), fg="blue")
    if style is None:
        style = c.config.style
    style = utils.get_style(style)
    utils.print_table(data, headers, style=style)


@app.command("get")
@utils.exit_on_error
def get(
    project_id: str = typer.Argument(..., help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Print full JSON representation."),
):
    """Get project details."""
    c = Client(project=project_id)
    project = c.projects.get(project_id)
    if json:
        console = Console()
        console.print(project.to_dict())
    else:
        data = format_project_data(project, zipped=True)
        typer.secho("\nRetrieving project %s: \n" % (project_id), fg="blue")
        utils.print_info(data)


@app.command("create")
@utils.exit_on_error
def create(
    project: str = typer.Argument(..., help="Name of project."),
    org: str = typer.Option(None, help="Name of organization.", show_default=False),
    feature_store: str = typer.Option(
        None, help="Feature store config name.", show_default=False
    ),
):
    """Create project."""
    if feature_store is not None:
        fs_config = FeaturestoreConfig()
        feature_store_dict = dict(fs_config._cp[feature_store])
        if feature_store_dict is None:
            typer.echo(
                "Unable to look up feature store configuration for %s. Exiting..."
                % feature_store
            )
            raise typer.Exit(code=1)
    else:
        feature_store = (
            "continual"  # no feature store specified, so use embedded postgres
        )
        feature_store_dict = None
    if (feature_store_dict is not None) or (feature_store == "continual"):
        proj = utils.get_or_create_project(project, org, feature_store_dict)
        typer.secho(
            "Successfully created project %s with feature store %s."
            % (proj.id, feature_store),
            fg="green",
        )
    else:
        typer.secho(
            "Unable to build project with feature store %s." % feature_store, fg="red"
        )


@app.command("delete")
@utils.exit_on_error
def delete(
    project_id: str = typer.Argument(..., help="Project ID."),
):
    """Delete project."""
    c = Client(project=project_id)
    project = c.projects.get(project_id)
    project.delete()
    typer.secho("Successfully deleted project %s." % project_id, fg="green")


@app.command("update")
@utils.exit_on_error
def update(
    project_id: str = typer.Argument(..., help="Project ID."),
    new_name: str = typer.Option(..., help="New project name"),
):
    """Update project name."""
    c = Client(project=project_id)
    project = c.projects.get(project_id)
    project.update(new_name)
    typer.secho("Successfully updated project %s." % project_id, fg="green")


@app.command("seed")
@utils.exit_on_error
def seed(
    paths: List[Path] = typer.Argument(
        None, exists=True, dir_okay=True, help="Path to CSV file(s)."
    ),
    project: str = typer.Option(None, help="Project ID."),
):
    """Upload data to data warehouse.

    Uploads all given CSV files to the project and create tables loaded with data.
    The PATHS can be a list of CSV files to be uploaded.
    """

    client = Client(project=project)
    if client.config.project is None:
        typer.secho(
            "No project set.  Use continual set-project or --project to set a project.",
            fg="red",
        )
        raise typer.Exit(code=1)
    project_id = client.config.project.split("/")[-1]
    project = client.projects.get(project_id)

    # typer path type is PosixPath, which our SDK doesn't expect. Only works w/ strings or list of strings.

    if len(paths) > 0:
        paths = [str(path) for path in paths]
    else:  # If no path provided, try to use a folder in cwd that is the project name. Used mainly for
        typer.secho(
            "No path provided. Attempting to use local folder with same name as the default project: %s"
            % project_id,
            fg="blue",
        )
        paths = [os.path.join(os.getcwd(), project_id)]

    for path in paths:
        try:
            (schema, table) = project.seed(path)
            typer.secho(
                "Successfully seeded file %s to %s.%s" % (path, schema, table),
                fg="green",
            )
        except:
            typer.secho("Failed to seed file %s." % path, fg="red")
            continue


@app.command("infer-schema")
@utils.exit_on_error
def infer_schema(
    schema_type: SchemaType = typer.Argument(..., help="Schema type to create."),
    project: str = typer.Option(None, help="Project ID."),
    target: str = typer.Option(None, help="Target column to predict (models only)."),
    entity: str = typer.Option(None, help="Entity to associate resource with."),
    table: str = typer.Option(None, help="Table name."),
    query: str = typer.Option(None, help="SQL query."),
    file: str = typer.Option(None, hidden=True, help="File name."),
    path: Path = typer.Option(None, help="Path to save schema."),
):
    """
    Infers schema from a table or SQL query.
    """
    c = Client(project=project)
    schema = c.infer_schema(
        project=project, table=table, query=query, file=file, type=schema_type.value
    )

    if table is not None:
        name = table.replace(".", "_")
    elif query is not None:
        name = "SQL_QUERY_INFERRED"
    else:
        name = file.split("/")[-1].split(".")[0]

    id_col = False
    columns = schema.to_dict().get("columns")
    for col in columns:
        col_name = col.get("name").lower()
        del col["dtype"]
        if col_name == "id":
            id_col = True
            col["type"] = "INDEX"
        elif col_name == "ts":
            col["type"] = "TIME_INDEX"

    new_schema = {
        "type": schema_type.value,
        "name": name,
        "description": "Inferred via Continual CLI.",
        "owners": [c.config.email],
        "columns": columns,
        "query": schema.query,
    }
    if entity:
        new_schema["entity"] = entity

    if schema_type == SchemaType.Model:
        new_schema["target"] = target

    if not id_col:
        typer.secho(
            "No id column found. You will need to declare a column with type 'Index' before attemping a push.",
            fg="yellow",
        )

    yaml_text = yaml.dump(new_schema, sort_keys=False)

    if path is None:
        typer.secho("Successfully inferred schema for %s: \n" % table, fg="green")
        print(yaml_text)
    else:
        path = str(path)
        if (path[-4:] != ".yml") and (path[-5:] != ".yaml"):
            path = "%s/%s.yaml" % (path, name)
        with open(path, "w+") as f:
            f.write(yaml_text)
        typer.secho(
            "Successfully inferred schema for %s and saved to file %s." % (table, path),
            fg="green",
        )

        typer.secho(
            "You may can push this file into continual via 'continual push %s`." % path,
            fg="blue",
        )
