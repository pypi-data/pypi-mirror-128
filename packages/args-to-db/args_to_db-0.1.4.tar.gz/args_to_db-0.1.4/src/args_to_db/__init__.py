from args_to_db.commands.args import cmd, flag, option
from args_to_db.commands.combine import combine
from args_to_db.commands.command import Command
from args_to_db.commands.commandlist import CommandList
from args_to_db.control.run import run
from args_to_db.runtime.result import config_from_args, write_results

__all__ = [
    'cmd',
    'combine',
    'Command',
    'CommandList',
    'config_from_args',
    'flag',
    'option',
    'run',
    'write_results',
]


from args_to_db.utility.logger import get_logger, init_logging

init_logging()

logger = get_logger(__name__)
logger.debug('args_to_db module loaded.')
