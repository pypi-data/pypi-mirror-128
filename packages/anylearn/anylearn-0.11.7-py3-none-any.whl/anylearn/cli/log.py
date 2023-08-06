import time
import os

import click

from anylearn.cli.utils import (
    check_config,
    check_connection,
    cmd_error, cmd_info,
    cmd_success,
    get_cmd_command,
)
from anylearn.interfaces.train_task import TrainTask


@click.group("log")
def commands():
    """
    Download remote task log of training, evaluation or serving.
    """
    pass


@commands.command()
@check_config()
@check_connection()
@get_cmd_command()
@click.argument('task_id')
@click.option(
    '-t', '--type',
    type=click.Choice(["all", "last", "custom"]),
    default="last",
    help="""
    All log or last log or custom log, default "last".
    """
)
@click.option(
    '-s', '--save-path',
    help="""
    Save path of task log (absolute path).
    Needed just type is all, else will be ignored.
    """
)
@click.option(
    '-d', '--direction',
    type=click.Choice(["init", "back"]),
    default="init",
    help="Log query direction, default \"init\". Needed just type is custom"
)
@click.option(
    '-l', '--limit',
    default=100,
    help="Maximum number of logs, default 100. Needed just type is custom"
)
@click.option(
    '-o', '--offset',
    default=0,
    help="Log query offset, default 0. Needed just type is custom"
)
@click.option(
    '-oi', '--offset-index',
    default=-1,
    help="""
    The offset index of log query is used together
    with the offset as the paging benchmark,
    default -1.
    Needed just type is custom
    """
)
@click.option(
    '--debug',
    is_flag=True,
    default=False,
    help="""
    Display more comprehensive debug information,
    default false.
    Needed just type is custom
    """
)
def training(task_id: str,
             type: str ,
             save_path: str,
             direction: str,
             limit: int,
             offset: int,
             offset_index: int,
             debug: bool,
             ):
    """
    Get training task's log.
    """
    if type == "all":
        if not save_path:
            save_path = click.prompt('Please enter save_path', type=str)
        if not os.path.exists(save_path):
            cmd_error(msg=f"保存路径{save_path}不存在")
            return
        log_file_name = f"train_log_{task_id}_{int(time.time())}.txt"
        try:
            train_task = TrainTask(id=task_id)
            logs = train_task.get_full_log()
            with open(f"{save_path}/{log_file_name}", 'w') as f:
                [f.write(f"{logs[i]}\r") for i in range(len(logs))]
        except Exception as e:
            cmd_error(msg=f"{e}")
            os.remove(f"{save_path}/{log_file_name}")
            return
        cmd_success(msg=f"{save_path}/{log_file_name}")
    elif type == "last":
        try:
            train_task = TrainTask(id=task_id)
            logs = train_task.get_last_log()
            logs = "\r\n".join(logs)
            cmd_info(msg=logs)
        except Exception as e:
            cmd_error(msg=f"{e}")
    else:
        try:
            train_task = TrainTask(id=task_id)
            logs = train_task.get_log(direction=direction,
                                      limit=limit,
                                      offset=offset,
                                      offset_index=offset_index,
                                      debug=debug,
                                      )
            logs = "\r\n".join(logs)
            cmd_info(msg=logs)
        except Exception as e:
            cmd_error(msg=f"{e}")

@commands.command()
@get_cmd_command()
def evaluation():
    """
    Get evaluation task's log.
    """
    pass


@commands.command()
@get_cmd_command()
def serving():
    """
    Get serving task's log.
    """
    pass
