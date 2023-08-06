from args_to_db.commands.commandlist import CommandList
from args_to_db.utility.logger import get_logger, logged

logger = get_logger(__name__)


@logged(logger)
def combine(*lists):
    assert all((isinstance(list, CommandList) for list in lists))

    return CommandList(sum((list.commands() for list in lists), []))
