import typer
import logging
import subprocess
import os
import pandas as pd

from continual.python.sdk.exceptions import BaseException
from continual.rpc.management.v1 import types
from continual import continual as c

from enum import Enum
from functools import wraps
from git import Repo

from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.layout import Layout

logger = logging.getLogger("continual.cli.utils")

continual_style_green = Style(color="rgb(157,209,186)")
continual_style_blue = Style(color="rgb(96,238,252)")
continual_style_purple = Style(color="rgb(63,47,159)")
continual_style_dark_blue = Style(color="rgb(5,27,71)")
continual_style_black = Style(color="rgb(0,0,0)")
continual_style_white = Style(color="rgb(255,255,255)")


class ContinualStyle(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    BLUE = "BLUE"
    GREEN = "GREEN"
    PURPLE = "PURPLE"
    DARK_BLUE = "DARK_BLUE"


def get_style(continual_style):
    if not isinstance(continual_style, str):
        continual_style = continual_style.value
    if continual_style.upper() == "WHITE":
        return continual_style_white
    elif continual_style.upper() == "BLACK":
        return continual_style_black
    elif continual_style.upper() == "BLUE":
        return continual_style_blue
    elif continual_style.upper() == "GREEN":
        return continual_style_green
    elif continual_style.upper() == "PURPLE":
        return continual_style_purple
    elif continual_style.upper() == "DARK_BLUE":
        return continual_style_dark_blue


# takes project and org display names
# returns project object
# creates project if it doesn't exist
def get_or_create_project(project_name, org_name, data_store, project_id=None):
    try:
        if not project_id:
            project_id = "projects/%s" % project_name
            project = get_project_from_display_name(project_name)
        else:
            project = c.projects.get(project_id)
    except Exception:
        org1 = get_or_create_org(org_name)
        ds = types.DataStore(**data_store)
        project = c.projects.create(
            display_name=project_name,
            project_id=project_id,
            data_store=ds,
            organization=org1.name,
        )
    return project


# takes environment display names
# returns environment object
# creates environment if it doesn't exist
def get_or_create_environment(display_name, data_store, environment_name=None):
    try:
        if not environment_name:
            env = get_environment_from_display_name(display_name)
        else:
            env = c.projects.get(environment_name)
    except Exception:
        env = c.environments.create(
            display_name=display_name,
            data_store=data_store,
        )
    return env


# returns proj obj of given display_name
# returns first found, if multiple exist w/ same name
# this exists because you can't re-use a project id once assigned,
### so the previous function may change your project id from projects/<project_name>
### to projects/<project_name>-#. This can be unexpected and lead to errors when trying
### to access the project downstream
# essentially, this imposes uniqueness of the display names
def get_project_from_display_name(project_name):
    try:
        projs = c.projects.list()
        proj = [x for x in projs if x.display_name == project_name][0]
        return proj
    except:
        raise


def get_environment_from_display_name(project_name, environment_name):
    try:
        envs = c.environments.list()
        env = [x for x in envs if x.display_name == environment_name][0]
        return env
    except:
        raise


# takes org display name or optionally id
# returns org object
# creates org if display_name doesn't exist
def get_or_create_org(display_name, id=None):
    try:
        if not id:
            org = get_org_from_display_name(display_name)
        else:
            org = c.organizations.get(id)
    except Exception:
        org = c.organizations.create(display_name)
    return org


# quick fix for dev-464
# returns org id of given display_name
# returns first found, if multiple exist w/ same name
def get_org_from_display_name(org_name):
    try:
        orgs = c.organizations.list()
        org = [x for x in orgs if x.display_name == org_name][0]
        return org
    except:
        raise


def get_project(project):
    if (project is None) or (project == ""):
        project = get_default_project()
    else:
        if "@" in project:
            project = project.split("@")[0]
    return project


def get_default_project():
    proj = c.config.project
    if proj is None or proj == "":
        typer.secho(
            "No project set.  Use continual config set-project or --project to set a project.",
            fg="red",
        )
        exit(1)
    return proj.split("/")[-1]


def get_environment(project, environment):
    if environment is None or environment == "":
        if project is not None and "@" in project:
            environment = project.split("@")[1]
        else:
            environment = get_default_environment()
    return environment
    ##get environment
    # first priority is to use environment variable if it's passed
    # second, try to get env out of project string via project@env (either passed or via default project)
    # third, get env from git branch
    # 4th, use prod (default)


def get_default_environment():
    env = c.config.environment
    if env is None or env == "":
        repo = Repo(search_parent_directories=True)
        env = repo.active_branch.name
        if (env.lower() == "master") or (env.lower() == "main"):
            env = "prod"
    if env is None or env == "":
        env = "prod"
    return env


def get_environment_name(project, environment) -> str:
    project = get_project(project)
    environment = get_environment(project, environment)
    if not project.startswith("projects/"):
        project = f"projects/{project}"
    return f"{project}@{environment}"


def get_endpoint():
    endpoint = c.config.endpoint
    # Assume development with SSH port forwarding.
    if endpoint == "http://localhost":
        endpoint = "http://localhost:9999"
    else:
        endpoint = "https://cloud.continual.ai"
    return endpoint


def print_table(
    data,
    headers,
    print=True,
    style=continual_style_green,
    row_styles=["default", "dim"],
    title=None,
    caption=None,
):
    table = Table(
        expand=True, style=style, row_styles=row_styles, title=title, caption=caption
    )
    for x in headers:
        table.add_column(x, overflow="fold")
    if isinstance(data, pd.DataFrame):
        for i, row in data.iterrows():
            table.add_row(*[str(x) for x in row])
    else:
        for row in data:
            table.add_row(*[str(x) for x in row])
    if print:
        console = Console()
        console.print(table)
    return table


def print_info(
    data, show_index=False, headers="", tablefmt="plain", style=continual_style_blue
):
    # typer.echo(tabulate(data, headers=headers, showindex=show_index, tablefmt=tablefmt))
    table = Table(style=style).grid(expand=True)
    for x in headers:
        table.add_column(x, overflow="fold")
    if isinstance(data, pd.DataFrame):
        for i, row in data.iterrows():
            table.add_row(*[str(x) for x in row])
    else:
        for row in data:
            table.add_row(*[str(x) for x in row])
    console = Console()
    console.print(table)


def process_template(template, layout, split_direction):
    children = []
    next_split = {}
    for obj in template:
        data = obj.get("data", None)
        split = obj.get("children", None)
        if data is not None:
            children.append(
                Layout(
                    obj.get("data"),
                    name=obj.get("name"),
                    ratio=obj.get("ratio", 1),
                    minimum_size=5,
                )
            )
        elif split is not None:
            name = obj.get("name")
            direction = obj.get("direction", "horizontal")
            children.append(
                Layout(name=name, ratio=obj.get("ratio", 1), minimum_size=5)
            )
            next_split["%s:%s" % (name, direction)] = split

    if len(children) > 0:
        layout.split(direction=split_direction, *children)

    if len(next_split) > 0:
        for index in next_split:
            parts = index.split(":")
            name = parts[0]
            direction = parts[1]
            process_template(next_split[index], layout[name], direction)


# template is a list of dict. Each dict defines a split or renderable
# renderable: [{"name":"Top", "ratio": 1, data:<renderable>},
# split: {"name":"Bottom", "ratio": 1, "direction": "horizontal", children: [<next_template]}]
#
def build_dashboard(template, direction="horizontal"):
    layout = Layout()
    process_template(template, layout, direction)
    return layout


def execute_cmd(cmd, print_it=True):
    popen = subprocess.Popen(
        [cmd], stdout=subprocess.PIPE, universal_newlines=True, shell=True
    )
    output = popen.stdout.read()
    exit_code = popen.wait()
    if print_it:
        print(output)
        # print("exit code: %s" %exit_code)
    return (output, exit_code)


def split_large_csv(csv, output, max_chunk_size=209715200):
    if not os.path.exists(output):
        os.mkdir(output)
    execute_cmd(
        "split -C %s -d %s %s/%s" % (max_chunk_size, csv, output, csv.split("/")[-1])
    )
    return [file.path for file in os.scandir(output) if file.is_file()]


# for progress bar


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def exit_with_error(e):
    """Print error and exit.

    Args:
        e: An exception to print.
    """
    if isinstance(e, BaseException):
        typer.secho("Error: " + str(e.message), fg="red")
        if isinstance(e.details, dict) and len(e.details) > 0:
            typer.secho("Details:", fg="red")
            for key, value in e.details.items():
                typer.secho(f"  {key}: {value}", fg="red")
    else:
        typer.secho("Error: " + str(e), fg="red")
    exit(1)


def exit_on_error(func):
    """Decorator that prints and exits on exceptions.

    Args:
        func: Function to wrap.
    Returns:
        A function that prints error and exit(1) on any exception.
    """

    @wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.debug("an error occured in command", exc_info=e)
            exit_with_error(e)

    return function_wrapper


# class OrderGroup(click.Group):
#     """OrderGroup ensures command groups maintain their order."""

#     def __init__(self, name=None, commands=None, **attrs):
#         if commands is None:
#             commands = OrderedDict()
#         elif not isinstance(commands, OrderedDict):
#             commands = OrderedDict(commands)
#         click.Group.__init__(self, name=name, commands=commands, **attrs)

#     def list_commands(self, ctx):
#         return self.commands.keys()
