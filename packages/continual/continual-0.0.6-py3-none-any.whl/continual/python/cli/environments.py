#!/usr/bin/env python3

import typer
import os
import yaml

from continual.python.cli import utils
from continual import Client

from rich.console import Console
from typing import List
from pathlib import Path
from enum import Enum

app = typer.Typer(help="Manage environments.")


class SchemaType(str, Enum):
    FeatureSet = "FeatureSet"
    Model = "Model"


def format_environment_data(p, zipped=False):
    create_time = p.create_time.replace(microsecond=0)
    update_time = p.update_time.replace(microsecond=0)
    fs_type = p.data_store.type
    db_schema = ""
    if fs_type == "snowflake":
        db_schema = p.data_store.snowflake.db_schema
    elif fs_type == "redshift":
        db_schema = p.data_store.redshift.db_schema
    elif fs_type == "big_query":
        db_schema = p.data_store.big_query.dataset
    elif fs_type == "continual" or fs_type == "postgres":
        db_schema = p.data_store.postgres.db_schema

    c = Client()

    environment_id = p.id
    current_project = utils.get_project(c.config.project)
    current_environment = c.config.environment

    if (
        "@" not in environment_id
        and current_project.endswith(environment_id)
        and (current_environment in ("prod", "production") or not current_environment)
    ):
        environment_id = f"{environment_id} (active)"
    elif p.name == utils.get_environment_name(current_project, current_environment):
        environment_id = f"{environment_id} (active)"

    data = [
        environment_id,
        fs_type,
        db_schema,
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
        "Data Warehouse",
        "Database Schema",
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
    """List environments."""
    c = Client()
    data = []
    headers = []
    filter_snippet = ""
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters)
    for p in c.environments.list(n, filters=filters):
        (p_data, headers) = format_environment_data(p)
        data.append(p_data)
    typer.secho("Found %s environments%s:" % (len(data), filter_snippet), fg="blue")
    if style is None:
        style = c.config.style
    style = utils.get_style(style)
    utils.print_table(data, headers, style=style)


@app.command("get")
@utils.exit_on_error
def get(
    environment_id: str = typer.Argument(..., help="Environment ID."),
    project: str = typer.Option("", help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Print full JSON representation."),
):
    """Get environment details."""
    if project == "" and "@" in environment_id:
        project = environment_id.split("@")[0]
        environment_id = environment_id.split("@")[-1]
    project = utils.get_project(project)
    environment_id = utils.get_environment(project, environment_id)

    c = Client(project=utils.get_environment_name(project, environment_id))
    environment = c.environments.get(environment_id)
    if json:
        console = Console()
        console.print(environment.to_dict())
    else:
        data = format_environment_data(environment, zipped=True)
        typer.secho("\nRetrieving environment %s: \n" % (environment_id), fg="blue")
        utils.print_info(data)


@app.command("create")
@utils.exit_on_error
def create(
    environment: str = typer.Argument(..., help="Environment ID."),
    project: str = typer.Option("", help="Project ID."),
    source: str = typer.Option(
        "",
        "--from",
        help="Fully-qualified Model, Feature Set, Project, or Environment name from which to create this Environment.",
    ),
):
    """Create environment."""
    project = utils.get_project(project)
    environment = utils.get_environment(project, environment)

    c = Client(project=f"projects/{project}")
    env = c.environments.create(id=environment, source=source)
    typer.secho("Successfully created environment %s." % env.name, fg="green")


@app.command("delete")
@utils.exit_on_error
def delete(
    environment_id: str = typer.Argument(..., help="Environment ID."),
    project: str = typer.Option("", help="Project ID."),
):
    """Delete environment."""
    if project == "" and "@" in environment_id:
        project = environment_id.split("@")[0]
        environment_id = environment_id.split("@")[-1]
    project = utils.get_project(project)
    environment_id = utils.get_environment(project, environment_id)

    c = Client(project=utils.get_environment_name(project, environment_id))
    environment = c.environments.get(environment_id)
    environment.delete()
    if c.config.environment == environment_id:
        typer.secho(
            "Since (%s) was the active environment, the active environment was switched to production."
            % environment_id,
            fg="green",
        )
        c.config.set_environment("production")
    typer.secho("Successfully deleted environment %s." % environment_id, fg="green")


@app.command("update")
@utils.exit_on_error
def update(
    environment_id: str = typer.Argument(..., help="environment ID."),
    project: str = typer.Option("", help="Project ID."),
    new_name: str = typer.Option(..., help="New environment name"),
):
    """Update environment name."""
    c = Client()
    environment = c.environments.get(environment_id)
    environment.update(new_name)
    typer.secho("Successfully updated environment %s." % environment_id, fg="green")


@app.command("seed")
@utils.exit_on_error
def seed(
    paths: List[Path] = typer.Argument(
        None, exists=True, dir_okay=True, help="Path to CSV file(s)."
    ),
    environment: str = typer.Option(None, help="environment ID."),
):
    """Upload data to data warehouse.

    Uploads all given CSV files to the environment and create tables loaded with data.
    The PATHS can be a list of CSV files to be uploaded.
    """

    client = Client()
    if client.config.project is None:
        typer.secho(
            "No environment set.  Use continual set-project or --project to set a environment.",
            fg="red",
        )
        raise typer.Exit(code=1)
    environment_id = client.config.project.split("/")[-1]
    environment = client.environments.get(environment_id)

    # typer path type is PosixPath, which our SDK doesn't expect. Only works w/ strings or list of strings.

    if len(paths) > 0:
        paths = [str(path) for path in paths]
    else:  # If no path provided, try to use a folder in cwd that is the environment name. Used mainly for
        typer.secho(
            "No path provided. Attempting to use local folder with same name as the default environment: %s"
            % environment_id,
            fg="blue",
        )
        paths = [os.path.join(os.getcwd(), environment_id)]

    for path in paths:
        try:
            (schema, table) = environment.seed(path)
            typer.secho(
                "Successfully seeded file %s to %s.%s.%s"
                % (path, environment.data_store.database, schema, table),
                fg="green",
            )
        except:
            typer.secho("Failed to seed file %s." % path, fg="red")
            continue


@app.command("infer-schema")
@utils.exit_on_error
def infer_schema(
    schema_type: SchemaType = typer.Argument(..., help="Schema type to create."),
    environment: str = typer.Option(None, help="environment ID."),
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
    c = Client(environment=environment)
    schema = c.infer_schema(
        environment=environment,
        table=table,
        query=query,
        file=file,
        type=schema_type.value,
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
