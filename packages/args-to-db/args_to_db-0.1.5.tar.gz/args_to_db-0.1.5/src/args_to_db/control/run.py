import concurrent.futures
import itertools
import os
import shutil
import subprocess  # nosec TODO!
from typing import Dict

import pandas
from args_to_db.commands.command import Command
from args_to_db.commands.commandlist import CommandList
from args_to_db.control.command_failed_exception import CommandFailedException
from args_to_db.control.result_thread import ResultThread
from args_to_db.control.run_result import RunResult
from args_to_db.control.state import State
from args_to_db.utility.logger import get_logger, logged

logger = get_logger(__name__)


@logged(logger)
def execute_command(cmd: Command, result_thread: ResultThread) -> None:
    result_thread.update_state(cmd, State.RUNNING)

    with subprocess.Popen(cmd.args(),  # nosec TODO!
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL) as process:
        exit_code = process.wait()

    end_state = State.SUCCESS if exit_code == 0 else State.FAILED
    result_thread.update_state(cmd, end_state)


def run_commands(command_list: CommandList,
                 threads: int,
                 print_status: bool) -> Dict[Command, State]:
    commands = command_list.commands()

    result_thread = ResultThread({cmd: State.QUEUED for cmd in commands},
                                 print_status=print_status)
    result_thread.start()

    result_threads = itertools.repeat(result_thread, len(commands))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as exe:
        exe.map(execute_command, commands, result_threads)

    result_thread.join()
    return result_thread.states()


def _combine_output_data(data_file: str, cache_dir: str) -> pandas.DataFrame:
    df = pandas.read_pickle(data_file) if os.path.isfile(data_file) else None

    for filename in os.listdir(cache_dir):
        row = pandas.read_pickle(f"{cache_dir}/{filename}")

        assert not row.empty

        if df is None:
            df = row
            continue

        if row.iloc[0].name in df.index:
            df.update(row)
        else:
            df = df.append(row, verify_integrity=True)

    return df


@logged(logger)
def run(  # pylint: disable=too-many-arguments
    commands: CommandList,
    check: bool = True,
    data_file: str = 'data.pkl',  # TODO: remove -> use Result
    remove_cache_dir: bool = True,
    threads: int = 1,
    write_data: bool = True,  # no longer has effect
    print_status: bool = True,
):
    # TODO: move this to conifg or some other form of constants storage
    cache_dir = 'args_to_db_cache'

    states = run_commands(commands, threads, print_status)

    if check:
        if not all((st == State.SUCCESS for st in states.values())):
            raise CommandFailedException()

    if not os.path.isdir(cache_dir):
        return RunResult(states, pandas.DataFrame())

    data = _combine_output_data(data_file, cache_dir)
    result = RunResult(states, data)

    if remove_cache_dir:
        shutil.rmtree(cache_dir)

    if write_data:
        result.write_data(data_file)

    return result
