from typing import List, Union

from args_to_db.commands.command import Command
from args_to_db.commands.commandlist import CommandList
from args_to_db.utility.logger import get_logger, logged

logger = get_logger(__name__)


@logged(logger)
def cmd(*args: Union[List[str], str]) -> CommandList:
    commandlist = CommandList.empty()
    for arg in args:
        if isinstance(arg, str):
            commandlist += CommandList([Command([arg])])
        else:
            commandlist += CommandList([Command([ar]) for ar in arg])

    return commandlist


@logged(logger)
def flag(name: str, vary=True) -> CommandList:
    commands = []
    if vary:
        commands += [Command([])]

    commands += [Command([name])]

    return CommandList(commands)


@logged(logger)
def option(identifier: str, values: List[str]) -> CommandList:
    if len(values) == 0:
        return CommandList.empty()

    commandlist = CommandList([Command([identifier])])
    commandlist += CommandList([Command([value]) for value in values])
    return commandlist
